number = int(input('Type a number from 0 to 9999:'))
unit = number % 10
dozen = number // 10 % 10
hundred = number // 100 % 10
thousand = number // 1000 % 10
print(f'''units:{unit}
dozens:{dozen}
hundreds:{hundred}
thousands:{thousand}''')
