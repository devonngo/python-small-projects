import pandas as pd


# define functions
def word_to_phonetics(upper_word):
    phonetics = []

    for i in range(len(upper_word)):
        phonetics.append(lookup['Word'].get(upper_word[i]))

    return phonetics


def phonetic_string(phonetic_array):
    pstring = ''
    for i in range(len(phonetic_array)):
        pstring += phonetic_array[i] + ' '
    return pstring


# import csv as dict
df = pd.read_csv('nato-alphabet.csv', header=None, sep=';', names=['Letter', 'Word', 'Phonetics'])
df = df.set_index('Letter')
lookup = df.to_dict(orient='dict')

# user input
user_word = input('Enter string to convert: ').upper()

# process & print
result = phonetic_string(word_to_phonetics(user_word))
print(result)


