import os
import time
import keyboard
import threading

# Lipp, et jälgida, kas programm peaks lõpetama
lõpeta_programm = False

def lõpeta_võti():
    global lõpeta_programm
    # "kuulab" klahvikombinatsiooni 'Ctrl+F' ja lõpetab programmi, kui seda vajutatakse
    keyboard.wait('ctrl+f')
    lõpeta_programm = True
    print("\n'Ctrl+F' tuvastatud. Programm peatub kohe...")

def main():
    global lõpeta_programm
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
        
        # algväärtused efektiivsuse jälgimiseks
        algne_muutmise_aeg = os.path.getmtime(faili_asukoht)
        tsüklid = 0
        kasulikud_tsüklid = 0
        
        try:
            while True:
                # ootab 5 minutit ehk 300 sekundit
                time.sleep(300)
                tsüklid += 1
                
                # kontrollib viimast muutmisaega
                praegune_muutmise_aeg = os.path.getmtime(faili_asukoht)
                
                # kui fail on muutunud alates viimasest kontrollist, arvestatakse tsükkel kasulikuks
                if praegune_muutmise_aeg != algne_muutmise_aeg:
                    kasulikud_tsüklid += 1
                    algne_muutmise_aeg = praegune_muutmise_aeg  # uuendab viimase teadaoleva muutmisaja
                
                # arvutab sessiooni efektiivsuse
                efektiivsus = (kasulikud_tsüklid / tsüklid) * 100
                print(f"Tsükkel {tsüklid}: Efektiivsus siiani on {efektiivsus:.2f}%")

        except KeyboardInterrupt:
            # programmi lõpetamine kasutaja poolt (ootab tsükli lõpuni, seejärel väljastab tulemuse)
            print("\nKontrollimine peatatud kasutaja poolt.")
            print(f"Lõplik efektiivsus: {efektiivsus:.2f}% {tsüklid} tsükli jooksul.")

    else:
        print("Märkmete faili ei antud. Programm lõpetab töö.")

# käivitab kogu programmi
main()

