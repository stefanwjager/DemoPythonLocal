from contextlib import nullcontext


total  = 0
expenses = []
num_expenses = int(input("enter # of expenses"))
                         
for i in range(num_expenses):
    expenses.append(float(input("enter expense")))

mytotal = sum(expenses)
print(expenses)
print(sum(expenses))
print(mytotal)

