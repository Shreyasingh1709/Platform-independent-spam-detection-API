from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, GRU, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Tokenize
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(data['cleaned'])

sequences = tokenizer.texts_to_sequences(data['cleaned'])
X = pad_sequences(sequences, maxlen=100)
y = data['label']

# Model
model_dl = Sequential()
model_dl.add(Embedding(5000, 128))
model_dl.add(LSTM(64, return_sequences=True))
model_dl.add(GRU(32))
model_dl.add(Dense(1, activation='sigmoid'))

model_dl.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model_dl.fit(X, y, epochs=3, batch_size=32)

print("LSTM-GRU model trained (for documentation/demo)")