import nltk
from nltk.corpus import stopwords
from collections import Counter
import codecs
import re
from sklearn.cluster import KMeans
from sklearn import preprocessing 
from gensim.models import Word2Vec
import numpy

TEXT_FILE = 'resources/farkas.txt' # Text to be processed
CLUSTERS_NUMBER = 80 # Number of clusters of words

def readFile():
	# Read the file TEXT_FILE.
	print("Loading file",TEXT_FILE)
	f = codecs.open(TEXT_FILE,'r','latin1')
	content = f.read()
	return content

def process_tokens(tokens):
	# Process the given list of tokens
	tokens = [token.lower() for token in tokens]	# All tokens to lowercase

	words = [token for token in tokens if token.isalpha()]	# Maintain strings with alphabetic characters

	words = [token for token in words if token not in stopwords.words('spanish')] # Remove stopwords

	lemmatized = [lemmatize(t) for t in words] # Lemmatization

	return lemmatized	

def tokenize(text):
	# Tokenize and normalize the given text.
	sents = nltk.sent_tokenize(text)

	tokenized_sents = [nltk.word_tokenize(sent) for sent in sents]

	tokenized_sents = [process_tokens(sent) for sent in tokenized_sents]

	return tokenized_sents

def read_lemmas():
	lemma_file = open("lemmatization-es.txt", "r")
	lemma_raw = lemma_file.read()
	lemmas = lemma_raw.split("\n")

	lemma_dict = {}
	for pair in lemmas:
	    w = pair.split("\t")
	    if len(w) == 2:
	        lemma_dict[w[1]] = w[0]
	return lemma_dict

def lemmatize(word):
    if word in lemma_dict:
        word = lemma_dict[word]
    return word

def gen_vectors(normalized_text):
	# Generate word vectors using neural word embeddings
	print("\nGenerating word vectors")
	model = Word2Vec(normalized_text, window=5, min_count=1)
	vects = []
	for word in model.wv.key_to_index:
		vects.append(model.wv[word])

	matrix = numpy.array(vects)
	print("Matrix shape:",matrix.shape)
	print("Vectors generated")
	return model.wv.key_to_index,matrix

def gen_clusters(vectors):
	# Generate word clusters using the k-means algorithm.
	print("\nClustering started")
	vectors = preprocessing.normalize(vectors)
	km_model = KMeans(n_clusters=CLUSTERS_NUMBER)
	km_model.fit(vectors)
	print("Clustering finished")
	return km_model

def show_results(vocabulary,model):
	# Show results
	c = Counter(sorted(model.labels_))
	print("\nTotal clusters:",len(c))
	for cluster in c:
		print ("Cluster#",cluster," - Total words:",c[cluster])

	# Show top terms and words per cluster
	print("Top words per cluster:")
	print()

	keysVocab = list(vocabulary.keys())
	for n in range(len(c)):
		print("Cluster %d" % n)
		print("Words:", end='')
		word_indexs = [i for i,x in enumerate(list(model.labels_)) if x == n]
		for i in word_indexs:
			print(' %s' % keysVocab[i], end=',')
		print()
		print()

	print()
if __name__ == "__main__":

	file_content = readFile() # Read the TEXT_FILE

	lemma_dict = read_lemmas() # Read the lemmatization file

	normalized = tokenize(file_content)

	vocabulary, vectors = gen_vectors(normalized)

	km_model = gen_clusters(vectors) # Generate clusters

	show_results(vocabulary,km_model)



