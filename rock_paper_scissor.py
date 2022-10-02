import random

computer_choice = random.choice(['scissors','rock','paper'])

user_choice = input ('do you want - rock, paper or scissors\n ')

if computer_choice == user_choice:
    print('same same')
elif user_choice =='rock' and computer_choice =='scissors':
    print ('You win, the computer had ' + computer_choice)
elif user_choice =='paper' and computer_choice =='rock':
    print ('You win, the computer had ' + computer_choice)
elif user_choice =='scissors' and computer_choice =='paper':
    print ('You win, the computer had ' + computer_choice)
else:
    print ('you lost, computer wins, computer had: ' + computer_choice )
    
# uitzoeken: wat als de gebruiker iets kiest dat niet in de lijst staat



