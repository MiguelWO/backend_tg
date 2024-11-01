import re
import email
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import validators
import dns.resolver
from collections import Counter
import tldextract
import quopri
import whois
import ipaddress

# Modules for Natural Language Processing
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from textblob import TextBlob

# Palabras comunes en inglés y español
common_words_en = {'the', 'is', 'in', 'and', 'you', 'of', 'to', 'a'}
common_words_es = {'el', 'es', 'en', 'y', 'tu', 'de', 'a', 'la', 'los'}

# Descargar recursos de NLTK si es necesario
nltk.download('punkt')
nltk.download('punkt_tab')


# Función para detectar el idioma basado en palabras comunes
def detect_language_basic(text):
    # Normalizar el texto y dividir en palabras
    words = re.findall(r'\b\w+\b', text.lower())

    # Contar cuántas palabras comunes en inglés y español aparecen
    en_count = sum(1 for word in words if word in common_words_en)
    es_count = sum(1 for word in words if word in common_words_es)

    # Determinar el idioma
    if en_count > es_count:
        return 'en'  # Inglés
    elif es_count > en_count:
        return 'es'  # Español
    else:
        return 'unknown'


black_list_en = ["click", "here", "login", "password", "account", "verify", "urgent", "immediately",
                 "immediate", "debit", "recently", "access", "information", "risk", " bank", "log",
                 "security", "secure", "verify", "update", "confirm", "fraud", "suspicious", "unauthorized",
                 "client", "notification", "service", "confirm", "password", "user", "credit", "pay",
                 "urgent", "click", "suspend", "username", "update", "bank", "pay", "secur", "notif",
                 "log", "inconvenien"]
black_list_en = list(set(black_list_en))

black_list_es = ["clic", "aquí", "iniciar sesión", "contraseña", "cuenta", "verificar", "urgente", "inmediatamente",
                 "inmediato", "débito", "recientemente", "acceder", "información", "riesgo", "banco",
                 "inicio de sesión",
                 "seguridad", "seguro", "verificar", "actualizar", "confirmar", "fraude", "sospechoso", "no autorizado",
                 "cliente", "notificación", "servicio", "confirmar", "contraseña", "usuario", "crédito", "pagar",
                 "urgente", "clic", "suspender", "nombre de usuario", "actualizar", "banco", "pagar", "seguro",
                 "notificación",
                 "inicio de sesión", "inconveniente"]

black_list_es = list(set(black_list_es))

sentiment = {
    "negative": ["hardly", "never", "nothing", "no", "scarcely", "nunca", "nada", "ningún", "ninguna", "escasamente",
                 "apenas"],
    "anxiety": ["anxious", "nervous", "worried", "fearful", "ansioso", "nervioso", "preocupado", "temeroso"],
    "indignation": ["mad", "annoyed", "indignant", "furious", "blue", "enojado", "molesto", "indignado", "furioso",
                    "triste"],
    "sadness": ["sad", "maze", "guilty", "error", "mistake", "triste", "laberinto", "culpable", "error",
                "equivocación"],
    "understanding": ["understand", "consider", "aware", "realize", "entender", "considerar", "consciente"],
    "indecision": ["maybe", "perhaps", "hesitate", "indecisive", "quizás", "tal vez", "vacilar", "indeciso"],
    "affirmation": ["always", "indeed", "sure", "affirmative", "siempre", "indeed", "seguro", "afirmativo"],
    "repression": ["constrain", "stop", "block", "desperate", "construir", "parar", "bloquear", "desesperado"],
    "trust": ["faithful", "fortune", "loving", "kind", "promise", "fiel", "fortuna", "amoroso", "amable", "promesa"],
}

sentiment_en = {
    "negative": ["hardly", "never", "nothing", "no", "scarcely"],
    "anxiety": ["anxious", "nervous", "worried", "fearful"],
    "indignation": ["mad", "annoyed", "indignant", "furious", "blue"],
    "sadness": ["sad", "maze", "guilty", "error", "mistake"],
    "understanding": ["understand", "consider", "aware", "realize"],
    "indecision": ["maybe", "perhaps", "hesitate", "indecisive"],
    "affirmation": ["always", "indeed", "sure", "affirmative"],
    "repression": ["constrain", "stop", "block", "desperate"],
    "trust": ["faithful", "fortune", "loving", "kind", "promise"],
}

