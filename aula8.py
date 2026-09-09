# The code checks if your city starts with the name Santo and also if your full name has Silva.
city = input(str('Type your city name:')).strip()
print(city.upper()[:5] == 'SANTO')
name = input(str('Type your first name and last name:')).strip()
print('Silva in name is', ('SILVA' in name.upper()))
