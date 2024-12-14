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
import keyboard
import tkinter as tk
import datetime






#ESILEHT
ekraan = tk.Tk()
ekraan.title(  "KESKENDUMISE HINDAJA")
laius= ekraan.winfo_screenwidth()               
kõrgus= ekraan.winfo_screenheight()               
ekraan.geometry("%dx%d" % (laius, kõrgus))
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
konspekt_linnuke = tk.IntVar()
video_linnuke = tk.IntVar()
konspekt = tk.Checkbutton(ekraan, text="Konspekt on arvutis", variable=konspekt_linnuke, 
                             onvalue=1, offvalue=0)
video = tk.Checkbutton(ekraan, text="Soovin näha videot", variable=video_linnuke, 
                             onvalue=1, offvalue=0)
konspekt.config(bg="antique white", fg="black", font=("Arial", 21), 
                   selectcolor="white")
video.config(bg="antique white", fg="black", font=("Arial", 21), 
                   selectcolor="white")
konspekt.config(width=45, height=1)
video.config(width=45, height=1)
konspekt.place(x=250, y=510)
video.place(x=250, y=580)

ekraan.mainloop()


#Muutujad linnukese panekul
konspet_muutuja = konspekt_linnuke.get()
video_muutuja = video_linnuke.get()
print()
print(f"Konspekt: {konspekt_muutuja}")
print(f"Video {video_muutuja}")
print()




#Esialgne aeg ning kuupäev
hetkeaeg = datetime.datetime.now()
kuupäev = (hetkeaeg.year, hetkeaeg.month, hetkeaeg.day)
algusaeg = (hetkeaeg.hour, hetkeaeg.minute)
print(kuupäev)
print(algusaeg)
print(hetkeaeg)




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


while True:
    
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
    cv2.imshow('Video', kaader)
    

    # vajutades "q" lõpetab tegevuse
    if cv2.waitKey(1) & 0xFF == ord('q') or keyboard.is_pressed('ctrl + q + space'):
        break


kaamera.release()
cv2.destroyAllWindows()




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
width= ekraan.winfo_screenwidth()               
height= ekraan.winfo_screenheight()               
ekraan.geometry("%dx%d" % (width, height))
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
        f=open("keskendumiste_ajalugu.txt", encoding="UTF-8")
        
        for i in range(len(andmed)):
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
    f.write(f"{protsent*100} - {ajakulu} - {kuup} - {algus} - {aasta}" + "\n")
    f.close()
    
