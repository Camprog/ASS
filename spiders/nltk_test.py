import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#nltk.download('all')

class Nltk():
    def __init__(self):
        f = open('article.txt', 'rU')
        self.content = f.read()
        fullf = open('fullarticle.txt', 'rU')
        self.fullcontent = fullf.read()
        self.stopWords = set(stopwords.words('english'))
        # stemming
        self.lemma = nltk.wordnet.WordNetLemmatizer()
        self.stemmer = nltk.SnowballStemmer("english")
    def Freqwordss(self):

        tokens = nltk.word_tokenize(self.content)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)

        filtered_word = nltk.word_tokenize(self.content)
        # Remove single-character tokens (mostly punctuation)
        filtered_word = [word for word in filtered_word if len(word) > 3]
        # Remove numbers
        filtered_word = [word for word in filtered_word if not word.isnumeric()]
        # Remove basic english words
        filtered_word = [word for word in filtered_word if word not in self.stopWords]
        #remove majuscule
        filtered_word = [word.lower() for word in filtered_word]

        wnl = WordNetLemmatizer()
        fdist = nltk.FreqDist(filtered_word)

        for word, frequency in fdist.most_common(50):
            print(u'{};{};{};{}'.format(word, wnl.lemmatize(word), self.stemmer.stem(word), self.lemma.lemmatize(word), frequency))

    def corpus(self, spliter):
        matrix=[]
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
        matrix=[]
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
    process.split_ngram(spliter=str("."))
    process.corpus(spliter=str("."))
