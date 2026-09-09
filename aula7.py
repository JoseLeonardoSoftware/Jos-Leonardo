#depois do print f usar dentro das {o.title} entre outros 
from random import choice
a1 = str(input('Nome do aluno 1:'))
a2 = str(input('Nome dp aluno 2:'))
a3 = str(input('Nome do aluno 3:'))
a4 = str(input('Nome do aluno 4:'))
lista = [a1, a2, a3, a4]
e = choice(lista)
print(f'O escolhido foi {e.title()}')
