def extract_email_content(email:str) :
    """
    Extract the content of an email message.
    """
    import re
    from bs4 import BeautifulSoup
    from email.parser import BytesParser
    from email import policy

    # # Extract the sender
    # sender = re.search(r"From: (.*)", raw).group(1)
    # # Extract the receiver
    # receiver = re.search(r"To: (.*)", raw).group(1)
    # # Extract the date
    # date = re.search(r"Date: (.*)", raw).group(1)
    # # Extract the subject
    # subject = re.search(r"Subject: (.*)", raw).group(1)
    
    # # Extract the body
    # body = re.search(r"Content-Type: text/plain; charset=us-ascii(.*)", raw, flags=re.DOTALL).group(1)



    # # Parse the body
    # body = re.sub(r"\n", "", body)
    # body = re.sub(r"=3D", "=", body)
    # body = re.sub(r"=C2=A0", " ", body)

    # # Clean the body
    # soup = BeautifulSoup(body, "html.parser")
    # body = soup.get_text()

    # # Remove URLS
    # clean_body = re.sub(r'https?://\S+', '', body)

    # # Remove special characters and numbers
    # clean_body = re.sub(r'[^A-Za-z\s]', '', clean_body)

    # # Lowercase the body
    # clean_body = clean_body.lower()

    # try:
    #   sender = re.search(r"From: (.*)", email).group(1)
    # except:
    #   sender = None
    # try:
    #   receiver = re.search(r"To: (.*)", email).group(1)
    # except:
    #   receiver = None
    # try:
    #   date = re.search(r"Date: (.*)", email).group(1)
    # except:
    #   date = None
    # try:
    #   subject = re.search(r"Subject: (.*)", email).group(1)
    # except:
    #   subject = None
    # body = ''

    # if "Content-Type: text/plain; charset=us-ascii" in email:
    #     print('Content-Type: text/plain; charset=us-ascii')
    #     body = re.search(r"Content-Type: text/plain; charset=us-ascii(.*)", email, flags=re.DOTALL).group(1)
    # elif "Content-Type: multipart/alternative" in email:
    #     print('Content-Type: multipart/alternative')
    #     match = re.search(r"Content-Type: multipart/alternative; boundary=(.*)", email)
    #     if match:
    #         body = match.group(1)
    #         match = re.search(r"--" + body + "(.*)", email, flags=re.DOTALL)
    #         if match:
    #             body = match.group(1)
    #             match = re.search(r"Content-Type: text/plain; charset=us-ascii(.*)", body, flags=re.DOTALL)
    #             if match:
    #                 body = match.group(1)
    #             else:
    #                print('No plain text found in multipart/alternative')
    #         else:
    #           print('No boundary found in multipart/alternative')
    #     else:
    #       print('No boundary found in multipart/alternative')

    # elif "Content-Type: text/html; charset=us-ascii" in email:
    #     print('Content-Type: text/html; charset=us-ascii')
    #     body = re.search(r"Content-Type: text/html; charset=us-ascii(.*)", email, flags=re.DOTALL).group(1)
    # elif "Content-Type: text/html;"  in email:
    #     print('Content-Type: text/html;')
    #     body = re.search(r"Content-Type: text/html;(.*)", email, flags=re.DOTALL).group(1)
    # elif "Content-Type: text/plain;"  in email:
    #     print('Content-Type: text/plain;')
    #     body = re.search(r"Content-Type: text/plain;(.*)", email, flags=re.DOTALL).group(1)
    # else:
    #     body = email

    message = BytesParser(policy=policy.default).parsebytes(email.encode())

    sender = message.get('From')
    receiver = message.get('To')
    date = message.get('Date')
    subject = message.get('Subject')
    body = message.get_body(preferencelist=('plain', 'html')).get_content()

 
    body = re.sub(r"\n", "", body)

    # Remove HTML tags
    soup = BeautifulSoup(body, "html.parser")
    body = soup.get_text()

    # # Remove URLS
    body = re.sub(r'https?://\S+', '', body)

    # Handle soft line breaks
    body = re.sub(r"=\n", "", body)
    body = re.sub(r"=([0-9A-Fa-f]{2})", lambda m: bytes.fromhex(m.group(1)).decode('utf-8', 'ignore'), body)

    # Remove email headers and metadata
    words = ['Mime-Version ', 'Content-Type', 'quoted-printable', 'charset=.*?']
    body = re.sub('|'.join(words), '', body)

    # Remove HTML tags
    soup = BeautifulSoup(body, "html.parser")
    body = soup.get_text()

    # # Remove excessive whitespace, non-printable characters, and redundant line breaks
    body = re.sub(r"\s+", " ", body)  # Replace multiple spaces/newlines with a single space
    body = re.sub(r"[^\x20-\x7E]+", " ", body)  # Remove non-printable ASCII characters

    # Remove lingering special sequences or artifacts
    body = re.sub(r"[-=]{2,}", "", body)  # Remove sequences like '--' or '=='
    body = body.replace("\xa0", " ")  # Replace non-breaking spaces

    # Delete = signs
    body = re.sub(r"=3D", "", body)
    body = re.sub(r"=C2=A0", " ", body)

  

    # # Remove special characters and numbers
    # body = re.sub(r'[^A-Za-z\s]', '', body)
    # body = re.sub(r"=3D", "=", body)
    # body = re.sub(r"=C2=A0", " ", body)

  

  
    return {
        "sender": sender,
        "receiver": receiver,
        "date": date,
        "subject": subject,
        "body": body
    }


