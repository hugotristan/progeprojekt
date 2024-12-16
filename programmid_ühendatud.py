import time
from multiprocessing import Process
from pynput import keyboard # pip install pynput
import face_recognition
import cv2
import datetime

# klaviatuuri jälgimise programm
lopeta_programm = False
sisestusi_tuvasatud = 0
tsuklid = 0
kasulikud_tsuklid = 0
tsükli_pikkus = 5 # aeg sekundites

def klaviatuuri_kuulaja(tegevus):
    """Funktsioon, mis registreerib klaviatuuri vajutusi."""
    global sisestusi_tuvasatud
    sisestusi_tuvasatud += 1

def klaviatuuri_programm():
    global lopeta_programm, tsuklid, kasulikud_tsuklid, sisestusi_tuvasatud

    print("Tere tulemast! See programm jälgib kõiki klaviatuuri sisestusi.")
    print("Programmi peatamiseks vajutage Ctrl + C.")

    # alustab klaviatuuri kuulamist
    kuulaja = keyboard.Listener(on_press=klaviatuuri_kuulaja)
    kuulaja.start()

    try:
        while True:
            sisestusi_tuvasatud = 0  # nullib tsükli sisestuste lugeri

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

    except KeyboardInterrupt:
        print("\nKlaviatuuri jälgija peatatud.")

    # kuvab lõpliku efektiivsuse
    if tsuklid > 0:
        efektiivsus = (kasulikud_tsuklid / tsuklid) * 100
        print(f"Lõplik tootlikkus: {efektiivsus:.2f}% {tsuklid} tsükli jooksul.")
    else:
        print("Tsüklite arv oli null. Programm peatati varakult.")

    lopeta_programm = True
    kuulaja.stop()

# kaamera jälgimise programm
def kaamera_programm():
    # valib veebikaamera
    kaamera = cv2.VideoCapture(0)

    näo_asukoht = []
    kontrollitav_kaader = True

    # muutujad
    d = 0.5  # muutuja kasti (näo tuvastuskauguse) jaoks
    s = int(1 / d)  # muutuja kasti (näo tuvastuskauguse) jaoks
    k = 1  # kaadrite arv (mitme kaadri tagant kontrollida kohalolu)
    p = 0  # positiivsed kaadrid
    n = 0  # negatiivsed kaadrid
    w = 0

    try:
        while True:
            i = 0
            while i < k:
                ret, kaader = kaamera.read()
                i += 1
                w += i

            if kontrollitav_kaader:
                pisem_kaader = cv2.resize(kaader, (0, 0), fx=d, fy=d)
                näo_asukoht = face_recognition.face_locations(pisem_kaader)
                if näo_asukoht:
                    p += 1
                else:
                    n += 1

            kontrollitav_kaader = not kontrollitav_kaader

            # kasti loomine ümber näo
            for (ülemine, parem, alumine, vasak) in näo_asukoht:
                ülemine *= s
                parem *= s
                alumine *= s
                vasak *= s
                cv2.rectangle(kaader, (vasak, ülemine), (parem, alumine), (0, 0, 255), 2)

            #näitab kontrollitavat kaadrit
            if video_muutuja:
                cv2.imshow('Video', kaader)

            # vajutades "ctrl + alt + e" lõpetab tegevuse
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Kaamera programm peatatud.")
    finally:
        kaamera.release()
        cv2.destroyAllWindows()

# peaprogramm
if __name__ == "__main__":
    klaviatuur_protsess = Process(target=klaviatuuri_programm)
    kaamera_protsess = Process(target=kaamera_programm)

    klaviatuur_protsess.start()
    kaamera_protsess.start()

    try:
        klaviatuur_protsess.join()
        kaamera_protsess.join()
    except KeyboardInterrupt:
        print("Peatatakse kõik protsessid...")
        klaviatuur_protsess.terminate()
        kaamera_protsess.terminate()
