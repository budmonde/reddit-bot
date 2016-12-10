# Small LSTM Network to Generate Text for Alice in Wonderland
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
# load ascii text and covert to lowercase
filename = "./data/redditcomments.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()
raw_words = raw_text.split()

raw_comments = raw_text.split('\n')
raw_words_with_spaces = []

for comment in raw_comments:
	words_in_comment = comment.split()
	for word in words_in_comment:
		raw_words_with_spaces.append(word)
		# raw_words_with_spaces.append(' ')
	# raw_words_with_spaces.pop()
	# raw_words_with_spaces.append('\n')
# raw_words_with_spaces.pop()

# create mapping of unique words to integers
words = sorted(list(set(raw_words)))
word_to_int = dict((c, i) for i, c in enumerate(words))
word_to_int[' '] = len(words)
word_to_int['\n'] = len(words) + 1

# summarize the loaded data
n_words = len(raw_words_with_spaces)
n_vocab = len(words)
print "Total Words: ", n_words
print "Total Vocabs: ", n_vocab
# prepare the dataset of input to output pairs encoded as integers
seq_length = 25
dataX = []
dataY = []

for i in range(0, n_words - seq_length, 1):
	seq_in = raw_words_with_spaces[i:i + seq_length]
	seq_out = raw_words_with_spaces[i + seq_length]
	dataX.append([word_to_int[word] for word in seq_in])
	dataY.append(word_to_int[seq_out])

n_patterns = len(dataX)
print "Total Patterns: ", n_patterns
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
filename = "./biggerwordsredditcomments/bigger-word-weights-improvement-19-6.9978.hdf5"
model.load_weights(filename)
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
filepath="./biggerwordsredditcomments/bigger-word-weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(X, y, nb_epoch=80, batch_size=64, callbacks=callbacks_list)