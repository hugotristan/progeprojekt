import tkinter as tk



#muutjuad: p, n, protsent

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
kanvas.create_rectangle(130, 150, 210, 570, fill="antique white")

protsent = 0.5
if protsent >= 0.8:
    värv = "green"
elif 0.8 > protsent > 0.70:
    värv = "yellow"
else:
    värv = "red"
osakaal = 420*protsent
kanvas.create_rectangle(130, 570, 210, 570-osakaal, fill=värv)



kanvas.create_line(250, 80, 250, 580, width=4, fill="black")
f=open("keskendumiste_ajalugu.txt", encoding="UTF-8")


#80 on maksimum, ehk
x=265
y1=float(f.readline().strip())
while True:
    y=f.readline().strip()
    if y == "":
        break
    else:
        y2=float(y)
    kanvas.create_line(x, 320-y1*2.2, x+50, 320-2.2*y2)
    y1=y2
    x+=50









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
    f.write(str(protsent*100) + "\n")
    f.close()
    
