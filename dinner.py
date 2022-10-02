#breakfast = ['english breakfast', 'bagel', 'continental breakfast' ]
#lunch =  ['blt', 'pb&j', 'turkey sandwich']
#dinner =['soup', 'salad', 'spaghetti','taco','lasagna' ]

#menus = [ ['english breakfast', 'bagel', 'continental breakfast' ],
#          ['blt', 'pb&j', 'turkey sandwich'],
#          ['soup', 'salad', 'spaghetti','taco','lasagna' ]]

#print ( 'breakfast menu : \n', menus[0])
#print ( 'lunch menu : \n', menus[1])
#print ( 'dinner menu : \n', menus[2])

#print ("\n\n")

#print (menus[0],[1])

#menus =[]
menus = {'breakfast':  ['english breakfast', 'bagel', 'continental breakfast' ],
         'lunch':      ['blt', 'pb&j', 'turkey sandwich'],
         'diner':      ['soup', 'salad', 'spaghetti','taco','lasagna' ]}

print ('breakfast menu ', menus ['breakfast'])
print ('lunch menu ', menus ['lunch'])

#print (menus[0],menus[1])

for menu in menus:
    print (menu)

for name, menu in menus.items():
    print(name, ": " , menu)
    # zou eigenlijk losse elementen willen weergeven ipv geblokte lijst
    
