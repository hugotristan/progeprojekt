import os
import time
import keyboard
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# vaja teha: pip install keyboard, pip install watchdog 
# py -m pip install keyboard, py -m pip install watchdog

# jälgib, kas programm peaks lõpetama
lõpeta_programm = False
tsüklid = 0
kasulikud_tsüklid = 0

class FailiJälgija(FileSystemEventHandler):
    def on_modified(self, event):
        global kasulikud_tsüklid
        if event.src_path == faili_asukoht:
            print("Faili muudatus tuvastatud!")
            kasulikud_tsüklid += 1

def lõpeta_võti():
    global lõpeta_programm
    # "kuulab" klahvikombinatsiooni 'Ctrl+F' ja lõpetab programmi, kui seda vajutatakse
    keyboard.wait('ctrl+f')
    lõpeta_programm = True
    print("\n'Ctrl+F' tuvastatud. Programm peatub kohe...")

def main():
    global lõpeta_programm, tsüklid, kasulikud_tsüklid, faili_asukoht
    # küsib, kas kasutajal on arvutis märkmete jaoks fail
    vastus = input("Tervist! Kas teil on arvutis märkmete tegemiseks fail? (jah/ei): ").strip().lower()
    
    if vastus == "jah":
        faili_asukoht = input("Palun sisestage oma märkmete faili täielik asukoht: ").strip()
        
        # kontrollib, kas fail eksisteerib
        if not os.path.isfile(faili_asukoht):
            print("Antud faili ei eksisteeri. Programm lõpetab töö.")
            return
        
        print("Alustatakse teie faili kontrollimist iga 5 minuti järel.")
        print("Programmi peatamiseks ükskõik, mis ajahetkel vajutage Ctrl + C.")

         # alustab taustaniidi 'Ctrl+F' kuulamiseks
        lõpeta_thread = threading.Thread(target=lõpeta_võti, daemon=True)
        lõpeta_thread.start()

        # loob failijälgija
        event_handler = FailiJälgija()
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(faili_asukoht), recursive=False)
        observer.start()
        
        try:
            while True:
                # ootab 5 minutit ehk 300 sekundit
                time.sleep(300)

                if lõpeta_programm:
                    break
                    
                tsüklid += 1
                
                # arvutab efektiivsuse
                efektiivsus = (kasulikud_tsüklid / tsüklid) * 100 if tsüklid > 0 else 0
                print(f"Tsükkel {tsüklid}: Tootlikkus siiani on {efektiivsus:.2f}%")

        except KeyboardInterrupt:
            print("\nJälgimine katkestatud kasutaja poolt käsitsi.")
        
        # peatab jälgija ja kuvab lõpliku efektiivsuse
        observer.stop()
        observer.join()

        if tsüklid > 0:
            print(f"Lõplik efektiivsus: {efektiivsus:.2f}% {tsüklid} tsükli jooksul.")
        else:
            print("Tsükleid ei toimunud. Programm peatati varakult.")
    else:
        print("Märkmete faili ei antud. Programm lõpetab töö.")

# käivitab programmi
main()