# Sentimientos en español pero mismas keys
sentiment_es = {
    "negative": ["nunca", "nada", "ningún", "ninguna", "escasamente"],
    "anxiety": ["ansioso", "nervioso", "preocupado", "temeroso"],
    "indignation": ["enojado", "molesto", "indignado", "furioso", "triste"],
    "sadness": ["triste", "laberinto", "culpable", "error", "equivocación"],
    "understanding": ["entender", "considerar", "consciente"],
    "indecision": ["quizás", "tal vez", "vacilar", "indeciso"],
    "affirmation": ["siempre", "indeed", "seguro", "afirmativo"],
    "repression": ["construir", "parar", "bloquear", "desesperado"],
    "trust": ["fiel", "fortuna", "amoroso", "amable", "promesa"],
}


# Función para calcular la distancia de Levenshtein (para detectar typosquatting)
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


# Función para extraer y analizar resultados de SPF
def extract_spf(header):
    spf_pattern = r"spf=(pass|fail|softfail|neutral|none|permerror|temperror)"
    if isinstance(header, str):
        match = re.search(spf_pattern, header, re.IGNORECASE)
        if match:
            return match.group(1)
        else:
            return None
    return None


# Función para extraer y analizar resultados de DKIM
def extract_dkim(header):
    dkim_pattern = r"dkim=(pass|fail)"
    if isinstance(header, str):
        match = re.search(dkim_pattern, header, re.IGNORECASE)
        if match:
            return match.group(1)
        return None
    return None


# Función para extraer características del encabezado con dict como argumento
def extract_header_feature(msg: dict, decoded=False):
    features = {}
    # print(msg)

    # Incoherencia entre dirección de respuesta y dirección de envío
    if 'Reply-To' in msg and 'From' in msg:
        from_address = msg['From']
        reply_to = msg['Reply-To']
        features['inconsistent_reply_to'] = int(reply_to != from_address)
    else:
        features['inconsistent_reply_to'] = 0
        if 'From' in msg:
            from_address = msg['From']
        else:
            from_address = ''

    # Dominio del remitente y del ID del mensaje
    try:
        msg_id = msg['Message-ID']
    except KeyError:
        if 'Message-Id' in msg:
            msg_id = msg['Message-Id']
        else:
            msg_id = ''
    from_domain = from_address.split('@')[-1] if from_address else ''
    # Quitar > al final del from_domain
    from_domain = from_domain.strip('>')
    msg_id_domain = msg_id.split('@')[-1].strip('>') if msg_id else ''
    # print("From Domain y Message ID Domain")
    # print(from_domain, msg_id_domain)
    features['inconsistent_msg_id'] = int(from_domain != msg_id_domain)

    # Verificación del dominio del remitente
    try:
        domain = tldextract.extract(from_domain).domain
        mx_records = dns.resolver.resolve(domain, 'MX')
        features['mx_found'] = 1
    except Exception:
        features['mx_found'] = 0

    # Verificación de la distancia de Levenshtein entre el dominio del remitente y el dominio del mensaje
    features['levenshtein_distance_domain'] = levenshtein_distance(from_domain, msg_id_domain)

    # Verificar la forma del from domain que siga el formato de un dominio
    features['valid_from_domain'] = int(re.match(r'^[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}$', from_domain) is not
                                        None)

    # Verificar consistence de Return-Path y From
    if 'Return-Path' in msg:
        return_path = msg['Return-Path']
        if return_path is not None and from_address is not None:
            features['consistent_return_path'] = int(return_path not in from_address)
        else:
            features['consistent_return_path'] = 0
    else:
        features['consistent_return_path'] = 0
        return_path = ''
    # print(return_path, " - ", from_address)
    # print(features['consistent_return_path'])

    # Inconsistencias entre la direccion del remitente y el campo "From" en "Received"
    if 'Received' in msg:
        received_headers = msg['Received']
        from_in_received = any(from_domain in header for header in received_headers)
        features['from_in_received'] = int(from_in_received)
    else:
        features['from_in_received'] = 0

    # Verificación de DKIM (Simulado como ejemplo)
    try:
        dkim_result = dns.resolver.resolve(from_domain, 'TXT')
        dkim_valid = any('v=dkim1' in str(r) for r in dkim_result)
    except Exception:
        dkim_valid = False
    features['dkim_passed'] = int(dkim_valid)

    # Verificación de DMARC (Simulado como ejemplo)
    try:
        dmarc_result = dns.resolver.resolve(from_domain, 'TXT')
        dmarc_valid = any('v=dmarc1' in str(r) for r in dmarc_result)
    except Exception:
        dmarc_valid = False
    features['dmarc_passed'] = int(dmarc_valid)

    # Verificar SPF y  DKIM con Authentication-Results
    if 'Authentication-Results' in msg:
        auth_results = msg['Authentication-Results']
        spf_result = extract_spf(auth_results)
        dkim_result = extract_dkim(auth_results)
        features['spf_result'] = spf_result
        features['dkim_result'] = dkim_result
    else:
        features['spf_result'] = 'none'
        features['dkim_result'] = 'none'

    # Verificación del SPF (Simulado como ejemplo)
    try:
        spf_result = dns.resolver.resolve(from_domain, 'TXT')
        spf_valid = any('v=spf1' in str(r) for r in spf_result)
    except Exception:
        spf_valid = False
    features['spf_passed'] = int(spf_valid)

    return features


