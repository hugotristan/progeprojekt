################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt Tuto
# Teema: Keskendumise hindaja
#
#
# Autorid: Mattias Rahnu, Hugo Tristan Tammik
#
# Eeskuju: Saadud inspiratsiooni face_recognitioni projektikirjelduses olevatest näidetest,
#          loodud teemakohasemaks.
#
#Käivitamiseks:Vaja laadida C++ Build tools (installimisel vaja märkida desktop development, kõige ülemine ning vasakpoolseim)
#              Laadida vaja face_recognition: pip install face-recognition cmd-s
#              Laadida vaja ka opencv: pip install opencv-python
#
##################################################


import face_recognition
import cv2
from pynput import keyboard
import tkinter as tk
import datetime






#ESILEHT
def käivita_programm():
    ekraan.destroy() #sulgeb esilehe akna enne põhiprogrammi käivitamist
ekraan = tk.Tk()
ekraan.title(  "KESKENDUMISE HINDAJA")
laius= ekraan.winfo_screenwidth()               
kõrgus= ekraan.winfo_screenheight()               
ekraan.geometry(f"{laius}x{kõrgus}")
ekraan.configure(bg="bisque3")


#Pilt
kanvas = tk.Canvas(ekraan, width=750, height=400, bg='antique white')
kanvas.place(x=250, y=40)
kanvas.create_rectangle(50, 50, 705, 360, fill="orange")
kanvas.create_rectangle(65, 65, 690, 345, fill="antique white")
kanvas.create_text(
    (375, 175),
    text="Keskendumise",
    fill="orange",
    font=('Arial', 50, "bold")
)
kanvas.create_text(
    (375, 250),
    text="hindaja",
    fill="orange",
    font=('Arial', 50, "bold")
)


# Nupud
klaviatuur_linnuke = tk.BooleanVar()
video_linnuke = tk.IntVar()
klaviatuur = tk.Checkbutton(ekraan, text="Soovin klaviatuuri sisestusi näha", variable=klaviatuur_linnuke, 
                             onvalue=True, offvalue=False)
video = tk.Checkbutton(ekraan, text="Soovin näha videot", variable=video_linnuke, 
                             onvalue=True, offvalue=False)
klaviatuur.config(bg="antique white", fg="black", font=("Arial", 21), 
                   selectcolor="white")
video.config(bg="antique white", fg="black", font=("Arial", 21), 
                   selectcolor="white")
klaviatuur.config(width=45, height=1)
video.config(width=45, height=1)
klaviatuur.place(x=250, y=510)
video.place(x=250, y=580)

# Alustamise nupp
alusta_nupp = tk.Button(ekraan, text="Alusta!", command=käivita_programm, bg="antique white", fg="black",
                        font=("Arial", 24))
alusta_nupp.place(x=550, y=650)

ekraan.mainloop()


#Muutujad linnukese panekul
klaviatuur_muutuja = klaviatuur_linnuke.get()
video_muutuja = video_linnuke.get()
print()
print(f"Klaviatuur: {klaviatuur_muutuja}")
print(f"Video: {video_muutuja}")
print()




#Esialgne aeg ning kuupäev
hetkeaeg = datetime.datetime.now()
kuupäev = (hetkeaeg.year, hetkeaeg.month, hetkeaeg.day)
algusaeg = (hetkeaeg.hour, hetkeaeg.minute)
print(kuupäev)
print(algusaeg)
print(hetkeaeg)


# aeg=0
# lõppaeg = (hetkeaeg.hour, hetkeaeg.minute)
# if lõppaeg[1] == algusaeg[1] + 20
# if algusaeg[1] > lõppaeg[1]:
#     
# else:
    


#PÕHIPROGRAMM

# valib veebikaamera
kaamera = cv2.VideoCapture(0)

näo_asukoht = []
kontrollitav_kaader = True


# muutujad
d = 0.5  # muutuja kasti (näo tuvastuskauguse) jaoks
s = int(1/d)  # muutuja kasti (näo tuvastuskauguse) jaoks
k = 1  #kaadrite arv (mitme kaadri tagant kontrollida kohalolu)
p=0  # positiivsed kaadrid
n=0  # negatiivsed kaadrid
w=0

