n1 = float(input('Type your first grade:'))
n2 = float(input('Type your second grade:'))
n3 = float(input('Type your third grade:'))
m = (n1 + n2 + n3) / 3
if m >= 6.0:
    print('You passed the course, Congratulations!')
else:
    print('Your average was low unfortunately')
print(f'Your average is {m: .1f}')
