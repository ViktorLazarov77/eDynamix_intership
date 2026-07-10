numbers_list = []
print("Enter numbers. Type 'stop' to finish.")
while True:
    user_input = input("Enter a number: ")
    if user_input == "stop":
        break
    number = int(user_input)
    numbers_list.append(number)

total_sum = sum(numbers_list)
print("The total sum of all entered numbers is:", total_sum)