###################################3
# Muutujate initsialiseerimine
klahv_tuvastatud = False  # Jälgib, kas klahvi on vajutatud jooksvas tsüklis
klahvide_tuvastamise_tsüklid = 0  # Loendab tsükleid, kus vähemalt üks klahv tuvastati
tuvastamise_aken_aktiivne = False  # Lipp tuvastamise akna aktiivsuse kohta
kõik = 0  # Kõigi tsüklite loendur
kasulikud_tsüklid = 0  # Kasulike tsüklite loendur

# Funktsioon klahvivajutuse käsitlemiseks
def klahvi_vajutusel(klahv):
    global klahv_tuvastatud, tuvastamise_aken_aktiivne
    # Tuvasta klahvivajutus ainult aktiivse tuvastamise akna ajal
    if tuvastamise_aken_aktiivne and not klahv_tuvastatud:
        klahv_tuvastatud = True  # Märgista, et klahvi vajutati

# Käivita klahvikuulaja taustal
kuulaja = keyboard.Listener(on_press=klahvi_vajutusel)
kuulaja.start()

# Salvesta algusaeg
algusaeg1 = datetime.datetime.now()
print("Ootan 10 sekundit enne tuvastamise alustamist...")
#############################################

while True:
#####################################################################
# Arvuta möödunud aeg
    möödunud_aeg = datetime.datetime.now() - algusaeg1

    # Aktiveeri tuvastamise aken pärast 10 sekundit
    if not tuvastamise_aken_aktiivne and möödunud_aeg >= datetime.timedelta(seconds=3):
        tuvastamise_aken_aktiivne = True
        akna_lopp_aeg = datetime.datetime.now() + datetime.timedelta(seconds=3)
        print("Tuvastamise aken on aktiivne. Vajuta mõnda klahvi selle tsükli jooksul.")

    # Kontrolli klahvivajutust 10-sekundilise akna jooksul
    if tuvastamise_aken_aktiivne:
        if klahv_tuvastatud:
            klahvide_tuvastamise_tsüklid += 1  # Suurenda tsüklite loendurit
            kasulikud_tsüklid += 1  # Suurenda kasulike tsüklite loendurit
            print("Klahv tuvastati selle tsükli jooksul.")
            kõik += 1
            klahv_tuvastatud = False  # Taasta klahvi tuvastamise lipp
            tuvastamise_aken_aktiivne = False  # Lõpeta tuvastamise aken selleks tsükliks
            algusaeg1 = datetime.datetime.now()  # Taasta algusaeg järgmiseks tsükliks
        elif datetime.datetime.now() >= akna_lopp_aeg:
            print("Tuvastamise aken lõppes ilma klahvivajutuseta.")
            kõik += 1
            tuvastamise_aken_aktiivne = False  # Lõpeta tuvastamise aken
            algusaeg1 = datetime.datetime.now()  # Taasta algusaeg järgmiseks tsükliks

    # Arvuta ja kuva efektiivsus iga tsükli järel
    if kõik > 0:
        efektiivsus = (kasulikud_tsüklid / kõik) * 100
        print(f"Efektiivsus: {efektiivsus:.2f}%")

##########################################
    
    
    
    # vahelejäävad kaadrid
    i=0
    while i < k:
        ret, kaader = kaamera.read()
        i+=1
        w+=i

    # näo tuvastamine ja koordinaatide lisamine järjendisse näo_asukohad
    if kontrollitav_kaader:
        pisem_kaader = cv2.resize(kaader, (0, 0), fx=d, fy=d)
        näo_asukoht = face_recognition.face_locations(pisem_kaader)
        if face_recognition.face_locations(pisem_kaader) != []:
            p +=1
        else:
            n +=1
            
    kontrollitav_kaader = not kontrollitav_kaader


    # kasti loomine ümber näo
    for (ülemine, parem, alumine, vasak) in näo_asukoht:
        ülemine *= s
        parem *= s
        alumine *= s
        vasak *= s
        
        cv2.rectangle(kaader, (vasak, ülemine), (parem, alumine), (0, 0, 255), 2)


    # näitab kontrollitavat kaadrit
    if video_muutuja:
        cv2.imshow('Video', kaader)
    

    # vajutades "ctrl + alt + e" lõpetab tegevuse
    if cv2.waitKey(1) & 0xFF == ord('q'): #or keyboard.is_pressed('ctrl + alt + e'):
        break
    
    
    


kaamera.release()
cv2.destroyAllWindows()

