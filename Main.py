import random
# check if string is in english alphabet ( isalpha() method returns true for hebrew )
def isalpha_eng(s : str) ->bool:
    alphabet = [chr(letter) for letter in range(ord('A'), ord('Z') + 1)]
    s = s.upper()
    for c in s:
        if c not in alphabet:
            return False
    return True

def random_str_list_element(l : list[str])->str:
    rnd_index = random.randint(0,len(l)-1)
    return l[rnd_index]

# puts 3-5 length words from string in set
def str_to_short_word_set(s : str)->set:
    word_set = set()
    s_index = 0
    word = ''
    while s_index < len(s):
        # count if word is under 5
        if len(word) <= 5 and isalpha_eng(s[s_index]):
            word = word + s[s_index]
        # if over discard it and continue in string until seperator
        elif len(word) > 5 and isalpha_eng(s[s_index]):
            word = ''
            while isalpha_eng(s[s_index]): s_index += 1
        # if we got to seperator and word wasn't discarded (meaning it's valid) add it to set
        elif not isalpha_eng(s[s_index]) and word:
            # if word is 3-5 in length add it to set
            if len(word) >=3:
                word_set.add(word.upper())
            word = ''
        # continue string index
        s_index += 1
    return word_set

# creates file containing words from set separated by \n
def set_to_file(file_name:str, words_set : set):
    with open(file_name,"w") as f:
        for word in words_set:
            f.write(word+'\n')

# returns random line from file separated by \n
def gen_random_file_word(file_name : str)->str:
    with open(file_name,'r') as f:
        words = f.readlines()
    random_index = random.randint(0,len(words)-1)
    return words[random_index][:-1]

def generate_anagrams(word : str)->list[str]:
    if len(word) == 1:
        return [word]
    anagrams = [word[i] + p for i in range(len(word)) for p in generate_anagrams(word[:i] + word[i + 1:])]
    return anagrams

def evaluate(guess : str, word : str)->int:
    if len(guess) != len(word):
        return 0
    n = 0
    for i in range(len(word)):
        if word[i] == guess[i]: n+=1
    return n

#Main
with open("story",'r') as f:
    s = ''.join(f.readlines())
set_to_file("words",str_to_short_word_set(s))

# Player 1 - get the random word
rnd_word = gen_random_file_word("words")
# Player 2 (User) - get same length input word
word = ''
while len(word) != len(rnd_word) or not isalpha_eng(word):
    word = input("Please enter a " + str(len(rnd_word)) + " length word containing only english letters: ")
candidates = generate_anagrams(rnd_word) # Anagrams

#Player2 guess:
guess = random_str_list_element(candidates)
print(evaluate(guess,rnd_word)) #test

# Slopy????????