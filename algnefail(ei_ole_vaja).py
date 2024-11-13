import os
import time

def main():
    # Küsib, kas kasutajal on arvutis märkmete fail
    vastus = input("Kas teil on arvutis märkmete tegemise fail? (jah/ei): ").strip().lower()
    
    if vastus == "jah":
        faili_asukoht = input("Palun sisestage oma märkmete faili täielik asukoht: ").strip()
        
        # Kontrollib, kas fail eksisteerib
        if not os.path.isfile(faili_asukoht):
            print("Määratud faili ei eksisteeri. Programm lõpetab töö.")
            return
        
        print("Alustatakse teie faili jälgimist iga 5 minuti järel.")
        print("Vajutage Ctrl+C, et programm igal ajal peatada.")
        
        # Algväärtused efektiivsuse jälgimiseks
        algne_muutmise_aeg = os.path.getmtime(faili_asukoht)
        tsüklid = 0
        tootlikud_tsüklid = 0
        
        try:
            while True:
                # Ootab 5 minutit (300 sekundit)
                time.sleep(300)
                tsüklid += 1
                
                # Kontrollib viimast muutmisaega
                praegune_muutmise_aeg = os.path.getmtime(faili_asukoht)
                
                # Kui fail on muutunud alates viimasest kontrollist, arvestatakse tsükkel tootlikuks
                if praegune_muutmise_aeg != algne_muutmise_aeg:
                    tootlikud_tsüklid += 1
                    algne_muutmise_aeg = praegune_muutmise_aeg  # Uuendab viimase teadaoleva muutmisaja
                
                # Arvutab efektiivsuse
                efektiivsus = (tootlikud_tsüklid / tsüklid) * 100
                print(f"Tsükkel {tsüklid}: Tootlikkus siiani on {efektiivsus:.2f}%")

        except KeyboardInterrupt:
            # Programmi lõpetamine kasutaja katkestuse korral
            print("\nJälgimine peatatud kasutaja poolt.")
            print(f"Lõplik tootlikkus: {efektiivsus:.2f}% {tsüklid} tsükli jooksul.")

    else:
        print("Märkmete faili ei antud. Programm lõpetab töö.")

# Käivitab programmi
main()
