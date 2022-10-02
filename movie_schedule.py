current_movies = {'the grinch': '11:00', 
                   'Rudolph': '1:00',
                   'frosty the snowman':  '3:00',
                   'christmas vacation': '5:00'}

print ("\n movies for today: \n" )
for key in current_movies:
    print (key)
    
movie = input ('\n for which movie do you want to see its schedule ?\n ')

showtime = current_movies.get(movie)

if showtime == None:
    print("requested show time is not available")
else:
    print(movie ,'is playing at ' , showtime)

