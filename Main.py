import random
MAX_WORD_LEN = 5
MIN_WORD_LEN = 3
FILE_STORY_NAME = "story"
FILE_WORDS_NAME = "words"

# check if string is in english alphabet ( isalpha() method returns true for hebrew )
def isalpha_eng(s : str) ->bool:
    s = s.upper()
    for c in s:
        if not 'A' <= c <= 'Z':
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
    s = s + ' ' # So the logic works if the story ends in a letter
    while s_index < len(s):
        # count if word is under 5
        if len(word) < MAX_WORD_LEN and isalpha_eng(s[s_index]):
            word = word + s[s_index]
        # if over discard it and continue in string until seperator
        elif len(word) >= MAX_WORD_LEN and isalpha_eng(s[s_index]):
            word = ''
            while s_index < len(s) and isalpha_eng(s[s_index]): s_index += 1
        # if we got to seperator and word wasn't discarded (meaning it's valid) add it to set
        elif not isalpha_eng(s[s_index]) and word:
            # if word is 3-5 in length add it to set
            if len(word) >= MIN_WORD_LEN:
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
    return words[random_index].strip() # strip to remove the \n

def generate_anagrams(word : str)->list[str]:
    if len(word) == 1:
        return [word]
    anagrams = set([word[i] + p for i in range(len(word)) for p in generate_anagrams(word[:i] + word[i + 1:])])
    return list(anagrams)

def evaluate(guess : str, word : str)->int:
    if len(guess) != len(word):
        return 0
    score = 0
    for i in range(len(word)):
        if word[i] == guess[i]: score+=1
    return score

def filter_candidates(candidates: list[str], guess: str,feedback : int)->  list[str]:
    items = []
    for c in  candidates:
        if evaluate(guess,c) == feedback:
            items.append(c)
    return items

def make_anagram(word:str,target:str)->str:
    word = word.upper()
    target = target.upper()
    all_anagrams = generate_anagrams(target)
    best_word = target # for edge case where only 1 anagram
    min_diff = MAX_WORD_LEN+1
    for candidate in all_anagrams:
        if candidate != target:
            current_diff = len(word)-evaluate(word,candidate) # calculate differance
            if current_diff < min_diff:
                min_diff = current_diff
                best_word = candidate
    return best_word

#Main
# Setup words
with open(FILE_STORY_NAME,'r') as f:
    s = ''.join(f.readlines())
set_to_file(FILE_WORDS_NAME,str_to_short_word_set(s)) # make words
try:
   original_word = gen_random_file_word(FILE_WORDS_NAME)  # get random word
except ValueError:
    print("ERROR: Story file doesn't contain "+str(MIN_WORD_LEN)+'-'+str(MAX_WORD_LEN)+" length words")
    exit()
original_word_len = len(original_word)

print("Chosen word by player 1: "+original_word+'')
print("All anagrams of the word: \n",generate_anagrams(original_word),"\n")
print("--- Pre-Game Step ---")

word = ''
while len(word) != original_word_len or not isalpha_eng(word):
    word = input("Player 1: Please enter "+str(original_word_len)+" length word containing english letters only: ")
anagram = make_anagram(word,original_word) # make anagram from player 2's word
print("Anagram provided to player 2 (Result): "+anagram+"\n")

#Player2 guess loop:
print("--- Guessing loop ---")
after_filter = generate_anagrams(anagram)
tries = 0
while len(after_filter)>1:
    tries+=1
    print("Guess number",tries,"\n-----------")
    guess = random_str_list_element(after_filter)
    feedback = evaluate(guess,original_word)
    print("Chosen word by player 2: "+guess)
    print("Score:" , feedback)
    after_filter = filter_candidates(after_filter, guess, feedback)
    print("Filter:",after_filter,'\n')
if len(after_filter) == 1:
    print("Success! player 2 found the word: ",after_filter[0])
    print("It took",tries,"tries")
