import time

# Muutujad, mis jälgivad programmi olekut ja efektiivsust
lopeta_programm = False  # Näitab, kas programm peaks lõpetama
tsuklid = 0              # Tsüklite arv (iga 5 minuti järel tehtav kontroll)
kasulikud_tsuklid = 0      # Kasulike tsüklite arv, kus sisendit tehti

# Peamine funktsioon, mis juhib programmi
def main():
    global lopeta_programm, tsuklid, kasulikud_tsuklid

    # Teavitab kasutajat programmi eesmärgist
    print("Tere tulemast! See programm kuulab teie klaviatuuri sisestusi.")
    print("Programmi peatamiseks vajutage Ctrl + C.")

    try:
        # Tsükline kontroll ja sisendite lugemine
        while True:
            # Loeb sisendi kasutajalt
            sisend = input("Sisesta midagi (või vajuta Enter, et jätta vahele): ").strip()
            if sisend:
                print("Sisend tuvastatud!")
                kasulikud_tsuklid += 1

            # Ootab 5 minutit (300 sekundit) enne järgmist tsüklit
            time.sleep(300)

            tsuklid += 1  # Suurendab tsüklite arvu ühe võrra

            # Arvutab efektiivsuse, kui palju tsükleid olid kasulikud
            efektiivsus = (kasulikud_tsuklid / tsuklid) * 100 if tsuklid > 0 else 0
            print(f"Tsükel {tsuklid}: Tootlikkus siiani on {efektiivsus:.2f}%")

    # Kasutaja võib programmi käsitsi lõpetada vajutades Ctrl + C
    except KeyboardInterrupt:
        print("\nProgramm peatatud kasutaja poolt.")

    # Kuvab lõpliku efektiivsuse, kui oli vähemalt üks tsükkel
    if tsuklid > 0:
        efektiivsus = (kasulikud_tsuklid / tsuklid) * 100
        print(f"Lõplik tootlikkus: {efektiivsus:.2f}% {tsuklid} tsükli jooksul.")
    else:
        print("Tsüklite arv oli null. Programm peatati varakult.")

    # Märgib programmi lõpetatuks
    lopeta_programm = True

# Käivitab programmi
main()
