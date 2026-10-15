#Laborator 5: Forensics si steganografie

**Student:** Roata Mihail    **Grupa:** Si-266

Lucrarea A:

Mesajul cu straturi  (probe/mesaj.txt)
Decoderul recunoaste stratul dupa forma (URL, hex sau base64) si il desface intr-o bucla. pana cand sirul nu mai seamana cu nicio codare. Mesajul din 'mesaj.txt' avea trei straturi, in ordinea: base64 -> base64 -> hex.
Mesajul final: 'Flag{straturi_de_encoding}'.
 
XOR cu cheie de un octet (probe/xor.bin)
0 cheie de un octet are doar 256 de valori, deci le-am incercat pe toate si am pastrat reultatele cu octeti imprimabili. Mai multe chei dau text ilizibil, iar cea corecta este **128**, cu textul clar care contine 'FLAG{xor_un_octet}'.

Hash-uri sparte (probe/hashuri.txt)
Hash-urile au 32 de caractere, deci sunt md5. Un hash nu se decripteaza: am hashuit foecare cuvant din wordlist si am comparat cu tinta. Parolele gasite: 'password', 'dragon', 'qwerty', 'letmein', 'monkey'.


Lucrarea B:

Tipul real al fisierelor
'foto.jpg' - jpeg incepe cu 'ff d8'
'ascuns.png' - png incepe cu '89 50 4e 47'
'xor.bin' - fara semnatura cunoscuta, date brute: 'd5eea0f3e9eee7f5'

Text ascuns intr-un binar
In 'ascuns.png', 'strings' a scos printre octetii aleatoare numele 'comoara.txt', un indiciu ca in fisier e ascuns altceva.

Model 'iPhone 13', DateTime '2026:09:14 10:30:00', GPSInfo = {1: 'N', 2: (47.0, 1.0, 0.0), 3: 'E', 4: (28.0, 51.0, 27.0)}, toate astea ne arata ce dispozitiv s-a folosit, cand si coordonatele aproximative alea pozei. Coordonatele permit plasarea pozei pe harta (OSINT), de aceea EXIF-ul se sterge inainte de a publica o poza.

Am scris mesajul 'FLAG{ascuns_in_pixeli}' in ultimul bit al canalelor r, g, b ale pixelilor, cate un bit per canal, cu un octet 0 la final ca marca de sfarsit. Poza arata la fel cu originalul. Am salvat in 'stego.png'. La dezvaluire am citit in aceeasi ordine ultimii biti, i-am grupat cate 8 si am convertit in text pana la primul octet 0, Mesajul dezavaluit: 'FLAG{ascuns_in_pixeli}'.