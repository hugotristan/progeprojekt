################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt Tuto
# Teema: Keskendumise hindaja
#
#
# Autorid: Hugo Tristan Tammik, Mattias Rahnu
#
# mõningane eeskuju: Algseks inspiratsiooniks võetud kirjelduses mainitud face_recognition. 
#
# Lisakommentaar: Vaja installida watchdog teek (windowsi klahv, otsingusse cmd ning py -m pip install watchdog või lihtsalt pip install watchdog)
#
##################################################

import os
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# Vaja installida watchdog teek, py -m pip install watchdog

# Muutujad, mis jälgivad programmi olekut ja efektiivsust
lõpeta_programm = False   # Näitab, kas programm peaks lõpetama
tsüklid = 0               # Tsüklite arv (iga 5 minuti järel tehtav kontroll)
kasulikud_tsüklid = 0     # Kasulike tsüklite arv, kus faili muudeti

# Klass, mis jälgib faili muutusi
class FailiJälgija(FileSystemEventHandler):
    # Funktsioon, mis käivitub, kui failis toimub muudatus
    def on_modified(self, event):
        global kasulikud_tsüklid
        # Kontrollib, kas muudetud fail on see, mida jälgime
        if event.src_path == faili_asukoht:
            print("Faili muudatus tuvastatud!")  # Teade, et faili on muudetud
            kasulikud_tsüklid += 1              # Suurendab kasulike tsüklite arvu

# Peamine funktsioon, mis juhib programmi
def main():
    global lõpeta_programm, tsüklid, kasulikud_tsüklid, faili_asukoht
    
    # Küsib kasutajalt, kas tal on märkmete tegemiseks fail
    vastus = input("Tervist! Kas teil on arvutis märkmete tegemiseks fail? (jah/ei): ").strip().lower()
    
    # Kontrollib, kas vastus oli "jah"
    if vastus == "jah":
        # Küsib kasutajalt faili täispikka asukohta
        faili_asukoht = input("Palun sisestage oma märkmete faili täielik asukoht: ").strip()
        
        # Kontrollib, kas fail asub antud asukohas
        if not os.path.isfile(faili_asukoht):
            print("Antud faili ei eksisteeri. Programm lõpetab töö.")
            return  # Kui faili ei leita, lõpetab programmi

        # Teavitab kasutajat, et faili jälgimist alustatakse iga 5 minuti järel
        print("Alustatakse teie faili kontrollimist iga 5 minuti järel.")
        print("Programmi peatamiseks ükskõik, mis ajahetkel vajutage Ctrl + C.")

        # Loob failijälgija objekti ja jälgija (observer)
        event_handler = FailiJälgija()
        observer = Observer()
        # Seob failijälgija jälgitava failiga (ei ole rekursiivne, jälgib ainult kindlat faili)
        observer.schedule(event_handler, path=os.path.dirname(faili_asukoht), recursive=False)
        observer.start()  # Alustab faili jälgimist

        try:
            # Tsükliline kontroll, mis toimub iga 5 minuti järel
            while True:
                # Ootab 5 minutit (300 sekundit) enne järgmist tsüklit
                time.sleep(300)
                
                # Kui lõpeta_programm on True, katkestab tsükli
                if lõpeta_programm:
                    break
                
                tsüklid += 1  # Suurendab tsüklite arvu ühe võrra
                
                # Arvutab efektiivsuse, kui palju tsükleid olid kasulikud
                efektiivsus = (kasulikud_tsüklid / tsüklid) * 100 if tsüklid > 0 else 0
                print(f"Tsükkel {tsüklid}: Tootlikkus siiani on {efektiivsus:.2f}%")
        
        # Kasutaja võib käsitsi lõpetada programmi vajutades Ctrl + C
        except KeyboardInterrupt:
            print("\nJälgimine katkestatud kasutaja poolt käsitsi.")
        
        # Peatab jälgimise ja kuvab lõpliku efektiivsuse
        observer.stop()  # Peatab failijälgija
        observer.join()  # Ootab, kuni jälgija lõpetab töö

        # Kuvab lõpliku efektiivsuse, kui oli vähemalt üks tsükkel
        if tsüklid > 0:
            print(f"Lõplik efektiivsus: {efektiivsus:.2f}% {tsüklid} tsükli jooksul.")
        else:
            print("Tsükleid ei toimunud. Programm peatati varakult.")
    
    # Kui kasutaja ei andnud failinime, lõpetab programm töö
    else:
        print("Märkmete faili ei antud. Programm lõpetab töö.")

# Käivitab programmi
main()
