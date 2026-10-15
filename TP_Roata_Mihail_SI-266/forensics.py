#Partea B1

def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):     
        return "png"
    elif cap.startswith(b"\xff\xd8"):     
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):     
        return "zip/docx"
    return cap.hex()

print(tip_real("probe/foto.jpg"))
print(tip_real("probe/ascuns.png"))
print(tip_real("probe/xor.bin"))


#Partea B2

import re

date = open("probe/ascuns.png", "rb").read()
for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())


#Partea B3

from PIL import Image
from PIL.ExifTags import TAGS

exif = Image.open("probe/foto.jpg")._getexif() or {}
for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif[34853]
print(gps)

lat = gps[2]
lon = gps[4]

latitudine = lat[0] + lat[1] / 60 + lat[2] / 3600
longitudine = lon[0] + lon[1] / 60 + lon[2] / 3600

if gps[1] == "S":
    latitudine = -latitudine
if gps[3] == "W":
    longitudine = -longitudine

print(latitudine, longitudine)


#Part B4

date = open("probe/ascuns.png", "rb").read()
i = date.find(b"PK\x03\x04")

if i != -1:
    open("gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i)


#Part B5

from PIL import Image 

img = Image.open("probe/foto.jpg").convert("RGB") 

px = list(img.getdata()) 

mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"

biti = "".join(f"{x:08b}" for x in mesaj) 

if len(biti) > len(px) * 3:
    print("poza e prea mica")
    raise SystemExit
px_nou = [list(p) for p in px]

for i, bit in enumerate(biti):
    pixel = i // 3
    canal = i % 3
    px_nou[pixel][canal] = (px_nou[pixel][canal] & ~1) | int (bit)

px_nou = [tuple(p) for p in px_nou]

img.putdata(px_nou)
img.save("stego.png") 


#Partea 6

px = list(Image.open("stego.png").convert("RGB").getdata())

biti = ""
for (r, g, b) in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)

mesaj = ""
for i in range(0, len(biti), 8):
    grup = biti[i:i + 8]
    if len(grup) < 8:
        break
    octet = int(grup, 2)
    if octet == 0:
        break
    mesaj += chr(octet)

print(mesaj)