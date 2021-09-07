import numpy as np
import nltk
# nltk.download('punkt')

# lancaster to gain speed but is not as good as the others
#from nltk.stem.lancaster import LancasterStemmer
#stemmerEn = LancasterStemmer("")
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
stemmerEng = PorterStemmer()
stemmerSpa = SnowballStemmer("spanish")


def tokenize(sentence):
    """
    split sentence into array of words/tokens
    a token can be a word or punctuation character, or number
    """
    return nltk.word_tokenize(sentence)


def stem(word, lang='es'):
    """
    stemming = find the root form of the word
    examples:
    words = ["organize", "organizes", "organizing"]
    words = [stem(w) for w in words]
    -> ["organ", "organ", "organ"]
    """
    stemed = None
    if lang == 'en':
        stemed = stemmerEng.stem(word.lower())
    elif lang == 'es':
        stemed = stemmerSpa.stem(word.lower())

    return stemed


def bag_of_words(tokenized_sentence, words, lang):
    """
    return bag of words array:
    1 for each known word that exists in the sentence, 0 otherwise
    example:
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
    """
    # stem each word
    sentence_words = [stem(word, lang) for word in tokenized_sentence]
    # initialize bag with 0 for each word
    bag = np.zeros(len(words), dtype=np.float32)
    for idx, w in enumerate(words):
        if w in sentence_words:
            bag[idx] = 1

    return bag
