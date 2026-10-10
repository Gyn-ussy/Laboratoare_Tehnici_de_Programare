# Laborator: funcții, metode și importuri pe web
# Student: Roata Mihail

import time
import re
import json
import socket
import ssl
import hashlib
import requests
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Descărcăm pagina principală o singură dată și o refolosim mai jos
response = requests.get(BASE_URL, timeout=TIMEOUT)
html = response.text
time.sleep(1)


# ---------- Exercițiul 35 ----------
def parse_url(url: str) -> None:
    """Afișează părțile unui URL."""
    p = urlparse(url)
    print("Ex35 scheme:", p.scheme)
    print("Ex35 netloc:", p.netloc)
    print("Ex35 path:", p.path)
    print("Ex35 query:", p.query)
    print("Ex35 fragment:", p.fragment)


parse_url("https://cybercor.org/path?x=1#top")


# ---------- Exercițiul 36 ----------
for legatura in ["/about", "contact.html", "../index.html"]:
    print("Ex36:", legatura, "->", urljoin(BASE_URL, legatura))


# ---------- Exercițiul 37 ----------
def extract_links(html: str) -> list:
    """Returnează legăturile href din html, fără duplicate (păstrează ordinea)."""
    legaturi = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(legaturi))


links = extract_links(html)
print("Ex37:", links)


# ---------- Exercițiul 38 ----------
def split_links(links: list, domain: str) -> tuple:
    """Returnează (interne, externe) față de domeniul dat."""
    interne, externe = [], []
    for link in links:
        complet = urljoin("https://" + domain, link)
        if urlparse(complet).netloc == domain:
            interne.append(link)
        else:
            externe.append(link)
    return interne, externe


interne, externe = split_links(links, "cybercor.org")
print("Ex38 interne:", interne)
print("Ex38 externe:", externe)


# ---------- Exercițiul 39 ----------
class ImageFinder(HTMLParser):
    """Colectează atributul src al fiecărui tag <img>."""

    def __init__(self):
        """Inițializează parserul și lista goală de imagini."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Apelată automat de parser la fiecare tag de deschidere.

        Dacă tagul este <img> și are atributul src, îl adaugă în listă.
        """
        if tag == "img":
            src = dict(attrs).get("src")
            if src is not None:
                self.images.append(src)


test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""

finder = ImageFinder()
finder.feed(test_html)
print(finder.images)

assert finder.images == [
    "/logo.png",                            # imagine obișnuită
    "poza.jpg",                             # tag scris cu majuscule
    "https://cdn.example.com/banner.webp",  # tag care se închide singur
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut!")

# Rulăm parserul pe pagina reală
finder = ImageFinder()
finder.feed(html)
print(len(finder.images), "imagini găsite")
for src in finder.images:
    print(src)
print("Ex39 <img în text:", html.lower().count("<img"))


# ---------- Exercițiul 40 ----------
def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 a conținutului paginii."""
    r = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(r.content).hexdigest()


f1 = page_fingerprint(BASE_URL)
time.sleep(1)
f2 = page_fingerprint(BASE_URL)
print("Ex40:", f1)
print("Ex40:", f2)
print("Ex40 identice:", f1 == f2)
# Ar fi diferite dacă s-ar schimba conținutul paginii (text nou, dată,
# reclame, valori generate la fiecare cerere). Orice schimbare, chiar de un
# singur caracter, dă o amprentă complet diferită.
time.sleep(1)


# ---------- Exercițiul 41 ----------
with open("headers.json", "w", encoding="utf-8") as fisier:
    json.dump(dict(response.headers), fisier, indent=2)

with open("headers.json", "r", encoding="utf-8") as fisier:
    incarcate = json.load(fisier)
print("Ex41 Server:", incarcate.get("Server", "lipsește"))


# ---------- Exercițiul 42 ----------
def resolve(hostname: str) -> str:
    """Returnează adresa IP a unui nume de domeniu."""
    return socket.gethostbyname(hostname)


print("Ex42:", resolve("cybercor.org"))


# ---------- Exercițiul 43 ----------
def cert_days_left(hostname: str) -> int:
    """Returnează câte zile mai sunt până expiră certificatul."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(cert["notAfter"])
    return int((expira - time.time()) // 86400)


print("Ex43: zile rămase:", cert_days_left("cybercor.org"))

#Verificați-vă: handle_starttag() este apelată de parser, nu de tine.
#Când rulezi finder.feed(html), HTMLParser citește textul și, de fiecare
#dată când întâlnește un tag de deschidere, apelează singur metoda ta cu
#numele tag-ului și lista de atribute. Tu doar o suprascrii 
#(ca să spui ce să se întâmple), iar parserul decide când o apelează.