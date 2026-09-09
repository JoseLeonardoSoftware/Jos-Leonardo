from datetime import date
y = int(input('Enter a year or type 0 to analyze the current year:'))
if y == 0:
    y = date.today().year

if y % 4 == 0 and y % 100 != 0 or y % 400 == 0:
    print(f'The year {y} is a leap year')
else:
    print(f'The year {y} is a not leap year')
