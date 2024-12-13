import datetime
import time


hetkeaeg = datetime.datetime.now()
kuupäev = (hetkeaeg.year, hetkeaeg.month, hetkeaeg.day)
algusaeg=(hetkeaeg.hour, hetkeaeg.minute)
print(kuupäev)
print(algusaeg)
print(hetkeaeg)


time.sleep(5)

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