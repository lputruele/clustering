import nltk
from nltk.corpus import stopwords
from collections import Counter
import codecs
from sklearn.cluster import KMeans
from sklearn import preprocessing 
from scipy.sparse import coo_matrix
import numpy

TEXT_FILE = 'resources/test.txt'	# Text to be processed
MIN_FREQUENCY = 20	# Min word frequency to be considered
#MIN_SENT_LENGTH = 10 # Sentence word count threshold
CLUSTERS_NUMBER = 80 # Number of clusters of words
WINDOWS_SIZE = 5 # Windows size to determine the contexts

def read_file():
	# Read the file TEXT_FILE.
	print("Loading file",TEXT_FILE)
	f = codecs.open(TEXT_FILE,'r','latin1')
	content = f.read()
	return content

def create_cooccurrence_matrix(words,frequent_words):
	# Create coocurrence matrix. Only create columns for those words that are in frequent_words
	print("\nCreating co-occurrence matrix")
	set_all_words={}
	set_freq_words={}
	data=[]
	row=[]
	col=[]
	for pos,token in enumerate(words):
		i=set_all_words.setdefault(token,len(set_all_words))
		start=max(0,pos-WINDOWS_SIZE)
		end=min(len(words),pos+WINDOWS_SIZE+1)
		for pos2 in range(start,end):
			if pos2==pos or words[pos2] not in frequent_words:
				continue
			j=set_freq_words.setdefault(words[pos2],len(set_freq_words))
			data.append(1.); row.append(i); col.append(j);
	cooccurrence_matrix=coo_matrix((data,(row,col)))
	print("Vocabulary size:",len(set_all_words))
	print("Matrix shape:",cooccurrence_matrix.shape)
	print("Co-occurrence matrix finished")
	return set_all_words,set_freq_words,cooccurrence_matrix

def tokenize(text):
	# Tokenize and normalize the given text.	
	tokens = nltk.word_tokenize(text)

	tokens = [token.lower() for token in tokens]	# All tokens to lowercase

	words = [token for token in tokens if token.isalpha()]	# Maintain strings with alphabetic characters

	words = [token for token in words if token not in stopwords.words('spanish')] # Remove stopwords

	lemmatized = [lemmatize(t) for t in words] # Lemmatization

	return lemmatized

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

def gen_clusters(vectors):
	# Generate word clusters using the k-means algorithm.
	print("\nClustering started")
	vectors = preprocessing.normalize(vectors)
	km_model = KMeans(n_clusters=CLUSTERS_NUMBER)
	km_model.fit(vectors)
	print("Clustering finished")
	return km_model

def frequent_words(words):
	# Returns the words that appear at least MIN_FREQUENCY times
	print("\nGetting most frequent words")
	most_frequents = []
	counter = Counter(words)
	for w in counter:
		if (counter[w]>=MIN_FREQUENCY):
			most_frequents.append(w)
	print("Most frequent words calculated. Total:",str(len(most_frequents)))
	#print("Most frequent words:",most_frequents)
	return most_frequents

def show_results(vocabulary,features,model):
	# Show results
	c = Counter(sorted(model.labels_))
	print("\nTotal clusters:",len(c))
	for cluster in c:
		print ("Cluster#",cluster," - Total words:",c[cluster])

	# Show top terms and words per cluster
	print("Top terms and words per cluster:")
	print()
	#sort cluster centers by proximity to centroid
	order_centroids = model.cluster_centers_.argsort()[:, ::-1] 

	keysFeatures = list(features.keys())
	keysVocab = list(vocabulary.keys())
	for n in range(len(c)):
		print("Cluster %d" % n)
		print("Frequent terms:", end='')
		for ind in order_centroids[n, :10]:
			print(' %s' % keysFeatures[ind], end=',')

		print()
		print("Words:", end='')
		word_indexs = [i for i,x in enumerate(list(model.labels_)) if x == n]
		#word_indexs =word_indexs[:20]
		for i in word_indexs:
			print(' %s' % keysVocab[i], end=',')
		print()
		print()

	print()

if __name__ == "__main__":

	file_content = read_file() # Read the TEXT_FILE

	lemma_dict = read_lemmas() # Read the lemmatization file

	words = tokenize(file_content)

	frequent_words = frequent_words(words) # Get the most frequent words

	vocabulary, features, vectors = create_cooccurrence_matrix(words,frequent_words) # Create the co-occurrence matrix

	km_model = gen_clusters(vectors) # Generate clusters

	show_results(vocabulary,features,km_model)
