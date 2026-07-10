date = input('Enter your date(like 03.12.2024): ')
new_date = date[:6] + str(int(date[6:])+1)
print(new_date)