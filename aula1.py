from random import shuffle

a1 = input('Digite o nome de seu aluno:')
a2 = input('Digite o nome de outro aluno:')
a3 = input('Digite o nome do Terceiro aluno:')
a4 = input('Digite o nome do Quarto aluno:')

al = [a1, a2, a3, a4]
shuffle(al)
# Organiza um embaixo do outro e coloca a ordem numérica
print('Ordem de apresentaçao dos alunos:')
for leo, nome in enumerate(al, start=1):
    print(f'{leo}. {nome}')
