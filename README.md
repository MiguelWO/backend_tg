# Phishing Email Detector Backend
Este repositorio contiene el backend de la aplicación **Phishing Email Detector**, una API construida con **FastAPI** que procesa el contenido de correos electrónicos y predice si se trata de phishing. La API permite a los usuarios realizar solicitudes para la detección de phishing y obtener una visualización en forma de nube de palabras basada en el contenido de los correos.

## Tabla de Contenidos

- [Phishing Email Detector Backend](#phishing-email-detector-backend)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Características](#características)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Endpoint](#endpoint)
  - [Licencia](#licencia)

## Características

- **Detección de phishing**: Procesa el contenido del correo electrónico y utiliza un modelo de aprendizaje automático para predecir si es phishing.
- **Generación de nubes de palabras**: Crea una visualización de la frecuencia de palabras del contenido del correo.
- **Validación y seguridad**: Soporte para validación de entrada y configuración de CORS para asegurar la API.

## Instalación

1. **Clona este repositorio**:

   ```bash
   git clone https://github.com/MiguelWO/phishing-email-detector-backend.git

2. **Navega a la carpeta del proyecto**:

3. **Crea y activa un entorno virtual**:
    ```bash
    python -m venv env
    source env/bin/activate  # En Linux/Mac
    env\Scripts\activate     # En Windows

4. **Instala las dependenias**:
    ```bash
    pip install -r requirements.txt
5. **Configura las variables de entorno**:
    Crea un archivo .env en la raíz del proyecto y configura las variables necesarias, como CORS_ORIGINS para especificar los orígenes permitidos.

## Uso
Para iniciar el servidor en desarrollo, ejecuta:

    ``bash
    uvicorn app.main:app --reload

La API estará disponible en http://127.0.0.1:8000.

## Endpoint
Endpoints
1. /predict
Método: POST

Predice si el contenido de un correo electrónico es phishing.

    Request Body:
        email_content (string): El contenido del correo electrónico.

    Response:

    {
      "email_content": "<texto>",
      "is_phishing": true,
      "confidence": 0.87
    }

        is_phishing: true si el modelo predice phishing, de lo contrario false.
        confidence: Nivel de confianza en la predicción (0-1).

2. /generate_wordcloud

Método: POST

Genera una nube de palabras en base al contenido del correo.

    Request Body:
        email_content (string): El contenido del correo electrónico.

    Response:

    {
      "wordcloud_image": "<base64-encoded-image>"
    }

        wordcloud_image: Imagen de la nube de palabras en formato Base64.

3. /docs

Interfaz interactiva generada automáticamente para probar y documentar la API. Visita http://127.0.0.1:8000/docs para acceder.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
