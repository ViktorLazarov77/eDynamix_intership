year = int(input("Enter a year: "))

if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
    print("This is leap year")
else:
    print("Not leap year")