hour = int(input("Enter hour: "))
day_of_week = str(input("Enter day of the week: "))

if hour>=10 and hour<=18 and (day_of_week == "Monday" or day_of_week == "Tuesday" or day_of_week == "Wednesday" or day_of_week == "Thursday" or day_of_week == "Friday"):
    print("In work time")
else:
    print("Not in work time")