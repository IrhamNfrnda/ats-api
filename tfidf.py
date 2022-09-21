import re
import nltk
import pandas as pd
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import TfidfVectorizer


nltk.download('stopwords')
nltk.download('punkt')

def best_term(dokumen):
    dokumen = dokumen.replace('\n', '')
    sentence = re.split('\. |\.',dokumen)

    #Tokenize
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    tokenized = [tokenizer.tokenize(s.lower()) for s in sentence]

    #Filtering
    listStopword = nltk.corpus.stopwords.words('indonesian')
    newStopword = ["ya", "kau", "yg", "tu", "ni", "aja", "aje", "ade", "si", "aku", "lah", "tak", "di", "lagi", "ada",
                   "gk", "ape", "nya", "https", "terimakasih", "makasih", "assalamualaikum", "2020", "2021", "2022",
                   "jam", "riau", "amik", "masuk", "link", "selamat", "silahkan", "info", "tanggal", "mohon", "nama",
                   "mengisi", "besok", "pemberitahuan", "ga", "nama", "terima", "kasih", "wassalamualaikum", "amin", "aamiin", "amiin", "baik", "pak", "yok",
                   "thank", "thanks", "kak", "bang", "kakk", "oke", "you", "i", "and"]
    number = []
    for i in range(100):
        number.append(str(i))

    listStopword.extend(newStopword)
    listStopword.extend(number)

    important_token = []
    for sent in tokenized:
        filtered = [s for s in sent if s not in listStopword]
        important_token.append(filtered)

    sw_removed = [' '.join(t) for t in important_token]

    #stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    stemmed_sent = [stemmer.stem(sent) for sent in sw_removed]

    #TF-IDF
    vec = TfidfVectorizer(max_features=10, lowercase=True, binary=True)
    document = vec.fit_transform(stemmed_sent)
    document = document.toarray()

    terms = vec.get_feature_names()
    sums = document.sum(axis=0)

    data = []
    for col, term in enumerate(terms):
        data.append((term, sums[col]))

    ranking = pd.DataFrame(data, columns=['term', 'rank'])
    ranking = ranking.sort_values('rank', ascending=False)

    best_term = []
    for term in ranking["term"]:
        best_term.append(term)

    return best_term

