import random

roll = random.randint(1,6)


guess = int(input("Guess the number of the dice? \n"))

if guess == roll:
    print("correct, you rolled: " + str(roll))
else:
    print("wrong, you rolled: " + str(guess) + ", computer rolled: " + str(roll))