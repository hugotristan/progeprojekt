import time
from pynput import keyboard #pip install pynput

lopeta_programm = False  
tsuklid = 0             
kasulikud_tsuklid = 0    
sisestusi_tuvasatud = 0  
tsükli_pikkus = 5 # aeg sekundites

def klaviatuuri_kuulaja(tegevus):
    """Funktsioon, mis registreerib klaviatuuri vajutusi."""
    global sisestusi_tuvasatud
    sisestusi_tuvasatud += 1

# peafunktsioon
def main():
    global lopeta_programm, tsuklid, kasulikud_tsuklid, sisestusi_tuvasatud

    # teavitab kasutajat programmi eesmärgist
    print("Tere tulemast! See programm jälgib kõiki klaviatuuri sisestusi.")
    print("Programmi peatamiseks vajutage Ctrl + C.")

    # alustab klaviatuuri kuulamist
    kuulaja = keyboard.Listener(on_press=klaviatuuri_kuulaja)
    kuulaja.start()

    try:
        # tsükliline kontroll ja sisendite lugemine
        while True:
            sisestusi_tuvasatud = 0  # nullime tsükli sisestuste lugeri

            # ootab määratud aja enne järgmist tsüklit
            time.sleep(tsükli_pikkus)

            tsuklid += 1  # suurendab tsüklite arvu ühe võrra

            if sisestusi_tuvasatud > 0:
                print("Sisestusi tuvastatud viimase tsükli jooksul.")
                kasulikud_tsuklid += 1
            else:
                print("Sisestusi ei tuvastatud viimase tsükli jooksul.")

            # arvutab efektiivsuse 
            efektiivsus = (kasulikud_tsuklid / tsuklid) * 100 if tsuklid > 0 else 0
            print(f"Tsükkel {tsuklid}: Tootlikkus siiani on {efektiivsus:.2f}%")

    # kasutaja saab programmi käsitsi lõpetada vajutades Ctrl + C
    except KeyboardInterrupt:
        print("\nProgramm peatatud kasutaja poolt.")

    # kuvab lõpliku efektiivsuse, kui oli vähemalt üks tsükkel
    if tsuklid > 0:
        efektiivsus = (kasulikud_tsuklid / tsuklid) * 100
        print(f"Lõplik tootlikkus: {efektiivsus:.2f}% {tsuklid} tsükli jooksul.")
    else:
        print("Tsüklite arv oli null. Programm peatati varakult.")

    # märgib programmi lõpetatuks
    lopeta_programm = True

    # peatab klaviatuuri kuulamise
    kuulaja.stop()

if __name__ == "__main__":
    main()
