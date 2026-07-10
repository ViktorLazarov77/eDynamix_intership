day = input("Enter day of the week: ").lower()

if day == "monday" or day == "tuesday" or day == "friday":
    print(12)
elif day == "wednesday" or day == "thursday":
    print(14)
elif day == "saturday" or day == "sunday":
    print(16)