################################################
print(f"Kõik tuvastatud tsüklid: {klahvide_tuvastamise_tsüklid}")
print(f"Kõik tsüklid: {kõik}")
########################################################
# arvutused
print()
print(p)
print(n)
protsent = 0.0
if p != 0:
    protsent = round((p)/(p+n), 2)
    print()
    print(f"{protsent*100}%")
    if (p*100)/(p+n) > 80:
        print("Keskendusid väga palju")
elif n == 0:
    protsent = 1
    print("Keskendusid kogu aja")
    

lõppaeg = (hetkeaeg.hour, hetkeaeg.minute)
aeg=0
minutid=""
tunnid=""
if lõppaeg[0] < algusaeg[0]:
    aeg = (24-lõppaeg[0] + algusaeg[0])*60 + (60-lõppaeg[1]+int(algusaeg[1]))
elif lõppaeg[0] == algusaeg[0]:
    aeg = lõppaeg[1] - algusaeg[1]
else:
    aeg = (lõppaeg[0] - algusaeg[0])*60 + (60-lõppaeg[1]+int(algusaeg[1]))
        
if aeg%60 < 10:
    minutid = "0" + str(aeg%60)
if int(aeg/60) < 10:
    tunnid = "0" + str(int(aeg/60))
t = (tunnid, minutid)
print(f"Aega kulus: {t}")


ajakulu = t[0] + ":" + t[1]
kuup = str(kuupäev[2]) + "." + str(kuupäev[1])
algus = str(algusaeg[0]) + "." + str(algusaeg[1])
aasta = kuupäev[0]


    


#VIIMANE LEHT

# ekraani loomine
ekraan = tk.Tk()
ekraan.title(  "KESKENDUMISE HINDAJA")
laius= ekraan.winfo_screenwidth()               
pikkus= ekraan.winfo_screenheight()               
ekraan.geometry(f"{laius}x{pikkus}")
ekraan.configure(bg="bisque3")


kanvas = tk.Canvas(ekraan, width=1206, height=600, bg='antique white')
kanvas.place(x=35, y=35)
kanvas.create_rectangle(30, 30, 140, 90, fill="orange")
kanvas.create_rectangle(34, 34, 136, 86, fill="antique white")
kanvas.create_text(
    (85, 50),
    text="Keskendumise",
    fill="orange",
    font=('Arial', 10, "bold")
)
kanvas.create_text(
    (85, 65),
    text="hindaja",
    fill="orange",
    font=('Arial', 10, "bold")
)


# soorituse protsent visuaalselt
kanvas.create_rectangle(130, 110, 210, 530, fill="antique white")
if protsent >= 0.8:
    värv = "green"
elif 0.8 > protsent > 0.70:
    värv = "yellow"
else:
    värv = "red"
osakaal = 420*protsent


# soorituse näitajad
kanvas.create_rectangle(130, 530, 210, 530-osakaal, fill=värv)
kanvas.create_text((170, 550), text=(str(int(round(protsent*100, 0))) + "%"), fill="midnight blue", font=("Arial", 15))
kanvas.create_text((55, 200), text=f"Aeg: {ajakulu}" , fill="midnight blue", font=("Arial", 10, "bold"))
kanvas.create_text((55, 260), text=f"Kuupäev: {kuup}", fill="midnight blue", font=("Arial", 10, "bold"))
kanvas.create_text((55, 320), text=f"Kellaaeg: {algus}", fill="midnight blue", font=("Arial", 10, "bold"))


x=320


kanvas.create_line(240, 80, 240, 580, width=4, fill="black")
kanvas.create_text((275, 360), text="Protsent:", fill="midnight blue")
kanvas.create_text((265, 390), text="Aeg:", fill="midnight blue")
kanvas.create_text((275, 420), text="Kuupäev:", fill="midnight blue")
kanvas.create_text((275, 450), text="Kellaaeg:", fill="midnight blue")


# "keskendumiste_ajalugu.txt" olemasolukontroll
puudub=False
try:
    f=open("keskendumiste_ajalugu.txt", encoding="UTF-8")
except:
    puudub = True
    print("Leht 'keskendumiste_ajalugu.txt' loodud")

