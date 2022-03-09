"""Find potential solutions to Wordle, Dordle, Quordle, or any derivative
word puzzle with five-letter solutions. I don't really recommend using this
unless you've already completed or failed the daily puzzle and want to see how
many different ways you could have wasted guesses.

Disclaimer: I pulled my list of five-letter words from CMUdict, so there's no
guarantee the results will match the word lists of Wordle or any of its
derivatives.

>>> possible_solutions(
...     green_letters='**ir*',
...     yellow_letters='ts',
...     available_letters='-alenouh'
... )
['skirt', 'stirs']

>>> possible_solutions('a*e*d', '', '-linptm')
['ahead']

>>> possible_solutions('***t*  ', 'tun', '*')
['nutty']

>>> possible_solutions('**P', 'EER   ', 'QWYUGHJKZXVB ')
['peper', 'rupee']

>>> possible_solutions('', 'torf', 'qyghjzx')
['forth', 'forty', 'froth', 'groft']
"""

import collections
import string

_WORD_LEN = 5
_CHAR_SET = set(string.ascii_lowercase)
with open('cmudict_5L.txt') as f:
    _WORDS = [line.strip() for line in f]


def _cleaned_input_set(input_string):
    input_string = input_string.lower()
    
    if input_string == '*':
        target_set = _CHAR_SET
    else:
        target_set = set(input_string) & _CHAR_SET
        if input_string.startswith('-'):
            target_set = _CHAR_SET - target_set
    
    return target_set


def _cleaned_green_letters_list(input_string):
    input_string = input_string.lower()
    green_list = []
    
    for c in input_string:
        if c in _CHAR_SET:
            green_list.append(c)
        else:
            green_list.append('*')
    
    return green_list


def _yellow_letter_counts(input_string):
    input_string = input_string.lower()
    counts = collections.defaultdict(int)
    
    for c in input_string:
        if c in _CHAR_SET:
            counts[c] += 1
    
    return counts


def possible_solutions(green_letters, yellow_letters, available_letters):
    green_letters = green_letters.ljust(_WORD_LEN, '*')[:_WORD_LEN]
    green_list = _cleaned_green_letters_list(green_letters)
    green_set = _cleaned_input_set(green_letters)
    yellow_counts = _yellow_letter_counts(yellow_letters)
    yellow_set = _cleaned_input_set(yellow_letters)
    available_letters = _cleaned_input_set(available_letters)
    available_letters |= (green_set | yellow_set)
    answers = []
    
    for w in _WORDS:
        reduced_w = w
        for c in green_list:
            if c != '*':
                reduced_w = reduced_w.replace(c, '', 1)
        
        if (all(green_list[i] == '*' or green_list[i] == w[i]
                for i in range(_WORD_LEN)) and
            all(l in available_letters for l in w) and
            all(reduced_w.count(k) >= v for k, v in yellow_counts.items())):
            answers.append(w)
    
    return answers


def main():
    while True:
        green_letters_raw = input(
            '\nGreen/fixed letters ' +
            '(length of {}, use "*" for unknown letters)\n'.format(_WORD_LEN)
        )
        yellow_letters_raw = input('\nYellow/other required letters:\n')
        letters_raw = input(
            '\nPossible letters ' +
            '(prepend with "-" to exclude, or use "*" to include all):\n'
        )
        
        print('\nList of possible solutions found:')
        for answer in possible_solutions(green_letters_raw, yellow_letters_raw, letters_raw):
            print(answer)
        
        if input('\nSearch again? (y/n)\n').lower() == 'n':
            break


if __name__ == '__main__':
    main()
