afkortingen = []

afkortingen.append ('z.o.z.')
afkortingen.append ('vr.gr.')
afkortingen.append ('m.a.w.')
afkortingen.append ('bijv.')
print (afkortingen)

for afkorting in afkortingen:
    print(afkorting)


afkortingen.remove ('bijv.')
print (afkortingen)
del afkortingen [2] # let op instructie
print (afkortingen)
if 'z.o.z.' in list(afkortingen):
    print ("In de lijst")
else:
    print ("NIET In de lijst")
    
if afkortingen[1] in list(afkortingen):
    print (True)
    