# Dividimos el cuerpo en text/plain y text/html
def split_email_body(email_body):
    plain_text_start = email_body.find("Content-Type: text/plain")
    html_text_start = email_body.find("Content-Type: text/html")

    # Extraemos el contenido de text/plain y text/html
    plain_text_part = email_body[plain_text_start:html_text_start].strip()
    html_text_part = email_body[html_text_start:].strip()

    return plain_text_part, html_text_part


# Decodificamos quoted-printable con manejo de errores de codificación
def decode_quoted_printable(content):
    content_start = content.find("\n\n")  # El contenido empieza después de dos saltos de línea
    content = content[content_start:].strip()

    # Convertimos la cadena a bytes para asegurarnos de que quopri pueda procesarla
    if isinstance(content, str):
        content = content.encode('utf-8', errors='replace')  # Codificamos como UTF-8 si es una cadena

    # Intentamos decodificar en UTF-8 primero, luego intentamos otras codificaciones si falla
    try:
        return quopri.decodestring(content).decode("utf-8")
    except (UnicodeDecodeError, ValueError):
        try:
            return quopri.decodestring(content).decode("latin-1")  # Intentamos con Latin-1
        except (UnicodeDecodeError, ValueError):
            return quopri.decodestring(content, header=False).decode("ascii", errors="replace")  # Reemplazo de errores


# Función para extraer y analizar formularios en el cuerpo del correo
def extract_forms(soup):
    features = {}

    if soup is None:
        return features
    forms = soup.find_all('form')
    # Verificar si alguno de los formularios tiene una URL sospechosa
    suspicious_urls = 0
    for form in forms:
        action = form.get('action')
        if action:
            suspicious_urls += int(validators.ipv4(action) or validators.ipv6(action))

    features['suspicious_urls'] = suspicious_urls

    # Presencia de JavaScript.
    scripts = soup.find_all('script')
    features['script_tags'] = len(scripts)

    for script in scripts:
        # Buscar si hay javascript que cambia la barra de estado
        if 'window.status' in script.text:
            features['window_status'] = 1
            break
        else:
            features['window_status'] = 0

        # Buscar si hay javascript que cambia el evento pop up
        if 'window.open' in script.text or 'alert(' in script.text:
            features['window_open'] = 1
            break
        else:
            features['window_open'] = 0

        # Buscar si hay javascript que cambia el evento de onClick
        if 'onClick' in script.text:
            features['onClick'] = 1
            break
        else:
            features['onClick'] = 0

    # Buscar uso de CSS
    if soup.find_all('style') or soup.find('link', rel='stylesheet'):
        features['css_tags'] = 1
    else:
        features['css_tags'] = 0

    # Buscar Imagenes en el cuerpo del correo
    images = soup.find_all('img')
    features['images'] = len(images)

    # Buscar si hay imagenes con enlaces
    image_links = 0
    for image in images:
        if image.parent.name == 'a':
            image_links += 1
    features['image_links'] = image_links

    return features


