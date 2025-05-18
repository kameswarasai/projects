cond = True # this is the condition for loop until you get a correct answer

# Function for fibonacci
def fibo(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

#starting main loop
while cond == True:
    # Taking command to differents types of outputs
    out = input("enter the type of input ou want(loop: -l/finction: -f): ")
    # Taking the nth term
    n = int(input("enter the nth number you want for fibo: "))

    # Starting the loop formate
    if out == "-l":
        a, b = 1, 1
        for i in range(n+1):
            print(a)
            a, b = b, a + b
        cond = False
    
    # Starting the functional format
    elif out == "-f":
        print(f"the {n}th fibonacci number is: {fibo(n)}")
        cond = False
    
    # Continue the loop if command given is wrong
    else:
        print("give correct perimeter")
        cond = True




