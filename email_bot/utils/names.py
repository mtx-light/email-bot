with open('./email_bot/utils/names.txt') as f:
    names = set(l.strip() for l in f.readlines())

def get_name(text):
    for input_word in text.split():
        cap_word = input_word.capitalize()
        if cap_word in names:
            return cap_word