raw = """
Delivered-To: wmiguel999@gmail.com
Received: by 2002:a05:7208:214f:b0:92:19f1:341d with SMTP id x15csp700227rbx;
        Sun, 24 Nov 2024 06:25:21 -0800 (PST)
X-Google-Smtp-Source: AGHT+IGY93F+c0t5JlqRIchyKo85OCT0tvU9NrvPNWVkHmBmkZGIzxiE54RjALoK9xavEOEYuJPc
X-Received: by 2002:a05:620a:f0b:b0:7a3:5f3f:c084 with SMTP id af79cd13be357-7b514531c31mr1235206085a.30.1732458321122;
        Sun, 24 Nov 2024 06:25:21 -0800 (PST)
ARC-Seal: i=1; a=rsa-sha256; t=1732458321; cv=none;
        d=google.com; s=arc-20240605;
        b=EdUo+vLag4HQBiEOb4XpAiqJnofYNva6ciLvAwjjLlkgoWfg8MY8LDD684uPvOZFOJ
         ZVFMHT9Tv9bWSqmYpAdLEuGvFhcqzFvISja5iw5jaybxxyOGGCKbdiXOGcRCZ7LI8rUw
         27d4k97E5aZuXWF8dyWkJGLjeIRLCeEwevnalIHkP4z+8VyCp0l3JnZSiQdS+X8NAH+6
         2M9AQcaxNtswKvNDA0o17B6g/NpDfZYvuXTSQW6+At5mzCu6n3dPkxYzV0h0WmOakN+b
         AD2QcQDnchvrhlxop4ihMWrD1RLV3LKiGlmLQ2S0AhULSCXRy3fAZYuZu9Ns70S6T7nw
         jwuQ==
ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20240605;
        h=to:list-unsubscribe:list-unsubscribe-post:reply-to:subject
         :message-id:mime-version:from:date:dkim-signature:dkim-signature;
        bh=atoSUehheB326vJKOFnceGVmnkWfw4XZ71VRZm25jRo=;
        fh=1CDB7imnTV+BoDKc6cXglJGf45R7+SBZObJ9YUr6hMY=;
        b=Zy1M2QF9yZYW+27yPFsqiSy2WW8CgkxsegnG691UhspXh7L6gRJ5W78VjFgUmDjNAP
         uR0BTFbXiaHur6XseJPrC1KlogHSsAsDzi0SSCxqBblIHyZxX/81/q6Q/Wyx24uQVvj8
         cVOMBBXg2z/9FSQzMdl25NFfDdRSJnNYTaz+AYL+3SAbhiXFyyToDwQRuvKYD9zxR6tG
         7CXQUVVBSteO6nHwkQc1dyK1gkKXEpbsthLWpS0VDCMaE5OHdgx6UsqcoPkMs4UulEs6
         RhZA22xqK6I2nL15pF9Lma45Js8udm20zWkARkhy3rEEdxHHqlsGAnSMGsjnAcigYv7h
         sRng==;
        dara=google.com
ARC-Authentication-Results: i=1; mx.google.com;
       dkim=pass header.i=@sender.skyscanner.com header.s=s1 header.b=cNSdMH9b;
       dkim=pass header.i=@sendgrid.info header.s=smtpapi header.b="uireNO/A";
       spf=pass (google.com: domain of bounces+9735476-1fdc-wmiguel999=gmail.com@abmail.sender.skyscanner.com designates 149.72.159.74 as permitted sender) smtp.mailfrom="bounces+9735476-1fdc-wmiguel999=gmail.com@abmail.sender.skyscanner.com";
       dmarc=pass (p=REJECT sp=NONE dis=NONE) header.from=skyscanner.com
Return-Path: <bounces+9735476-1fdc-wmiguel999=gmail.com@abmail.sender.skyscanner.com>
Received: from o1770.abmail.sender.skyscanner.com (o1770.abmail.sender.skyscanner.com. [149.72.159.74])
        by mx.google.com with ESMTPS id af79cd13be357-7b66bd30945si42563585a.550.2024.11.24.06.25.20
        for <wmiguel999@gmail.com>
        (version=TLS1_3 cipher=TLS_AES_128_GCM_SHA256 bits=128/128);
        Sun, 24 Nov 2024 06:25:21 -0800 (PST)
Received-SPF: pass (google.com: domain of bounces+9735476-1fdc-wmiguel999=gmail.com@abmail.sender.skyscanner.com designates 149.72.159.74 as permitted sender) client-ip=149.72.159.74;
Authentication-Results: mx.google.com;
       dkim=pass header.i=@sender.skyscanner.com header.s=s1 header.b=cNSdMH9b;
       dkim=pass header.i=@sendgrid.info header.s=smtpapi header.b="uireNO/A";
       spf=pass (google.com: domain of bounces+9735476-1fdc-wmiguel999=gmail.com@abmail.sender.skyscanner.com designates 149.72.159.74 as permitted sender) smtp.mailfrom="bounces+9735476-1fdc-wmiguel999=gmail.com@abmail.sender.skyscanner.com";
       dmarc=pass (p=REJECT sp=NONE dis=NONE) header.from=skyscanner.com
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=sender.skyscanner.com; h=content-type:from:mime-version:subject:reply-to:list-unsubscribe-post: list-unsubscribe:x-feedback-id:to:cc:content-type:from:subject:to; s=s1; bh=atoSUehheB326vJKOFnceGVmnkWfw4XZ71VRZm25jRo=; b=cNSdMH9b2fOqYOSR1hFY1g2/4lLXY2rM7slWn1n1TCm/NjqYOlhuAcwlBF7vmqfpeZK0 DTQKXwuMKcXQOefZ4ggaN0Ekbg7C3KuSGeD8LmDExDYNORfjLYZvKoXhr5aaor+CjKIHcf BktAypG/cMXzknyPNi6mbNtGJUJqQ4ErNS4yIKsXA1Mzm4OfDryXbxDOpvhrH2BuqbebMg HWwXM67KYLlCC6JxDwDSkDBrFW2V2mO4GGB1aSWCl0qJFG+FvRU14D5FLMR7DSiYoqf25Z ur4bHx87uzyLzZWa041URZ09YAcqCqH3Z29ziO+FMrSHAHOvo9OSdlWa+FEPZANg==
DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=sendgrid.info; h=content-type:from:mime-version:subject:reply-to:list-unsubscribe-post: list-unsubscribe:x-feedback-id:to:cc:content-type:from:subject:to; s=smtpapi; bh=atoSUehheB326vJKOFnceGVmnkWfw4XZ71VRZm25jRo=; b=uireNO/AqghK/u38bW6x93E+FUWuUz4Myncv2lX7YNvMd72y83hNKep6LovEaZx4Cmao V3Xa/J0QeRc4oshnuGR8PTBfaATDAmvOLTLCXJw1+wGXbki9sYKBMZ3EzUnNYzqdwWzsvU Tnu4G7oAAkgQOOPEr2rqpUNm4/jXyTaaU=
Received: by recvd-6f546cf478-2s96q with SMTP id recvd-6f546cf478-2s96q-1-6743374F-9 2024-11-24 14:25:19.166060456 +0000 UTC m=+839023.439312109
Received: from OTczNTQ3Ng (unknown) by geopod-ismtpd-9 (SG) with HTTP id I6_Zq8KvSV-Oueuk8_H7EQ Sun, 24 Nov 2024 14:25:19.114 +0000 (UTC)
Content-Type: multipart/alternative; boundary=b8d57104611303067edaf6209d6b906a770ffda77ae6998548cc1a7a6ae0
Date: Sun, 24 Nov 2024 14:25:19 +0000 (UTC)
From: Skyscanner <no-reply@sender.skyscanner.com>
Mime-Version: 1.0
Message-ID: <I6_Zq8KvSV-Oueuk8_H7EQ@geopod-ismtpd-9>
Subject: Spotlight on: Krakow
Reply-To: no-reply@sender.skyscanner.com
List-Unsubscribe-Post: List-Unsubscribe=One-Click
List-Unsubscribe: <https://www.skyscanner.net/subscriptions/consent/email/false?market=co&locale=en-gb&token=eyJjdHkiOiJKV1QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwidGFnIjoiOVVvcFR6V0dfdFpxc0VDM2hndWw2USIsImFsZyI6IkEyNTZHQ01LVyIsIml2IjoiaEluTGtQNnRPUHFRVHd1WSJ9.C5Iz64Y6RNHjKDs1t140AQODq2Mlrz-lFK32LoUtdsFtEeliz6y1hQkAX9ldQd77t4X4TEwcg9Joh80chPrGlg.0blU5D9Bu243DNuyMrFdVw.5naR6WVU0ocAsd22tLtWS2_jI0adYrWiVtvfK_zJPVMzGJjja-GJZMi8NyK9oNI7FgbM0wp4VNboVktOGWQ0bJWr9rN_3j3oYBGPnYFNfXlzmaAnG26Df1QpuOzQ4v5RXONez1xva5j59O4nzI3kR7Aa6Mt7keMbE-yVBe1F1gLeboj2OPhSuxTSTOSUDb5z70Kn3iohfvAcZWfiHXoatFS-QMwYgxBR_mbw-GnpsVo.0TbuTi6yiNaI8cnQAZNXAB32WjDeDZFVTdSK4n5Y0FE&source=list-unsub&channel=email>
X-Feedback-ID: 9735476:SG
X-SG-EID: u001.FQNiPRBDq505EtdtWOJ4NuIheNFmdmn/NhGdootfi1qvmWoXUSphCJF5WvhH+BH73koLbVnYQh6IhdW/4ArbuQsTeB8artWhWL7T36x5Fl/UM598+6+QMmv18NkZI4Zn1XVXQrmDQXRms8T3EkDJQU8gs5lBqDkL1BV798gTOBnzWYezKNHWJkyudnoAnZjaXOv/6WRGPS+2y7BbscAz4zbOsJIgyqMlQ6aa/lorPHLv20wj/w7EfBDWNImgz6xO
X-SG-ID: u001.SdBcvi+Evd/bQef8eZF3BpTL9BgbK5wfSJMJGMsmprDrjDW6011yC6XOo3uya5MXisOasKr8f85wmTThZMcE8+pwzZC1qYvLXO/z60DRWpdanc92Uz5NPSedlHiACEaeV1JTH49w1CFqw4fV4PL6juUjT14UuGE5N/hEmNMspbSWK1GXlj9a1SVO7h3+AeB8SODuy8VrwjM+fg1ujrTcnDAmbFehRRy31XnZvpp7Ii2QHYp1h8bOVZAWJ0Du5kElR93+vHiRlqYOulFUzq5yVx0CH7YF6YN6eheALu4VzbtBGy9+fNiK8of3aF1JpRKn0G6ixfVl05TlOMLC+cnHuVxPZBmiE/HkJiTeAjkOVfxcxRn6hHB7pYNSQfCI06kQTXEyoDBO9mdU92KOBglzUqAZhPRbGBIwkQryTOWyhfe62lm2tHvLPifVURB7wJ6KOFaIhShoRJ1h5j5H6XLTyxhIyiWmnPdvxcfO/E4gxdcvh7E6XgQ/cniuiKQn/a6bgeQp5V25FBBwVKe1OH0B+/wy4+g96+D+7gnTP8hULoS4owHXikiZx2BskHXN6RcQ
To: wmiguel999@gmail.com
X-Entity-ID: u001.3jHH0MzQG2IlfggWa26EvA==

--b8d57104611303067edaf6209d6b906a770ffda77ae6998548cc1a7a6ae0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/plain; charset=us-ascii
Mime-Version: 1.0

Discover something different on your next trip to Krakow.
































































Flights(https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_=
SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbn=
rOkTFFOWQe8mZPLAtWtKxwXfCTnpC9Rmxcdnffx8UUR56L98uWz64Z_hg3g3-Zdyu2mXwyhQdzJ=
GrrDJFzbGoD_Y27ZMzOguFaamzZh5ZKgM_pVn1qyWFLXpS5WegL5okdE1QPbVUY0a1NUqDlP30M=
1iS3klntvmkGU8LsxnsYwSEXNMIc7c5Pxoe64H1CTU6c80th4Q1vdANVTPOqUgP95xXQStY9quK=
64ZrBmSnf3O2B9ukuacMJpvpFQ6hTuxk-8X_FqiCwxivy0Pm2XBQO7g7noMwKYXlLUiPj-u2uic=
xSW3sgMaSifdomo4AW9W-iGDaAo2bVgG43cwL2jCqiOf3PhZqjeKpssqSK1We-xiWXB7OYKf6tc=
tnl1pCu1TADZuafapY6WioAdJXTH4yPWpPqffIWtXcPq2e1co3atpA9mbLhwlSPe2t5OYHBVQfn=
dDJGWZjiTJ2wuykkqIPDxL_15nUJaIlbGEVaqK3p-8FQLjjwf3U1vfXLaAveUvkWo8UFremOf8D=
jrdndRNd0bMjP5et-sPKMaCPNTJFu2L64B4zf649h9q9VXH_t5PmjTONPbzxac7MapTqnWQ9ccs=
7IICeqbnb3kggHJg97SpZT_IQC4vGkmxciffiDYvB4WB4W9PSm0boW3ps3zJ8LbHFU0ZdNz0jIT=
jDqbotE5MwbshjXSqk_s2h5T-Nu28VTXvtV0Eggp0eUMZ6176_TkF781sdxb_ffuAq7Y5hW9nBw=
WkArRV0zaDDW_YH6PyHDxjDduoi168R_BI_osFV7qPwXrjxcQFJnWwB5tFjQN0FsIFi9IHCWopJ=
E13r05blRt26fqdLA-BfYFVl8x8wRfHf06zSTmALiIqZNQ_n6P9a8GMangqMGyn6pBLnvpfqcTq=
DqEwVfxg/4bq/kEQStHXPR369e8SlRa1G8w/t0/h001.hpxwh8w0_gv7JbyDu_8WmJX5yPBrRMj=
aRnAnRYxDL5I<imgsrc=3D"https://ablink.sender.skyscanner.com/ss/c/u001.OHuv9=
NcSpqjkTP75eZwI3N-ykbgT7829eclfSUmC3VwKOhooUtCXPr04k1mLi44FqXPNrdOO1BjSdreM=
5f2IIj-eFiX_Oy4g4wCOqyyNony3LrjW5uJjZfftp9-3Ua4RZPwb-SPfU7tbVwwgOh_htLMK22s=
ylU_BUxkoVxGhZcPSjaXxm4th7zNWv6XUSGbJ98olzexxPgC3V3iFDace1dTCjSGSPpvE7Zt_6H=
AI5bnezlpPSEGfv_wKrRTmKZvL2_B4YexwRqxqbAF3nEqFLnwD0JLporcHyfK_nfpOQx-Ri1jyq=
qDnhZz1RYmGDjWR_Yr0gM58753tQ-4UUpimOFfn4PmdwXbst_RhgzmSYTxG3nthMxijiJUXUDoM=
SfmiQcZa9vQwCA_a5Ldx8X3e6JbdamvoLIjNfgBOgIYvL-st-zi3Rt532FZ2NWeWxHOgOcV_NTU=
XdYZXQz0xVAtplkFkMQwNxb0MLZW0O75sL91XdOz969voESI5po3rB2hBwecPE7ku-px2AZyqcj=
BKl2GyttDXBdK0LtEJnbHa43JbXcPbq-kX9dem4V1GHFxJW6rt34k6SNp2uteM7ngDNuxez2dTs=
yATfH716PTD4vupNZvYsM09jjybe9r4DaEs_U-QqU1tFhlAxByVaof209skbYAEaoNM6Qd96u70=
gCTvb0l6u-HplO_QBhMFUdW8vL6bvrA824wfGIf7FEBoL45JvokIYPmuLC8FVgDowrTzHMylGus=
Irzp0UUnCb1FHd9yn3RfwriNec3RP3fBfn1AUqzdOwsJIIV2mlYhFZFGrlYdBnItVPaFJ9wvzod=
U8cZjC5ig1l6WCPH9Ofxbb2ivfYwzkvbIJRZy16enVC9QZbc71tZvRQjphAfj2Dul0dN0G0xFSn=
AmEc_RvPVbw-Jr91nkFVhV7wbB0NTTIrq37W2MEewTDNuF9CQqh3AVYMDq5BJKKCIMt9HLbEViL=
1Y6BGtXEZXrTQ5Le_wQxMQiHtI1DfhaPv-t-7P_qGKyOXCWxA2qYBdnH5hKKHXhRz1NVQSKdrXc=
yEhVJluVU0c6lmF4rfwJwkhkPgvrl8TaKLr4z7FkkXHgfoaMPNtQFvmoOBc3jpWHQLAbjaj-xWn=
iBxhyh1bNJRo5qX_FP_T0C6_eZNO5ig7spGJgwdmPYAsvGO2rYlRSOeHeKAdVMCKrvRru8oD9bd=
pjAIlFrGbn3MdRh6gCN7FctO7CN9v5H7r8l16cLSxj7CwHKvseE76rY77kh-jrl8G2XwfLAY-p1=
T4RKbJRZhnCzxX521Ras-U5D36ZTPFOUoiym8tA7bbMNE4ljz6IyhDCOlj55cgxBPKGvhRRaFKL=
knhcDF_PBPmn6243NkpCUVxAtLrOeSCe5lEGID7omLhNlOkMmWu4ManvHKuECMMyhQDFltJX0RR=
9P5LXprTHCUQKzL5JDl9kWNziLNSIvrnIj4PoIxFerfrk8sN9XEN4jJm9yynYUHTdBG1UVVmu42=
pihAGX-vA8iM2yklJAgQUDgNbkYyQd9kfjnWLACw3PJSmuZ3m3zgIrC65uuU0gavaIC5OS9CTEG=
W-w-nLAclZyw1onjth-QOGZe4f1UuAQuyRxK_8pyUl1_cEDLKzqXkE_9FrZIMEdS1jyHJR_l9r0=
86lWatOFfkxmdZdDGJqZkhgq0LeXwv4GmGk8wV_lAX4eZ2Ujkqw-JgqFwoyutZ2PwfGDzsrTNTd=
WZK4uX6Bbr10OjtF3WoTzthHHtxZrBKxAt1wgYseYykUKSEmX1Kon-i2gVZc-gT2t3ObDx5cbeR=
Dw1XcQiQHSOot8-TfnVTuKZI6AtFGHDfNVBXMk1EsSE2u1WZ7U_zht6wyhb40YIamaYbQ9erQJL=
8pf_Q6_qJxE2neqSixrt82oqsM0EUSllNmOPnKRFpRMOEvHqBDU6qpektMO4Ka75pttnL9BkRyQ=
9kpO0vHvkUsOYIfE1f-zD77z3wlMqkJYW3-rZqHR4OVw7bIdXj3pOEnhpEgYzJNFRv7Oc-QwAMz=
zIQiL9c3pjPQoqg1MPFKBjOuCGqL47rbV2K5up_DGW58mUcoqr1sqnK517yO_JeA38ZCtSblpgV=
u8kdGXq4HsehFMPLP18AUL4SanxgslhbSuRjOXsjnANYCauFu5ViStR6Je8fb-tDB_Yjo2xMdJF=
Vxp-VvUEjVItUVOTuFOMtTO3gvYrjRiaWsePvKD1PygtvWDU07yD_T6LRGApwb7NJ4ldjD8z8o1=
Y1UBYljSE4K02WKsm787lkfjTgCVtRWn9UBJPxAPmL0XceJn4bNapupup0XniwqtATMLjEWPqLH=
uafVbOw5yvx-kTHsHjD_5dsHw66OtJYtaSG8mQK-JaUlD9i8vKHz2bUzYjBqt1oU0hcMllr73dd=
YtABibFlkvIVviorCLTq8kdUEyd_Ix0vJBaYi6Z-Zvl_juL8CHmPtS6IRFM6CPRJ1ngYQbhKydL=
-ajRIpdweFdtWWbG1yorldyYrkFjyQL3uv5L1kG0E33ml596zVJV6OusKUlq3cRzsmoiS4k4eCi=
mLn0afvUjrzRDJWZg80JucdFoXTrg89KZFdwfckki7h5y-IOTqTg2krcTKmuCtYX91h3xoeRrNE=
z8dvjJnylekRfbop9jnqjS3itfsNywSwpVG_9vqIQ5GJ3JtRl6ZLol2okWGMdMvXMTx4WqQGfs_=
hecuQsUNvUkkDiZrTVuytDb9pp7g_0fjbmeDkemMN434VMCcbN-0frzeRr1FJoncFVwKJ7nNnKi=
ak8J7Mrk0Tndn1cQWHhl6FEq_8yqKS0-h0EdZx6s1QjK7KI4hbv3tou2Efj21UJYyYpthXO6JcC=
Q97aDM71K7iP0bnXUtDx1AlelMto_3Fzj4DxrSNG-xRc5ZGOwfcdlTuHH6QAoRCZHP-aLjFOp86=
dcQqDC11KDnTBnB8oyiUZW8VMHpxKU18JYN0gZcgSZigETjKFLKevjqLLDoZkKcDdidazZtVwSF=
1SEQPPWvTW5cLEGqzVBcPGHfEnAzCVfWSC6HFohK8S0Lq4biuT2Jt4HgoF9KGZ_roMLHJ2PW95e=
OtYpbV_suLJbDK23V-v1j79YooKOG934f8eoUr7Y7GGM2QX53xT-eGQ69AXxMgfIokAXJvr9p2V=
i6Cx9rX6Wib9EsZQK41VQa6yDBld4_WLZ46gHLKDSbiuM/4bq/kEQStHXPR369e8SlRa1G8w/t1=
/h001.7_dsoJ2wNYdadb6mEyvBpQQ2G2pbxL8YsktktpeB4vM<spanstyle=3D'font-size:40=
px;line-height:36px;font-weight:bold;color:#05203C;display:block;'class=3D'=
small-header-title'>$1,027,594</span>Seemoreflightdeals(https://ablink.send=
er.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZr=
UkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTn=
pC9RmxJaBiXQQcdvWQLErd_5gqjrZkvvLP3_1O3nEbqtIuhwTZ_apCTI9wJYZGDhS3lvWRZmVHp=
0lX9vyf6vxnm4oo3Be5Yb1Q6-hXn8h2pUxNiCSdZxp9VU6f1XBoDgXiKx1iqlJE_4ZA_SGpuJ3b=
RTZ5jWwal4ypwF-rY2B_7cDWeXBPCwh3635Xo_4T2vYL0Jpwmb_QW7lqsdBvyKkbxl_A3LF7kII=
8fIwRrBHI7ETAJsQK7gtfjoFRY82rkBB9yuex80nTSnztZCUms-Fa4XrrELSpMUbAfy6Lh6Agnl=
EEmruttjyoRMDXCuaMoi_pt5XboCtN0eWQwRIRpC-j9UCeHbhZfTtSpaOh2K8-o3QoBXNzr3Ycm=
q1PGCMokg62VXprKgWCnfxwEFy4rVS8Xw0504E3jJTLMIbP7urSXOfiMh0v4MMMGAOthRcasarE=
0vQ449kRVoxQeoP71Mf3XwsOIQray68EY3hCnJU1w0XmkBGcZihiBdsxPr81oqX8yqTEnHkfWfY=
CV1C_C4eTyYhFUj3xvSKzcGv2NZUv7E5PMrWm2edxRhR_N7KACjcCO-A5-eJqQ5NwUdIfVs3DfD=
J63xkdB4-fB2tvmUqpYfM3rAi3zAar_9m6SSWLHqw-vNyr5pEG8FXSfzQkoRYYxKUXvKlorcPil=
PHK1f7IyNTbm_Lcde11dTtV9QMrAZ4XYhwYn4nLNOPFwNYAqhmodaF1lClm8cphc8wy9otewWfA=
dw14BmPfGPY6JQQJZFkA57C7ZX5cpFUJl0EUEyhz5SKdjjBGhH29uPqSop0Op8xV3aJxUIAMlq8=
n5UXZn8KmSrw0i6T00KpMqslGHu7wVPhiHVjPsnZN2BBdv9vnxLAFxiIwQm21HZQNNQVZ1Y1Fse=
P8FDMnTtqg_UMoWXkhagOjwCwEeCiJaKBbvN_dImkWeeZ8b0oWuDrG2ZEPyTINXQzowdGWFcFZD=
nNAOol11BarKU6zRWR_BrOdX7vSgk8yY8aVqwjCcDXvaawMJIpjnEZTCETz3EesmPlm0Yiq6c-E=
eV3oql2Ab8nohkPFL2oitl2hYb_VhhkZywrvPnQex4JD4zgOIHGa2pVlxgguioJTi1qTKCcibqC=
1EWxZcu1Kx48-sPqmjlTgzBoKJhACzPvPNiUuNqiz8x4H7bJo5bYIYJDS1_M_w-g9HewRA-WD6X=
iNqQ46Bc8s45xVUcbO0I2tD8HV55oKApnMnf08JRCMaaRCqgMUWCb0VmDCLayPH-MNyMB6Tei8B=
BAsWmC_z32sOyZ0fmxtfZYP1pYZ17sPYrusc2rKiC62Cx4iuLeghYaUhXaxlSyZWnZm2kfp0jOi=
imsmZvGqb9Y0h1VYa9brN79mBJvnzawOJsiVUqlJaNc8BcowzL7KlCot9HHMaLYBzqK7Iwr_jFD=
PnhBzpgOWFBKHQIFKrJ0rEaKoQcICI94cnb_Ow9LdAk6St7XV1w7crTjucE02dc37A0JUx8Jx3k=
prBVBYe0y8ByXAfEt5W5N6u_q5zXVjFdiZgw8tbhGbZbcMcoMn5QEzTx0RVUvYJonMttwImIhH2=
mEw_lGM8pAG2UPjB2H6a1R_VO5QSJ4UEysoyUQ6-nxLRQrPQLL1NxpE0wN74xQ2jBdCfbDGBwqN=
2RqQFxK_n8Vrfa9UbIkrugXWKTJ6Aa1c9f9LPBHR72SoGNDVM4h2PlWfy6WXbcdiWMhuAYQbaY8=
IZFf8vNRi2oUnHV913veU9nFoz63lDoCf173OhT_a6SrRCrViOgVi2ct0Gk5SrFKSfbXjcXX8SM=
G7J-wb32RQft-hOsBta84-q1sBHNF7HltWH0Q4hQPy2rcMIrCc4q-88dZM5byE/4bq/kEQStHXP=
R369e8SlRa1G8w/t2/h001.eXWffColIRmr9CyLxXPMUh2pe_QxBdom08qku6TIuRI<strong>$=
253,483</strong>anight(https://ablink.sender.skyscanner.com/ss/c/u001.xvxeT=
nj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyU=
nEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2N=
QFg8lXHrZZFLtAEWh-0gwvNENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5I=
SMA-4u78Cbk_KeGWU7k0mjKqANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvV=
L6xmm6Ze0mCpUcEtsqD8csoouaFd6hKL4BU2H9etixnzd5o_y0h-rjY6CahJv4WVJ_NaxgnJpRJ=
_Q2CDn442BESC8fCoQ4HLT5Um0x8MAcgN9FONu98NxyqFuYJlwqPR66HBndw1Bnma2SSgWcFt9t=
WMtIcr8uSqfPoaa2cWnRT2Zw6CMrfIJy0fbXe-Y1Q46kyKg27rvG8SOM5DKtCBDt8clukzt9rmI=
kyrEaxqvOdKOMtzDjkzRUdqhEHPzIL9IZVRDUaru2-eMGa98ij_BlaaZeRwAJC73S053f0pA7wP=
2572OaEytCPDA0rT6U87GzmscNrs5rUJpL5OMQXyGm834ThVsSyJCnpZcQoQCoRWAeQjnqacN71=
TYpLFLu0mVgspPOUxygITPfXf38gYoyHDtriXnzfGC-WjOYT2ksM_Hey1iu1vzvvit_ouyn_h5-=
Bk9pARSJhueGQoc7HGMYwXIc7PfhHfQKzLY2KmKfmWYH-n6d0LU19EhNiJvjKqAw2O54Qu58YfO=
f0Sl9D94ClAuTjG6If4pZ7YWUkLn_HNFXQiB01NklgyWB6zHapom2hajthj7MPfi90rPJBxRSTR=
rRQUDjjUMPaozg9eP45bnk_ihJc8sTxOYZfUa8lJJYh2c1b5jzkzTKWbM6WxMGI3jh9HbdmK05m=
lIGuETa_d-NJTBpm7Xe-3QLj8Ct-bzi3S5hhU7iCK5E2EzJ2yR48q3LdfFQh_ILOFOpjn5G2ADj=
OeDtAfYb_XwCnU5L9FtB-78fYk6opBVth4yZM_6tnS2BUDgl_cJjhRpJQz6R3bUTqYVxO-gBiMp=
2BfmsBnqeDvb73iQkXDV8dBZr9k5G_eSVknzxr1d5zhgQ_lMxFEMMJy_VP1aVQ517WIgInlQ9DI=
EC9DQp29lgTzso7Y03An5NQ0RlaWEEW7RWLjFA1bqPQN9oAZzhHtpJdLGcvPrBbjcrlsDJ89YZb=
JIirqOkLTxuLhFgZGf9AWqzQo8q1p_xMBQk_xd_SplvyFx-R6enMQKyctuFWTolqU2uDzd5r38C=
4Oi6-AD-c6HE0L0gPse7LfJJsO02FFN3IUCHYyQV6Yz64e7cLFpCAo_Wp6SmMKSUAgLSvhVbmOv=
O6WMqoIKWzvAcVqBHxFwjEHXHPFgYQz96yyXUiHusAyraneb0z7hytH3gkkNodmDuE_clbNg7FP=
KRmOfBBfT1STF854RR7wJrf_-xuow1L8rhtaQ8Uy9fZDTQ19LfhyU4sPjEJnb13dh7SXq9BWK0f=
HBhNkeflxoX4rCStbsrhDW1PJajoEZDzD2JDfymNZqeG8-Wp8HMCR9pjcBJ9A_8yl6T1RwuNLOX=
-DwMYgEI6LyDMdKzXyKlH1C6-PKvOAChGXx39HcJS1N00IOAqcc_qTzSzFVKX7GsxFuSt4crfXO=
ZzGG6dm6p7P7JE2AWJKZYiNrp_DkM7d4lvm-KhwBtcq2UGvgq6uWRKFy3W_8cvMUPhN84fmoVAf=
92QcKTEr1h_X8pPXo1yS30X2irjF_NPKLfKyKSQbV4qyQ4TPbw1h_VesVG5A7NTTViT_dQSrSTA=
2FZmb92_l-SF96oNuQZq_Js08E9isWvc_R-DNsfPCdT1PA00nY8CgGd6iizTGo-WMsy07EJN1O0=
tVVucaHh5g3qb8y8R0QJXs2_vIWuwMWxW5I6B7oRPJ8bmw64LiBuMZabsjkBvr-u6e29lnubedP=
IIT5_Kp7RgZCsLkOswprq_Ka3QAYb1l680Coxhc6aS-vn7ExpL2d7yDPJ4ZmYG9jE9NJA9sDgnt=
NhW-HEZBDbKuBT8fm2hQXZfgjtHAV2eB4VXWj-xAjdF1WVl4aW6P7ljS_MvMGp-0N2X_MAzhE6R=
A6UNJDWpnps5LUTVC2yhw7OPMEwhzpyvj_GaBAza-juuBu1NR7c-meZwwW_BQguZRQUe5vS1ih_=
Te94bhA/4bq/kEQStHXPR369e8SlRa1G8w/t3/h001.bW5x6J9tpdJ5WIomRYVdLVMwVeH3dq36=
SyCYw8MQ5v4<strong>$828,785</strong>anight(https://ablink.sender.skyscanner=
.com/ss/c/u001.OHuv9NcSpqjkTP75eZwI3CjPK-7qN7psx4T9G3BAnjC6Q5Oc9WvU0UjmDcW5=
_l5LU7wmpp0igRBWsRiO4WCxHHR0KwDiY7GNcRsYGrHLL7IcI6-NVmGQ3ns5eTxvmKUuNdwaZua=
kIq6kQTOjx_dp9BJpUMNSmzTpoo7hMDnMdzpDEQ505nGucMuu8mX3bHUh1iiM5BTPgEB_VOaolZ=
nMjXN1taBqWminY1SWKsXLYilXQZJHz3FCAxW5Nh4Y5hQ82B1ZkORzsDNxnmrtMAsV10A8H1V-b=
OSYERO1zFzBxM61GuSG3VZjmjjviQIgWvR9s_87cF0JHxunHYQCxvI4C-fx2W8svhnLMmZlrPie=
iii2qL8W0TOx4Hl05VunSAArf4kgltsG-9rNDu0yuntZFDYYmIAbngIyFcW62tEyB-ym8EjAlDl=
kYTQvZJFCpgueojxPdmePFy_z0wEigTaoV9x0RC5mzBJuAoFv9YaZEFLvqhyNwvSV49Ybt74StU=
vdFogccYXzJyzXj9HZmqrmbOEbUqWSLWkXOxvP-9efx65SxwmJ1AyChgwiX5dbqPvxhrVYOxwzu=
6oFPkUJ_3utxvxH8WfYESO1Bpk6pObeVWk8GO2xp5SbyL_nPmrODCLDrt0aFGHmqLoymVERe5Lg=
67q1fMPcyko2AWUz0L6BiDB3RHKSkXkIYWiAMMIQI_jkwuscY-3UysSQnd_BTSVbgaZxXZEpyTT=
F8W88tSNvuTxfCROWunzEuYQklPPJ9WWBPF52pG0FXz228dOofx0mSs8XibS5LM1LtYCIxfrKal=
2L14gP-Zdmv-QzBvFMwp3zzhiVAXyMUmlEVa380ooEy9H7fvkmQzFOFDNbZFDeUZsgLzjvYPKQh=
lU8txklDsgcxiTJuSAHmbiInzPkwo5uUgxBEjC9KhBA_-VquLPeFpCc6jFInILPWl-WOV2Jtbct=
lVevXro9UK66jAFHS8l9VgGwGrv12mue9QPXrWf1Q3oT4IKa1SUCsGMM2gXpaiZePxpGXz9xVXO=
x7lGjH3vQP3pKySooI7hNZK_OfB9CQIrCiWb1jkZpx0_xq4XNd6CBCbLRs926F7GSgfh4fHGOFp=
l9-4EYp_cOvM6dyTpL-nG4J0ptFe4e75UI8CLsJbDOTzErrqF8cpzxgcZVBGmYZGaoDm96hnUdz=
l699jX80ADIsvzBaXLwGVu7gRMvcNLormooBRTcOpGIfAAsodwqGznfAij2NFd7I4bfGplLV61J=
F9vbMxJZFgKZ9y-76dnIyub7UfdL0ydUzdXrk4_XPwYL6H0xuMlt7H4zF9njd-ygk7XBomAkkzX=
cG3LYj5W8jr6hqvVXpceMXAOVHh7S8UC5QmWEWZjVzv6E9-CmzNm8Hsf1M4URvKLDy-FSg64yyO=
6MNya9_QhLvETYZlnPgXtXPqqSJpNL5CYpuG6YYWcwzRymyRk8Y5oDszLXnRcVYmBL0p7dlfl9o=
FGaxQ3AoR-ZJYqxAtTqfm1gofKxP1QYPbMLTg0KrLRgEpNZ2Aoa1ENBaF9FK9qsvVrqYVwc3fS1=
fyiuAAU9g0NGVPFcXh99Mo5_P9NL1G0f5NmgFNH65vXaD60qEbGZEZjXl2rdkC3XrEQYQfvk459=
saoMfNMwwI8tzSXAkBdHsmgXVgTwHUfMtGRPFYU25uoGJF-uL8eIui0UY0WbAmZPQVQfKrm0wTz=
7vgnMj06X4yc7XrocAhlJYHeJ-Gu2_L2QyZ8FGGx12OrPOIw-Lt7bfosjmFcbBxR0Ul0XoqAYKh=
9qI88eQcNfoqSqShZdfnfnWz2Ibg-381GvUjzrkyxJSU5pIC-DsDFbePqddQkq1q4YgTnczyLYR=
vydygaQvNAxHl4rl71nWGjGQxBM7POBTZ1tXS2TPJlodsDis525gqb7GFg8HAX20jOWI6Oz-I5k=
_z-m1iWiMEtFkIwSd3zWZOC4DWVJ7Zg_bKgUSbokZDBS1KRe5HcjbLEcGr6m4OYxP4F9YxWuMec=
0PB9rfV5SHkBr8u5liOcWhK6YecpaYZoq34-bnYCWRcPp3RoUDw-mAZYEJrw9GgzcO_1FDEP7K1=
j7-akAm74FTAMbJuOunWX724pHXYF8DtXTYpFcEriqJPP2qCxTrMuRMlxr6ilDQq3K9qsBRHnhP=
3-VrcXgVsPvsQpa1K6arvLHauPP71V8TEYxVaegMjrvaUAgo37YGANM3CDrwT1K0YOXxKRaAI0N=
QDk8eJfqeHIwoj_vVwK3QIEj-oK_1I7RUa-nv5MWz1h1aK5oTXJCHi_OEwy9ROnPmp8xho2y2MN=
aB192donkJvM5uMIaqxFPNNs1dQiQCRhVOcGdw_mxuwMAR2kDdKABBCiIqtO7xR4OUbH7EatOHr=
mv6IOCNFxwHEm5jeA4KZvCHTU8UHHxQxwRBkYhkdzXHsph_GFkMJOPxJ4L2XYlwrxNYOM7BaMtd=
wUyObRmc93g6lggBULnbBIejzC-mDWJ3idXzRVg1oOFpol6i5sJcvGfNCdzFBLTl5aO-Hc3ldVh=
gBvu6rN_5_Uqlme0cQFLE6IHu2gQC_nRt9X6ovs3qD60J4f8oy3ZaUrF_t39ttZi0W-czLBDna3=
wCTkLh-Vki0cD2IcuOWzd-fogt0ykTFEoEi89AFkDWCoxL1Qg32490Ox8urtAks1Gkg5Nwtb7-g=
OBQOqaJvB8iRBRbTnVIOEtrkp25wQ4dzNQ-DvrHM-5uIYxtGfxl9Zv5dqpWuvAd7JTcsF1eQStj=
wiOwGiP6HPUA76UNi2yFEKer56TQ5zUn3vAUX8UedCHKBg7Ub7cmHxFasjfrj70w3VTnaESCpVv=
c_PF8wGVWGiZjh1YDVrAHNgjaLGKanDxn6GUkzALsn9OKDsKIJJ60park9Bb51wdLn1dWNg0CcC=
oRx_zUBcp6kSfOmGyNTr3W6OfBFyHtd25aymh-f9TafkHIjMaxq9oBzx3RdfS42eEevQumth3xH=
Z2dpEhCkv_Sfx_ZFF_g2yPIkKtQE2f2byH1yGvFS0p_XFBRjWFGql87s_oU7eph4ypM8NG-aIyR=
sySw7ArPhUGmxbZCgzmtUAgLsZ_m9RJqKIm6ARkFDB0nnXXsNKNhpbGEtnKN1a-zPDIKrTXD-7m=
w0IVtwvXnfmXKZ-efiYEjcjR6S9EU04_XrFn08kths-C2TA5s9Xn5yA8oD8VZh21SaA8lk-n_Bs=
hMzFxse7LA_xm6hW_pfbOsfVeeL18S2XyErURuHOSWaUetNykwMyoX/4bq/kEQStHXPR369e8Sl=
Ra1G8w/t4/h001.hVS50VYhnCXMovPzoRnwUUXXIOtUqQb1E1w90pJKz4s<spanstyle=3D'fon=
t-size:40px;line-height:36px;font-weight:bold;color:#05203C;display:block;'=
class=3D'small-header-title'>$254,884</span>Bucharest(https://ablink.sender=
.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUk=
iO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daC=
ClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJjxD4dPTDOYg23VN6RzsFOKpS8ju3N=
4XtORXwQJVx4zTV9Q_0ExHksN_bW4Nw8ONwLGswnEROGIQyaBrGlLRYbAHl4-o5Hvh-gZ8h037z=
NBUOaCudNxV3YPVvjZ9luspDbI1kTGlkQAyw8uDB0WRkXLfxoc1i1ECswUtODFIS6Zd3gRFjYYb=
l0J_ycE5itGH_oaVErVrkk-sPuUwwHOBB59ee0mlVeWCRRqV3XREKQNILcZwn-mkWQDCNwIjV7r=
GPKXW-seEJWlnn0E1b-uT-YqtKC8DNmoOOEjOSPBX89eZ_fr0ytbpMw-3GEkdomnmHGKZTKJmaY=
X_G7iC29bp0NG0X8kKBGaQymKzukz1OGHijLsf9A2QkIsVVb2iUfz7wLoKBcMuYO6OWNNPmksBT=
4RNSJ-2EBtJtKDrFnELnWT5Oy_JEiIVPIfjfAHpFxL_w50ChDf7nMD6mAXP7No_4Eh4zf6cwSXO=
up74ajqquUlrC1vSAhzAq5AT-svYvVY2GEBlB7p-ONCpBa_D7olsDOUldteRIoeN3d6cfge_57i=
32qKWOCrqzIbIKbdZDSLQ9ZMlHwddewXSGU2Wq6jlluPmrlDj-cUviTD6jpgWEFwUGWeADjbGq_=
HZGiIzhcZceBjOTCxPxgF9C1ZYeKw8rbjxzdfgtUr9DjooJ9R3QPi3JDMskTxdb0Ea91hePdDGY=
e74eeh-B-p4NDjKSCxaCt-fk_5X9UYLRsywddTpUDKMm81GW03ndYpSA8slg3zpJqWNrwUIkCoA=
S55E5B1EtvHKfQn1KWcqv1HYwu05YCy0yP9KQIwCmk171b5BAIewNc0GKUJEwS73_ZVEa-HSCOL=
4KABX760HXcecOQu1z3ZGsWx1V3WWf8IaAXxrKYsk_8ZcZsYXnWz8r1-KMhVMJ7j9nXTTfiTKKs=
VWDo6Xil8yeEf4NPFMYucXAQqcEFg46VnwrMPwkSa6-DMGedb3rTaDbxGIDJvcoeY3aCmaTJHd6=
2T0BXEIFdDZv5UsHHwDZPmOb-heJjolb_Td2hyz2lcxLTMoWlxZUoLV8jCIeGCm7O3I15xyqzPP=
qnkDFqYl0hcL43b5kU44iuvvN5oG9jesQd4m9-ZDtUO326l3ZZad4AsubAf-PylHekiG0-JTori=
fwy9HMykUUqOJ3O11YDfpYsWJW14VNxirijnTwa7T7xQdF6YIkIeqe2zVke53ql_O7TGTXDJm0i=
42VaXgjnMK1HsfeP7-JPc3Z8IMt2sp3oqlZdtQ8d2xWkGnL0Omu-BMx96EfD7c6qRr-fX4qTZVk=
vAHNHHDgphV6JNbuJeiErSp85y7zLtE73DvQbfWa0nQW4S9ijyoXARmMiSK4ntdjq5qyccqAo-z=
KnikmrSVGvy9nVwtncbFwK4Y1slp-n5aYnGOaCyavfNjJnNHCHASi5Uit9gaNQtSTu8qp8Ot55r=
VqqHslrc1snIwrphvaBsal2QiyGwGZdsP49dzmqDx1RTuDgoQXzvF1E0vCk7kr8evRh2wqQx9oS=
SLRbk7uqV2FwGv6KYB13okPoLoH30bUzXou5mtonUb726A2R_s-3tW5nfEgkDyJeiOLQyTVP-FP=
c7MHBHo8cSEPxPTTvoSkJOFYJJpl9klFya0TtvfHjIM_GOXijFeIezNLu8Vr3v_Ce_KAe6ooAc1=
mIRCOVmRjM3LxqTY_LZ7D0lvTMAVA/4bq/kEQStHXPR369e8SlRa1G8w/t5/h001.oPii-lKi-O=
4bXYamPvsTvlj1f4tIy2TVyQMu9ZOhMZU<spanstyle=3D'font-size:40px;line-height:3=
6px;font-weight:bold;color:#05203C;display:block;'class=3D'small-header-tit=
le'>$508,893</span>London(https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJgjPTKlgmqebo8hXVzX04FROs4rw5t6nIORJFH36v9m5SXmBdAaWhXydMa=
YSN2AX1NDsskSDE__mvyXDhJchq9GkvZ2Y4q2eog3CJGriOG-jqMztwVGToOWRQnf6LPwhB2uo9=
fZ6pZGMsXB7Jau_Gz_VH5a33ZVsP98OAhcGBofH96-VYwGY8l0GND_RiLPfee4IFzqdqyCK2Mgt=
SJijTmTvj05lKK2WJFJ5HsUX4CRN7nXYcbhP5PABuYTEcuJQPUqhZ8KTG-PsxmDGDwyJNoaXCfe=
leWlNlr5h8rwD40qY4Q1WVAnPPHlDoySC-Jh04jd7zzzZ-E6Il8Bp5MofwECetM-HbvAJ8w_mP9=
wuK958JyaLS-XjflF8E_MjQd4EPV0gJEmedte9b0-ZVUi235Y5wsYzXRMdqbT5d9neT9RhZtvyn=
1NF4Hu6gX0u1wU9u2N5twq7xtmVdyMkl_Aayc0Ys0rhonCD5oOuqTlrGcYjQ1k5jX23v4bNhKtX=
-TF5YswshfUmtPCxEc4piQdLSkxj9HqpCco9omjliDaxIOa7UNLk4nZ1f6qphwGttPqHJuIhZlC=
RvSx_Nqwi5-TjE8zhkGdghWYKQhY3yIohmLO_XloNTgKkxJSqbgHRrRd_LFt7KWBySxQ0SLBbX_=
EhN03Grc85SODJMlEBNhE3OuKmz5A-nQCjSyUiVGDWdk5NjLGiXLk97hNCzgJs45OrsXm99o7nE=
G_dv796dhhk7mv6zYSimVcx0XX7j1k-eV14StQE7wYTM0pRM1OhHWeqGL020HSjxqGQTNBMeUzw=
qpoSrhVruhc-B-YZk1EdIcL4FFgE1QuqAs1JmkjZGlizq72XVlN8q6TZ3o2Y9B_fhd0OOXVVU8Q=
HDF5z2_3k9eU3ZXL5xASa0spiGCYATEm48UuZDrJyIhKvoiGt7y7CKndXKMqgEmOegfv2f47exG=
EcaC7V3l1iQWLWPdlarourjvE22XT5gndtBO2GEstlI_RGoHHnS0EyT4e1nYOsXnQGBbXq4WkHm=
CKercBLFD2sJxEhkK5Rg4l14IjiVRhcGHbI5_XN6wSdwHytXvyjBvpQmH7O9dPacRip8RWHttUK=
OWAfxC4jLkUE3f7Usf77yzb_ua9d5RKkLVXwfhNnL9LdTZBBXQ6eHwmNfuTkklzZRoDqBBU9IcC=
eveBEeGm4mm-7CJtTtOXFL19k2YQccbzTvqUQf8IdKsnVB73NFY9lmnh-JAHxibYZ98eQ_Mx3sV=
i32lf2H_vEC19GlZwtIOfQjyX43NcuTZFlCCSTHSSq7ADtDcDGG-pbR72o_C9M-Nn9iNLLuPS1a=
y793F_T6fCwSgM9rSJFuioX6t6uPC139ItJJGIeEVyf3SlAJIDxVMPyybNFmyu39F9EIbIqXmcn=
ojMxpPQv9cXbkQKH3e_35U66AWloFFlIkjcLrlt-cMSOpU9hqP6IfIWbfEUyTeEJ-77AFtVWy_8=
4AiLx9qdwr66EDs1rt2sUwXPelLvCdS2FGBhQ3jIrFjm6osgq-2KzP0P6YHQEwZgMLr7VWb2u_J=
WYVEZ9YnozrAbXTRQIfD9DYudKBxinUEwtbz-lSzg0QsxqI_b0MFCaBqw8l0tc6sAdeRalK3El3=
crSg0n5QK3w6I_uX8_I6IYaa1jIUJ8A4Q6TuQ_FvMa1lJbLo6DCvYvyTnKl9WbWveujjS_fK32j=
w/4bq/kEQStHXPR369e8SlRa1G8w/t6/h001.5uDdlRKlhxZZvFJpJK6sqgNGHxKySaFuOJKbdH=
CUsJI<spanstyle=3D'font-size:40px;line-height:36px;font-weight:bold;color:#=
05203C;display:block;'class=3D'small-header-title'>$531,407</span>Budapest(=
https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0p=
Ni9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOW=
Qe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJhTyuHqGD=
W_y9_654yIaPDxF4J6lYiugG3wBK4Zqgpdt02-Y4KuEgv8D-CbXg-uyO0_oWQ9dv6k-iMY9y_zn=
bpsSfs5Ogk-EQl1VkAgypEREpWAwTZKlRW6RCewZMJexFc7Wk9wtrhethdDfn8lyXmo5ing7j0i=
2RkrcZcCMleDSkoIkl2xwEoE3bhis88g1PdxKmg-XQFTFSLzq5nxTbM8-PGKlGBZOslwnvDRidV=
OQMNVryy1iLT3-cgDJHQa8t_t8n8DGpYDle3qM_wLblBxLubHJaBrx9rg_3KpOmnOJpU6dSB4Nq=
1FsIMkDsAtLpo-J4f2D--Ds41QwP39Y3Ar27iCc1344ia0iFPcYPid1h7fYZBzHDX0p_N9fVECP=
EDJP8jnHMbFnOSYbtTlDoOIVM-L4DreBRo07ksvHQbgSXU8Qso_4f5Hd2-NoaioG5ijNqnjQd4Q=
rliwm6UT-8wOLVFuGW6AaOs5Gd8CJ1W0We68ltjn1QzgBYKYqD2tXNGUE34lS_NEvt4RT_94Fm3=
YuLVMmfNmOam8n5vJMLr2x3LcoCPVTdzrHQuldBUL62ytSixUfk51mw6QOV1avuqkKea-6zWiqU=
TQjXgp4y32B5vn_iCmNyYe0Yzoq0p3D59_GeokIw99xstKgUoxpYf7gjAGlLtnYWWMCnwWa9TqJ=
jGDchuOKSQGNZiesBAinRlwzio127lB0hRI85nvduzBkzsLvfMro7XMa-lgMKCInlUKFIS4Hoh5=
5WmmI8ZC3cbwPQD7yGxvdK1cySSH-ep9Czkmner9JNv7sjkIV6dFaDCkPMBylMfcxVEuVQ-SLNY=
QJlzaqRpKGHgqPy9txSiXJ12Gl08EWLRKePVYJDBM3684ZUjEFnc9gErpR5wg0mUx4LbAh8hRHq=
wyEKlCEwKoUDcNOUje9TvBeP_DR4na-eKqW6wClYotRMZpIjpl9LNyUXTY8qDi3GlpDYN4rN4Id=
4nEHObfXIFRgM-Bgt48r-77UYa_3qpySDpWXIZP8kS-f0OibS0ijBau1YJL3D0xvCfP4buEdPBK=
icIAltsbalhPG6BsI6oyKnxvkyjlYrxk5L06PZiJfQFi1AZ6R_tr2OLfpP64z0ewHwRAyq-Nlg4=
yW2XE4K5MimFvkTXhh9XW5M0ZUt2xq1dE00NaR9OxnSS0PRziw6YiSaM7BE9EFrI1V35bNfg5iE=
xkXNa6HdVcOycWSXNrcr62MeNp6voxCUO0kQfxfRxbgmUONhklDpT_ZIXO5_8MUREO2S55py89W=
_U1jRxSu4HoYnKj4kOwv2jjQ3qS659s-Lg7yj4UXJBDlblvW8_95rwKwuuZqi-_bF5Cf4xdjL3p=
JodX2Lc86fMYPZRH5sbVOVykMoajR4sGESVull6lA84YTymEp01W2Rlzp9ME350UeGKkPV2wYuq=
7mNftYuR1QW-IUoE-yIKeC2S1qpU-kfxXJ8UQ-QcvxICKouP_FPsp9WJG-5OKZZWc2hxphpDXcq=
3ZHMT99_MYGdI2wKhZm_dfe2626Ui3exiqRICstvbOU-uUWbeWQcshm-jM_QqhPKh1mncpEdRXU=
wmh9sprnUY-IuDQxCnFgh3UQQuHlWa4djT2EHixS7vP3k1a3pwkkyke4G80Vo04xWXVzObfTKFG=
DZdzPeNi1-JuaOI1yfZe9XAy_6fbzPp_JsRj1IODtCcZo35GeA/4bq/kEQStHXPR369e8SlRa1G=
8w/t7/h001.kDSrUmJH8TejeEILTwZHqtKX0kqTvAekbcGlcQgJ9sw<spanstyle=3D'font-si=
ze:40px;line-height:36px;font-weight:bold;color:#05203C;display:block;'clas=
s=3D'small-header-title'>$627,910</span>Wroclaw(https://ablink.sender.skysc=
anner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmu=
zG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHD=
pQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgh8WiUuS7xGh9mBNY8HSPNquDpCx2is0l6Z=
wW76Hnw0dJYxklaUx7JLR0-RK88yUAbFH1phgJ4Vw57bZXZDT7NIWaXWAEytQbccULoHKZIr7L3=
c0fswcySN5W6tZpTLGQdfUoV9XZDPn3O12U_2FntgpQWF1H1kvUo11-EYzARaSvwb7n4G2WO_0E=
YZwv5hC8CsCX8ARIJ3RnUuiv3DGhzCOzYEoherzFLfgmAuIJcwjXxearTqCSyfu1yc_7H1vo3yr=
4jHSo74de1bN-dAvL_Fe4RSw6BkNE40gZjPb1AOg_geEZJLTKgiMElJehS6IcZgqJlcjR0wA6w3=
2cH3WqUTUgw2jj9wE1V4LJx8uTjd5qWVrqWdIsXzuIc8tgebYs6DBJ0AERS6SHrWNoKwBNwLV-3=
dej8zQCLGxEOdGp9mfqruB2Y9SUe6dU_nXaXUlNgqA_y5rLLnaFSzSOVt57QO6N6mcxipOtYA0j=
_pl9_WwX8HmYE11n0a5_jT4-KnykfTj0bjcURRuFdqFfdEtlDibXaYTQKzuZMS717Ee03qE_UFF=
2sAiDzpuKK_7EZJS7_XOqqZoH5G7Zb_2M1MO1rsUN1-P54VkAW4xoj3D6ARQiHf1lci7dcF-BHb=
J6kk2IfxQvjucpGc3jVfWHWMbGjydP31GYc8r8lFrftG1_KVRhCmFPMtv3pVnXDWS7szfs2Ad5U=
QNq8X5yy8M400egr9XqlVWqf-v5v1D9FuiXfTtDVgdhAeIHCeYpQ5iwVWHtb_mMgIIK-wJRntQb=
ifyM8JlnUZgZtwccMMwrGAPZRH1W-PKSlVBCGa_Bk5fW6idrEWSEmjxsdemmlwXLQJy6JYfDue4=
lx4AjhQxvIFjlHw4Tg5KHSfRPWonTsgL6b5_v32JKOcALU_ej56-creqhvCz882kEHb9k02X2qj=
Pwr5sbJ1A-2t2gmcXANkQ2G7Ao32lAa3DSFlFW1FV-rhmFJNvU9ZJT0bMKa7jARNNAMsZXNF_y3=
R0ql4KPsX3p1r9rP_j40P25dCSQbIqy4H1EBnGm5aJn9ZMYoAVW0nd_gqwQ8HR33Mz7BTsTD8in=
bpNFeDVErmxuGQMKMjR-PIBJqDOEzzRLn8cXbUCVHjg2mOAD6zWkFSRoz0rBTGfJays14U9-YX-=
_ert4RAUE4lOFQ8Ek0BeM3C6XH2-Q85edJu9RVsbOR9kq6l4_H9mKfiAfVJeSbt7tjpDZHdtKmN=
fajiHGkwEQEulkSf6f56ygKBQ_qmyBSTAn4aJeu_Raf-4qmdjayrjonSBwyEfwBIWURgPd9J_0o=
LpDwoX0AgGH483ImUjBZs6CA9VroMGBDIem67SzhxYBIT1Z2XvwiIYqAH7sUPfRXlJ5BNnX22UL=
gABy6MsplXZHLRo7jorfh0Ul3U4wIVooyGhM6cP1UfGN0jrynMmm4BudtuVpmKjXSH-69Lhh6yp=
VCujYZSQF9GyHl7UkuePoG-DgbdNKqROIzW6hQB0k2EWq9q_wRIZPJJ-C0lqphqJsbwiQZF2bPn=
snFaJLI08hgsLf1qFWBbTALB4m7rpViEfWklQjELrxMzuds_Wopyk-i4irf9T-cFxvCGgN2oCpx=
JM5yo0oqn346YoOWEQKgaoD8uIcqYkxEotuotcQr8xGeNTb48boU-dKWDc1rzDALMVmpsfanyti=
inzLYbPz09vWh33xOAQQ2YQ/4bq/kEQStHXPR369e8SlRa1G8w/t8/h001.8t8nyKPmADFWd-oz=
fn1YUbgeE6Oi1mDu8AKxN9YAgT4<spanstyle=3D'font-size:40px;line-height:36px;fo=
nt-weight:bold;color:#05203C;display:block;'class=3D'small-header-title'>$6=
44,669</span>Seemoreflightdeals(https://ablink.sender.skyscanner.com/ss/c/u=
001.OHuv9NcSpqjkTP75eZwI3CjPK-7qN7psx4T9G3BAnjC6Q5Oc9WvU0UjmDcW5_l5LU7wmpp0=
igRBWsRiO4WCxHHR0KwDiY7GNcRsYGrHLL7IcI6-NVmGQ3ns5eTxvmKUuefxM-SFJYytJmvF-qM=
rHryHtVvgLnVxgtBeaTLCnouYefedRK5dGlmuVF-avEVrRYXMu7M-id2c0iom2hrouZYAyfzb2a=
PElYlJe4g2MXQ6vQr0VOoC-ZXqBj-_L7VQZf8mVR8MFTFHJFo039O3mEiB5g7iygoJG-2QtcA8x=
0YxzhAu4suGpaPsTnpcg3Mq10ofcBtW4gZWZ72LF5Frsg-4yE4YsjoOh2eZ4lt0_WzUNwMq1Bx1=
EsMu8g0virsgHU9vokJjy_62AM2ZGPHogrcEBk6_c3DW28sjvYCIXBnHGXjp8NVOQY6KLWMic3w=
PfWZj8oUrfh00hw8GQu5-94mvcA3lGwbeggELPSakCclgJKznAMKOJm94UemIXBIvAc0CZ2tXOY=
zw7LlpP42yK6Af5vZ1WnB4AXcl6W7yWkeeqeZaCusZD1LsMEEize9ZkpeZEukm1_BeJWSEBpT0z=
1qVwUKT6-wRsxH9QGX2LzIFA4XOpMvfsbTvZ16fQBpqXMDxRPd4PwvhDTvstje67fZtIXYXKAS5=
jNVKFhoKRLxmTSaGKrHNxJ3VByjF1QtWHdd-bPrj3iZaijuIQPf3d-8VbnMo-mmZdGPaAjg8dj5=
OLdiRlOffkzZD0PV8_lFSf/4bq/kEQStHXPR369e8SlRa1G8w/t9/h001.QmI2dk_nB16Y9o65V=
16izT_GrA4-nuPm215S5CuE8zQ
Flights(https://ablink.sender.skyscanner.com/ss/c/u001.OHuv9NcSpqjkTP75eZwI=
3CjPK-7qN7psx4T9G3BAnjC6Q5Oc9WvU0UjmDcW5_l5LU7wmpp0igRBWsRiO4WCxHHR0KwDiY7G=
NcRsYGrHLL7IcI6-NVmGQ3ns5eTxvmKUuXPJOxR6HnlIJsHPRRT9BFJgFmM4WGN91siLG6_6NDL=
qzBEEBe-YErhHV3xUS_r8v4Jt3fA9zD1APhTpuee-LjyGbhUbNewwMEMFaz98kinwMWRrWnNNU8=
LuzOT81wWm07reEq5Jpzz4I9NYQJqUQA6F22KU1hXlryzY34ggrisk3IMjBnaMpIXCxnzDfAaXU=
Ci4iGmA2__vHQFj7RpYA2Nbuh8mKKqscJHl8muRkv8v9wOaZ3RZScUyf7ZmJDbscwQdhnASTa72=
2HJvDP4DAJXEowafZyCvdHhV_b6FwJL8owNeqfLiSSmQszXT5eaN3n2xdJeE4nH_wm_zwd8N9wD=
2VKMrfpsW-LuZ2Z1wWwF5t7ZiiRDLDgwlD78_X50Qvdf_qk0-_JQv3QXu9VLhrjmD97UHZYIUOX=
v-TSLp0qGE0_v1UbH-mlF_hLfQXi7qkqICg1NKctCejh4k1bhLVzXLJ82Eblo0GtAhjJ7BugnaI=
ozVRLCT--1llG8AQWg9cyXeYlP_EbBESnGo3QinGZ4UF9Iq0yCwCJi3lRFXzT4wnYGDCx2H17F1=
KgsJoYf0qGYF_tYxguLi5kKPMJtjFzrQ602j9q9nm7RrTePK9-EXajikFaNPtuFxgcFw5KOUM76=
MiO7zHjK_qnvom-yZ_LAzCHNb1D2FZDQj_kQpF-oK-oXmdAK5PojDC7CbpRBQRP4-n41_wqCju-=
kHGCZ4QuqwFap-qgaWRsyR3DRIrU1ugnR1MkjbWDkDC_MhZb7oyMYf1v37iwaxBIoe2sNO2iMDW=
jggnufbugNzyotJPgLv-aQD2q9VLCDF-psgU1QfoksGzLAeyW5ryaJ_JrjF-QeZfapnJyX9HUJu=
KiWosoqr6fnZRbtCU9bex_35r9IaBEW9X4pbV5jCNiudiogWOzEOT6nXDkeurcWCXsOIYpRRJI9=
Hb_nWsaXNM12at1my1W4vNFiuYKARLu4jSq5fEHGvAHMIRSKVwOERl7aeohXbrm3kMY38pZC7lm=
8yYRL-HkzNIfqKwJtXoZ5IRmCyqDJ9EnaozI--DvRAr2njPYURB_eGbZTVEmg5BguCLohY2KLDu=
Fj90sFIo69nln2S_nOFeO_VBfqjZiGGEoOca1B1DOmMG7bG7VzmgqR6fFoiWhW57z_oscbZgGo-=
_M8n3YJQJqeL3A2Hbg2Y2qTHiQhoaPCHyH3jHHMs4tIgNC2fNAxapu9nx3XNpRlURVzM2jMAlx5=
SIG7tBMTEKhBPAklxnZdvm4y4LNlG6uNmm9QCt303mSq-tCV_CnCxD45tp32iUoz4Vfd_zSIBRP=
pIPew-ygXUnYZtwNbqRB_sM3RQDlofbUGoAyOttJH34FPHg97cWkTV22t2Q7BT-dDPCuFkvAGVC=
l_HRd6azm94KFVf4koxntiwSIfJofnTd0KVuR8F3P3ADcJgsNQ9JvaMT_HOR7v-vbgJhX7H_eOB=
Bu2NCpaVwkMk9cd4zOO58YAn7i226Oni6Q7_wNScFQLv8xXTdnx92Zi2NmdNgS5lWJwG7WndIka=
J_7MAABEwJhio3xZUEYvKFQwq5ffrNsNDS4FpsU_LIuJfyi4GF7f4WdqIbhQY155siVcdBj4CKb=
caGrKD7wNSgDL6m169NvrCLRf15r-e7nLaMVgRmhSm0BFONaMxwtWNdHadw-mTSvxrV9YEIJlcD=
zrGEdEzZirWY5ecHWTwIaTQoE6-a0RNlQmjO8CsyNsuouw44KvNN6iq1dUx3RmGrVD8JJS1J3v5=
nbkeD_Vs58McCxlqCNVDLRXuQx-Uvnuuhy80_apnVur4JVgOuBTLXnnU9YyduXVGT-5ncBPQeUR=
eIcyJ2QNrnCWmeJgXyD3J00fiTtT-4myJFNmi4LUV4rq17sVOIQwF10Df7DN296nCrl1vbm26Ho=
NOy6AptBydRIB0KUqm7bki0BfwL-2EvHReIGTSjFBAjS7SkaVwjZVVCkqRaFJbjm_VmSfYyKZvK=
1Jd5wUSFOSMVqBTol1mv1yCek0NbmwAB8ne2GajYIJ5NmMJaKRzhPTybuEdm8J3M2ggfJ5Vpi_i=
7PytxN2HMdeQu2MLctqxXk-L-W_HjbiBAyIBr30AHH6L4RUW6cbSSIYvd1ptOvrPxEwPvGAwPYT=
7ns0i0csV40RBeAYPb2sE47a0CcA9JhcMC3FIskd9sQ5S_vAhwjfUfozxe6twwJmw5eLaq-yZZp=
x68OPS4w6rYcDxQYa216ACkDbRXkAx_zuhliWHfy6Z4G2eACR_1a8trJz8n8EmJZ3C8AvV-nAV8=
t3gRSJo1GpBMXEDREBC1wTqIB2oMBAqsi7dHP9tUQkBzIwmU0n6xWC-m9_x69DMe25VmAdzIn_T=
8xcwS7xIlqN3NtKzrSUGp3_rRaFO6FOANMiXlyA3jtF9135qmCMY4Ur3TB99uZ1OT1OPS4cjuyK=
imaINKwZFUO6-14DjabUOLELdEzxPvCQRoOKZ62iQ1r8x8qH6fSq_v8XoLlTYoU7xlYFjhNkuES=
j_GxNFEWM-lRzs5XtOHcZ93qacOlkYgSvHFn1mJ6kmcZIiLnCe15yBE0NPIC-xXyIqlYDTk2pn-=
ipSNYhgGIik8PWMKjugUbBeRBt8IaPpRpQz51JIrv-L2-aoism5ZbBp2Fygn4HV68pHoMECgRp0=
ivSu6wJpxeENz4EfgvQvM4sVbel6tbdpEVoo6QRHjOiyX6jw7GCU36_tp-qeC8Nxnq3Wt_BOLii=
Lf24KkN3VOPxBmIFVi2fSj3WnBjHMqXBibbmLY8bPS6KR72-MZUeS_nJzX_1Cjwj3xcrtm83aBb=
EVL1zkNSWd3XxgdUkpSZe9_1rwQxVdk6ie4fIfpjtt9XgbzUxjzLnKTiTI8pNfSwqz1SCbv0cxa=
gWP8QMYAdcy9BLxkh0jXD5w7jIjNBn6YH6mNoy-OrNcvVCkrSiA_RexMh88dTIGF2RkQp5h_70V=
vRVFfeDPEaYIITFskSavNhgLxBygg2JWGOSrsYqQmxut7ndG3kKaQue0lOQ45Kk9RX4BE1Mg7kf=
cQth3qORKOscRLJ4Ukt4NUFjecD4fmovOtFsWGs8Gu9pSi5M-IA480jOYQj2gKKsrbJjvzjA4uI=
rVz6zxYBjbg-I-im66ceQRVJ00bGmyjeyVBHp0caS641yeM1DZYEjT0dQnAIF03CpF0JQgWdtwD=
Qhn3n_yHjJ04e8Pnq01kJ_CStCS_r_DVqo1VGWpX6FzEE5gbj0CEA7yLexV8Md6UgCSBB0FC67Q=
cks7MXBkkqJ2YrnDkyZqdXle7mAdaomKCTfxrXANk5qjzpiNucBaeEVRCG5C2u3tqPZsmxbzD8r=
xB-7UpVOTmjt4VTcXyG0wk39j8E0JabvSvWmahTEl3ROsh54B3sJ9_YgNoSF9WAJaA4iJ7UjNku=
5ugZxxepMuCj5j_2qdSFxb4BQPnNHVFjdR7zzjJJdqWxtJyDCGDiCZ9JayTl2htsEOuWIMl0LF6=
whB4HojGedyfsmIBCgd752fOx8FkBrt7WaqRR26zWpFqFlunxk_bAz76BSTQoapX31wsSxQvcFi=
y0qxlI59DI29Sj-Sh1pHf6metlwI2L7GfSkJewGrPTJbRd-irtJjQo4wELcn244I3tNFsEhTcvG=
g838kb2fmNk-AYCnAPrlXhogQSXBXuIjJSwq4dZH4E6SKg5Lk7ImlVHHDMm3W0umpg78NcQQ4EQ=
KK0NODJElTgECd8LI_jPg5fivjJXWSS34LsWOiwdIduIq6X71dkIBcPsffN3RDWYDaz6WvOUUZK=
14FbPkgp7LuRajyRCyjnKsnVS1PBpEawC5PgYzy42_h87H8fHuTLRjJiFS5SSoWSQ81sNNGJQ6c=
t7REbzM0UBowqw6_dRG_iDJvKe5ebl6fLviUcgV8pkosKtNskto30sPFdzTQr7yj6KYWXCQQMp_=
E5Aug86RXPO_Dwr_t7I9lehWxsc1y-z61VtmKibms0xBHbek6HRCNdvBG7Mmq0ksrkaSFyNDWse=
LWS2DwFrydL7cqqtIp0ES4NIpsuiaLhbfPq5mgSJ5vQV3to2aIq4aATRCJYWo0mfrltpxesbnG5=
mYDeCVXKraKaDECRTefYNIaOUdRB2N_NoNDt-ONkHwGRelf7YfhvkR1lNB2kef-9hbtoSynt5iV=
-PAJl5i6TRiQh3IDcSwLLMqrkitf3u3oXNERgoiQHSdhe8zjCZh9HQTUrLsGjwVa2NnyFPIcs-D=
hVzz9KJnVT5Hda1pCyaD0ulFST7CfdVlGHMzrK3onQljBiX2IO68YcynCNuP8xAmtD2-_ewpbis=
e5hHsvMZbOqWoEFYxXeVvabYYzes4axtwm8G-Ri4XqZiSv53qzbQZ5-1D4y2SCZZmKYYdYNPof_=
SbEGgYrfpbojwAtvgMlcxwspMcWMrZQ084YHtvV-hy5w0g-9urYgiRYJnQIUiEwu702Js174dUs=
5mMIUHIE0qd94A8dUOt2_11dtjWlKH_6k49rS4k8ceeUHzDWvJZrIgkWglsfuTdIBcKR4rb0pXz=
ttOdgxIKAqnnYZM5u4433LtJ1LacNeOoIiws-U0_iQHLY/4bq/kEQStHXPR369e8SlRa1G8w/t1=
0/h001.khaItpp17OgQVic_Rlsd2-VAjSfatEtTfC6bO45phIM
--b8d57104611303067edaf6209d6b906a770ffda77ae6998548cc1a7a6ae0
Content-Transfer-Encoding: quoted-printable
Content-Type: text/html; charset=utf-8
Mime-Version: 1.0

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.=
w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns=3D"http://www.w3.org/1999/xhtml" xmlns:v=3D"urn:schemas-microso=
ft-com:vml" xmlns:o=3D"urn:schemas-microsoft-com:office:office" style=3D"wi=
dth: 100%;">
  <head>
<meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3Dutf-8">
<meta name=3D"viewport" content=3D"width=3Ddevice-width, initial-scale=3D1"=
>
<meta name=3D"format-detection" content=3D"telephone=3Dno">
<meta name=3D"format-detection" content=3D"address=3Dno">
<meta http-equiv=3D"X-UA-Compatible" content=3D"IE=3Dedge">

<!--[if gte mso 9]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG/>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
<style>@font-face {
font-family: "Relative Black"; font-style: normal; font-weight: bold; src: =
url(https://js.skyscnr.com/sttc/bpk-fonts/SkyscannerRelative-Black-Roman-9e=
7daec9.woff) format("woff"); mso-font-alt: "Arial";
}
@font-face {
font-family: "Larken"; font-style: normal; font-weight: normal; src: url(ht=
tps://www.skyscanner.net/wp-content/themes/skyscanner-4.0/build/cf46ffc68a2=
b400dc127ecf5a03aade9.woff2) format("woff2"); mso-font-alt: "Times New Roma=
n";
}
@font-face {
font-family: "Larken"; font-style: normal; font-weight: bold; src: url(http=
s://www.skyscanner.net/wp-content/themes/skyscanner-4.0/build/0c0d2784e2768=
a3e8c715b4cdcb34200.woff2) format("woff2"); mso-font-alt: "Times New Roman"=
;
}
@font-face {
font-family: "Relative Black"; font-style: normal; font-weight: bold; src: =
url(https://js.skyscnr.com/sttc/bpk-fonts/SkyscannerRelative-Black-Roman-9e=
7daec9.woff) format("woff"); mso-font-alt: "Arial";
}
@font-face {
font-family: 'Relative'; font-style: normal; font-weight: normal; src: url(=
https://js.skyscnr.com/sttc/bpk-fonts/SkyscannerRelative-Book-748018a8.woff=
) format('woff'); mso-font-alt: 'Arial';
}
@font-face {
font-family: 'Relative'; font-style: normal; font-weight: bold; src: url(ht=
tps://js.skyscnr.com/sttc/bpk-fonts/SkyscannerRelative-Bold-05814807.woff) =
format('woff'); mso-font-alt: 'Arial';
}
body {
width: 100% !important; -webkit-text-size-adjust: 100%; -ms-text-size-adjus=
t: 100%; margin: 0; padding: 0;
}
.ExternalClass {
width: 100%;
}
.ExternalClass {
line-height: 100%;
}
#backgroundTable {
margin: 0; padding: 0; width: 100% !important; line-height: 100% !important=
;
}
img {
outline: none; text-decoration: none; border: none; -ms-interpolation-mode:=
 bicubic;
}
@media only screen and (max-width: 681px) {
  body [yahoofix] {
    padding: 0 2px !important; width: auto !important;
  }
  body [yahoofix] a[href^=3D"tel"] {
    text-decoration: none; color: #000; pointer-events: none; cursor: defau=
lt;
  }
  a[href^=3D"sms"] {
    text-decoration: none; color: #000; pointer-events: none; cursor: defau=
lt;
  }
  table.wrapper {
    width: 100% !important;
  }
  table[class=3Dwrapper] {
    width: 100% !important;
  }
  img.image-size {
    width: 100% !important;
  }
  img[class=3Dimage-size] {
    width: 100% !important;
  }
  img.image-size-mob {
    width: 100% !important;
  }
  img[class=3Dimage-size-mob] {
    width: 100% !important;
  }
  td.full-width {
    width: 100% !important; float: left !important; box-sizing: border-box =
!important;
  }
  td[class=3Dfull-width] {
    width: 100% !important; float: left !important; box-sizing: border-box =
!important;
  }
  table.full-width {
    width: 100% !important; float: left !important; box-sizing: border-box =
!important;
  }
  table[class=3Dfull-width] {
    width: 100% !important; float: left !important; box-sizing: border-box =
!important;
  }
  .full-width {
    width: 100% !important; float: left !important; box-sizing: border-box =
!important;
  }
  [class=3Dfull-width] {
    width: 100% !important; float: left !important; box-sizing: border-box =
!important;
  }
  td.hide-mobile {
    display: none !important;
  }
  td[class=3Dhide-mobile] {
    display: none !important;
  }
  .hide-mobile {
    display: none !important;
  }
  [class=3Dhide-mobile] {
    display: none !important;
  }
  td.show-mobile {
    display: block !important; max-height: none !important;
  }
  td[class=3Dshow-mobile] {
    display: block !important; max-height: none !important;
  }
  .show-mobile {
    display: block !important; max-height: none !important;
  }
  [class=3Dshow-mobile] {
    display: block !important; max-height: none !important;
  }
  td.hide-desktop {
    display: block !important; max-height: none !important;
  }
  td[class=3Dhide-desktop] {
    display: block !important; max-height: none !important;
  }
  .hide-desktop {
    display: block !important; max-height: none !important;
  }
  [class=3Dhide-desktop] {
    display: block !important; max-height: none !important;
  }
  .pad-vertical-0 {
    padding-top: 0 !important; padding-bottom: 0 !important;
  }
  [class=3Dpad-vertical-0] {
    padding-top: 0 !important; padding-bottom: 0 !important;
  }
  .pad-vertical-6 {
    padding-top: 6px !important; padding-bottom: 6px !important;
  }
  [class=3Dpad-vertical-6] {
    padding-top: 6px !important; padding-bottom: 6px !important;
  }
  .pad-vertical-12 {
    padding-top: 12px !important; padding-bottom: 12px !important;
  }
  [class=3Dpad-vertical-12] {
    padding-top: 12px !important; padding-bottom: 12px !important;
  }
  .pad-vertical-18 {
    padding-top: 18px !important; padding-bottom: 18px !important;
  }
  [class=3Dpad-vertical-18] {
    padding-top: 18px !important; padding-bottom: 18px !important;
  }
  .pad-vertical-24 {
    padding-top: 24px !important; padding-bottom: 24px !important;
  }
  [class=3Dpad-vertical-24] {
    padding-top: 24px !important; padding-bottom: 24px !important;
  }
  .pad-vertical-30 {
    padding-top: 30px !important; padding-bottom: 30px !important;
  }
  [class=3Dpad-vertical-30] {
    padding-top: 30px !important; padding-bottom: 30px !important;
  }
  .pad-vertical-36 {
    padding-top: 36px !important; padding-bottom: 36px !important;
  }
  [class=3Dpad-vertical-36] {
    padding-top: 36px !important; padding-bottom: 36px !important;
  }
  .pad-top-0 {
    padding-top: 0 !important;
  }
  [class=3Dpad-top-0] {
    padding-top: 0 !important;
  }
  .pad-top-6 {
    padding-top: 6px !important;
  }
  [class=3Dpad-top-6] {
    padding-top: 6px !important;
  }
  .pad-top-8 {
    padding-top: 8px !important;
  }
  [class=3Dpad-top-8] {
    padding-top: 8px !important;
  }
  .pad-top-12 {
    padding-top: 12px !important;
  }
  [class=3Dpad-top-12] {
    padding-top: 12px !important;
  }
  .pad-top-16 {
    padding-top: 16px !important;
  }
  [class=3Dpad-top-16] {
    padding-top: 16px !important;
  }
  .pad-top-18 {
    padding-top: 18px !important;
  }
  [class=3Dpad-top-18] {
    padding-top: 18px !important;
  }
  .pad-top-24 {
    padding-top: 24px !important;
  }
  [class=3Dpad-top-24] {
    padding-top: 24px !important;
  }
  .pad-top-30 {
    padding-top: 30px !important;
  }
  [class=3Dpad-top-30] {
    padding-top: 30px !important;
  }
  .pad-top-36 {
    padding-top: 36px !important;
  }
  [class=3Dpad-top-36] {
    padding-top: 36px !important;
  }
  .pad-bottom-0 {
    padding-bottom: 0 !important;
  }
  [class=3Dpad-bottom-0] {
    padding-bottom: 0 !important;
  }
  .pad-bottom-4 {
    padding-bottom: 4px !important;
  }
  [class=3Dpad-bottom-4] {
    padding-bottom: 4px !important;
  }
  .pad-bottom-6 {
    padding-bottom: 6px !important;
  }
  [class=3Dpad-bottom-6] {
    padding-bottom: 6px !important;
  }
  .pad-bottom-8 {
    padding-bottom: 8px !important;
  }
  [class=3Dpad-bottom-8] {
    padding-bottom: 8px !important;
  }
  .pad-bottom-12 {
    padding-bottom: 12px !important;
  }
  [class=3Dpad-bottom-12] {
    padding-bottom: 12px !important;
  }
  .pad-bottom-18 {
    padding-bottom: 18px !important;
  }
  [class=3Dpad-bottom-18] {
    padding-bottom: 18px !important;
  }
  .pad-bottom-24 {
    padding-bottom: 24px !important;
  }
  [class=3Dpad-bottom-24] {
    padding-bottom: 24px !important;
  }
  .pad-bottom-30 {
    padding-bottom: 30px !important;
  }
  [class=3Dpad-bottom-30] {
    padding-bottom: 30px !important;
  }
  .pad-bottom-36 {
    padding-bottom: 36px !important;
  }
  [class=3Dpad-bottom-36] {
    padding-bottom: 36px !important;
  }
  .pad-bottom-48 {
    padding-bottom: 48px !important;
  }
  [class=3Dpad-bottom-48] {
    padding-bottom: 48px !important;
  }
  .pad-horizontal-0 {
    padding-right: 0 !important; padding-left: 0 !important;
  }
  [class=3Dpad-horizontal-0] {
    padding-right: 0 !important; padding-left: 0 !important;
  }
  .pad-horizontal-24 {
    padding-right: 24px !important; padding-left: 24px !important;
  }
  [class=3Dpad-horizontal-24] {
    padding-right: 24px !important; padding-left: 24px !important;
  }
  .pad-right-0 {
    padding-right: 0 !important;
  }
  [class=3Dpad-right-0] {
    padding-right: 0 !important;
  }
  .pad-right-10 {
    padding-right: 10px !important;
  }
  [class=3Dpad-right-10] {
    padding-right: 10px !important;
  }
  .pad-left-0 {
    padding-left: 0 !important;
  }
  [class=3Dpad-left-0] {
    padding-left: 0 !important;
  }
  .pad-left-16 {
    padding-left: 16px !important;
  }
  [class=3Dpad-left-16] {
    padding-left: 16px !important;
  }
  td.main-title {
    font-size: 50px !important; line-height: 56px !important;
  }
  td[class=3Dmain-title] {
    font-size: 50px !important; line-height: 56px !important;
  }
  td.edges {
    padding-left: 16px !important; padding-right: 16px !important;
  }
  td[class=3Dedges] {
    padding-left: 16px !important; padding-right: 16px !important;
  }
  td.gutters {
    padding-left: 24px !important; padding-right: 24px !important;
  }
  td[class=3Dgutters] {
    padding-left: 24px !important; padding-right: 24px !important;
  }
  td.gutters_grid {
    padding-left: 24px !important; padding-right: 14px !important;
  }
  [class=3Dgutters_grid] {
    padding-left: 24px !important; padding-right: 14px !important;
  }
  td.gutter-left {
    padding-left: 24px !important;
  }
  td[class=3Dgutter-left] {
    padding-left: 24px !important;
  }
  td.footer-logo {
    text-align: left !important; padding-top: 24px !important;
  }
  td[class=3Dfooter-logo] {
    text-align: left !important; padding-top: 24px !important;
  }
  td.app-banner-title {
    font-size: 24px !important; line-height: 31px !important;
  }
  td[class=3Dapp-banner-title] {
    font-size: 24px !important; line-height: 31px !important;
  }
  .image-height {
    height: auto !important;
  }
  [class=3Dimage-height] {
    height: auto !important;
  }
  .image-width {
    width: 50% !important;
  }
  [class=3Dimage-width] {
    width: 50% !important;
  }
  .border-hide {
    border: none !important;
  }
  .font12 {
    font-size: 12px !important; line-height: 16px !important;
  }
  [class=3Dfont12] {
    font-size: 12px !important; line-height: 16px !important;
  }
  .font14 {
    font-size: 14px !important; line-height: 18px !important;
  }
  [class=3Dfont14] {
    font-size: 14px !important; line-height: 18px !important;
  }
  .font16 {
    font-size: 16px !important; line-height: 20px !important;
  }
  [class=3Dfont16] {
    font-size: 16px !important; line-height: 20px !important;
  }
  .white-space {
    white-space: normal !important;
  }
  [class=3Dwhite-space] {
    white-space: normal !important;
  }
  td.left-mobile {
    text-align: left !important;
  }
  td[class=3Dleft-mobile] {
    text-align: left !important;
  }
  .small-header-title {
    font-size: 34px !important; line-height: 40px !important;
  }
  [class=3Dsmall-header-title] {
    font-size: 34px !important; line-height: 40px !important;
  }
  .h2-title {
    font-size: 24px !important; line-height: 28px !important;
  }
  [class=3Dh2-title] {
    font-size: 24px !important; line-height: 28px !important;
  }
  .hero-title {
    font-size: 20px !important; line-height: 24px !important;
  }
  [class=3Dhero-title] {
    font-size: 20px !important; line-height: 24px !important;
  }
  td.hero-subtitle {
    font-size: 16px !important; line-height: 24px !important;
  }
  td[class=3Dhero-subtitle] {
    font-size: 16px !important; line-height: 24px !important;
  }
  .ugc-box {
    width: 50% !important; float: left !important; box-sizing: border-box !=
important;
  }
  [class=3Dugc-box] {
    width: 50% !important; float: left !important; box-sizing: border-box !=
important;
  }
  .pad-ugc {
    padding: 2px !important;
  }
  [class=3Dpad-ugc] {
    padding: 2px !important;
  }
  .app-install-mobile {
    width: 164px !important;
  }
  [class=3Dapp-install-mobile] {
    width: 164px !important;
  }
  td.width16 {
    width: 16px !important;
  }
  td[class=3Dwidth16] {
    width: 16px !important;
  }
  .width-24 {
    width: 24px !important;
  }
  [class=3Dwidth-24] {
    width: 24px !important;
  }
  td.width24 {
    width: 24px !important;
  }
  td[class=3Dwidth24] {
    width: 24px !important;
  }
  td.header-title {
    font-size: 48px !important; line-height: 48px !important;
  }
  td[class=3Dheader-title] {
    font-size: 48px !important; line-height: 48px !important;
  }
  td.header-title-spaced {
    font-size: 48px !important; line-height: 68px !important;
  }
  td[class=3Dheader-title-spaced] {
    font-size: 48px !important; line-height: 68px !important;
  }
  td.flight-alert-title {
    font-size: 32px !important; line-height: 40px !important;
  }
  td[class=3Dflight-alert-title] {
    font-size: 32px !important; line-height: 40px !important;
  }
  td.flight-alert-subtitle {
    font-size: 16px !important; line-height: 24px !important;
  }
  td[class=3Dflight-alert-subtitle] {
    font-size: 16px !important; line-height: 24px !important;
  }
  td.flight-alert-h3 {
    font-size: 20px !important; line-height: 24px !important;
  }
  td[class=3Dflight-alert-h3] {
    font-size: 20px !important; line-height: 24px !important;
  }
  td.pad-horizontal-8 {
    padding-left: 8px !important; padding-right: 8px !important;
  }
  td[class=3Dpad-horizontal-8] {
    padding-left: 8px !important; padding-right: 8px !important;
  }
  .pad-bottom-16 {
    padding-bottom: 16px !important;
  }
  [class=3Dpad-bottom-16] {
    padding-bottom: 16px !important;
  }
  .pad-bottom-40 {
    padding-bottom: 40px !important;
  }
  [class=3Dpad-bottom-40] {
    padding-bottom: 40px !important;
  }
  .pad-bottom-48 {
    padding-bottom: 48px !important;
  }
  [class=3Dpad-bottom-48] {
    padding-bottom: 48px !important;
  }
  .pad-vertical-16 {
    padding-top: 16px !important; padding-bottom: 16px !important;
  }
  [class=3Dpad-vertical-16] {
    padding-top: 16px !important; padding-bottom: 16px !important;
  }
  td.pad-horizontal-12 {
    padding-left: 12px !important; padding-right: 12px !important;
  }
  td[class=3Dpad-horizontal-12] {
    padding-left: 12px !important; padding-right: 12px !important;
  }
  td.pad-horizontal-16 {
    padding-left: 16px !important; padding-right: 16px !important;
  }
  td[class=3Dpad-horizontal-16] {
    padding-left: 16px !important; padding-right: 16px !important;
  }
  td.banner {
    border-radius: 0px 0px 12px 12px !important; border-right: 1px solid #C=
2C9CD !important; border-top: 0 !important;
  }
  td[class=3Dbanner] {
    border-radius: 0px 0px 12px 12px !important; border-right: 1px solid #C=
2C9CD !important; border-top: 0 !important;
  }
  td.banner2 {
    border-radius: 0px 0px 12px 12px !important; border-left: 1px solid #C2=
C9CD !important; border-top: 0 !important;
  }
  td[class=3Dbanner2] {
    border-radius: 0px 0px 12px 12px !important; border-left: 1px solid #C2=
C9CD !important; border-top: 0 !important;
  }
  td.brandtitle {
    font-size: 48px !important; line-height: 56px !important;
  }
  td[class=3Dbrandtitle] {
    font-size: 48px !important; line-height: 56px !important;
  }
  td.brandsubtitle {
    font-size: 20px !important; line-height: 28px !important;
  }
  td[class=3Dbrandsubtitle] {
    font-size: 20px !important; line-height: 28px !important;
  }
  td.brandtitle2 {
    font-size: 28px !important; line-height: 34px !important;
  }
  td[class=3Dbrandtitle2] {
    font-size: 28px !important; line-height: 34px !important;
  }
  td.brandsubtitle2 {
    font-size: 16px !important; line-height: 20px !important;
  }
  td[class=3Dbrandsubtitle2] {
    font-size: 16px !important; line-height: 20px !important;
  }
  td.brandsubtitle3 {
    font-size: 18px !important; line-height: 18px !important;
  }
  td[class=3Dbrandsubtitle3] {
    font-size: 18px !important; line-height: 18px !important;
  }
}
</style>
</head>
  <body style=3D"width: 100% !important; -webkit-text-size-adjust: 100%; -m=
s-text-size-adjust: 100%; margin: 0; padding: 0;"><img src=3D"https://ablin=
k.sender.skyscanner.com/ss/o/u001.Uvqp-0iCH0FhTSLRTBE_QQ/4bq/kEQStHXPR369e8=
SlRa1G8w/ho.gif" alt=3D"" width=3D"1" height=3D"1" border=3D"0" style=3D"he=
ight:1px !important;width:1px !important;border-width:0 !important;margin-t=
op:0 !important;margin-bottom:0 !important;margin-right:0 !important;margin=
-left:0 !important;padding-top:0 !important;padding-bottom:0 !important;pad=
ding-right:0 !important;padding-left:0 !important;"/>
<div style=3D"display:none !important;visibility:hidden;mso-hide:all;font-s=
ize:1px;color:#ffffff;line-height:1px;max-height:0px;max-width:0px;opacity:=
0;overflow:hidden;">Discover something different on your next trip to Krako=
w.</div>
    <p style=3D"-webkit-text-size-adjust: none; margin: 0;">


























































































</p>
    <table role=3D"presentation" width=3D"100%" border=3D"0" cellpadding=3D=
"0" cellspacing=3D"0" style=3D"width: 100%; mso-table-lspace: 0pt; mso-tabl=
e-rspace: 0pt; border-width: 0;">
      <tr>
        <td style=3D"-webkit-text-size-adjust: none;" bgcolor=3D"#FFFFFF">
          <table role=3D"presentation" class=3D"wrapper" width=3D"680" styl=
e=3D"width: 680px; font-family: 'Relative', Arial, sans-serif; max-width: 6=
80px; text-align: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; borde=
r-width: 0;" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"cent=
er">


<tr bgcolor=3D"#FFFFFF"><td bgcolor=3D"#FFFFFF" style=3D"-webkit-text-size-=
adjust: none;"><table role=3D"presentation" cellpadding=3D"0" cellspacing=
=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-tabl=
e-rspace: 0pt; border-width: 0;">
<tr> <td class=3D"edges" style=3D"-webkit-text-size-adjust: none; padding: =
8px 24px 0;" align=3D"center"> <table width=3D"100%" role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" style=3D"mso-table-lspace:=
 0pt; mso-table-rspace: 0pt; border-width: 0;"> <tr> <td width=3D"100%" cla=
ss=3D"pad-top-8 pad-bottom-24" align=3D"left" style=3D"font-size: 0; -webki=
t-text-size-adjust: none; padding: 16px 0 32px;"> <table role=3D"presentati=
on" align=3D"left" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" style=
=3D"float: left; font-size: 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt=
; border-width: 0;"> <tr> <td valign=3D"middle" style=3D"direction: ltr; fo=
nt-size: 0; -webkit-text-size-adjust: none; padding: 0 16px 0 0;" align=3D"=
left"> <a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG=
7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2=
tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9Rmxcdnffx8UUR56L98uWz64Z_hg3g3-Zdyu=
2mXwyhQdzJGrrDJFzbGoD_Y27ZMzOguFaamzZh5ZKgM_pVn1qyWFLXpS5WegL5okdE1QPbVUY0a=
1NUqDlP30M1iS3klntvmkGU8LsxnsYwSEXNMIc7c5Pxoe64H1CTU6c80th4Q1vdANVTPOqUgP95=
xXQStY9quKKlEbjgu6gJuvy7qoMOAhiA/4bq/kEQStHXPR369e8SlRa1G8w/h11/h001.o9JLzQ=
Pl43JilvRg5fDbImon-M-Jd7KY4u86mQ4f4xQ" style=3D"color: #FFFFFF; text-decora=
tion: none; -webkit-text-size-adjust: none;"><img src=3D"https://cdn.braze.=
eu/appboy/communication/assets/image_assets/images/662f591c321e40006212de52=
/original.png?1714379036" width=3D"24" alt=3D"" style=3D"display: inline; v=
ertical-align: middle; outline: none; text-decoration: none; -ms-interpolat=
ion-mode: bicubic; border-style: none;"><span style=3D"font-family: 'Relati=
ve', Arial, sans-serif; font-size: 16px; line-height: 20px; color: #05203C;=
 display: inline; vertical-align: middle;">Flights</span></a> </td> </tr> <=
/table> <table role=3D"presentation" align=3D"left" cellpadding=3D"0" cells=
pacing=3D"0" border=3D"0" style=3D"float: left; font-size: 0; mso-table-lsp=
ace: 0pt; mso-table-rspace: 0pt; border-width: 0;"> <tr> <td valign=3D"midd=
le" style=3D"direction: ltr; font-size: 0; -webkit-text-size-adjust: none; =
padding: 0 16px 0 0;" align=3D"left"> <a href=3D"https://ablink.sender.skys=
canner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rm=
uzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9RmxX=
Ka2RuvDaGzp8ytL6xoAAXBitKH9WxARi0cF6iS2fCqyI4FVUc8MzWffx2V5vOXSJHzsKLQTX4we=
--Q2udA7i2YiizUWrHE6ytJuY-XvlId9_BKrQG0OW1opijL1c9iegxPSULD4h93Ku8UGnKbZDOy=
9u55ETWdFhVu7iLpz9XEv06VVtzco-fxPG6akO3XeM_r_FhsRbQ9q89xYX3t3UA/4bq/kEQStHX=
PR369e8SlRa1G8w/h12/h001.E3_UyhK9MiOVwOdjQAIuTWVsdO1AT7EwRxf2Ny-ur7Y" style=
=3D"color: #FFFFFF; text-decoration: none; -webkit-text-size-adjust: none;"=
><img src=3D"https://cdn.braze.eu/appboy/communication/assets/image_assets/=
images/662f591e64a7b0005c01c77f/original.png?1714379038" width=3D"24" alt=
=3D"" style=3D"display: inline; vertical-align: middle; outline: none; text=
-decoration: none; -ms-interpolation-mode: bicubic; border-style: none;"><s=
pan style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 16px; l=
ine-height: 20px; color: #05203C; display: inline; vertical-align: middle;"=
>Hotels</span></a> </td>
</tr> </table> <table role=3D"presentation" align=3D"left" cellpadding=3D"0=
" cellspacing=3D"0" border=3D"0" style=3D"float: left; font-size: 0; mso-ta=
ble-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;"> <tr> <td valign=
=3D"middle" style=3D"direction: ltr; font-size: 0; -webkit-text-size-adjust=
: none; padding: 0 16px 0 0;" align=3D"left"> <a href=3D"https://ablink.sen=
der.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZ=
rUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCT=
npC9RmxKC5KvkEYZJGmffvYpcuo-r5D4MPSdM0JQDEjyo-Tl0Bbmd-1tHoh8utkhGCzM5waFFST=
-xwF8yP6oL5ea2qn43CDQQfatLdytFN_bDtJJoG8e7G2Qafi9G-U28HkZ38VpQFI2KBjN5dY584=
JUPZ2QlXTobU3NWgSGqfMFsp0UVVewa29YSLPwWDG4YFAO-6FGnvXnf4mrVxly2yKdVBumQ/4bq=
/kEQStHXPR369e8SlRa1G8w/h13/h001.jr7aZliwYnXArpZQG34NFahuXzGXlxTaDLAC_3i1BF=
c" style=3D"color: #FFFFFF; text-decoration: none; -webkit-text-size-adjust=
: none;"><img src=3D"https://cdn.braze.eu/appboy/communication/assets/image=
_assets/images/662f5920b307b90066285492/original.png?1714379040" width=3D"2=
4" alt=3D"" style=3D"display: inline; vertical-align: middle; outline: none=
; text-decoration: none; -ms-interpolation-mode: bicubic; border-style: non=
e;"><span style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 1=
6px; line-height: 20px; color: #05203C; display: inline; vertical-align: mi=
ddle;">Car hire</span></a> </td> </tr> </table> </td> </tr> <tr> <td class=
=3D"pad-bottom-16" align=3D"left" style=3D"padding-top: 8px; padding-bottom=
: 24px; font-size: 0; -webkit-text-size-adjust: none;"> <a href=3D"https://=
ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehV=
AkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLA=
tWtKxwXfCTnpC9Rmxcdnffx8UUR56L98uWz64ZxpFPfqmjVXc46tZnxsEIQ3jYK2HlqXhE_Lol6=
jPpVh1L35DG8KOZIOFbdBZ4B3E91yuhgQW_Ej_tHSImauBcbq4pNVNyj2mLGEzUEyE370DeYr73=
31MGg0JU-9K8nBDyDh8iS7bhtgKThKypp12Sz1OH0NN6qdvra89PV8grD3J/4bq/kEQStHXPR36=
9e8SlRa1G8w/h14/h001.NWSB9EWNRUdsTti5tsxR1iJgusx2npEHGAZskcZdgFQ" style=3D"=
-webkit-text-size-adjust: none; color: #776f6b;"><img src=3D"https://cdn.br=
aze.eu/appboy/communication/assets/image_assets/images/662f5cbee61d08006f60=
7e7f/original.png?1714379966" width=3D"170" style=3D"width: 170px; height: =
auto;" alt=3D"Skyscanner"> </a>
</td> </tr> </table> </td>
</tr>
<tr><td class=3D"edges pad-bottom-24" style=3D"-webkit-text-size-adjust: no=
ne; padding: 0 24px 32px;" align=3D"center"><table role=3D"presentation" ce=
llpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-=
table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;">
<tr><td class=3D"header-title pad-bottom-24" style=3D"font-family: 'Relativ=
e Black', Arial, sans-serif; font-weight: bold; color: #0062E3; font-size: =
64px; line-height: 64px; letter-spacing: -1px; direction: ltr; padding-bott=
om: 32px; -webkit-text-size-adjust: none;" align=3D"left">Spotlight on: Kra=
kow</td></tr>
<tr><td class=3D"pad-bottom-24" style=3D"padding-bottom: 32px; font-size: 0=
; -webkit-text-size-adjust: none;"><a href=3D"https://ablink.sender.skyscan=
ner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG=
6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9RmxJaBi=
XQQcdvWQLErd_5gqjrZkvvLP3_1O3nEbqtIuhwTZ_apCTI9wJYZGDhS3lvWRZmVHp0lX9vyf6vx=
nm4oo3Be5Yb1Q6-hXn8h2pUxNiCSdZxp9VU6f1XBoDgXiKx1iqlJE_4ZA_SGpuJ3bRTZ5jWwal4=
ypwF-rY2B_7cDWeXBPCwh3635Xo_4T2vYL0Jpwmb_QW7lqsdBvyKkbxl_A3LF7kII8fIwRrBHI7=
ETAJsTJvk8GdATdPV0srNzZstYy/4bq/kEQStHXPR369e8SlRa1G8w/h15/h001.5Dz5GxDSwqR=
Pl7VPe6k5vuetn_7Z_5WKGP9o0_QLeZs" style=3D"-webkit-text-size-adjust: none; =
color: #776f6b;"><img src=3D"https://cdn.braze.eu/appboy/communication/asse=
ts/image_assets/images/6628ff20c4b2340dd9cd49e7/original.png?1713962783" wi=
dth=3D"632" class=3D"full-width" style=3D"width: 632px; height: auto; outli=
ne: none; text-decoration: none; -ms-interpolation-mode: bicubic; border-st=
yle: none;" alt=3D""></a></td></tr>
<tr><td class=3D"hero-title pad-bottom-24" style=3D"font-family: 'Larken', =
'Times New Roman', Times, serif; color: #05203C; font-size: 24px; line-heig=
ht: 30px; letter-spacing: -0.1px; direction: ltr; padding-bottom: 32px; -we=
bkit-text-size-adjust: none;" align=3D"left">A city of cobbled streets and =
cultural hotspots. Dine on dumplings, wander through arty Kazimierz and tak=
e a tour of Wawel Castle. You can also visit Auschwitz, less than 2 hours a=
way by arranged tour or train.</td></tr>
<tr><td class=3D"pad-bottom-8" style=3D"padding-bottom: 16px; -webkit-text-=
size-adjust: none;" align=3D"left"><table class=3D"full-width" role=3D"pres=
entation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"left" s=
tyle=3D"float: left; font-size: 0; mso-table-lspace: 0pt; mso-table-rspace:=
 0pt; border-width: 0;"><tr><td style=3D"mso-padding-alt: 11px 64px 13px; b=
order-radius: 8px; direction: ltr; -webkit-text-size-adjust: none; padding:=
 0 64px;" align=3D"center" valign=3D"middle" bgcolor=3D"#0062E3"><a href=3D=
"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0=
pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFO=
WQe8mZPLAtWtKxwXfCTnpC9RmxJaBiXQQcdvWQLErd_5gqjrZkvvLP3_1O3nEbqtIuhwTZ_apCT=
I9wJYZGDhS3lvWRZmVHp0lX9vyf6vxnm4oo3Be5Yb1Q6-hXn8h2pUxNiCSdZxp9VU6f1XBoDgXi=
Kx1iqlJE_4ZA_SGpuJ3bRTZ5jWwal4ypwF-rY2B_7cDWeXBPCwh3635Xo_4T2vYL0Jpwmb_QW7l=
qsdBvyKkbxl_A3LF7kII8fIwRrBHI7ETAJsTJvk8GdATdPV0srNzZstYy/4bq/kEQStHXPR369e=
8SlRa1G8w/h16/h001.Tt4Qp_vHeFePW3UrjlKYf7ejeBmPPf33AyCjSoFad6c" style=3D"di=
splay: block; vertical-align: middle; text-decoration: none; width: 100%; f=
ont-size: 0; text-align: center; mso-padding-alt: 8px 0; -webkit-text-size-=
adjust: none; color: #776f6b; padding: 11px 0 13px;"><span style=3D"display=
: inline; vertical-align: middle; font-family: 'Relative', Arial, sans-seri=
f; font-size: 16px; line-height: 24px; font-weight: bold; color: #FFFFFF;">=
Find flights</span></a></td></tr></table></td></tr>
</table></td></tr>
</table></td></tr>
<tr><td class=3D"edges pad-bottom-24" style=3D"-webkit-text-size-adjust: no=
ne; padding: 0 24px 32px;" bgcolor=3D"#FFFFFF"><table role=3D"presentation"=
 cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"m=
so-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;">
<tr><td style=3D"padding-bottom: 24px; -webkit-text-size-adjust: none;"><ta=
ble role=3D"presentation" width=3D"100%" cellpadding=3D"0" cellspacing=3D"0=
" border=3D"0" align=3D"left" style=3D"float: left; mso-table-lspace: 0pt; =
mso-table-rspace: 0pt; border-width: 0;">
<tr><td class=3D"h2-title" style=3D"font-family: 'Relative', Arial, sans-se=
rif; font-weight: bold; font-size: 32px; line-height: 40px; color: #161616;=
 direction: ltr; padding-bottom: 8px; -webkit-text-size-adjust: none;" alig=
n=3D"left">Check out the latest flight prices to Krakow</td></tr>
<tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 16p=
x; line-height: 24px; color: #545860; direction: ltr; -webkit-text-size-adj=
ust: none;" align=3D"left">Plan your perfect trip</td></tr>
</table></td></tr>
<tr><td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentati=
on" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=
=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;"><tr><td=
 style=3D"border-radius: 12px; font-family: 'Relative', Arial, sans-serif; =
-webkit-text-size-adjust: none; border: 1px solid #E6E4EB;"><table role=3D"=
presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100=
%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;"=
>
<tr><td class=3D"show-mobile" style=3D"display: none; max-height: 0; overfl=
ow: hidden; border-top-left-radius: 12px; border-top-right-radius: 12px; -w=
ebkit-text-size-adjust: none;"><a href=3D"https://ablink.sender.skyscanner.=
com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8=
SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92Wt=
X1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgvl8s6x1UkxT9cP_9ot0IITazC-7L3nmp5KvKuq-t=
eZygvIIbhQ83mve12VCNu4pOEelgAeR16smx6NZRaJcAJSPZdY-vcOCq2iDP-MLDGsByGkMaz9m=
j9T8KG2FCNYwCP9tsj56Dju8Shj-ONPMEY5EZ6uVQpw8tVdsILO5U9v7r15wAAAYRcB3W2Qkm5V=
cNTlX1k2F1aodb_kutD9-1Ko59SaoxMHRNdV8pGeWOVerZdWfocI_OhjWMjRvab1nnswi5JcdiC=
bkHlrkPfQ4sRPZYKQUenEe9GSpcFWEPm1dtefnzl5ZX3kF6SD-OuDzbCYDY29DIAZOAf1QRiXaB=
3mmWohcqCU0uHuR0FHS9y-p4ehFwTOsYctJ_GeuqGGggPEClhO6B0Uc78QoMC4uzUmWudZDB9k1=
bKLSyUfDEoupCo0CEqVj-VmNLXFJjXvNePfx1PnxIgg_34MqbQgqUg/4bq/kEQStHXPR369e8Sl=
Ra1G8w/h17/h001.bzGx_FBY-EpxBD4qqd_spuwATjGLzRrp7H2sAEusqVs" style=3D"-webk=
it-text-size-adjust: none; color: #776f6b;"><img src=3D"https://content.sky=
scnr.com/f7f6af4f80f12335dd8b34745ce453a4/krakow.jpg?crop=3D304px:121px&amp=
;quality=3D70" alt=3D"Krakow" width=3D"100%" style=3D"display: block; borde=
r-top-left-radius: 12px; border-top-right-radius: 12px; outline: none; text=
-decoration: none; -ms-interpolation-mode: bicubic; border-style: none;"></=
a></td></tr>
<tr><td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentati=
on" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=
=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;"><tr>
<td class=3D"hide-mobile" style=3D"border-top-left-radius: 12px; border-bot=
tom-left-radius: 12px; -webkit-text-size-adjust: none;" width=3D"208" bgcol=
or=3D"#FBFBFB"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJgvl8s6x1UkxT9cP_9ot0IITazC-7L3nmp5KvKuq-teZygvIIbhQ83mve1=
2VCNu4pOEelgAeR16smx6NZRaJcAJSPZdY-vcOCq2iDP-MLDGsByGkMaz9mj9T8KG2FCNYwCP9t=
sj56Dju8Shj-ONPMEY5EZ6uVQpw8tVdsILO5U9v7r15wAAAYRcB3W2Qkm5VcNTlX1k2F1aodb_k=
utD9-1Ko59SaoxMHRNdV8pGeWOVerZdWfocI_OhjWMjRvab1nnswi5JcdiCbkHlrkPfQ4sRPZYK=
QUenEe9GSpcFWEPm1dtefnzl5ZX3kF6SD-OuDzbCYDY29DIAZOAf1QRiXaB3mmWohcqCU0uHuR0=
FHS9y-p4ehFwTOsYctJ_GeuqGGggPEClhO6B0Uc78QoMC4uzUmWudZDB9k1bKLSyUfDEoupCo0C=
EqVj-VmNLXFJjXvNePfx1PnxIgg_34MqbQgqUg/4bq/kEQStHXPR369e8SlRa1G8w/h18/h001.=
j-mmtbhVOLWxlKpeFbJqKVHNoiGGl6jBs2djRM8RQBs" style=3D"-webkit-text-size-adj=
ust: none; color: #776f6b;"><img src=3D"https://content.skyscnr.com/f7f6af4=
f80f12335dd8b34745ce453a4/krakow.jpg?crop=3D208px:108px&amp;quality=3D70" a=
lt=3D"Krakow" width=3D"208" style=3D"display: block; border-top-left-radius=
: 12px; border-bottom-left-radius: 12px; outline: none; text-decoration: no=
ne; -ms-interpolation-mode: bicubic; border-style: none;"></a></td>
<td style=3D"direction: ltr; -webkit-text-size-adjust: none; padding: 0 8px=
 0 24px;" class=3D"pad-vertical-16" align=3D"left"><a href=3D"https://ablin=
k.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufa=
cXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr=
-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgvl8s6x1UkxT9cP_9ot0I=
ITazC-7L3nmp5KvKuq-teZygvIIbhQ83mve12VCNu4pOEelgAeR16smx6NZRaJcAJSPZdY-vcOC=
q2iDP-MLDGsByGkMaz9mj9T8KG2FCNYwCP9tsj56Dju8Shj-ONPMEY5EZ6uVQpw8tVdsILO5U9v=
7r15wAAAYRcB3W2Qkm5VcNTlX1k2F1aodb_kutD9-1Ko59SaoxMHRNdV8pGeWOVerZdWfocI_Oh=
jWMjRvab1nnswi5JcdiCbkHlrkPfQ4sRPZYKQUenEe9GSpcFWEPm1dtefnzl5ZX3kF6SD-OuDzb=
CYDY29DIAZOAf1QRiXaB3mmWohcqCU0uHuR0FHS9y-p4ehFwTOsYctJ_GeuqGGggPEClhO6B0Uc=
78QoMC4uzUmWudZDB9k1bKLSyUfDEoupCo0CEqVj-VmNLXFJjXvNePfx1PnxIgg_34MqbQgqUg/=
4bq/kEQStHXPR369e8SlRa1G8w/h19/h001.Lv2jcsg6UrowupI5h7CR9ox7VfhDDv2jaagEV6J=
1iek" style=3D"display: block; width: 100%; color: #161616; text-decoration=
: none; -webkit-text-size-adjust: none;"><span style=3D"font-size: 24px; li=
ne-height: 28px; font-weight: bold;" class=3D"hero-title">Krakow</span><br>=
<span style=3D"font-size: 14px; line-height: 20px; font-weight: normal; col=
or: #545860;">Poland<br>23&nbsp;Dec - 27&nbsp;Dec</span></a></td>
<td valign=3D"bottom" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 12px; line-height: 16px; direction: ltr; color: #545860; -webkit=
-text-size-adjust: none; padding: 0 24px 16px 0;" align=3D"right">Flights f=
rom <span style=3D"font-size: 40px; line-height: 36px; font-weight: bold; c=
olor: #05203C; display: block;" class=3D"small-header-title">$ 1,027,594</s=
pan>
</td>
</tr></table></td></tr>
</table></td></tr></table></td></tr>
</table></td></tr>
<tr><td style=3D"-webkit-text-size-adjust: none; padding: 0 24px 32px;" cla=
ss=3D"edges pad-bottom-24" bgcolor=3D"#FFFFFF"><table role=3D"presentation"=
 cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"m=
so-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;"><tr><td styl=
e=3D"font-family: 'Relative', Arial, sans-serif; mso-padding-alt: 11px 25px=
 13px; font-size: 16px; line-height: 24px; color: #FFFFFF; border-radius: 8=
px; direction: ltr; -webkit-text-size-adjust: none; padding: 0 25px;" align=
=3D"center" valign=3D"middle" bgcolor=3D"#0062E3"><a href=3D"https://ablink=
.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufac=
XuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxw=
XfCTnpC9RmxJaBiXQQcdvWQLErd_5gqjrZkvvLP3_1O3nEbqtIuhwTZ_apCTI9wJYZGDhS3lvWR=
ZmVHp0lX9vyf6vxnm4oo3Be5Yb1Q6-hXn8h2pUxNiCSdZxp9VU6f1XBoDgXiKx1iqlJE_4ZA_SG=
puJ3bRTZ5jWwal4ypwF-rY2B_7cDWeXBPCwh3635Xo_4T2vYL0Jpwmb_QW7lqsdBvyKkbxl_A3L=
F7kII8fIwRrBHI7ETAJsTJvk8GdATdPV0srNzZstYy/4bq/kEQStHXPR369e8SlRa1G8w/h20/h=
001.glFsuHJPjEA8Qt527ZhE9PETpV0DL1GvXRwJ1hyL3mI" style=3D"display: block; t=
ext-decoration: none; font-weight: bold; color: #FFFFFF; width: 100%; mso-p=
adding-alt: 8px 0; -webkit-text-size-adjust: none; padding: 11px 0 13px;">S=
ee more flight deals</a></td></tr></table></td></tr>=09=09=09=09=09=09=09=
=09=09=09<tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-=
size: 32px; line-height: 40px; font-weight: bold; direction: ltr; -webkit-t=
ext-size-adjust: none; padding: 0 24px 8px;" class=3D"edges h2-title" align=
=3D"left" bgcolor=3D"#FFFFFF">Trending now: Krakow getaways</td></tr>
<tr><td valign=3D"top" style=3D"font-family: 'Relative', Arial, sans-serif;=
 color: #545860; font-size: 16px; line-height: 24px; direction: ltr; -webki=
t-text-size-adjust: none; padding: 0 24px 8px;" class=3D"edges" align=3D"le=
ft" bgcolor=3D"#FFFFFF">Wake up somewhere new for the lowest price.</td></t=
r>
<tr><td style=3D"padding-bottom: 30px; -webkit-text-size-adjust: none;" bgc=
olor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=3D"0" cellspacing=
=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-tabl=
e-rspace: 0pt; border-width: 0;"><tr><td valign=3D"top" style=3D"font-size:=
 0; -webkit-text-size-adjust: none;">
<table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"=
0" align=3D"left" style=3D"float: left; mso-table-lspace: 0pt; mso-table-rs=
pace: 0pt; border-width: 0;"><tr><td style=3D"-webkit-text-size-adjust: non=
e; padding: 24px 0 0 24px;" class=3D"edges"><table width=3D"304" cellpaddin=
g=3D"0" cellspacing=3D"0" border=3D"0" align=3D"left" class=3D"full-width" =
style=3D"float: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-=
width: 0;">
<tr><td style=3D"font-size: 0; -webkit-text-size-adjust: none;"><a href=3D"=
https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0p=
Ni9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOW=
Qe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2NQFg8lXHrZZFLtAEWh-0gwvN=
ENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5ISMA-4u78Cbk_KeGWU7k0mjK=
qANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvVL6xmm6Ze0mCpUcEtsqD8cso=
ouaFd6hKL4BU2H9etixnzd5o_y0h-rjY6CahJv4WVJ_NaxgnJpRJ_Q2CDn442BESC8fCoQ4HLT5=
Um0x8MAcgN9FONu98NxyqFuYJlwqPR66HBndw1Bnma2SSgWcFt9tWMtIcr8uSqfPoaa2cWnRT2Z=
w6CMrfIJy0fbXe-Y1Q46kyKg27rvG8SOM5DKtCBDt8clukzt9rmIkyrEaxqvOdKOMtzDjkzRUdq=
hEHPzIL9IZVRDUaru2-eMGa98ij_BlaaZeRwAJC73S053f0pA7wP2572OaEytCPDA0rT6U87Gzm=
scNrs5rUJpL5OMQXyGm834ThVsSyJCnpZcQoQCoRWAeQjnqacN71TYpLFLu0mVgspPOUxygITPf=
Xf38gYoyHDtriXnzfGC-WjKY4-7lksq0ZtocOpDyFE1g/4bq/kEQStHXPR369e8SlRa1G8w/h21=
/h001.q0gBTfx3j7sOG3nV77pbLv0E_JrBMrsxcTPvwGr0-wE" style=3D"-webkit-text-si=
ze-adjust: none; color: #776f6b;"><img src=3D"https://content.skyscnr.com/a=
vailable/1646084139/1646084139_562x224.jpg" width=3D"304" class=3D"image-si=
ze" style=3D"border-top-right-radius: 12px; border-top-left-radius: 12px; o=
utline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width=
: 100% !important; border-style: none;" alt=3D"Metropolo Krakow by Golden T=
ulip"></a></td></tr>
<tr><td style=3D"border-left-width: 1px; border-left-color: #E6E4EB; border=
-left-style: solid; border-right-width: 1px; border-right-color: #E6E4EB; b=
order-right-style: solid; border-bottom-width: 1px; border-bottom-color: #E=
6E4EB; border-bottom-style: solid; border-bottom-right-radius: 12px; border=
-bottom-left-radius: 12px; -webkit-text-size-adjust: none; padding: 6px 12p=
x 12px;" bgcolor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=3D"0"=
 cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0=
pt; mso-table-rspace: 0pt; border-width: 0;">
<tr><td colspan=3D"2" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 16px; line-height: 26px; font-weight: bold; padding-bottom: 8px;=
 direction: ltr; -webkit-text-size-adjust: none;" align=3D"left"><a href=3D=
"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0=
pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFO=
WQe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2NQFg8lXHrZZFLtAEWh-0gwv=
NENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5ISMA-4u78Cbk_KeGWU7k0mj=
KqANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvVL6xmm6Ze0mCpUcEtsqD8cs=
oouaFd6hKL4BU2H9etixnzd5o_y0h-rjY6CahJv4WVJ_NaxgnJpRJ_Q2CDn442BESC8fCoQ4HLT=
5Um0x8MAcgN9FONu98NxyqFuYJlwqPR66HBndw1Bnma2SSgWcFt9tWMtIcr8uSqfPoaa2cWnRT2=
Zw6CMrfIJy0fbXe-Y1Q46kyKg27rvG8SOM5DKtCBDt8clukzt9rmIkyrEaxqvOdKOMtzDjkzRUd=
qhEHPzIL9IZVRDUaru2-eMGa98ij_BlaaZeRwAJC73S053f0pA7wP2572OaEytCPDA0rT6U87Gz=
mscNrs5rUJpL5OMQXyGm834ThVsSyJCnpZcQoQCoRWAeQjnqacN71TYpLFLu0mVgspPOUxygITP=
fXf38gYoyHDtriXnzfGC-WjKY4-7lksq0ZtocOpDyFE1g/4bq/kEQStHXPR369e8SlRa1G8w/h2=
2/h001.cz79Jutl11e4lgqKCCvmH4LaI45EwpIeUbhCu-LL_HA" style=3D"color: #161616=
; text-decoration: none; -webkit-text-size-adjust: none;">Metropolo Krakow =
by Golden ...</a></td></tr>
<tr>
<td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 16px; l=
ine-height: 20px; direction: ltr; -webkit-text-size-adjust: none;"><a href=
=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU=
0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkT=
FFOWQe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2NQFg8lXHrZZFLtAEWh-0=
gwvNENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5ISMA-4u78Cbk_KeGWU7k=
0mjKqANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvVL6xmm6Ze0mCpUcEtsqD=
8csoouaFd6hKL4BU2H9etixnzd5o_y0h-rjY6CahJv4WVJ_NaxgnJpRJ_Q2CDn442BESC8fCoQ4=
HLT5Um0x8MAcgN9FONu98NxyqFuYJlwqPR66HBndw1Bnma2SSgWcFt9tWMtIcr8uSqfPoaa2cWn=
RT2Zw6CMrfIJy0fbXe-Y1Q46kyKg27rvG8SOM5DKtCBDt8clukzt9rmIkyrEaxqvOdKOMtzDjkz=
RUdqhEHPzIL9IZVRDUaru2-eMGa98ij_BlaaZeRwAJC73S053f0pA7wP2572OaEytCPDA0rT6U8=
7GzmscNrs5rUJpL5OMQXyGm834ThVsSyJCnpZcQoQCoRWAeQjnqacN71TYpLFLu0mVgspPOUxyg=
ITPfXf38gYoyHDtriXnzfGC-WjKY4-7lksq0ZtocOpDyFE1g/4bq/kEQStHXPR369e8SlRa1G8w=
/h23/h001.JQY-gf3nvZ_oEp8fm__hpk7zywt9wJTvyqgBoEYuEN0" style=3D"color: #161=
616; text-decoration: none; -webkit-text-size-adjust: none;"><strong>$ 253,=
483</strong> a night</a></td>
<td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"right" style=3D"f=
loat: right; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;=
"><tr>
<td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"right" style=3D"f=
loat: right; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;=
"><tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 1=
4px; line-height: 18px; color: #FFFFFF; border-radius: 50px; direction: ltr=
; -webkit-text-size-adjust: none; padding: 2px 6px;" bgcolor=3D"#00AA6C">4.=
5</td></tr></table></td>
<td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"right" style=3D"f=
loat: right; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;=
">
<tr><td style=3D"-webkit-text-size-adjust: none;" align=3D"center"><img src=
=3D"https://www.tripadvisor.com/img/cdsi/img2/ratings/traveler/4.5-64600-4.=
png" width=3D"70" alt=3D"Tripadvisor score - 4.5." style=3D"outline: none; =
text-decoration: none; -ms-interpolation-mode: bicubic; border-style: none;=
"></td></tr>
<tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 10p=
x; line-height: 10px; color: #161616; padding-left: 4px; direction: ltr; -w=
ebkit-text-size-adjust: none;" align=3D"center">209 reviews</td></tr>
</table></td>
</tr></table></td>
</tr>
</table></td></tr>
</table></td></tr></table>
<table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"=
0" align=3D"left" style=3D"float: left; mso-table-lspace: 0pt; mso-table-rs=
pace: 0pt; border-width: 0;"><tr><td style=3D"-webkit-text-size-adjust: non=
e; padding: 24px 0 0 24px;" class=3D"edges"><table width=3D"304" cellpaddin=
g=3D"0" cellspacing=3D"0" border=3D"0" align=3D"left" class=3D"full-width" =
style=3D"float: left; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-=
width: 0;">
<tr><td style=3D"font-size: 0; -webkit-text-size-adjust: none;"><a href=3D"=
https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0p=
Ni9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOW=
Qe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2NQFg8lXHrZZFLtAEWh-0gwvN=
ENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5ISMA-4u78Cbk_KeGWU7k0mjK=
qANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvVL6xmm6Ze0mCpUcEtsqD8cso=
ouaFd6hKL4BU2FuatPdtFvJf4aNr84ZYL_wPYTXY7hjDxpBukMLlO6QsorF1xSFJrHFsb7EUrR-=
zLtK5dNYmeKBw4NRCWd4VDB5TWAfmVH-3CYoprC2Zi3F4Rmw68PRtG1OBn_HmEnUyD_yprOWq2g=
g87nz2ZfPGUmCt7KKIPv_-6jsv2VCXK7b8aFVcBPAXA6bO1h0VABsOdeZQ5j2JTnpyVzzwB0qWd=
RnuZ_xCg_GYPVdwMaBsifBNuDrmTkpiRonu4wLbLzJRZvqYlSvO2a0KuX-7TGSmwLHTPmNYoXMP=
6D8j9acr1hFClfUag9w81pLQaunnPGG1hJ3MbWArl5cf0r8G6FjayJtRL0UNsjpr4D1L2bQLJl6=
-kkQhmWYbnTWJoeOfnZ6trW7eeDoonY0y49l0w6KEwI4/4bq/kEQStHXPR369e8SlRa1G8w/h24=
/h001.lsdmetT_eG7R3JGUjQg8GBIbKU1_LGKO3m_2hX3tZSk" style=3D"-webkit-text-si=
ze-adjust: none; color: #776f6b;"><img src=3D"https://content.skyscnr.com/a=
vailable/1579957566/1579957566_562x224.jpg" width=3D"304" class=3D"image-si=
ze" style=3D"border-top-right-radius: 12px; border-top-left-radius: 12px; o=
utline: none; text-decoration: none; -ms-interpolation-mode: bicubic; width=
: 100% !important; border-style: none;" alt=3D"Hotel Stary"></a></td></tr>
<tr><td style=3D"border-left-width: 1px; border-left-color: #E6E4EB; border=
-left-style: solid; border-right-width: 1px; border-right-color: #E6E4EB; b=
order-right-style: solid; border-bottom-width: 1px; border-bottom-color: #E=
6E4EB; border-bottom-style: solid; border-bottom-right-radius: 12px; border=
-bottom-left-radius: 12px; -webkit-text-size-adjust: none; padding: 6px 12p=
x 12px;" bgcolor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=3D"0"=
 cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0=
pt; mso-table-rspace: 0pt; border-width: 0;">
<tr><td colspan=3D"2" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 16px; line-height: 26px; font-weight: bold; padding-bottom: 8px;=
 direction: ltr; -webkit-text-size-adjust: none;" align=3D"left"><a href=3D=
"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0=
pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFO=
WQe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2NQFg8lXHrZZFLtAEWh-0gwv=
NENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5ISMA-4u78Cbk_KeGWU7k0mj=
KqANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvVL6xmm6Ze0mCpUcEtsqD8cs=
oouaFd6hKL4BU2FuatPdtFvJf4aNr84ZYL_wPYTXY7hjDxpBukMLlO6QsorF1xSFJrHFsb7EUrR=
-zLtK5dNYmeKBw4NRCWd4VDB5TWAfmVH-3CYoprC2Zi3F4Rmw68PRtG1OBn_HmEnUyD_yprOWq2=
gg87nz2ZfPGUmCt7KKIPv_-6jsv2VCXK7b8aFVcBPAXA6bO1h0VABsOdeZQ5j2JTnpyVzzwB0qW=
dRnuZ_xCg_GYPVdwMaBsifBNuDrmTkpiRonu4wLbLzJRZvqYlSvO2a0KuX-7TGSmwLHTPmNYoXM=
P6D8j9acr1hFClfUag9w81pLQaunnPGG1hJ3MbWArl5cf0r8G6FjayJtRL0UNsjpr4D1L2bQLJl=
6-kkQhmWYbnTWJoeOfnZ6trW7eeDoonY0y49l0w6KEwI4/4bq/kEQStHXPR369e8SlRa1G8w/h2=
5/h001.-1ndJM3LUDtS0tEmq70lreYrmjITX0hMhSxenMwScY8" style=3D"color: #161616=
; text-decoration: none; -webkit-text-size-adjust: none;">Hotel Stary</a></=
td></tr>
<tr>
<td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 16px; l=
ine-height: 20px; direction: ltr; -webkit-text-size-adjust: none;"><a href=
=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU=
0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkT=
FFOWQe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAVJRQ2NQFg8lXHrZZFLtAEWh-0=
gwvNENV31sz6lez_Rfs7LTYTeij84-boyeReTiYWYuRgc4J-o32B1S5ISMA-4u78Cbk_KeGWU7k=
0mjKqANbFfG0h7JMR8upSOLivwp_4Y7MSDYmd6UFk6OIY1SeE3Gm6JvVL6xmm6Ze0mCpUcEtsqD=
8csoouaFd6hKL4BU2FuatPdtFvJf4aNr84ZYL_wPYTXY7hjDxpBukMLlO6QsorF1xSFJrHFsb7E=
UrR-zLtK5dNYmeKBw4NRCWd4VDB5TWAfmVH-3CYoprC2Zi3F4Rmw68PRtG1OBn_HmEnUyD_yprO=
Wq2gg87nz2ZfPGUmCt7KKIPv_-6jsv2VCXK7b8aFVcBPAXA6bO1h0VABsOdeZQ5j2JTnpyVzzwB=
0qWdRnuZ_xCg_GYPVdwMaBsifBNuDrmTkpiRonu4wLbLzJRZvqYlSvO2a0KuX-7TGSmwLHTPmNY=
oXMP6D8j9acr1hFClfUag9w81pLQaunnPGG1hJ3MbWArl5cf0r8G6FjayJtRL0UNsjpr4D1L2bQ=
LJl6-kkQhmWYbnTWJoeOfnZ6trW7eeDoonY0y49l0w6KEwI4/4bq/kEQStHXPR369e8SlRa1G8w=
/h26/h001.eCW4NjFHmAJXdgTFC5MMuq_LG_yP9Ar3dE2fQrTsjtY" style=3D"color: #161=
616; text-decoration: none; -webkit-text-size-adjust: none;"><strong>$ 828,=
785</strong> a night</a></td>
<td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"right" style=3D"f=
loat: right; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;=
"><tr>
<td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"right" style=3D"f=
loat: right; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;=
"><tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 1=
4px; line-height: 18px; color: #FFFFFF; border-radius: 50px; direction: ltr=
; -webkit-text-size-adjust: none; padding: 2px 6px;" bgcolor=3D"#00AA6C">4.=
5</td></tr></table></td>
<td style=3D"-webkit-text-size-adjust: none;"><table role=3D"presentation" =
cellpadding=3D"0" cellspacing=3D"0" border=3D"0" align=3D"right" style=3D"f=
loat: right; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;=
">
<tr><td style=3D"-webkit-text-size-adjust: none;" align=3D"center"><img src=
=3D"https://www.tripadvisor.com/img/cdsi/img2/ratings/traveler/4.5-64600-4.=
png" width=3D"70" alt=3D"Tripadvisor score - 4.5." style=3D"outline: none; =
text-decoration: none; -ms-interpolation-mode: bicubic; border-style: none;=
"></td></tr>
<tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 10p=
x; line-height: 10px; color: #161616; padding-left: 4px; direction: ltr; -w=
ebkit-text-size-adjust: none;" align=3D"center">1025 reviews</td></tr>
</table></td>
</tr></table></td>
</tr>
</table></td></tr>
</table></td></tr></table>
<table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"=
0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; bo=
rder-width: 0;"><tr><td style=3D"font-size: 1px; -webkit-text-size-adjust: =
none;">&nbsp;</td></tr></table>
</td></tr></table></td></tr>
<tr><td style=3D"-webkit-text-size-adjust: none; padding: 0 24px 30px;" cla=
ss=3D"edges" bgcolor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=
=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lsp=
ace: 0pt; mso-table-rspace: 0pt; border-width: 0;"><tr><td style=3D"font-fa=
mily: 'Relative', Arial, sans-serif; mso-padding-alt: 11px 25px 13px; font-=
size: 16px; line-height: 24px; color: #FFFFFF; border-radius: 8px; directio=
n: ltr; -webkit-text-size-adjust: none; padding: 0 25px;" align=3D"center" =
valign=3D"middle" bgcolor=3D"#0062E3"><a href=3D"https://ablink.sender.skys=
canner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rm=
uzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9RmxX=
Ka2RuvDaGzp8ytL6xoAAVx4JZtOZ0UEeBMWTo39DqkRB2VnMuctt4w5y9K0AIlrQ4XlqXlV2tFD=
E3G1O-CFSMEOBNLttGzgSZyQbB8eDV1iFZMr6GcBf4IQ4CCHlFB0e_AJeLo6KeRsjDpBanhKbeg=
ok-78pAmM0VA8wLFChYsNza2NfxH0l6Q9e8d-K7ZwYi9clApvaOZah9AdCa24jhjIg63x3-mXl3=
edMhpx33Dw_eQnzwGrFgKRLnLk6110VNLOd5ovEnq0XmPNhADeLNCim-JehcsVkiJc6_rIGprB9=
DIXFjLwGeTvnhqBh6g6sCuxP32GPP3S-i06vCnB4Vd3fXmQokIhlxxHaVjHqMU/4bq/kEQStHXP=
R369e8SlRa1G8w/h27/h001.MnPGCIL7jV6aCWlLglLASQsVN3I8HAPcWqsGnoBOC84" style=
=3D"display: block; text-decoration: none; font-weight: bold; color: #FFFFF=
F; width: 100%; mso-padding-alt: 8px 0; -webkit-text-size-adjust: none; pad=
ding: 11px 0 13px;">See more Krakow hotels</a></td></tr></table></td></tr>
<tr><td class=3D"edges padding-bottom-24" style=3D"-webkit-text-size-adjust=
: none; padding: 0 24px 32px;" bgcolor=3D"#FFFFFF"><table role=3D"presentat=
ion" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=
=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-width: 0;">
<tr><td class=3D"h2-title" style=3D"font-family: 'Relative', Arial, sans-se=
rif; font-weight: bold; color: #161616; font-size: 32px; line-height: 40px;=
 direction: ltr; padding-bottom: 8px; -webkit-text-size-adjust: none;" alig=
n=3D"left">More inspiration</td></tr>
<tr><td valign=3D"top" style=3D"font-family: 'Relative', Arial, sans-serif;=
 color: #545860; font-size: 16px; line-height: 24px; direction: ltr; -webki=
t-text-size-adjust: none;" align=3D"left">Browse, book and enjoy the places=
 and prices your fellow travellers are absolutely loving this week.</td></t=
r>
</table></td></tr>
<tr><td class=3D"edges" style=3D"-webkit-text-size-adjust: none; padding: 0=
 24px;" bgcolor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=3D"0" =
cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0p=
t; mso-table-rspace: 0pt; border-width: 0;">
<tr><td style=3D"padding-bottom: 16px; -webkit-text-size-adjust: none;"><ta=
ble role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" =
width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; borde=
r-width: 0;"><tr><td style=3D"border-radius: 12px; font-family: 'Relative',=
 Arial, sans-serif; -webkit-text-size-adjust: none; border: 1px solid #E6E4=
EB;"><table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" borde=
r=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0p=
t; border-width: 0;">
<!--[if !mso]><!--><tr><td class=3D"show-mobile" style=3D"display: none; ma=
x-height: 0; overflow: hidden; border-top-left-radius: 12px; border-top-rig=
ht-radius: 12px; -webkit-text-size-adjust: none;"><a href=3D"https://ablink=
.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufac=
XuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-=
eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJj0IGV4s70IE1MxEjvre-7r=
3QTWdleD7tgtJu8OeqrA78ZbP6anlDt_v63cVMC1611y_ZgMGSJqfvDeTfPbjTTHeyC0y7E5CGU=
jwCAIK9U0n1VK_EqrC94eCKAowWy8V7nZ9F_xtA2KLSZYsAEO5HW3PoLy0hsuMwAYu1jK2IMBHF=
1CWRZiFBN04p_qNQGedoz4M1K2yyrX5FC9FoU6fPU2y6Opaswnd28RzJU0VdcnvY4eKF_jC5Hj5=
uXINlU_EVJFMIFMx81Er4POwKn6RhVVB2IXeM2mXm1-WsF9bLAjyGNp9mXscKcff58_5PBd-8o6=
LWdbsGNc4jOE3laEvH55zq-spiyDDEGGtias6Zu6bM4VKrZBL8gEHo9EaXQgfLQRRzDaSqDC66o=
LmrEYzaHapKwFPWypiLd_sG7civ6F66pTP8qDPXdykdIB2JB9j2A/4bq/kEQStHXPR369e8SlRa=
1G8w/h28/h001.paV4zjX5Inj2RruI0hqw_w1PzHTkj2prhSgrB2ZfICs" style=3D"-webkit=
-text-size-adjust: none; color: #776f6b;"><img src=3D"https://content.skysc=
nr.com/0f320987e189f43d5256fd38df04a977/GettyImages-461823317.jpg?crop=3D34=
3px:86px&amp;quality=3D70" alt=3D"Milan" width=3D"100%" style=3D"display: b=
lock; border-top-left-radius: 12px; border-top-right-radius: 12px; outline:=
 none; text-decoration: none; -ms-interpolation-mode: bicubic; border-style=
: none;"></a></td></tr>
<!--<![endif]--><tr><td style=3D"-webkit-text-size-adjust: none;"><table ro=
le=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=
=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-wid=
th: 0;"><tr>
<td class=3D"hide-mobile" style=3D"border-top-left-radius: 12px; border-bot=
tom-left-radius: 12px; -webkit-text-size-adjust: none;" width=3D"208" bgcol=
or=3D"#FBFBFB"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJj0IGV4s70IE1MxEjvre-7r3QTWdleD7tgtJu8OeqrA78ZbP6anlDt_v63=
cVMC1611y_ZgMGSJqfvDeTfPbjTTHeyC0y7E5CGUjwCAIK9U0n1VK_EqrC94eCKAowWy8V7nZ9F=
_xtA2KLSZYsAEO5HW3PoLy0hsuMwAYu1jK2IMBHF1CWRZiFBN04p_qNQGedoz4M1K2yyrX5FC9F=
oU6fPU2y6Opaswnd28RzJU0VdcnvY4eKF_jC5Hj5uXINlU_EVJFMIFMx81Er4POwKn6RhVVB2IX=
eM2mXm1-WsF9bLAjyGNp9mXscKcff58_5PBd-8o6LWdbsGNc4jOE3laEvH55zq-spiyDDEGGtia=
s6Zu6bM4VKrZBL8gEHo9EaXQgfLQRRzDaSqDC66oLmrEYzaHapKwFPWypiLd_sG7civ6F66pTP8=
qDPXdykdIB2JB9j2A/4bq/kEQStHXPR369e8SlRa1G8w/h29/h001.HDreBVYLe790yJvsE_9pE=
bZi8E01MWpHJZ76SDcKUYI" style=3D"-webkit-text-size-adjust: none; color: #77=
6f6b;"><img src=3D"https://content.skyscnr.com/0f320987e189f43d5256fd38df04=
a977/GettyImages-461823317.jpg?crop=3D208px:108px&amp;quality=3D70" alt=3D"=
Milan" width=3D"208" style=3D"display: block; border-top-left-radius: 12px;=
 border-bottom-left-radius: 12px; outline: none; text-decoration: none; -ms=
-interpolation-mode: bicubic; border-style: none;"></a></td>
<td style=3D"direction: ltr; -webkit-text-size-adjust: none; padding: 0 8px=
 0 24px;" class=3D"pad-vertical-16" align=3D"left"><a href=3D"https://ablin=
k.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufa=
cXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr=
-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJj0IGV4s70IE1MxEjvre-7=
r3QTWdleD7tgtJu8OeqrA78ZbP6anlDt_v63cVMC1611y_ZgMGSJqfvDeTfPbjTTHeyC0y7E5CG=
UjwCAIK9U0n1VK_EqrC94eCKAowWy8V7nZ9F_xtA2KLSZYsAEO5HW3PoLy0hsuMwAYu1jK2IMBH=
F1CWRZiFBN04p_qNQGedoz4M1K2yyrX5FC9FoU6fPU2y6Opaswnd28RzJU0VdcnvY4eKF_jC5Hj=
5uXINlU_EVJFMIFMx81Er4POwKn6RhVVB2IXeM2mXm1-WsF9bLAjyGNp9mXscKcff58_5PBd-8o=
6LWdbsGNc4jOE3laEvH55zq-spiyDDEGGtias6Zu6bM4VKrZBL8gEHo9EaXQgfLQRRzDaSqDC66=
oLmrEYzaHapKwFPWypiLd_sG7civ6F66pTP8qDPXdykdIB2JB9j2A/4bq/kEQStHXPR369e8SlR=
a1G8w/h30/h001.07rEqU81ndYqVmp3YZvpKeL8SPNZ3HNZJq-Cf8kJ-2g" style=3D"displa=
y: block; width: 100%; color: #161616; text-decoration: none; -webkit-text-=
size-adjust: none;"><span style=3D"font-size: 24px; line-height: 28px; font=
-weight: bold;" class=3D"hero-title">Milan</span><br><span style=3D"font-si=
ze: 14px; line-height: 20px; font-weight: normal; color: #545860;">Italy<br=
>2 Dec - 4 Dec</span></a></td>
<td valign=3D"bottom" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 12px; line-height: 16px; direction: ltr; color: #545860; -webkit=
-text-size-adjust: none; padding: 0 24px 16px 0;" align=3D"right">Flights f=
rom <span style=3D"font-size: 40px; line-height: 36px; font-weight: bold; c=
olor: #05203C; display: block;" class=3D"small-header-title">$ 254,884</spa=
n>
</td>
</tr></table></td></tr>
</table></td></tr></table></td></tr>
<tr><td style=3D"padding-bottom: 16px; -webkit-text-size-adjust: none;"><ta=
ble role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" =
width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; borde=
r-width: 0;"><tr><td style=3D"border-radius: 12px; font-family: 'Relative',=
 Arial, sans-serif; -webkit-text-size-adjust: none; border: 1px solid #E6E4=
EB;"><table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" borde=
r=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0p=
t; border-width: 0;">
<!--[if !mso]><!--><tr><td class=3D"show-mobile" style=3D"display: none; ma=
x-height: 0; overflow: hidden; border-top-left-radius: 12px; border-top-rig=
ht-radius: 12px; -webkit-text-size-adjust: none;"><a href=3D"https://ablink=
.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufac=
XuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-=
eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJjxD4dPTDOYg23VN6RzsFOK=
pS8ju3N4XtORXwQJVx4zTV9Q_0ExHksN_bW4Nw8ONwLGswnEROGIQyaBrGlLRYbAHl4-o5Hvh-g=
Z8h037zNBUOaCudNxV3YPVvjZ9luspDbI1kTGlkQAyw8uDB0WRkXLfxoc1i1ECswUtODFIS6Zd3=
gRFjYYbl0J_ycE5itGH_oaVErVrkk-sPuUwwHOBB59ee0mlVeWCRRqV3XREKQNILcZwn-mkWQDC=
NwIjV7rGPKXW-seEJWlnn0E1b-uT-YqtKC8DNmoOOEjOSPBX89eZ_fr0ytbpMw-3GEkdomnmHGK=
ZTKJmaYX_G7iC29bp0NG0X8kKBGaQymKzukz1OGHijLsf9A2QkIsVVb2iUfz7wLoKBcMuYO6OWN=
NPmksBT4RNSJ-2EBtJtKDrFnELnWT5HKVcnj1iq65YY_V5qtxU7k/4bq/kEQStHXPR369e8SlRa=
1G8w/h31/h001.8voQvf-v4eZ5eXPoexG8bATLmuoKU1o2CEgn4ikC5OQ" style=3D"-webkit=
-text-size-adjust: none; color: #776f6b;"><img src=3D"https://content.skysc=
nr.com/m/4dc3cee04825a86f/original/GettyImages-149110112_doc.jpg?crop=3D343=
px:86px&amp;quality=3D70" alt=3D"Bucharest" width=3D"100%" style=3D"display=
: block; border-top-left-radius: 12px; border-top-right-radius: 12px; outli=
ne: none; text-decoration: none; -ms-interpolation-mode: bicubic; border-st=
yle: none;"></a></td></tr>
<!--<![endif]--><tr><td style=3D"-webkit-text-size-adjust: none;"><table ro=
le=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=
=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-wid=
th: 0;"><tr>
<td class=3D"hide-mobile" style=3D"border-top-left-radius: 12px; border-bot=
tom-left-radius: 12px; -webkit-text-size-adjust: none;" width=3D"208" bgcol=
or=3D"#FBFBFB"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJjxD4dPTDOYg23VN6RzsFOKpS8ju3N4XtORXwQJVx4zTV9Q_0ExHksN_bW=
4Nw8ONwLGswnEROGIQyaBrGlLRYbAHl4-o5Hvh-gZ8h037zNBUOaCudNxV3YPVvjZ9luspDbI1k=
TGlkQAyw8uDB0WRkXLfxoc1i1ECswUtODFIS6Zd3gRFjYYbl0J_ycE5itGH_oaVErVrkk-sPuUw=
wHOBB59ee0mlVeWCRRqV3XREKQNILcZwn-mkWQDCNwIjV7rGPKXW-seEJWlnn0E1b-uT-YqtKC8=
DNmoOOEjOSPBX89eZ_fr0ytbpMw-3GEkdomnmHGKZTKJmaYX_G7iC29bp0NG0X8kKBGaQymKzuk=
z1OGHijLsf9A2QkIsVVb2iUfz7wLoKBcMuYO6OWNNPmksBT4RNSJ-2EBtJtKDrFnELnWT5HKVcn=
j1iq65YY_V5qtxU7k/4bq/kEQStHXPR369e8SlRa1G8w/h32/h001.tFwwfcYOn5dUqOp6uEeeY=
jCGrORLvrCzX75o1EGv58g" style=3D"-webkit-text-size-adjust: none; color: #77=
6f6b;"><img src=3D"https://content.skyscnr.com/m/4dc3cee04825a86f/original/=
GettyImages-149110112_doc.jpg?crop=3D208px:108px&amp;quality=3D70" alt=3D"B=
ucharest" width=3D"208" style=3D"display: block; border-top-left-radius: 12=
px; border-bottom-left-radius: 12px; outline: none; text-decoration: none; =
-ms-interpolation-mode: bicubic; border-style: none;"></a></td>
<td style=3D"direction: ltr; -webkit-text-size-adjust: none; padding: 0 8px=
 0 24px;" class=3D"pad-vertical-16" align=3D"left"><a href=3D"https://ablin=
k.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufa=
cXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr=
-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJjxD4dPTDOYg23VN6RzsFO=
KpS8ju3N4XtORXwQJVx4zTV9Q_0ExHksN_bW4Nw8ONwLGswnEROGIQyaBrGlLRYbAHl4-o5Hvh-=
gZ8h037zNBUOaCudNxV3YPVvjZ9luspDbI1kTGlkQAyw8uDB0WRkXLfxoc1i1ECswUtODFIS6Zd=
3gRFjYYbl0J_ycE5itGH_oaVErVrkk-sPuUwwHOBB59ee0mlVeWCRRqV3XREKQNILcZwn-mkWQD=
CNwIjV7rGPKXW-seEJWlnn0E1b-uT-YqtKC8DNmoOOEjOSPBX89eZ_fr0ytbpMw-3GEkdomnmHG=
KZTKJmaYX_G7iC29bp0NG0X8kKBGaQymKzukz1OGHijLsf9A2QkIsVVb2iUfz7wLoKBcMuYO6OW=
NNPmksBT4RNSJ-2EBtJtKDrFnELnWT5HKVcnj1iq65YY_V5qtxU7k/4bq/kEQStHXPR369e8SlR=
a1G8w/h33/h001.lwg7uQtZUNL7FVwrozuLaU9UxbCnd8j-Gn8wXoG0UfI" style=3D"displa=
y: block; width: 100%; color: #161616; text-decoration: none; -webkit-text-=
size-adjust: none;"><span style=3D"font-size: 24px; line-height: 28px; font=
-weight: bold;" class=3D"hero-title">Bucharest</span><br><span style=3D"fon=
t-size: 14px; line-height: 20px; font-weight: normal; color: #545860;">Roma=
nia<br>8 Dec - 13 Dec</span></a></td>
<td valign=3D"bottom" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 12px; line-height: 16px; direction: ltr; color: #545860; -webkit=
-text-size-adjust: none; padding: 0 24px 16px 0;" align=3D"right">Flights f=
rom <span style=3D"font-size: 40px; line-height: 36px; font-weight: bold; c=
olor: #05203C; display: block;" class=3D"small-header-title">$ 508,893</spa=
n>
</td>
</tr></table></td></tr>
</table></td></tr></table></td></tr>
<tr><td style=3D"padding-bottom: 16px; -webkit-text-size-adjust: none;"><ta=
ble role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" =
width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; borde=
r-width: 0;"><tr><td style=3D"border-radius: 12px; font-family: 'Relative',=
 Arial, sans-serif; -webkit-text-size-adjust: none; border: 1px solid #E6E4=
EB;"><table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" borde=
r=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0p=
t; border-width: 0;">
<!--[if !mso]><!--><tr><td class=3D"show-mobile" style=3D"display: none; ma=
x-height: 0; overflow: hidden; border-top-left-radius: 12px; border-top-rig=
ht-radius: 12px; -webkit-text-size-adjust: none;"><a href=3D"https://ablink=
.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufac=
XuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-=
eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgjPTKlgmqebo8hXVzX04FR=
Os4rw5t6nIORJFH36v9m5SXmBdAaWhXydMaYSN2AX1NDsskSDE__mvyXDhJchq9GkvZ2Y4q2eog=
3CJGriOG-jqMztwVGToOWRQnf6LPwhB2uo9fZ6pZGMsXB7Jau_Gz_VH5a33ZVsP98OAhcGBofH9=
6-VYwGY8l0GND_RiLPfee4IFzqdqyCK2MgtSJijTmTvj05lKK2WJFJ5HsUX4CRN7nXYcbhP5PAB=
uYTEcuJQPUqhZ8KTG-PsxmDGDwyJNoaXCfeleWlNlr5h8rwD40qY4Q1WVAnPPHlDoySC-Jh04jd=
7zzzZ-E6Il8Bp5MofwECetM-HbvAJ8w_mP9wuK958JyaLS-XjflF8E_MjQd4EPV0gJEmedte9b0=
-ZVUi235Y5wsYzXRMdqbT5d9neT9RhTGmF14o3e5FnZsSkW7yukA/4bq/kEQStHXPR369e8SlRa=
1G8w/h34/h001.1tsSsyAPFkPebdYONjkqOtQiGDD7dYMDRE1I0O_JexE" style=3D"-webkit=
-text-size-adjust: none; color: #776f6b;"><img src=3D"https://content.skysc=
nr.com/m/1a55403f63baf856/Large-London-England-Aug-2017-Brendan-van-Son-5.j=
pg?crop=3D343px:86px&amp;quality=3D70" alt=3D"London" width=3D"100%" style=
=3D"display: block; border-top-left-radius: 12px; border-top-right-radius: =
12px; outline: none; text-decoration: none; -ms-interpolation-mode: bicubic=
; border-style: none;"></a></td></tr>
<!--<![endif]--><tr><td style=3D"-webkit-text-size-adjust: none;"><table ro=
le=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=
=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-wid=
th: 0;"><tr>
<td class=3D"hide-mobile" style=3D"border-top-left-radius: 12px; border-bot=
tom-left-radius: 12px; -webkit-text-size-adjust: none;" width=3D"208" bgcol=
or=3D"#FBFBFB"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJgjPTKlgmqebo8hXVzX04FROs4rw5t6nIORJFH36v9m5SXmBdAaWhXydMa=
YSN2AX1NDsskSDE__mvyXDhJchq9GkvZ2Y4q2eog3CJGriOG-jqMztwVGToOWRQnf6LPwhB2uo9=
fZ6pZGMsXB7Jau_Gz_VH5a33ZVsP98OAhcGBofH96-VYwGY8l0GND_RiLPfee4IFzqdqyCK2Mgt=
SJijTmTvj05lKK2WJFJ5HsUX4CRN7nXYcbhP5PABuYTEcuJQPUqhZ8KTG-PsxmDGDwyJNoaXCfe=
leWlNlr5h8rwD40qY4Q1WVAnPPHlDoySC-Jh04jd7zzzZ-E6Il8Bp5MofwECetM-HbvAJ8w_mP9=
wuK958JyaLS-XjflF8E_MjQd4EPV0gJEmedte9b0-ZVUi235Y5wsYzXRMdqbT5d9neT9RhTGmF1=
4o3e5FnZsSkW7yukA/4bq/kEQStHXPR369e8SlRa1G8w/h35/h001.Qv5K64uxFPrEqAvHMb3XQ=
0xwooUgMCLS4WHC86BAveg" style=3D"-webkit-text-size-adjust: none; color: #77=
6f6b;"><img src=3D"https://content.skyscnr.com/m/1a55403f63baf856/Large-Lon=
don-England-Aug-2017-Brendan-van-Son-5.jpg?crop=3D208px:108px&amp;quality=
=3D70" alt=3D"London" width=3D"208" style=3D"display: block; border-top-lef=
t-radius: 12px; border-bottom-left-radius: 12px; outline: none; text-decora=
tion: none; -ms-interpolation-mode: bicubic; border-style: none;"></a></td>
<td style=3D"direction: ltr; -webkit-text-size-adjust: none; padding: 0 8px=
 0 24px;" class=3D"pad-vertical-16" align=3D"left"><a href=3D"https://ablin=
k.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufa=
cXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr=
-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgjPTKlgmqebo8hXVzX04F=
ROs4rw5t6nIORJFH36v9m5SXmBdAaWhXydMaYSN2AX1NDsskSDE__mvyXDhJchq9GkvZ2Y4q2eo=
g3CJGriOG-jqMztwVGToOWRQnf6LPwhB2uo9fZ6pZGMsXB7Jau_Gz_VH5a33ZVsP98OAhcGBofH=
96-VYwGY8l0GND_RiLPfee4IFzqdqyCK2MgtSJijTmTvj05lKK2WJFJ5HsUX4CRN7nXYcbhP5PA=
BuYTEcuJQPUqhZ8KTG-PsxmDGDwyJNoaXCfeleWlNlr5h8rwD40qY4Q1WVAnPPHlDoySC-Jh04j=
d7zzzZ-E6Il8Bp5MofwECetM-HbvAJ8w_mP9wuK958JyaLS-XjflF8E_MjQd4EPV0gJEmedte9b=
0-ZVUi235Y5wsYzXRMdqbT5d9neT9RhTGmF14o3e5FnZsSkW7yukA/4bq/kEQStHXPR369e8SlR=
a1G8w/h36/h001.29IU5rws8l6vugyWKwhiOc_QRpkLQNOxhj8p0m_n4Eg" style=3D"displa=
y: block; width: 100%; color: #161616; text-decoration: none; -webkit-text-=
size-adjust: none;"><span style=3D"font-size: 24px; line-height: 28px; font=
-weight: bold;" class=3D"hero-title">London</span><br><span style=3D"font-s=
ize: 14px; line-height: 20px; font-weight: normal; color: #545860;">United =
Kingdom<br>19 Dec - 31 Dec</span></a></td>
<td valign=3D"bottom" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 12px; line-height: 16px; direction: ltr; color: #545860; -webkit=
-text-size-adjust: none; padding: 0 24px 16px 0;" align=3D"right">Flights f=
rom <span style=3D"font-size: 40px; line-height: 36px; font-weight: bold; c=
olor: #05203C; display: block;" class=3D"small-header-title">$ 531,407</spa=
n>
</td>
</tr></table></td></tr>
</table></td></tr></table></td></tr>
<tr><td style=3D"padding-bottom: 16px; -webkit-text-size-adjust: none;"><ta=
ble role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" =
width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; borde=
r-width: 0;"><tr><td style=3D"border-radius: 12px; font-family: 'Relative',=
 Arial, sans-serif; -webkit-text-size-adjust: none; border: 1px solid #E6E4=
EB;"><table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" borde=
r=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0p=
t; border-width: 0;">
<!--[if !mso]><!--><tr><td class=3D"show-mobile" style=3D"display: none; ma=
x-height: 0; overflow: hidden; border-top-left-radius: 12px; border-top-rig=
ht-radius: 12px; -webkit-text-size-adjust: none;"><a href=3D"https://ablink=
.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufac=
XuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-=
eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJhTyuHqGDW_y9_654yIaPDx=
F4J6lYiugG3wBK4Zqgpdt02-Y4KuEgv8D-CbXg-uyO0_oWQ9dv6k-iMY9y_znbpsSfs5Ogk-EQl=
1VkAgypEREpWAwTZKlRW6RCewZMJexFc7Wk9wtrhethdDfn8lyXmo5ing7j0i2RkrcZcCMleDSk=
oIkl2xwEoE3bhis88g1PdxKmg-XQFTFSLzq5nxTbM8-PGKlGBZOslwnvDRidVOQMNVryy1iLT3-=
cgDJHQa8t_t8n8DGpYDle3qM_wLblBxLubHJaBrx9rg_3KpOmnOJpU6dSB4Nq1FsIMkDsAtLpo-=
J4f2D--Ds41QwP39Y3Ar27iCc1344ia0iFPcYPid1h7fYZBzHDX0p_N9fVECPEDJP8jnHMbFnOS=
YbtTlDoOIVM-L4DreBRo07ksvHQbgSckIA5osCGzyttkbgMBj0Qs/4bq/kEQStHXPR369e8SlRa=
1G8w/h37/h001.HaC-9DorU-YVbcEcjDnG_L9VZk4_OTKvoXXTf--YuC8" style=3D"-webkit=
-text-size-adjust: none; color: #776f6b;"><img src=3D"https://content.skysc=
nr.com/m/1c7b8e0703dcc64/original/Budapest-Citadella.jpg?crop=3D343px:86px&=
amp;quality=3D70" alt=3D"Budapest" width=3D"100%" style=3D"display: block; =
border-top-left-radius: 12px; border-top-right-radius: 12px; outline: none;=
 text-decoration: none; -ms-interpolation-mode: bicubic; border-style: none=
;"></a></td></tr>
<!--<![endif]--><tr><td style=3D"-webkit-text-size-adjust: none;"><table ro=
le=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=
=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-wid=
th: 0;"><tr>
<td class=3D"hide-mobile" style=3D"border-top-left-radius: 12px; border-bot=
tom-left-radius: 12px; -webkit-text-size-adjust: none;" width=3D"208" bgcol=
or=3D"#FBFBFB"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJhTyuHqGDW_y9_654yIaPDxF4J6lYiugG3wBK4Zqgpdt02-Y4KuEgv8D-C=
bXg-uyO0_oWQ9dv6k-iMY9y_znbpsSfs5Ogk-EQl1VkAgypEREpWAwTZKlRW6RCewZMJexFc7Wk=
9wtrhethdDfn8lyXmo5ing7j0i2RkrcZcCMleDSkoIkl2xwEoE3bhis88g1PdxKmg-XQFTFSLzq=
5nxTbM8-PGKlGBZOslwnvDRidVOQMNVryy1iLT3-cgDJHQa8t_t8n8DGpYDle3qM_wLblBxLubH=
JaBrx9rg_3KpOmnOJpU6dSB4Nq1FsIMkDsAtLpo-J4f2D--Ds41QwP39Y3Ar27iCc1344ia0iFP=
cYPid1h7fYZBzHDX0p_N9fVECPEDJP8jnHMbFnOSYbtTlDoOIVM-L4DreBRo07ksvHQbgSckIA5=
osCGzyttkbgMBj0Qs/4bq/kEQStHXPR369e8SlRa1G8w/h38/h001.lcz9jyj6GOsPotfrJAKkQ=
iLuIFQyZnTdVj7uBt3HR7o" style=3D"-webkit-text-size-adjust: none; color: #77=
6f6b;"><img src=3D"https://content.skyscnr.com/m/1c7b8e0703dcc64/original/B=
udapest-Citadella.jpg?crop=3D208px:108px&amp;quality=3D70" alt=3D"Budapest"=
 width=3D"208" style=3D"display: block; border-top-left-radius: 12px; borde=
r-bottom-left-radius: 12px; outline: none; text-decoration: none; -ms-inter=
polation-mode: bicubic; border-style: none;"></a></td>
<td style=3D"direction: ltr; -webkit-text-size-adjust: none; padding: 0 8px=
 0 24px;" class=3D"pad-vertical-16" align=3D"left"><a href=3D"https://ablin=
k.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufa=
cXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr=
-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJhTyuHqGDW_y9_654yIaPD=
xF4J6lYiugG3wBK4Zqgpdt02-Y4KuEgv8D-CbXg-uyO0_oWQ9dv6k-iMY9y_znbpsSfs5Ogk-EQ=
l1VkAgypEREpWAwTZKlRW6RCewZMJexFc7Wk9wtrhethdDfn8lyXmo5ing7j0i2RkrcZcCMleDS=
koIkl2xwEoE3bhis88g1PdxKmg-XQFTFSLzq5nxTbM8-PGKlGBZOslwnvDRidVOQMNVryy1iLT3=
-cgDJHQa8t_t8n8DGpYDle3qM_wLblBxLubHJaBrx9rg_3KpOmnOJpU6dSB4Nq1FsIMkDsAtLpo=
-J4f2D--Ds41QwP39Y3Ar27iCc1344ia0iFPcYPid1h7fYZBzHDX0p_N9fVECPEDJP8jnHMbFnO=
SYbtTlDoOIVM-L4DreBRo07ksvHQbgSckIA5osCGzyttkbgMBj0Qs/4bq/kEQStHXPR369e8SlR=
a1G8w/h39/h001.DfCvMmLXDtpjen8gKTdVXj9C4NqOy-sGzuj8xT1Q9KE" style=3D"displa=
y: block; width: 100%; color: #161616; text-decoration: none; -webkit-text-=
size-adjust: none;"><span style=3D"font-size: 24px; line-height: 28px; font=
-weight: bold;" class=3D"hero-title">Budapest</span><br><span style=3D"font=
-size: 14px; line-height: 20px; font-weight: normal; color: #545860;">Hunga=
ry<br>1 Dec - 5 Dec</span></a></td>
<td valign=3D"bottom" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 12px; line-height: 16px; direction: ltr; color: #545860; -webkit=
-text-size-adjust: none; padding: 0 24px 16px 0;" align=3D"right">Flights f=
rom <span style=3D"font-size: 40px; line-height: 36px; font-weight: bold; c=
olor: #05203C; display: block;" class=3D"small-header-title">$ 627,910</spa=
n>
</td>
</tr></table></td></tr>
</table></td></tr></table></td></tr>
<tr><td style=3D"padding-bottom: 16px; -webkit-text-size-adjust: none;"><ta=
ble role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" =
width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; borde=
r-width: 0;"><tr><td style=3D"border-radius: 12px; font-family: 'Relative',=
 Arial, sans-serif; -webkit-text-size-adjust: none; border: 1px solid #E6E4=
EB;"><table role=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" borde=
r=3D"0" width=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0p=
t; border-width: 0;">
<!--[if !mso]><!--><tr><td class=3D"show-mobile" style=3D"display: none; ma=
x-height: 0; overflow: hidden; border-top-left-radius: 12px; border-top-rig=
ht-radius: 12px; -webkit-text-size-adjust: none;"><a href=3D"https://ablink=
.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufac=
XuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-=
eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgh8WiUuS7xGh9mBNY8HSPN=
quDpCx2is0l6ZwW76Hnw0dJYxklaUx7JLR0-RK88yUAbFH1phgJ4Vw57bZXZDT7NIWaXWAEytQb=
ccULoHKZIr7L3c0fswcySN5W6tZpTLGQdfUoV9XZDPn3O12U_2FntgpQWF1H1kvUo11-EYzARaS=
vwb7n4G2WO_0EYZwv5hC8CsCX8ARIJ3RnUuiv3DGhzCOzYEoherzFLfgmAuIJcwjXxearTqCSyf=
u1yc_7H1vo3yr4jHSo74de1bN-dAvL_Fe4RSw6BkNE40gZjPb1AOg_geEZJLTKgiMElJehS6IcZ=
gqJlcjR0wA6w32cH3WqUTUgw2jj9wE1V4LJx8uTjd5qWVrqWdIsXzuIc8tgebYs6DBJ0AERS6SH=
rWNoKwBNwLV-3dej8zQCLGxEOdGp9mTGBon9NY4PshdIWuVIRQUI/4bq/kEQStHXPR369e8SlRa=
1G8w/h40/h001.XdvJCP6DQ1tNQtiUSmyn1TkIqhNrz4BZOsKXLijDlSg" style=3D"-webkit=
-text-size-adjust: none; color: #776f6b;"><img src=3D"https://content.skysc=
nr.com/7387d4b223075dd116e68295d7ae2f19/GettyImages-470289252.jpg?crop=3D34=
3px:86px&amp;quality=3D70" alt=3D"Wroclaw" width=3D"100%" style=3D"display:=
 block; border-top-left-radius: 12px; border-top-right-radius: 12px; outlin=
e: none; text-decoration: none; -ms-interpolation-mode: bicubic; border-sty=
le: none;"></a></td></tr>
<!--<![endif]--><tr><td style=3D"-webkit-text-size-adjust: none;"><table ro=
le=3D"presentation" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" width=
=3D"100%" style=3D"mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-wid=
th: 0;"><tr>
<td class=3D"hide-mobile" style=3D"border-top-left-radius: 12px; border-bot=
tom-left-radius: 12px; -webkit-text-size-adjust: none;" width=3D"208" bgcol=
or=3D"#FBFBFB"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xv=
xeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbi=
eyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BT=
TvwogvIBc70DFE4JZJgh8WiUuS7xGh9mBNY8HSPNquDpCx2is0l6ZwW76Hnw0dJYxklaUx7JLR0=
-RK88yUAbFH1phgJ4Vw57bZXZDT7NIWaXWAEytQbccULoHKZIr7L3c0fswcySN5W6tZpTLGQdfU=
oV9XZDPn3O12U_2FntgpQWF1H1kvUo11-EYzARaSvwb7n4G2WO_0EYZwv5hC8CsCX8ARIJ3RnUu=
iv3DGhzCOzYEoherzFLfgmAuIJcwjXxearTqCSyfu1yc_7H1vo3yr4jHSo74de1bN-dAvL_Fe4R=
Sw6BkNE40gZjPb1AOg_geEZJLTKgiMElJehS6IcZgqJlcjR0wA6w32cH3WqUTUgw2jj9wE1V4LJ=
x8uTjd5qWVrqWdIsXzuIc8tgebYs6DBJ0AERS6SHrWNoKwBNwLV-3dej8zQCLGxEOdGp9mTGBon=
9NY4PshdIWuVIRQUI/4bq/kEQStHXPR369e8SlRa1G8w/h41/h001.yzwGK5D3Ub4IiiFqLHW33=
vdI4WZrK7Hyi3-yTvx0k9o" style=3D"-webkit-text-size-adjust: none; color: #77=
6f6b;"><img src=3D"https://content.skyscnr.com/7387d4b223075dd116e68295d7ae=
2f19/GettyImages-470289252.jpg?crop=3D208px:108px&amp;quality=3D70" alt=3D"=
Wroclaw" width=3D"208" style=3D"display: block; border-top-left-radius: 12p=
x; border-bottom-left-radius: 12px; outline: none; text-decoration: none; -=
ms-interpolation-mode: bicubic; border-style: none;"></a></td>
<td style=3D"direction: ltr; -webkit-text-size-adjust: none; padding: 0 8px=
 0 24px;" class=3D"pad-vertical-16" align=3D"left"><a href=3D"https://ablin=
k.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufa=
cXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mlz3Gicxcr=
-eAx5daCClhYHDpQ92WtX1_Cp7I4H1zhY_BTTvwogvIBc70DFE4JZJgh8WiUuS7xGh9mBNY8HSP=
NquDpCx2is0l6ZwW76Hnw0dJYxklaUx7JLR0-RK88yUAbFH1phgJ4Vw57bZXZDT7NIWaXWAEytQ=
bccULoHKZIr7L3c0fswcySN5W6tZpTLGQdfUoV9XZDPn3O12U_2FntgpQWF1H1kvUo11-EYzARa=
Svwb7n4G2WO_0EYZwv5hC8CsCX8ARIJ3RnUuiv3DGhzCOzYEoherzFLfgmAuIJcwjXxearTqCSy=
fu1yc_7H1vo3yr4jHSo74de1bN-dAvL_Fe4RSw6BkNE40gZjPb1AOg_geEZJLTKgiMElJehS6Ic=
ZgqJlcjR0wA6w32cH3WqUTUgw2jj9wE1V4LJx8uTjd5qWVrqWdIsXzuIc8tgebYs6DBJ0AERS6S=
HrWNoKwBNwLV-3dej8zQCLGxEOdGp9mTGBon9NY4PshdIWuVIRQUI/4bq/kEQStHXPR369e8SlR=
a1G8w/h42/h001.F-cu0OTpTN1HX8PSflmgdbhfD7Yal5aFv4eZPiFUTOo" style=3D"displa=
y: block; width: 100%; color: #161616; text-decoration: none; -webkit-text-=
size-adjust: none;"><span style=3D"font-size: 24px; line-height: 28px; font=
-weight: bold;" class=3D"hero-title">Wroclaw</span><br><span style=3D"font-=
size: 14px; line-height: 20px; font-weight: normal; color: #545860;">Poland=
<br>7 Dec - 13 Dec</span></a></td>
<td valign=3D"bottom" style=3D"font-family: 'Relative', Arial, sans-serif; =
font-size: 12px; line-height: 16px; direction: ltr; color: #545860; -webkit=
-text-size-adjust: none; padding: 0 24px 16px 0;" align=3D"right">Flights f=
rom <span style=3D"font-size: 40px; line-height: 36px; font-weight: bold; c=
olor: #05203C; display: block;" class=3D"small-header-title">$ 644,669</spa=
n>
</td>
</tr></table></td></tr>
</table></td></tr></table></td></tr>
</table></td></tr>
<tr><td style=3D"-webkit-text-size-adjust: none; padding: 0 24px 32px;" cla=
ss=3D"edges" bgcolor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=
=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lsp=
ace: 0pt; mso-table-rspace: 0pt; border-width: 0;"><tr><td style=3D"font-fa=
mily: 'Relative', Arial, sans-serif; mso-padding-alt: 11px 25px 13px; font-=
size: 16px; line-height: 24px; color: #FFFFFF; border-radius: 8px; directio=
n: ltr; -webkit-text-size-adjust: none; padding: 0 25px;" align=3D"center" =
valign=3D"middle" bgcolor=3D"#0062E3"><a href=3D"https://ablink.sender.skys=
canner.com/ss/c/u001.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rm=
uzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9Rmxy=
ZH9dMr9RVmppWu9dftl6SM2DaAXanei9VYKBukFolFcjCQVt2tMYNvESh4zKEIJ4WDIFuXwnwKC=
9Lar7tsU7WCP0UYoYGEPqMumHOBbjaQTcYo6216FUXPFlpONQM8VoUfPNK5IPIbWHO7l98KQQkQ=
uKPU0G5Xpw3ACzi6fdgViS0lM3ChWYT0jXp1gyOJYwTrkhgStG28YwVgx1IorRNCfXYWR9xGXw3=
BdLKKOQ-p-oMl52d00y7f3Mp4g3warJg4M622-O5ENuzFrOPlOAd260VyRcjJpLxkDztBVRKELA=
WCCLWp9lESd4Y-MbtUzbKsK_1S4penv6rN4U9JF5bK72PqbqDtXV2Go3yuOSABGkZCDy9oqcSEl=
ADsR2Ef3pEyEaVIL5-gKyOfYvdtW8XMoqxFvYLNpz4XlIVbyAIrbPNKzUOVhRzWEppD9psNakyU=
2UZAWewd_Lazh-Sz-qQ/4bq/kEQStHXPR369e8SlRa1G8w/h43/h001.dfoRzNE4Xbaqh60OvB-=
UAeAYGqmRQf2j-rWCS2f2pks" style=3D"display: block; text-decoration: none; f=
ont-weight: bold; color: #FFFFFF; width: 100%; mso-padding-alt: 8px 0; -web=
kit-text-size-adjust: none; padding: 11px 0 13px;">See more flight deals</a=
></td></tr></table></td></tr>
<tr><td style=3D"-webkit-text-size-adjust: none; padding: 0 24px 32px;" cla=
ss=3D"edges" bgcolor=3D"#FFFFFF"><table role=3D"presentation" cellpadding=
=3D"0" cellspacing=3D"0" border=3D"0" width=3D"100%" style=3D"mso-table-lsp=
ace: 0pt; mso-table-rspace: 0pt; border-width: 0;"><tr>
<td style=3D"padding-right: 20px; font-size: 0; -webkit-text-size-adjust: n=
one;" width=3D"32" valign=3D"top"><img src=3D"https://cdn.braze.eu/appboy/c=
ommunication/assets/image_assets/images/5f4f59763092112aa29d2267/original.p=
ng?1599035766" width=3D"32" alt=3D"" style=3D"outline: none; text-decoratio=
n: none; -ms-interpolation-mode: bicubic; border-style: none;"></td>
<td style=3D"font-family: 'Relative', Arial, sans-serif; color: #545860; fo=
nt-size: 12px; line-height: 16px; direction: ltr; -webkit-text-size-adjust:=
 none;" align=3D"left">
<strong>How did we find these deals?</strong> They're simply the lowest far=
es we found for these destinations within the last 4 days, and are subject =
to change and availability.</td>
</tr></table></td></tr>

<tr><td class=3D"edges pad-bottom-24" style=3D"-webkit-text-size-adjust: no=
ne; padding: 24px;" bgcolor=3D"#05203C"><table role=3D"presentation" align=
=3D"left" cellpadding=3D"0" cellspacing=3D"0" border=3D"0" style=3D"float: =
left; font-size: 0; mso-table-lspace: 0pt; mso-table-rspace: 0pt; border-wi=
dth: 0;">
<tr><td width=3D"100%" align=3D"left" style=3D"font-size: 0; -webkit-text-s=
ize-adjust: none;">
<table role=3D"presentation" align=3D"left" cellpadding=3D"0" cellspacing=
=3D"0" border=3D"0" style=3D"float: left; mso-table-lspace: 0pt; mso-table-=
rspace: 0pt; border-width: 0;"><tr><td valign=3D"middle" style=3D"direction=
: ltr; font-size: 0; -webkit-text-size-adjust: none; padding: 0 16px 16px 0=
;" align=3D"left"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001=
.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeM=
mbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9Rmxcdnffx8UUR56L98uWz64Z=
3wReQVohk1LINM9gAyENSQa3VXYPGgJBejWeS1nvupVFIMxqWwP23jpBZ8pKonuvsOmWSxi-Onx=
qf11SGanLi503PBowd8E2wFj8FVJ0G2-_cETH-Trg_GibZd3adhRg7G3orJZelLdppFb5_TCi-H=
87Vx20sZPT6jJUqcmiVXeSonSQFkNmeIJm9UQJ723cQ/4bq/kEQStHXPR369e8SlRa1G8w/h44/=
h001.ilE0hpinHXoTPj1p9_X4aYD525VK5K6Xqc-58KynT9k" style=3D"color: #05203C; =
text-decoration: none; font-size: 0; -webkit-text-size-adjust: none;"><img =
src=3D"https://cdn.braze.eu/appboy/communication/assets/image_assets/images=
/642fe948bfd06460c57809cf/original.png?1680861512" width=3D"24" alt=3D"" st=
yle=3D"display: inline; vertical-align: middle; outline: none; text-decorat=
ion: none; -ms-interpolation-mode: bicubic; border-style: none;"><span styl=
e=3D"font-family: 'Relative', Arial, sans-serif; font-size: 16px; line-heig=
ht: 20px; color: #FFFFFF; display: inline; vertical-align: middle;">Flights=
</span></a></td></tr></table>
<table role=3D"presentation" align=3D"left" cellpadding=3D"0" cellspacing=
=3D"0" border=3D"0" style=3D"float: left; mso-table-lspace: 0pt; mso-table-=
rspace: 0pt; border-width: 0;"><tr><td valign=3D"middle" style=3D"direction=
: ltr; font-size: 0; -webkit-text-size-adjust: none; padding: 0 16px 16px 0=
;" align=3D"left">
<a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xvxeTnj4EG7fcfOeG=
kr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbieyUnEjt2tsPkjPw=
sbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9RmxXKa2RuvDaGzp8ytL6xoAAdwDcOX_ZxnjXmvyKXh=
r_YARG_xD7JPG2l13aXqV5R4GFd0nYkCfDoufDeij7KeEOx7Um8m9XsB-gXZ2I7JGUbxzVsYv-J=
ASWTduQYuuOp42T3CDNPnCTtE7iz2B6O_h0tayn8Kyrw9nvuLGbns-zru2ouyRvJ87MdZS5uVsi=
gxNJLDwT6JqgwWWzbpkn6dCHQ/4bq/kEQStHXPR369e8SlRa1G8w/h45/h001.LWzcHCMyhjCGN=
dZGfslxOPVUMiXrtx0dTun9Z47NdOM" style=3D"color: #05203C; text-decoration: n=
one; font-size: 0; -webkit-text-size-adjust: none;"><img src=3D"https://cdn=
.braze.eu/appboy/communication/assets/image_assets/images/642fe94c3110353a2=
f4498c8/original.png?1680861516" width=3D"24" alt=3D"" style=3D"display: in=
line; vertical-align: middle; outline: none; text-decoration: none; -ms-int=
erpolation-mode: bicubic; border-style: none;"><span style=3D"font-family: =
'Relative', Arial, sans-serif; font-size: 16px; line-height: 20px; color: #=
FFFFFF; display: inline; vertical-align: middle;">Hotels</span></a> </td></=
tr></table>
<table role=3D"presentation" align=3D"left" cellpadding=3D"0" cellspacing=
=3D"0" border=3D"0" style=3D"float: left; mso-table-lspace: 0pt; mso-table-=
rspace: 0pt; border-width: 0;"><tr><td valign=3D"middle" style=3D"direction=
: ltr; font-size: 0; -webkit-text-size-adjust: none; padding: 0 16px 16px 0=
;" align=3D"left"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001=
.xvxeTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeM=
mbieyUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9RmxKC5KvkEYZJGmffvYpcuo-=
r5D4MPSdM0JQDEjyo-Tl0D_-Bggis39Z9RzyYxtTJhEHUcwTlwyiM9mALoBS72Bdte2tnC3iBgR=
XtOQVRbLET6-0kih1FBawqxb1TYDflToZxUGGpqdF9uqaZ68X6iUUH18RKzrCh0NoOG6qDF9kOI=
_UVlV32PAUHis2IDNlEUFqRdg1PC59oqWagHasG5N8Q/4bq/kEQStHXPR369e8SlRa1G8w/h46/=
h001.fKsNACusyrSW0g2856IOQz8MZA3DYCPxRdvnaySTyOU" style=3D"color: #05203C; =
text-decoration: none; font-size: 0; -webkit-text-size-adjust: none;"><img =
src=3D"https://cdn.braze.eu/appboy/communication/assets/image_assets/images=
/642fe94dcb770f73f385781e/original.png?1680861517" width=3D"24" alt=3D"" st=
yle=3D"display: inline; vertical-align: middle; outline: none; text-decorat=
ion: none; -ms-interpolation-mode: bicubic; border-style: none;"><span styl=
e=3D"font-family: 'Relative', Arial, sans-serif; font-size: 16px; line-heig=
ht: 20px; color: #FFFFFF; display: inline; vertical-align: middle;">Car hir=
e</span></a></td></tr></table>
</td></tr>
<tr><td style=3D"font-family: 'Relative', Arial, sans-serif; color: #FFFFFF=
; font-size: 12px; line-height: 16px; padding-bottom: 16px; direction: ltr;=
 -webkit-text-size-adjust: none;" align=3D"left">Based on your activity we=
=E2=80=99ve set your home airport as Alghero Sardinia. <a href=3D"https://a=
blink.sender.skyscanner.com/ss/c/u001.Z7kxosXrAU3mKizuSTS8eOk0XcVpAK7-85Rg8=
6McO-PB7HcFFcPPfJqKYrl722zxfrZeDjUJLyoVfiFQXX2Zy4Qd0SjU53UBOKfk81UXbq4wjZt9=
Lkx6_wAIXoKCTROA5d8GKVDQ5THcfEeFk-a-PerpXqZN1n5i8spcqMfaU7i9HpZdEFyhQlmKpao=
X2dWMb_y-Qlw9X1W78KnV7X_NnBcF3v4h5-8HVidKgraV79LysnUeF0HuICWON3mKO4wTT2sjpl=
pfuJiOov_SPh8jSJox440byMWAI_utHkFGxqgwAw7I_Kcy9x8SbExZJJeneekC8E5U70a7oqpW0=
h7mffedUGSX-pSb9kA7LCOH_sg/4bq/kEQStHXPR369e8SlRa1G8w/h47/h001.9Dz7m3aJ-uj_=
o36z3FhisqqeF1ELIW7ixcuhJrGXzrI" style=3D"font-weight: bold; text-decoratio=
n: underline; color: #FFFFFF; -webkit-text-size-adjust: none;">Change your =
home airport here.</a>
</td></tr>
<tr><td class=3D"pad-bottom-24" style=3D"font-family: 'Relative', Arial, sa=
ns-serif; font-size: 12px; color: #FFFFFF; line-height: 16px; padding-botto=
m: 16px; direction: ltr; -webkit-text-size-adjust: none;" align=3D"left">Re=
gistered=E2=80=8B Office:=E2=80=8B Skyscanner=E2=80=8B Limited,=E2=80=8B Le=
vel=E2=80=8B 5,=E2=80=8B Ilona=E2=80=8B Rose=E2=80=8B House,=E2=80=8B Manet=
te=E2=80=8B Street,=E2=80=8B London=E2=80=8B W1D=E2=80=8B 4AL,=E2=80=8B Uni=
ted=E2=80=8B Kingdom. UK Company Number: 04217916; VAT Registration Number:=
 GB 208148618</td></tr>
<tr><td style=3D"font-family: 'Relative', Arial, sans-serif; font-size: 12p=
x; line-height: 16px; direction: ltr; -webkit-text-size-adjust: none;" alig=
n=3D"left">
<a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.Z7kxosXrAU3mKizuS=
TS8eObHvtzyLUrTlrEU-Q-7woCWAxoeMJQzsnHMkGq5IxUcdO_hB5jzhoz_lnDhqIrU1biUVNaY=
PnwGWsPBNimRqXkPbTLA2gL-roFKOWebiycvPU5b-IAVPzM4vn2_BluHyZHkZFtrsiHKn64SZQb=
YEKjAKn218OcU7vY7uBoUDLiWobgMLmW-WYDxZCPDsmW0cXDoax0REOnysDGEDumQzOFWiLSZSA=
de86rKJbt7HX6LoyRsTZW-VYQgVEwq37y17ypPhgBpjqeC1KJFpkB3VtjcoSScNE6NruAqmM6Hf=
p_SimvIrTF2snsuAn3M8M5nCAfGhmlCPs2b2a7SOVwZxNAk51-nVTX-6U1OW0k21CBqVQ9GnEiG=
NdbI-qUhGJbuLFSIB-xf4tVMEu4d4oGS0THHyMMfMZi8MgNiJo9-vxeHKbhK5wOdOV2WmgRYB-4=
mT5olTH0BudX3z2Jq-5Z34q0d39rtV2xlEW2mmPvysculGHdLlUgdJi3Wl9yEYc5oEwWG7xbL_P=
Q5p3Ru4CqRSWAKfc3T5RRaxE5YNhhhLiUg4UPXRzlbiztZ_Jism4fPZePqwr1lC-RYEQzBocmDq=
H4avJWEYcuHP43Gfy-RCC_C8JStyk5B0XuTNiB4Nu8dKY7CucM0RJpLGsJBNs8Sl3IPDbklMvx0=
i8tEsfh2bDhnKewIceyoS8kRIgCRbHQrZppmKj4Ma_50YV8QVXOb45T9GSwx6MVIjjz7KTHDhsK=
qnQVkq8XzyIVMfa-HYJUEjtJyeszMvEzKsoVkcxlOXsBPUkfKLRBhbOyGxlHfQA8umoWzHGgmkl=
H7TLTO0WPCZ2U2Z9rwaO8XTiDXDSgJaxmsYNfYhHOeNsAXMOyTDqoD24eFsLTgvqKrbbNI-epsF=
lR5A_-2h0d3c3tOXSAy_sgVq9xEvDL7D5gLrwRlLKFcVaSXtVsnbfASahmHnn4lBu8OLVD-GIrY=
thDWxgJl1Td3L9RMtkc9zQiWM5sJGpVcAwIH-AQBagzACUcSn-J0pFMlLIDzM2SiTpkcbpHwQz0=
/4bq/kEQStHXPR369e8SlRa1G8w/h48/h001.iJqSevm_iI2MAVmvwTZezOz6V6izk6GzmkiaHc=
ZoZVg" style=3D"font-weight: bold; text-decoration: underline; color: #FFFF=
FF; -webkit-text-size-adjust: none;">Unsubscribe</a> <!--[if mso]>&nbsp;<![=
endif]--><img src=3D"https://cdn.braze.eu/appboy/communication/assets/image=
_assets/images/664b2d32b79a330062577e67/original.png?1716202802" width=3D"3=
" height=3D"9" alt=3D"" style=3D"outline: none; text-decoration: none; -ms-=
interpolation-mode: bicubic; border-style: none;"><!--[if mso]>&nbsp;<![end=
if]--> <a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.Z7kxosXrAU=
3mKizuSTS8eOk0XcVpAK7-85Rg86McO-PB7HcFFcPPfJqKYrl722zxfrZeDjUJLyoVfiFQXX2Zy=
_INqfh3e4j5WELSj_Q0_KSCLcPwKamYoOTvNJIne3uQbg85OhLCTnxPIgAYfINVGqCUDEC3gcna=
9w_cOiVysa281qATXVGGhwYkkWOWykUxTbtp_FvMs4EykwYLSLOLEjqVqgeag3iD1Xtr1KAYn49=
xICRiZGelzSVb_s5tu-lL-alZGs0d2vtmoE6uBD-OB4Nf5hbkM-v1Sb4KKM3WIb4/4bq/kEQStH=
XPR369e8SlRa1G8w/h49/h001.QrizqiLXDMBgYVR884T1VdTUdofJ9DqoWAxsxNV5P5Y" styl=
e=3D"font-weight: bold; text-decoration: underline; color: #FFFFFF; -webkit=
-text-size-adjust: none;">Edit My Preferences</a> <span class=3D"hide-mobil=
e"> <!--[if mso]>&nbsp;<![endif]--><img src=3D"https://cdn.braze.eu/appboy/=
communication/assets/image_assets/images/664b2d32b79a330062577e67/original.=
png?1716202802" width=3D"3" height=3D"9" alt=3D"" style=3D"outline: none; t=
ext-decoration: none; -ms-interpolation-mode: bicubic; border-style: none;"=
><!--[if mso]>&nbsp;<![endif]--> </span><!--[if !mso]><!--><span class=3D"s=
how-mobile" style=3D"display: none; max-height: 0; overflow: hidden;"></spa=
n><!--<![endif]--> <a href=3D"https://ablink.sender.skyscanner.com/ss/c/u00=
1.Z7kxosXrAU3mKizuSTS8eOk0XcVpAK7-85Rg86McO-OK5bs-0RRCE1V3xECGGoVNk3OXpk7_c=
3AcJEFZbwyFXnIpbwWh0gVyvQ9NQHsm-vEWuedp484VbmsvaJBuqEe1_LLOKSBdzMgjgHfTJ7T0=
xQgdY2XDmU4Th-0yoKN6EzAEsC5h6G8L2AQnvtp5So3c9NmDTjV2Ubd8TpLi7WzzLEgNcPeFmBf=
rzgVB6R6njQYDmlZJJp6QwA2QZ00jmVaX8CZrdJ6rPYAJGVA67T2Qnw/4bq/kEQStHXPR369e8S=
lRa1G8w/h50/h001.D03mX8eUSKFuD3AQYZSttWzw9DVbGSj-ueX2Ks5wtA4" style=3D"font=
-weight: bold; text-decoration: underline; color: #FFFFFF; -webkit-text-siz=
e-adjust: none;">Privacy Policy</a> <!--[if mso]>&nbsp;<![endif]--><img src=
=3D"https://cdn.braze.eu/appboy/communication/assets/image_assets/images/66=
4b2d32b79a330062577e67/original.png?1716202802" width=3D"3" height=3D"9" al=
t=3D"" style=3D"outline: none; text-decoration: none; -ms-interpolation-mod=
e: bicubic; border-style: none;"><!--[if mso]>&nbsp;<![endif]--> <a href=3D=
"https://ablink.sender.skyscanner.com/ss/c/u001.9ZjNoQbfk7t1QwcSf_gK7iztyIY=
g5iIHmPFrlYhyczDnwe9PPRqeQdpBjQac8MZeBOegnjpqAfqiiX1Zv5yWv7SbZsq7v7A6frWfCH=
b0VfixNEHYcZjJXCg3FsrRgCPr2lUlH9cdLC9refqJ-gI8YDzyoufRCHXn1Ue2KxW75q4102zIS=
jiWd9E2i89AnXdzBEtYaeIambD312RvkEoKnqEPQcmayPm9cE8tsqt_spsq5Zs9Ru7aKBrzOuFt=
iHnYqMiSYrn0NGmziM9tdlS_0xfkyXUtjZPFLZj1wyN9xQGxqd2wZTdQrZUMk4atA9GFF4QhbZc=
pWLMRIanHLoENdYn-J7X_Peih8k_VXuY0nAqTpJwjZzBFpIwsG5f8Y4pH/4bq/kEQStHXPR369e=
8SlRa1G8w/h51/h001.BANII-lzT3-dVNYq2xVo3aICVr8Sn1cjE4IrQMbsGio" style=3D"fo=
nt-weight: bold; text-decoration: underline; color: #FFFFFF; -webkit-text-s=
ize-adjust: none;">Contact us</a>
</td></tr>
<tr><td style=3D"padding-top: 24px; -webkit-text-size-adjust: none;"><table=
 role=3D"presentation" cellspacing=3D"0" border=3D"0" align=3D"left" width=
=3D"100%" style=3D"float: left; mso-table-lspace: 0pt; mso-table-rspace: 0p=
t; border-width: 0;"><tr>
<td class=3D"brandsubtitle3 pad-top-8" style=3D"direction: ltr; -webkit-tex=
t-size-adjust: none; padding: 12px 24px 0 0;" align=3D"left"><a href=3D"htt=
ps://ablink.sender.skyscanner.com/ss/c/u001.Z7kxosXrAU3mKizuSTS8eObHvtzyLUr=
TlrEU-Q-7woCC81BeScUCRq0E-9qYJwF3davNJq6EdHgygFWljbiHkr8aQK56xZ4MapqhsPxYhc=
St9OgChlHOdxUkb25MNC2dNeyqMiIm6RqROrT2C6-B2LIs48W_M5az5k4YAIV2P8AXBhlTIWQES=
7yHHh0Bg633dThTrf0GPgWX43mefbINuKXH-w-cIjtf3BfbrwjwfkOT9VnwsEMHS9nFkdVeEGXO=
jN1IPV-p022B8oZO-D62gw/4bq/kEQStHXPR369e8SlRa1G8w/h52/h001.mF1gRAakZakNNQdf=
vJWTXCES0VO9hyk09mXYq1-i7Eg" style=3D"font-family: 'Relative Black', Arial,=
 sans-serif; font-size: 20px; line-height: 21px; font-weight: bold; letter-=
spacing: -1px; color: #FFFFFF; text-decoration: none; -webkit-text-size-adj=
ust: none;">Global Partner of the 2024 Solheim Cup</a></td>
<td width=3D"59" style=3D"font-size: 0; -webkit-text-size-adjust: none;" al=
ign=3D"right"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.Z7k=
xosXrAU3mKizuSTS8eObHvtzyLUrTlrEU-Q-7woCC81BeScUCRq0E-9qYJwF3davNJq6EdHgygF=
WljbiHkr8aQK56xZ4MapqhsPxYhcTQl14qQR-ylnb3J8JOwBFIXpMz4Ntcimk73Er7B11ypQsRj=
3rHI3ETwqhZIt2a1b_fsJc0uQhy2atuARnWsb4IHMxJ2i7-jyD7_J5MxwJ8_NOch3eW0RnC3MTQ=
F5NoXlP2A3xJm3UNLUjf8GEhcJ7YGaQrjWzpYCG4q_Ov8VfrKg/4bq/kEQStHXPR369e8SlRa1G=
8w/h53/h001.5x7HvcGMuvpLsueF3ev9j3YsCw_KSqc63WJPNVAPgTA" style=3D"font-size=
: 0; -webkit-text-size-adjust: none; color: #776f6b;"><img src=3D"https://c=
dn.braze.eu/appboy/communication/assets/image_assets/images/665984e50aa2370=
062ce6538/original.png?1717142756" width=3D"59" height=3D"75" alt=3D"Solhei=
m Cup 2024" style=3D"outline: none; text-decoration: none; -ms-interpolatio=
n-mode: bicubic; border-style: none;"></a></td>
<td width=3D"95" style=3D"font-size: 0; -webkit-text-size-adjust: none;" al=
ign=3D"right"><a href=3D"https://ablink.sender.skyscanner.com/ss/c/u001.xvx=
eTnj4EG7fcfOeGkr_SGeU0G0pNi9kGehVAkufacXuWZrUkiO7rmuzG6vh8SAiZu9o_NqbeMmbie=
yUnEjt2tsPkjPwsbnrOkTFFOWQe8mZPLAtWtKxwXfCTnpC9Rmxcdnffx8UUR56L98uWz64Z5UTq=
uBZKUMT1vh3Sb8qpmt1OrIQ6Un31EQhaOIcYvK4MC92kifY7ZEcuwoMFUYBtMUOgh2MwVNXw082=
zIA1RiOo0dfzYZxZUP4KstLQXS4n5k_nDg7WbO9J1PP3QHAhsEpAq2bi4hUjZLgVjyCzDt5aE0z=
YksqGVRFiAFKNHUkL/4bq/kEQStHXPR369e8SlRa1G8w/h54/h001.KwLgZtSWgdiKAxxejzqhl=
M_mYFYOBP-0k80sfIvX83E" style=3D"font-size: 0; -webkit-text-size-adjust: no=
ne; color: #776f6b;"><img src=3D"https://cdn.braze.eu/appboy/communication/=
assets/image_assets/images/665984e519054a006216ee35/original.png?1717142756=
" width=3D"95" height=3D"75" alt=3D"Skyscanner" style=3D"outline: none; tex=
t-decoration: none; -ms-interpolation-mode: bicubic; border-style: none;"><=
/a></td>
</tr></table></td></tr>
</table></td></tr>
</table>
</td>
</tr>
</table>

       =20
     =20
   =20
  </body>
</html>

--b8d57104611303067edaf6209d6b906a770ffda77ae6998548cc1a7a6ae0--
"""

# def main():
#     print(extract_email_content(raw))
#     # extract_email_content(raw)

# if __name__ == "__main__":
#     main()

