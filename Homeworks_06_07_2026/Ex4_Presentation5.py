degree = int(input("Enter a degree: "))

if degree < 0:
    print("Cold")
elif degree >= 0 and degree <= 25:
    print("Good")
else:
    print("Warm")