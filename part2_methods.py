# Laborator: funcții, metode și importuri pe web
# Student: Roata Mihail

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# ---------- Exercițiul 9 ----------
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex9 status_code:", response.status_code)  # atribut
print("Ex9 ok:", response.ok)                    # atribut
print("Ex9 url:", response.url)                  # atribut
print("Ex9 encoding:", response.encoding)        # atribut
time.sleep(1)

# ---------- Exercițiul 10 ----------
response.raise_for_status()  # metodă: nu face nimic dacă totul e în regulă
print("Ex10: pagina principală e în regulă")
time.sleep(1)

try:
    r404 = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    r404.raise_for_status()
    print("Ex10: serverul a răspuns fără eroare:", r404.status_code)
except requests.HTTPError as e:
    print("Ex10: pagina nu există (cod", e.response.status_code, ")")
time.sleep(1)

# ---------- Exercițiul 11 ----------
print("Ex11: antetele răspunsului")
for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")

# ---------- Exercițiul 12 ----------
print("Ex12 Server:", response.headers.get("Server", "lipsește"))
print("Ex12 Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("Ex12 content-type (litere mici):", response.headers.get("content-type", "lipsește"))
# Observație: obții aceeași valoare. Numele antetelor nu țin cont de
# majuscule/minuscule (response.headers nu e un dicționar obișnuit).

# ---------- Exercițiul 13 ----------
numar = response.text.lower().count("cyber")
print("Ex13: 'cyber' apare de", numar, "ori")
# Fiecare metodă returnează un șir nou (str), iar pe un șir poți apela
# din nou metode de șir, deci .lower() și .count() se pot înlănțui.

# ---------- Exercițiul 14 ----------
html = response.text
start = html.find("<title>") + len("<title>")
sfarsit = html.find("</title>")
titlu = html[start:sfarsit].strip()
print("Ex14 titlu:", titlu)

# ---------- Exercițiul 15 ----------
lines = html.splitlines()
print("Ex15 număr de linii:", len(lines))
print("Ex15 cea mai lungă linie:", len(max(lines, key=len)), "caractere")

# ---------- Exercițiul 16 ----------
if response.url.startswith("https://"):
    print("Ex16: Conexiune securizată")
else:
    print("Ex16: Conexiune nesecurizată")
time.sleep(1)

# ---------- Exercițiul 17 ----------
r_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
print("Ex17: redirecționări:")
for pas in r_http.history:
    print("  ", pas.status_code, pas.url)
print("Ex17 URL final:", r_http.url)
time.sleep(1)

# ---------- Exercițiul 18 ----------
r_head = requests.head(BASE_URL, timeout=TIMEOUT)
time.sleep(1)
r_get = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex18 HEAD:", len(r_head.content), "octeți")
print("Ex18 GET:", len(r_get.content), "octeți")
# HEAD cere doar antetele, fără corp, deci content e gol (0 octeți).
# GET returnează și corpul paginii (HTML-ul).
time.sleep(1)

# ---------- Exercițiul 19 ----------
print("Ex19:")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print(cookie.name, cookie.secure)

# ---------- Exercițiul 20 ----------
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Roata_Mihail"})
r_echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Ex20:", r_echo.json()["headers"]["User-Agent"])

#Verificați-vă:response.text e atribut (valoare deja calculată), response.json() e metodă 
#(face o acțiune, interpretează corpul ca JSON, și poate da eroare dacă nu e JSON valid).