import re


#Partea A1

s = "Salut"
b = s.encode("utf-8")
print(b, b[0])
h = b.hex()
print(h)
b2 = bytes.fromhex(h)
print(b2)


#Partea A2
import base64
def ghici_strat(s):
    
    if re.search(r"%[0-9a-fA-F]{2}", s):
       return "url"
    
    elif re.fullmatch(r"[0-9a-f]+", s) and len(s) % 2 == 0:
        return "hex"
    
    elif re.fullmatch(r"[A-Za-z0-9+/=]+", s) and len(s) % 4 == 0:
        return "base64"

    else: 
        return "necunoscut"
    
print(ghici_strat("%2Fetc"))   # url 
print(ghici_strat("48656c6c6f"))  # hex
print(ghici_strat("U2FsdXQ=")) # base64
print(ghici_strat("Salut"))  # necunoscut


#Partea A3
from urllib.parse import unquote 

def desfa(s): 
    
    strat = ghici_strat(s) 

    if strat == "base64":
        rezultat = base64.b64decode(s)

    elif strat == "hex":
        rezultat = bytes.fromhex(s)
        
    elif strat == "url":
        rezultat = unquote(s).encode()

    else:
        strat = "necunoscut"
        rezultat = s.encode()         

    return strat, rezultat

print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%2Fetc"))
print(desfa("Salut"))


#Partea A4
def citibil(b): 
 
    return all(32 <= c < 127 for c in b) 

  

val = open("probe/mesaj.txt").read().strip()

for _ in range(8): 

    strat, b = desfa(val) 
    print(strat)

    if strat == "necunoscut":
        print(b.decode())
        break
    else:
        val = b.decode() 


#Partea A5
date = open("probe/xor.bin", "rb").read() 

for k in range(256): 

    clar = bytes(b ^ k for b in date) 

    if citibil(clar): 
        print("cheie:", k, clar.decode()) 


#Partea A6
import hashlib 

tinta = open("probe/hashuri.txt").readline().strip() 

print(len(tinta))   # 32 md5 / 40 sha1 / 64 sha256 


for tinta in open("probe/hashuri.txt"):
    tinta = tinta.strip()

    if len(tinta) == 32:
        alg = "md5"
    elif len(tinta) == 40:
        alg = "sha1"
    else:
        alg = "sha256"

    for cuv in open("probe/wordlist.txt", encoding="latin1"): 

        cuv = cuv.strip() 

        if hashlib.new(alg, cuv.encode()).hexdigest() == tinta: print(alg, "gasit:", cuv); break 
    

#Partea A7    
import argparse, json

if __name__ == "__main__":

    p = argparse.ArgumentParser() 

    p.add_argument("intrare")    

    p.add_argument("--fisier", action="store_true") 

    a = p.parse_args() 
 
    if a.fisier:
        text = open(a.intrare, "rb").read().decode().strip()  
    else:
        text = a.intrare

    strat, rezultat = desfa(text)

    print(strat, rezultat)

    fisa = {"strat": strat, "rezultat": rezultat.decode()}

    with open("arsenal/forensics/fisa.json", "w") as f:
        json.dump(fisa, f)
