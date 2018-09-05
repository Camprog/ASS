import ngram as ngram
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
from scipy.sparse import csr_matrix
from nltk.util import ngrams
#nltk.download('all')

class Nltk():
    def __init__(self):
        fullf = open('fullarticle.txt', 'rU')
        f = open('article.txt', 'rU')
        self.content = f.read()
        f.close()
        self.fullcontent = fullf.read()
        self.stopWords = set(stopwords.words('english'))
        # stemming
        self.lemma = nltk.wordnet.WordNetLemmatizer()
        self.stemmer = nltk.SnowballStemmer("english")

    def Nlp_article(self):

        tokens = nltk.word_tokenize(self.content)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)

        filtered_word = nltk.word_tokenize(self.content)
        # Remove single-character tokens (mostly punctuation)
        filtered_word = [word for word in filtered_word if len(word) > 1]
        # Remove numbers
        filtered_word = [word for word in filtered_word if not word.isnumeric()]
        # Remove basic english words
        filtered_word = [word for word in filtered_word if word not in self.stopWords]
        # remove majuscule
        filtered_word = [word.lower() for word in filtered_word]
        filtered_word = [self.lemma.lemmatize(word) for word in filtered_word]
        wnl = WordNetLemmatizer()
        fdist = nltk.FreqDist(filtered_word)
        print(filtered_word)

        #mot + emplacement dans la matrice
        vocab_to_index = {word: i for i, word in enumerate(filtered_word)}
        print(vocab_to_index)

        #finder = bigram de la liste de mot
        finder = list(nltk.bigrams(filtered_word))
        print(finder)

        #bigram_freq est la list du bigram ainsi que la frequence
        bigram_freq = nltk.FreqDist(finder).most_common(len(finder))
        print(len(filtered_word))
        co_occurrence_matrix = np.zeros((len(filtered_word), len(filtered_word)))

        for bigram in bigram_freq:
            current = bigram[0][1]
            previous = bigram[0][0]
            count = bigram[1]

            pos_current = vocab_to_index[current]
            pos_previous = vocab_to_index[previous]
            co_occurrence_matrix[pos_current][pos_previous] = count

        co_occurrence_matrix = csr_matrix(np.matrix(co_occurrence_matrix))
        print(co_occurrence_matrix)

    def corpus(self, spliter):
        matrix = []
        filtered_word = self.fullcontent.split(spliter)

        filtered_word = [word.lower() for word in filtered_word]
        filtered_word = [word.split() for word in filtered_word]

        for word in filtered_word:
            word = [words for words in word if words not in self.stopWords]
            word = [words for words in word if len(words) > 3]
            word = [words for words in word if not words.isnumeric()]
            matrix.append(word)

        print(matrix)

    def split_ngram(self, spliter):
        matrix = []
        filtered_word = self.content.split(spliter)

        filtered_word = [word.lower() for word in filtered_word]
        filtered_word = [word.split() for word in filtered_word]

        for word in filtered_word:
            word = [words for words in word if words not in self.stopWords]
            word = [words for words in word if len(words) > 3]
            word = [words for words in word if not words.isnumeric()]
            matrix.append(word)

        print(matrix)


if __name__ == "__main__":
    process = Nltk()
    # process.split_ngram(spliter=str("."))
    # process.corpus(spliter=str("."))
    process.Nlp_article()
