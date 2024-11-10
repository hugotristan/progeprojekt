import face_recognition
import cv2
#import numpy as np

#Vaja laadida C++ Build tools (installimisel vasakult kõige ülemine ära märkida)
#laadida vaja face_recognition: pip install face-recognition cmd-s



# valib veebikaamera (0 on esimene (ainuke))
kaamera = cv2.VideoCapture(0)

# tulevad koordinaadid
face_locations = []
kontrollitav_kaader = True

# muutuja kasti (näo tuvastuskauguse) jaoks
D = 0.5
S = int(1/D)

#kaadrite arv (mitme kaadri tagant kontrollida kohalolu)
F = 1

# p - mitu kaadrit oldi kohal | n - mitu kaadrit ei tuvastatud inimest
p=0
n=0

while True:


    # vahelejäävad kaadrid
    i=0
    while i < F:
        #ret on tagastusväärtus
        ret, kaader = kaamera.read()
        i+=1

    # kontrollitav kaader
    if kontrollitav_kaader:
        # kaadri väiksemaks tegemine näo kiiremaks tuvastamiseks
        pisem_kaader = cv2.resize(kaader, (0, 0), fx=D, fy=D)
        
        # peaks olema ebaoluline
        # Convert BGR color (OpenCV) to RGB color (face_recognition)
        #rgb_small_kaader = np.array(small_kaader, dtype=np.uint8)

        # Näotuvastus - tuvastab ning lisab koordinaadid järjendisse face_locations
        face_locations = face_recognition.face_locations(pisem_kaader)
        # Juhul kui nägu ei tuvastatud
        if face_recognition.face_locations(pisem_kaader) != []:
            p +=1
        else:
            n +=1


    kontrollitav_kaader = not kontrollitav_kaader

    # Teeb kasti
    for (ülemine, parem, alumine, vasak) in face_locations:
        # näo asukoha toob tagasi e kasti asukoha muudab õigeks
        ülemine *= S
        parem *= S
        alumine *= S
        vasak *= S

        cv2.rectangle(kaader, (vasak, ülemine), (parem, alumine), (0, 0, 255), 2)

    # Näitab kontrollitavat kaadrit
    cv2.imshow('Video', kaader)
    

    # Press 'q' to quit the video display
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    

# Lõpetab tegevuse
kaamera.release()
cv2.destroyAllWindows()

# arvutused
print(p)
print(n)
if n != 0:
    print((p*100)/(p+n))
    if (p*100)/(p+n) > 80:
        print("Keskendusid väga palju!")
        
else:
    print("Keskendusid kogu aja!")
    
    
    
