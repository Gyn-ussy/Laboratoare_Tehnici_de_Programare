# Laborator: funcții, metode și importuri pe web
# Student: Roata Mihail

import json
import re
import socket
import ssl
import time
import requests
from urllib.parse import urlparse, urljoin

BASE_URL = "https://cybercor.org"
TIMEOUT = 10  # secunde

# Ex. 47: constantă de modul, folosită în fetch()
DEFAULT_HEADERS = {"User-Agent": "WebLab-Roata_Mihail"}


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă url cu GET și returnează obiectul răspuns."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Returnează textul dintre <title> și </title>."""
    start = html.find("<title>") + len("<title>")
    sfarsit = html.find("</title>")
    return html[start:sfarsit].strip()


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


def score_headers(results: dict) -> str:
    """Primește dicționarul din security_headers și returnează ex. '3/5'."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Returnează {cale: cod_de_stare} pentru fiecare cale din listă."""
    rezultate = {}
    for cale in paths:
        rezultate[cale] = get_status(base + cale)
        time.sleep(1)
    return rezultate


def resolve(hostname: str) -> str:
    """Returnează adresa IP a unui nume de domeniu."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează câte zile mai sunt până expiră certificatul."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    expira = ssl.cert_time_to_seconds(cert["notAfter"])
    return int((expira - time.time()) // 86400)


def extract_links(html: str) -> list:
    """Returnează legăturile href din html, fără duplicate."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


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


def fetch_robots(base: str):
    """Returnează textul /robots.txt sau None dacă fișierul lipsește."""
    try:
        r = fetch(base.rstrip("/") + "/robots.txt")
    except requests.RequestException:
        return None
    # Site-ul răspunde 200 și pentru pagini inexistente (returnează HTML),
    # așa că ignorăm răspunsurile HTML.
    if r.status_code != 200 or "html" in r.headers.get("Content-Type", ""):
        return None
    return r.text


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow: (listă goală pentru None)."""
    if robots_text is None:
        return []
    cai = []
    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cai.append(linie.split(":", 1)[1].strip())
    return cai


def redirect_chain(url: str) -> list:
    """Pornește de la http:// și returnează lista 'cod -> destinație'."""
    http_url = "http://" + urlparse(url).netloc + "/"
    r = fetch(http_url)
    pasi = []
    for i, pas in enumerate(r.history):
        if i + 1 < len(r.history):
            destinatie = r.history[i + 1].url
        else:
            destinatie = r.url
        pasi.append(f"{pas.status_code} -> {destinatie}")
    return pasi


def site_report(url: str, save_to: str = "report.json") -> dict:
    """Colectează informații despre site, le afișează și le salvează în JSON."""
    host = urlparse(url).netloc

    r = fetch(url)
    time.sleep(1)
    lanț = redirect_chain(url)
    time.sleep(1)
    scor = score_headers(security_headers(url))
    time.sleep(1)
    robots = disallowed_paths(fetch_robots(url))

    interne, externe = split_links(extract_links(r.text), host)

    raport = {
        "url": url,
        "status": r.status_code,
        "final_url": r.url,
        "title": get_title(r.text),
        "ip": resolve(host),
        "redirects": lanț,
        "security_score": scor,
        "cert_days_left": cert_days_left(host),
        "internal_links": len(interne),
        "external_links": len(externe),
        "disallowed_paths": robots,
    }

    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {raport['status']} (URL final: {raport['final_url']})")
    print(f"Titlu:             {raport['title']}")
    print(f"Adresă IP:         {raport['ip']}")
    print(f"Redirecționări:    {', '.join(lanț) if lanț else 'niciuna'}")
    print(f"Scor securitate:   {scor}")
    print(f"Certificat:        {raport['cert_days_left']} de zile rămase")
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    print(f"Căi interzise:     {', '.join(robots) if robots else 'niciuna'}")

    with open(save_to, "w", encoding="utf-8") as fisier:
        json.dump(raport, fisier, indent=2, ensure_ascii=False)
    print(f"Salvat în {save_to}")
    return raport


# Ex. 46: autotestul rulează doar la "py webtools.py". Când fișierul e pornit
# direct, Python setează __name__ la "__main__", deci condiția e adevărată.
# Când main.py face "import webtools", __name__ devine "webtools", deci
# condiția e falsă și autotestul nu se execută.
if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))