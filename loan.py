# get the loan details

from calendar import month


money_owed = float(input("How much money do you owe ? \n ")) #50,000
apr = float(input("what is the annual percentage rate? \n ")) #3%
payment = float(input("what is the manual payment in dollars? \n ")) #1,000
months = int(input("how many months? \n"))

#DIV apri by 100 to make it a percent
# then divide by 12 to make it monthly

monthly_rate = apr/100/12

for i in range (months):
    # add in interest
    interest_paid = money_owed * monthly_rate
    money_owed = money_owed + interest_paid

    if (money_owed - payment < 0 ):
        print ("the last payment is", money_owed)
        print ("done", i+1, "months")
        break
    
    #make payment
    money_owed = money_owed - payment

    #print the results
    print ("Paid", payment, "of which ", interest_paid, "was interest", end = ' ') 
    print ("Now I owe", money_owed)