k = float(input('How many kilometers will your trip be?:'))
v1 = k * 0.50
v2 = k * 0.45
if k <= 200:
    print(f'You will have to pay R${v1:.2f} for the ticket, have a good trip')
else:
    print(f'You will have to play R${v2:.2f} for the ticket, have a good trip')