# Manejo del cuerpo del mensaje
def extract_body(msg: dict, decoded=False, soup=None):
    features = {}
    if not decoded:
        pattern_html = r'^<!DOCTYPE html>\s*<html[^>]*>'
        pattern_plain = r'^Content-Type: text/plain'
        if "Body" in msg and msg["Body"]:
            # Revisar si es un html
            # if '<!DOCTYPE html>' in msg["Body"] or msg["Body"].startswith('<html>'):
            #     soup = BeautifulSoup(msg["Body"], 'html.parser')
            #     features = extract_forms(soup)
            #     body = soup.get_text()
            # else:
            #     body_raw = msg["Body"]
            #     plain_text_part, html_text_part = split_email_body(body_raw)
            #
            #     soup = BeautifulSoup(html_text_part, 'html.parser')
            #     features = extract_forms(soup)
            #     body = soup.get_text()
            try:
                body = msg['Body']
                soup = BeautifulSoup(body, 'html.parser')
                features = extract_forms(soup)
            except Exception:
                try:
                    body_raw = msg["Body"]
                    plain_text_part, html_text_part = split_email_body(body_raw)

                    soup = BeautifulSoup(html_text_part, 'html.parser')
                    features = extract_forms(soup)
                    body = soup.get_text()
                except Exception:
                    body = msg['Body']
                    features = {}
        else:
            body = ''
    else:
        body = msg['Body']
        features = extract_forms(soup)

    return body, features


