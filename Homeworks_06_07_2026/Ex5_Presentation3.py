import sys

n = int(input("Enter N: "))

valid_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
counts = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}

for _ in range(n):
    day_input = input("Enter day: ").strip()
    if day_input.lower() not in valid_days:
        print("Invalis day!")
        sys.exit()

    capitalized_day = day_input.capitalize()
    counts[capitalized_day] += 1

for day, count in counts.items():
    if count > 0:
        if count == 1:
            print(f"{day} - {count} time")
        else:
            print(f"{day} - {count} times")