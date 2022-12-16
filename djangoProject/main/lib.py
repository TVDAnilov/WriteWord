import re


def clear_text(words_in_text):
    words = []
    count_meets = 0
    words_in_text = words_in_text.lower()
    words_in_text = re.split(r"\W", words_in_text)
    for i, word in enumerate(words_in_text):
        word = re.sub(r"\d", '', word)
        tmp = re.findall(r"_", word)
        if len(tmp) != 0:
            word = ''
        tmp = re.findall(r"(.)\1{2,}", word)
        if len(tmp) != 0:
            word = ''

        if len(word) <= 2:
            word = ''
        if len(word) <= 5:
            tmp = re.findall(r"[wrtpsdfghjklzxcvbnm][wrtpsdfghjklzxcvbnm][wrtpsdfghjklzxcvbnm][wrtpsdfghjklzxcvbnm]", word)
            if len(tmp) != 0:
                word = ''
        if len(word) <= 4:
            tmp = re.findall(r"[wrtpsdfghjklzxcvbnm][wrtpsdfghjklzxcvbnm][wrtpsdfghjklzxcvbnm]", word)
            if len(tmp) != 0:
                word = ''

        words_in_text[i] = word
    #                print(word)
    words_in_text = list(filter(len, words_in_text))
    for i, word in enumerate(words_in_text, start=0):
        if word == "":
            continue
        #                print("i = ", i, word)
        count_meets = 1
        for j in range(i, len(words_in_text)):
            #                    print("j = ", j, words_in_text[j])
            #                    print(words_in_text)

            if (word == words_in_text[j]) and (j != i):
                count_meets = count_meets + 1
                words_in_text[j] = ''

        words.append(dict(word=word, CountMeets=count_meets))

    #    words_in_text = list(filter(len, words_in_text))
    return words
