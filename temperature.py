from operator import truediv
from signal import raise_signal
from traceback import format_exc


temperature = 75
forecast = "rain" 

if temperature  < 80 and forecast != "rain":
    print ("go outside")
else:
    print ("stay where you are ")
    
print ("...\n")
    
    
if not forecast == "rain":
    print("lekker naar buiten")
else:
    print ("blijf maar binnen")


print ("have a good day")

print ("...\n")
    
raining = True

if not raining:
    print ("go outside")
else:
    print("stay inside")
