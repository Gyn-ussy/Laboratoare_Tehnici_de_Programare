# Laborator: funcții, metode și importuri pe web
# Student: Roata Mihail

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


# ---------- Exercițiul 21 ----------
def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Descarcă url cu GET și returnează obiectul răspuns."""
    return requests.get(url, timeout=timeout)


r = fetch(BASE_URL)
print("Ex21:", r.status_code)
time.sleep(1)


# ---------- Exercițiul 22 (+ adnotări de la 26) ----------
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


for cale in ["/", "/robots.txt", "/sitemap.xml"]:
    print("Ex22:", cale, get_status(BASE_URL + cale))
    time.sleep(1)


# ---------- Exercițiul 23 ----------
# Parametrul timeout are acum valoarea implicită 10 (vezi def fetch de mai sus).
r = fetch(BASE_URL)               # folosește valoarea implicită: timeout=10
print("Ex23 (implicit, timeout=10):", r.status_code)
time.sleep(1)

r = fetch(BASE_URL, timeout=3)    # suprascrie valoarea implicită
print("Ex23 (timeout=3):", r.status_code)
time.sleep(1)


# ---------- Exercițiile 24 și 25 ----------
def get_title(html: str) -> str:
    """Returnează textul dintre <title> și </title> dintr-un șir HTML.

    Funcția nu face operații de rețea; primește doar textul HTML.
    """
    start = html.find("<title>") + len("<title>")
    sfarsit = html.find("</title>")
    return html[start:sfarsit].strip()


print("Ex24 titlu:", get_title(fetch(BASE_URL).text))
help(get_title)
time.sleep(1)


# ---------- Exercițiul 26 ----------
try:
    get_status(123)
except requests.RequestException as e:
    print("Ex26: get_status(123) a dat eroare:", type(e).__name__)
# Adnotările de tip nu opresc apelul cu un tip greșit: Python nu le verifică
# la rulare. Eroarea vine din requests, nu din adnotare.


# ---------- Exercițiul 27 ----------
def page_exists(url: str) -> bool:
    """Returnează True dacă url răspunde fără eroare, altfel False."""
    try:
        return fetch(url).status_code < 400
    except requests.RequestException:
        return False


print("Ex27 (valid):", page_exists(BASE_URL))
print("Ex27 (inexistent):", page_exists("https://this-domain-does-not-exist.invalid"))
time.sleep(1)


# ---------- Exercițiul 28 ----------
def check_paths(base: str, paths: list) -> dict:
    """Returnează {cale: cod_de_stare} pentru fiecare cale din listă."""
    rezultate = {}
    for cale in paths:
        rezultate[cale] = get_status(base + cale)
        time.sleep(1)
    return rezultate


print("Ex28:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))


# ---------- Exercițiul 29 ----------
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea antetului name din răspunsul la url."""
    return fetch(url).headers.get(name, default)


print("Ex29:", get_header(BASE_URL, name="Server"))
time.sleep(1)


# ---------- Exercițiul 30 ----------
def security_headers(url: str) -> dict:
    """Returnează {antet: True/False} pentru cinci antete de securitate."""
    de_verificat = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    antete = fetch(url).headers
    return {nume: nume in antete for nume in de_verificat}


rezultat = security_headers(BASE_URL)
print("Ex30:", rezultat)
time.sleep(1)


# ---------- Exercițiul 31 ----------
def score_headers(results: dict) -> str:
    """Primește dicționarul din security_headers și returnează ex. '3/5'."""
    return f"{sum(results.values())}/{len(results)}"


print("Ex31:", score_headers(rezultat))


# ---------- Exercițiul 32 ----------
def fetch_robots(base: str):
    """Returnează textul /robots.txt sau None dacă fișierul lipsește."""
    try:
        r = fetch(base + "/robots.txt")
    except requests.RequestException:
        return None
    return r.text if r.status_code == 200 else None


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow: (listă goală pentru None)."""
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cai.append(linie.split(":", 1)[1].strip())
    return cai


time.sleep(1)
print("Ex32:", disallowed_paths(fetch_robots(BASE_URL)))
print("Ex32 (None):", disallowed_paths(None))
time.sleep(1)


# ---------- Exercițiul 33 ----------
def response_times(*urls: str) -> dict:
    """Returnează {url: secunde} pentru fiecare url primit."""
    timpi = {}
    for url in urls:
        start = time.perf_counter()
        fetch(url)
        timpi[url] = time.perf_counter() - start
        time.sleep(1)
    return timpi


print("Ex33:", response_times(BASE_URL, BASE_URL + "/robots.txt"))


# ---------- Exercițiul 34 ----------
def log(message: str, **details) -> None:
    """Afișează mesajul urmat de fiecare detaliu, separate prin ' | '."""
    bucati = [message] + [f"{k}={v}" for k, v in details.items()]
    print(" | ".join(bucati))


log("verificat", url=BASE_URL, status=200)

#Verificați-vă:print() doar afișează valoarea pe ecran și se pierde, funcția nu o dă mai departe.
#return trimite valoarea înapoi celui care a apelat funcția,
#ca să o poată salva într-o variabilă sau folosi în alt calcul (de exemplu score_headers(security_headers(BASE_URL))).