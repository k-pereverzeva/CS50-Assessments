from cs50 import get_string


def main():
    text = get_string("Text: ")
    num_let = count_letters(text)
    num_words = count_words(text)
    num_sent = count_sentences(text)
    
    L = num_let * 100 / num_words
    S = num_sent * 100 / num_words
    index = round(0.0588 * L - 0.296 * S - 15.8)
    
    if index < 1:
        print('Before Grade 1')
    elif index >= 16:
        print('Grade 16+')
    else:
        print(f'Grade {index}')
     
        
def count_letters(text):
    letters = 0
    for i in range(len(text)):
        if text[i].isalpha():
            letters += 1
    return letters
    
    
def count_words(text):
    words = 1
    for i in range(len(text)):
        if text[i] == ' ':
            words += 1
    return words
    
    
def count_sentences(text):
    sentences = 0
    for i in range(len(text)):
        if text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences += 1
    return sentences
    
    
main()