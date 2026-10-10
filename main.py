# Laborator: funcții, metode și importuri pe web
# Student: Roata Mihail

import argparse
import csv
import time
from datetime import datetime

import webtools                                   # Ex. 44
from webtools import get_title, security_headers  # Ex. 45
from webtools import DEFAULT_HEADERS, check_paths, fetch, site_report

# Ex. 48: URL-ul vine din linia de comandă
parser = argparse.ArgumentParser(description="Raport despre un site web")
parser.add_argument("url", nargs="?", default="https://cybercor.org",
                    help="adresa site-ului (ex. https://cybercor.org)")
args = parser.parse_args()
url = args.url.rstrip("/")

# Ex. 44
print("Ex44:", webtools.get_title(webtools.fetch(url).text))
time.sleep(1)

# Ex. 45
# Dacă main.py ar avea și o funcție proprie get_title, ar rămâne valabilă
# cea definită sau importată mai târziu în fișier; cea mai nouă o înlocuiește
# pe cealaltă, iar funcția din webtools nu ar mai putea fi apelată prin
# numele get_title.
print("Ex45:", get_title(fetch(url).text))
time.sleep(1)
print("Ex45:", security_headers(url))
time.sleep(1)

# Ex. 47
print("Ex47:", DEFAULT_HEADERS)

# Ex. 49
rezultate = check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
with open("report.csv", "w", newline="", encoding="utf-8") as fisier:
    scriitor = csv.writer(fisier)
    scriitor.writerow(["path", "status", "checked_at"])
    for cale, status in rezultate.items():
        scriitor.writerow([cale, status, datetime.now().isoformat()])
print("Ex49: salvat în report.csv")
time.sleep(1)

# Ex. 50
site_report(url)