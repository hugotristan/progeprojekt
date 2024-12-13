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


hetkeaeg = datetime.datetime.now()
kuupäev = (hetkeaeg.year, hetkeaeg.month, hetkeaeg.day)
algusaeg=(hetkeaeg.hour, hetkeaeg.minute)
print(kuupäev)
print(algusaeg)
print(hetkeaeg)






#Ekraani loomine
ekraan = tk.Tk()
ekraan.title(  "KESKENDUMISE HINDAJA")
laius= ekraan.winfo_screenwidth()               
kõrgus= ekraan.winfo_screenheight()               
ekraan.geometry("%dx%d" % (laius, kõrgus))
ekraan.configure(bg="bisque3")

#Esilehe pilt
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

print(konspekt_linnuke.get())   #Muutujad linnukese panekul
print(video_linnuke.get())




#PÕHIPROGRAMM

# valib veebikaamera (0 on esimene (ainuke))
kaamera = cv2.VideoCapture(0)

# tulevad koordinaadid
näo_asukoht = []
kontrollitav_kaader = True

# muutuja kasti (näo tuvastuskauguse) jaoks
d = 0.5
s = int(1/d)

#kaadrite arv (mitme kaadri tagant kontrollida kohalolu)
k = 1

# p - mitu kaadrit oldi kohal | n - mitu kaadrit ei tuvastatud inimest
p=0
n=0
w=0
while True:

    

    # vahelejäävad kaadrid
    i=0
    while i < k:
        #ret on tagastusväärtus
        ret, kaader = kaamera.read()
        i+=1
        w+=i

    # kontrollitav kaader
    if kontrollitav_kaader:
        # kaadri väiksemaks tegemine näo kiiremaks tuvastamiseks
        pisem_kaader = cv2.resize(kaader, (0, 0), fx=d, fy=d)

        # Näotuvastus - tuvastab ning lisab koordinaadid järjendisse face_locations
        näo_asukoht = face_recognition.face_locations(pisem_kaader)
        # Juhul kui nägu ei tuvastatud
        if face_recognition.face_locations(pisem_kaader) != []:
            p +=1
        else:
            n +=1


    kontrollitav_kaader = not kontrollitav_kaader

    # Teeb kasti
    for (ülemine, parem, alumine, vasak) in näo_asukoht:
        # näo asukoha toob tagasi e kasti asukoha muudab õigeks
        ülemine *= s
        parem *= s
        alumine *= s
        vasak *= s

        cv2.rectangle(kaader, (vasak, ülemine), (parem, alumine), (0, 0, 255), 2)



    # Näitab kontrollitavat kaadrit
    cv2.imshow('Video', kaader)
    

    # Vajutades q-d, lõpetab tegevuse
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

    
# Lõpetab tegevuse
kaamera.release()
cv2.destroyAllWindows()


# arvutused
print(p)
print(n)
protsent = 0.0
if p != 0:
    protsent = (p)/(p+n)
    print()
    print(f"{protsent*100}%")
    if (p*100)/(p+n) > 80:
        print("Keskendusid väga palju")
elif n == 0:
    protsent = 1
    print("Keskendusid kogu aja")

lõppaeg = (hetkeaeg.hour, hetkeaeg.minute)
aeg=0
if lõppaeg[0] < algusaeg[0]:
    aeg = (24-lõppaeg[0] + algusaeg[0])*60 + (60-lõppaeg[1]+algusaeg[1])
elif lõppaeg[0] == algusaeg[0]:
    aeg = lõppaeg[1] - algusaeg[1]
else:
    aeg = (lõppaeg[0] - algusaeg[0])*60 + (60-lõppaeg[1]+algusaeg[1])
t = (int(aeg/60), aeg%60)
print(f"Aega kulus: {t} min")


    



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


#protsent visuaalselt
kanvas.create_rectangle(150, 150, 230, 570, fill="antique white")
if protsent >= 0.8:
    värv = "green"
elif 0.8 > protsent > 0.70:
    värv = "yellow"
else:
    värv = "red"
osakaal = 420*protsent
kanvas.create_rectangle(150, 570, 230, 570-osakaal, fill=värv)


kanvas.create_line(250, 80, 250, 580, width=4, fill="black")
#80 on maksimum, veits alla
puudub=False
try:
    f=open("keskendumiste_ajalugu.txt", encoding="UTF-8")
except:
    puudub = True
    print("Leht loodud")
    
if puudub == False:
    andmed = list(f)
    if andmed[0].strip() == "":
        print()
        print("---- Failiga 'keskendumiste_ajalugu.txt' on probleem: Esimene rida on tühi." + "\n" +
              "---- Kustuta fail või eemalda esimene rida.")
        print()
    if len(andmed) != 0 and andmed[0].strip() != "":
        if len(andmed) > 25:
            andmed = andmed[-25:-1]
        f=open("keskendumiste_ajalugu.txt", encoding="UTF-8")
        x=310

        for i in range(len(andmed)):
            y1=float(andmed[i].strip().split(" - ")[0])
            a=andmed[i].strip().split(" - ")[1]
            try:
                y=float(andmed[i+1].strip().split(" - ")[0])
            except:
                kanvas.create_line(x, 320-y1*2.2, x, 340, width=2, fill="black", dash=(10,1))
                kanvas.create_oval(x-4, 320-y1*2.2-4, x+4, 320-2.2*y1+4, fill="black")
                kanvas.create_text((x, 355), text=a, fill="black", font=('Arial', 10, "bold"))
                
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
            kanvas.create_text((x, 355), text=a, fill="black", font=('Arial', 10, "bold"))
            y1=y2
            x+=35        



salvestus_linnuke = tk.BooleanVar(value=True)
salvestus = tk.Checkbutton(ekraan, text="Soovin tulemust salvestada", variable=salvestus_linnuke, 
                             onvalue=True, offvalue=False)
salvestus.config(bg="antique white", fg="black", font=("Arial", 18), 
                   selectcolor="white")
salvestus.config(width=84, height=1)
salvestus.place(x=35, y=650)





ekraan.mainloop()

print(salvestus_linnuke.get())

if salvestus_linnuke:
    fail="keskendumiste_ajalugu.txt"
    f=open(fail, "a", encoding="UTF-8")
    ajakulu = str(t[0]) + ":" + str(t[1])
    kuup = str(kuupäev[1]) + "." + str(kuupäev[0])
    algus = str(algusaeg[0]) + "." + str(algusaeg[1])
    f.write(f"{protsent*100} - {ajakulu} - {kuup} kell {algus}" + "\n")
    f.close()
    
