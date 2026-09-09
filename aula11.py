# The unicodedata library removes the accents.
import unicodedata
phrase = str(input('Write a sentence:')).upper().strip()
u_phrase = unicodedata.normalize('NFD', phrase).encode(
    'ascii', 'ignore').decode('ascii')
print(f'The letter A appears in the sentence {u_phrase.count('A')} times')
print(f'The first letter A appeared in position {u_phrase.find('A')+1}')
print(f'The last letter A appeared in position {u_phrase.rfind('A')+1}')