# Función para extraer características del cuerpo
def extract_body_features(msg: dict, decoded=False, soup=None):
    features = {}

    body, features_aux = extract_body(msg, decoded, soup)

    features.update(features_aux)

    # Chequear si el body no es nulo
    if not body:
        return features

    # Número de URLs
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    features['url_count'] = len(urls)

    # Presencia de URLs basadas en IP
    ip_based_urls = [url for url in urls if validators.ipv4(url)]
    features['ip_based_url'] = int(len(ip_based_urls) > 0)

    # Número de caracteres % en la URL
    percent_in_urls = sum(url.count('%') for url in urls)
    features['percent_in_urls'] = percent_in_urls

    # Número de simbolos @ en la URL
    at_in_urls = sum(url.count('@') for url in urls)
    features['at_in_urls'] = at_in_urls

    # Numero de . en la URL
    dot_in_urls = sum(url.count('.') for url in urls)
    features['dot_in_urls'] = dot_in_urls

    # Antigüedad del nombre de dominio
    if len(urls) > 0:
        domain = tldextract.extract(urls[0]).domain
        try:
            whois_info = whois.whois(domain)
            domain_age = 2024 - whois_info.creation_date.year
        except Exception:
            domain_age = 0
        features['domain_age'] = domain_age
    else:
        features['domain_age'] = 0

    # Número de subdominios promedio en las URLs
    subdomains = [tldextract.extract(url).subdomain for url in urls]
    subdomain_count = Counter(subdomains)
    if len(subdomain_count) != 0:
        features['avg_subdomains'] = sum(len(subdomain) for subdomain in subdomain_count) / len(subdomain_count)
    else:
        features['avg_subdomains'] = 0

    # Comparamos el dominio en el encabezado del correo con los dominios presentes en el cuerpo
    if 'From' in msg and msg['From'] is not None:
        from_domain = tldextract.extract(msg['From']).domain
        body_domains = [tldextract.extract(url).domain for url in urls]
        features['from_domain_in_body'] = int(from_domain in body_domains)
    else:
        features['from_domain_in_body'] = 0

    # Número de URLs con números o caracteres especiales.
    special_chars = re.compile(r'[^a-zA-Z0-9]')
    special_urls = sum(1 for url in urls if special_chars.search(url))
    features['special_urls'] = special_urls

    # Número de enlaces con direcciones IP.
    ip_links = sum(1 for url in urls if validators.ipv4(url))
    features['ip_links'] = ip_links

    # Cantidad de enlaces con discrepancia entre URL visible y URL real (phishing)
    links = re.findall(r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"', body)
    visible_texts = re.findall(r'<a.*?>(.*?)</a>', body)
    phishing_links = sum(1 for link, visible in zip(links, visible_texts) if link != visible)
    features['phishing_links'] = phishing_links

    return features


def is_ip_public(ip):
    try:
        ip = ipaddress.ip_address(ip)
        return ip.is_global
    except ValueError:
        return False


def is_ip_private(ip):
    try:
        ip = ipaddress.ip_address(ip)
        return ip.is_private
    except ValueError:
        return False


# Función para verificar coherencia de IP y dominios
def extract_ip_features(msg: dict):
    features = {}

    received_pattern = r"from\s+([^\s]+)\s+\((?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)|from\s+\[?(?P<alt_ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]?\s+by\s+([^\s]+)"

    match = re.search(received_pattern, msg['Received'])
    if match:
        ip = match.group('ip') if match.group('ip') else match.group('alt_ip')
        server = match.group(1) if match.group(1) else match.group(3)
    else:
        ip = ''
        server = ''

    features['received_ips'] = len(ip)
    features['received_servers'] = len(server)

    # Contar el numero de ip publicas o privadas
    ip_count = Counter(ip)
    features['public_ips'] = sum(1 for ip in ip_count if is_ip_public(ip))
    features['private_ips'] = sum(1 for ip in ip_count if is_ip_private(ip))

    return features


def extract_subject_features(msg: dict):
    features = {}
    try:
        subject = msg['Subject']
        if not subject:
            return features
        # Repetición de 3 o más caracteres
        features['repeated_chars_in_subject'] = int(re.search(r'(.)\1{2,}', subject) is not None)

        # Proporción de palabras en mayúsculas
        words = subject.split()
        upper_case_words = sum(1 for word in words if word.isupper())
        features['upper_case_ratio'] = upper_case_words / len(words) if words else 0

        #     Palabras sin vocales: Determina cuántas palabras en el asunto no contienen vocales.
        no_vowels = re.findall(r'\b[^aeiouAEIOU]*\b', subject)
        features['no_vowels'] = len(no_vowels)
    except KeyError:
        features['repeated_chars_in_subject'] = 0
        features['upper_case_ratio'] = 0
        features['no_vowels'] = 0

    return features


# # Función para extraer características de sentimiento
# def extract_sentiment_features(msg, decoded=False):
#     features = {}
#     body, features_aux = extract_body(msg, decoded)
#
#     features.update(features_aux)
#
#     # Chequear si el body no es nulo
#     if not body:
#         return features
#
#     # Tokenizar el texto
#     words = word_tokenize(body.lower())
#
#     # Eliminar stopwords
#     stop_words = set(stopwords.words('english')) | set(stopwords.words('spanish'))
#     # Stemming
#     stemmer_en = SnowballStemmer('english')
#     stemmer_es = SnowballStemmer('spanish')


# Función para extraer características de palabras en la lista negra
def extract_black_list_features(msg, decoded=False, soup=None):
    features = {}
    body, features_aux = extract_body(msg, decoded, soup)

    features.update(features_aux)

    # Chequear si el body no es nulo
    if not body:
        return features

    # Tokenizar el texto
    words = word_tokenize(body.lower())

    # Eliminar stopwords
    stop_words = set(stopwords.words('english')) | set(stopwords.words('spanish'))
    # Stemming
    stemmer_en = SnowballStemmer('english')
    stemmer_es = SnowballStemmer('spanish')

    # detectar idioma
    language = detect_language_basic(body)

    if language == 'en':
        words = [stemmer_en.stem(word) for word in words]
        words = [word for word in words if word not in stop_words]
        black_list = black_list_en
        #     Stemming en ingles para palabras en la lista negra y sentimiento
        black_list = [stemmer_en.stem(word) for word in black_list]
        for sentiment in sentiment_en:
            sentiment_words = sentiment_en[sentiment]
            sentiment_en[sentiment] = [stemmer_en.stem(word) for word in sentiment_words]
        sentiment = sentiment_en
    elif language == 'es':
        words = [stemmer_es.stem(word) for word in words]
        words = [word for word in words if word not in stop_words]
        black_list = black_list_es
        #     Stemming en español para palabras en la lista negra y sentimiento
        black_list = [stemmer_es.stem(word) for word in black_list]
        for sentiment in sentiment_es:
            sentiment_words = sentiment_es[sentiment]
            sentiment_es[sentiment] = [stemmer_es.stem(word) for word in sentiment_words]
        sentiment = sentiment_es
    else:
        return features

    # Contar palabras en la lista negra
    black_list_count = sum(1 for word in words if word in black_list)
    features['black_list_count'] = black_list_count

    # Contar palabras de cada sentimiento
    for sentiment_type, sentiment_words in sentiment.items():
        sentiment_count = sum(1 for word in words if word in sentiment_words)
        features[sentiment_type] = sentiment_count

    return features


# Análisis de Contenido (Texto, Formato y Estilo)
def extract_content_features(msg, decoded=False, soup=None):
    features = {}
    body, features_aux = extract_body(msg, decoded, soup)

    features.update(features_aux)

    # Chequear si el body no es nulo
    if not body:
        return features

    # Si el correo tiene formato HTML.
    features['html_format'] = int('<html>' in body)

    # Tipo de contenido: Revisa si el tipo de contenido está presente y si está configurado como "text/html",
    # lo cual puede ser indicativo de phishing.
    features['text_html_content'] = int('Content-Type: text/html' in msg)

    # Palabras largas: Identifica palabras que tienen al menos 15 caracteres.
    long_words = re.findall(r'\b\w{15,}\b', body)
    features['long_words'] = len(long_words)

    # Porcentaje de palabras largas al menos 15 caracteres.
    words = re.findall(r'\b\w{15,}\b', body)
    long_word_ratio = len(long_words) / len(words) if words else 0
    features['long_word_ratio'] = long_word_ratio

    # Uso de letras inusuales: Registra la cantidad de palabras que contienen
    # al menos dos letras poco comunes, como J, K, Q, X o Z.
    unusual_letters = re.findall(r'\b\w*[JKQXZjkqxz]\w*\b', body)
    features['unusual_letters'] = len(unusual_letters)

    # Porcentaje de palabras con letras inusuales.
    unusual_letter_ratio = len(unusual_letters) / len(words) if words else 0
    features['unusual_letter_ratio'] = unusual_letter_ratio

    # Palabras con caracteres especiales: Detecta palabras que incluyen caracteres no estándar,
    # números o símbolos especiales.
    special_char_word_pattern = re.compile(r'\b\w*[^a-zA-Z\s]\w*\b')
    special_char_words = re.findall(special_char_word_pattern, body)
    features['special_char_word_count'] = len(special_char_words)

    # Porcentaje de palabras con caracteres especiales.
    special_char_word_ratio = len(special_char_words) / len(words) if words else 0
    features['special_char_word_ratio'] = special_char_word_ratio

    # Longitud media de las palabras.
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    features['avg_word_length'] = avg_word_length

    # Uso de mayúsculas y minúsculas.
    upper_case_words = sum(1 for word in words if word.isupper())
    features['upper_case_words'] = upper_case_words

    # Porcentaje de palabras en mayúsculas en el cuerpo del correo.
    upper_case_ratio = upper_case_words / len(words) if words else 0
    features['upper_case_ratio_body'] = upper_case_ratio

    # Uso de mayúsculas y minúsculas.
    lower_case_words = sum(1 for word in words if word.islower())
    features['lower_case_words'] = lower_case_words

    # Porcentaje de palabras en minúsculas en el cuerpo del correo.
    lower_case_ratio = lower_case_words / len(words) if words else 0
    features['lower_case_ratio_body'] = lower_case_ratio

    # Formas de saludo.
    word_count = Counter(words)
    greetings = ["hi", "hello", "dear", "good", "morning", "afternoon", "evening", "night"]
    greetings_count = sum(word_count[word] for word in greetings)
    features['greetings'] = greetings_count

    # Formas de despedida.
    farewells = ["regards", "sincerely", "best", "wishes", "goodbye", "farewell", "bye"]
    farewells_count = sum(word_count[word] for word in farewells)
    features['farewells'] = farewells_count

    return features


# Función principal de extracción de características
def extract_email_features(email_dict, decoded=False, soup=None):
    features = {}
    features.update(extract_header_feature(email_dict, decoded))
    features.update(extract_body_features(email_dict, decoded, soup))
    features.update(extract_ip_features(email_dict))
    features.update(extract_subject_features(email_dict))
    # features.update(extract_sentiment_features(email_dict, decoded))
    features.update(extract_black_list_features(email_dict, decoded, soup))
    features.update(extract_content_features(email_dict, decoded, soup))

    return features