l=0
u = False
if puudub == False:
    andmed = list(f)
    if andmed[0].strip() == "":
        print()
        print("---- Failiga 'keskendumiste_ajalugu.txt' on probleem: Esimene rida on tühi." + "\n" +
              "---- Kustuta fail või eemalda esimene rida.")
        print()
        
    if len(andmed) != 0 and andmed[0].strip() != "":
        if len(andmed) > 25:
            andmed = andmed[-26:-1]
            u = True
        f=open("keskendumiste_ajalugu.txt", encoding="UTF-8")
        
        for i in range(len(andmed)):
            l+=1
            y1=float(andmed[i].strip().split(" - ")[0])
            a1=andmed[i].strip().split(" - ")[1]  # ajakulu
            a2=andmed[i].strip().split(" - ")[2]  # kuupäev
            a3=andmed[i].strip().split(" - ")[3]  # algusaeg
            try:
                y=float(andmed[i+1].strip().split(" - ")[0])
            except:
                kanvas.create_line(x, 320-y1*2.2, x, 340, width=2, fill="black", dash=(10,1))
                kanvas.create_oval(x-4, 320-y1*2.2-4, x+4, 320-2.2*y1+4, fill="black")
                kanvas.create_text((x, 360), text=(str(int(round(y1,0))) + "%"), fill="black", font=('Arial', 10, "bold"))
                kanvas.create_text((x, 390), text=a1, fill="black", font=('Arial', 10))
                kanvas.create_text((x, 420), text=a2, fill="black", font=('Arial', 8))
                kanvas.create_text((x, 450), text=a3, fill="black", font=('Arial', 8))
                if l<25 and u:
                    print()
                    print("---- Failiga 'keskendumiste_ajalugu.txt' on probleem: Vahepeal on tühi rida." + "\n" +
                          "---- Kustuta failist tühi rida, et saada kõiki andmeid.")
                    print()
        
                f.close()
                break
            else:
                y2=float(y)
                if y1 > y2:
                    värv = "darkred"
                else:
                    värv = "green"
            kanvas.create_line(x, 320-y1*2.2, x+35, 320-2.2*y2, width=3, fill=värv)
            kanvas.create_oval(x-4, 320-y1*2.2-4, x+4, 320-2.2*y1+4, fill="black")
            kanvas.create_line(x, 320-y1*2.2, x, 340, width=2, fill="black", dash=(10,1))
            kanvas.create_text((x, 360), text=(str(int(round(y1,0))) + "%"), fill="black", font=('Arial', 10, "bold"))
            kanvas.create_text((x, 390), text=a1, fill="black", font=('Arial', 10))
            kanvas.create_text((x, 420), text=a2, fill="black", font=('Arial', 8))
            kanvas.create_text((x, 450), text=a3, fill="black", font=('Arial', 8))
            
            y1=y2
            x+=35        
###
#klaviatuuri tulemus 
kanvas.create_text((600, 50), text=f"Kõik tsüklid: {kõik}", fill="midnight blue", font=("Arial", 12, "bold"))
kanvas.create_text((600, 90), text=f"Kasulikud tsüklid: {kasulikud_tsüklid}", fill="midnight blue", font=("Arial", 12, "bold"))
kanvas.create_text((600, 130), text=f"Efektiivsus: {efektiivsus:.2f}%", fill="midnight blue", font=("Arial", 12, "bold"))

###
salvestus_linnuke = tk.BooleanVar(value=True)
salvestus = tk.Checkbutton(ekraan, text="Soovin tulemust salvestada", variable=salvestus_linnuke, 
                             onvalue=True, offvalue=False)
salvestus.config(bg="antique white", fg="black", font=("Arial", 18), 
                   selectcolor="white")
salvestus.config(width=84, height=1)
salvestus.place(x=35, y=650)


nupp_väljumiseks = tk.Button(ekraan, text="Välju programmist", command=ekraan.destroy, bg="antique white", fg="black", font=("Arial", 16))
nupp_väljumiseks.place(x=310, y=540)

ekraan.mainloop()


print(salvestus_linnuke.get())

if salvestus_linnuke.get():
    fail="keskendumiste_ajalugu.txt"
    f=open(fail, "a", encoding="UTF-8")
    f.write(f"{protsent*100} - {ajakulu} - {kuup} - {algus} - {aasta} - Kõik tsüklid: {kõik} - Kasulikud tsüklid: {kasulikud_tsüklid} - Efektiivsus: {efektiivsus:.2f}%" + "\n")
    f.close()
