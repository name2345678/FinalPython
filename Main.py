import random
# puts 3-5 length words from string in set
def str_to_short_word_set(s : str)->set:
    word_set = set()
    s_index = 0
    word = ''
    while s_index < len(s):
        # count if word is under 5
        if len(word) <= 5 and s[s_index].isalpha():
            word = word + s[s_index]
        # if over discard it and continue in string until seperator
        elif len(word) > 5 and s[s_index].isalpha():
            word = ''
            while s[s_index].isalpha(): s_index += 1
        # if we got to seperator and word wasn't discarded (meaning it's valid) add it to set
        elif not s[s_index].isalpha() and word:
            # if word is 3-5 in length add it to set
            if len(word) >=3:
                word_set.add(word)
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
def random_file_word(file_name : str)->str:
    with open(file_name,'r') as f:
        words = f.readlines()
    random_index = random.randint(0,len(words)-1)
    return words[random_index]

#Main
with open("story",'r') as f:
    l = f.readlines()
    s = ''.join(l)
set_to_file("words",str_to_short_word_set(s))
print(random_file_word("words"))