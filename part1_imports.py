# Laborator: funcții, metode și importuri pe web
# Student: Roata Mihail

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

import time

# ---------- Exercițiul 1 ----------
import requests
import urllib.request

print("Versiunea requests:", requests.__version__)
# requests este un modul extern (scris de alții, nu vine cu Python), de aceea
# trebuie descărcat cu pip install. urllib face parte din biblioteca standard,
# deci este instalat odată cu Python.

# ---------- Exercițiul 2 ----------
r = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex2 (import requests):", r.status_code)
time.sleep(1)

from requests import get
r = get(BASE_URL, timeout=TIMEOUT)
print("Ex2 (from requests import get):", r.status_code)
time.sleep(1)
# import requests: se vede mereu de unde vine funcția (requests.get) și nu
#   apar conflicte de nume.
# from requests import get: codul e mai scurt, scrii direct get(...).

# ---------- Exercițiul 3 ----------
import requests as rq

r = rq.get(BASE_URL, timeout=TIMEOUT)
print("Ex3 (alias):", r.status_code)
time.sleep(1)
# Un alias ajută când numele modulului e lung și îl folosești des
# (ex. import numpy as np). Îl face mai greu de citit când alias-ul e
# obscur sau neobișnuit (ex. rq), pentru că cititorul trebuie să ghicească
# la ce modul se referă.

# ---------- Exercițiul 4 ----------
import urllib.error

try:
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as resp:
        print("Ex4 status:", resp.status)
        corp = resp.read().decode("utf-8")
        print(corp[:200])
except urllib.error.HTTPError as e:
    print("Ex4: serverul a răspuns cu", e.code, e.reason)
    # Serverul respinge clientul implicit urllib (403), deși requests merge.
time.sleep(1)

# ---------- Exercițiul 5 ----------
print(dir(requests))
# get        -> funcție (requests.get)
# Session    -> clasă (requests.Session)
# exceptions -> modul (requests.exceptions)


# ---------- Exercițiul 6 ----------
help(requests.get)
# În documentație apar parametrii prin **kwargs; parametrul pentru timpul
# maxim de așteptare este timeout.
r = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex6:", r.status_code)
time.sleep(1)

# ---------- Exercițiul 7 ----------
start = time.perf_counter()
r = requests.get(BASE_URL, timeout=TIMEOUT)
durata = time.perf_counter() - start
print("Ex 7: perf_counter:", durata, "secunde")
print("Ex 7: response.elapsed:", r.elapsed.total_seconds(), "secunde")
# perf_counter măsoară tot timpul scurs în programul tău, inclusiv pregătirea
# cererii. response.elapsed măsoară doar timpul de la trimiterea cererii
# până la primirea antetelor răspunsului, deci e de obicei puțin mai mic.

# ---------- Exercițiul 8 ----------
try:
    import bs4
    print("Ex 8: bs4 este instalat")
except ImportError:
    print("Ex 8: Instalați modulul cu: pip install beautifulsoup4")

#Verificați-vă:Modul: un fișier .py cu cod (ex. time).
#Pachet: un director cu mai multe module (ex. urllib).
#Bibliotecă: termen general pentru o colecție de cod gata făcut,
#formată din unul sau mai multe module/pachete (ex. requests).