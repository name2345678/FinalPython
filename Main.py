import random

MAX_WORD_LEN = 5
MIN_WORD_LEN = 3
FILE_WORDS_NAME = "words"


# check if string is in english alphabet ( isalpha() method returns true for hebrew )
def isalpha_eng(s: str) -> bool:
    s = s.upper()
    for c in s:
        if not 'A' <= c <= 'Z':
            return False
    return True


# returns a random item from a string list
def random_str_list_element(l: list[str]) -> str:
    rnd_index = random.randint(0, len(l) - 1)
    return l[rnd_index]


# puts 3-5 length words from string in set
def str_to_short_word_set(s: str) -> set:
    word_set = set()
    s_index = 0
    word = ''
    s = s + ' '  # So the logic works if the story ends in a letter
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


# creates file containing words from set
def set_to_file(file_name: str, words_set: set):
    with open(file_name, "w") as f:
        for word in words_set:
            f.write(word + '\n')


# returns random line from file
def gen_random_file_word(file_name: str) -> str:
    with open(file_name, 'r') as f:
        words = f.readlines()
    random_index = random.randint(0, len(words) - 1)
    return words[random_index].strip()  # strip to remove the \n


# anagram generator for player 2 guessing list and player 1 anagram making
def generate_anagrams(word: str) -> list[str]:
    if len(word) == 1:
        return [word]
    anagrams = set([word[i] + p for i in range(len(word)) for p in generate_anagrams(word[:i] + word[i + 1:])])
    return list(anagrams)


# returns how simular words are
def evaluate(guess: str, word: str) -> int:
    if len(guess) != len(word):
        return 0
    score = 0
    for i in range(len(word)):
        if word[i] == guess[i]: score += 1
    return score


# filter the guessing list for player2 during guessing loop
def filter_candidates(candidates: list[str], guess: str, feedback: int) -> list[str]:
    items = []
    for c in candidates:
        if evaluate(guess, c) == feedback:
            items.append(c)
    return items


# player1 making anagram for player2
def make_anagram(word: str, target: str) -> str:
    word = word.upper()
    target = target.upper()
    all_anagrams = generate_anagrams(target)
    best_word = target  # for edge case where only 1 anagram
    min_diff = MAX_WORD_LEN + 1
    for candidate in all_anagrams:
        if candidate != target:
            current_diff = len(word) - evaluate(word, candidate)  # calculate differance
            if current_diff < min_diff:
                min_diff = current_diff
                best_word = candidate
    return best_word


# Check if story exists and if not give option to create one
def setup_story_file(file_name: str) -> str:
    try:
        with open(file_name, 'r') as f:
            story = ''.join(f.readlines())
    except:
        choice = None
        while choice not in {'1', '0'}:
            print(
                "the file: \"" + file_name + "\" doesn't exist. \n Enter 0 if you want to exit, or 1 if you want to create a file: ")
            choice = input().strip()
        if choice == '0':
            exit()
        elif choice == '1':
            with open(file_name, 'w') as f:
                story = input("Please enter a story in english:\n")
                f.write(story)
    return story


# start guessing loop for player2
def player2_guessing_loop(anagram: str):
    print("--- Guessing loop ---")
    after_filter = generate_anagrams(anagram)
    tries = 0
    while len(after_filter) > 1:
        tries += 1
        print("Guess number", tries, "\n-----------")
        guess = random_str_list_element(after_filter)
        feedback = evaluate(guess, original_word)

        print("Chosen word by player 2: " + guess)
        print("Score:", feedback)
        after_filter = filter_candidates(after_filter, guess, feedback)
        print("Filter:", after_filter, '\n')

    if len(after_filter) == 1:
        print("Success! player 2 found the word: ", after_filter[0])
        print("It took", tries, "tries")


# -----Main-------
# Setup story file
file_story_name = input("Please enter the story's file name: ")
story = setup_story_file(file_story_name)

# Setup words file and get word
words = str_to_short_word_set(story)  # make words
if not words:  # if words is empty
    print("ERROR: Story file doesn't contain " + str(MIN_WORD_LEN) + '-' + str(MAX_WORD_LEN) + " length words")
    exit()
set_to_file(FILE_WORDS_NAME, words)
original_word = gen_random_file_word(FILE_WORDS_NAME)  # get random word
original_word_len = len(original_word)  # word length for player 2

# Pre-game prompts
print("Chosen word by player 1: " + original_word + '')
print("All anagrams of the word: \n", generate_anagrams(original_word), "\n")
print("--- Pre-Game Step ---")

# Get new word same length as the chosen word
word = ''
while len(word) != original_word_len or not isalpha_eng(word):
    word = input("Player 1: Please enter " + str(
        original_word_len) + " length word containing english letters only: ").upper().strip()
    if word == original_word:
        print("\nPlayer2 miraculously guessed the word " + word + " first try! Wow!")
        exit()
anagram = make_anagram(word, original_word)  # make anagram from player 2's word

# Player2 guess loop:
print("Anagram provided to player 2 (Result): " + anagram + "\n")
player2_guessing_loop(anagram)
