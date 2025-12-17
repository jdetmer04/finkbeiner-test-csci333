import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf
import json

from tensorflow.keras import layers
from tensorflow.keras import losses

# Add standardization function
def custom_standardization(input_data):
    lowercase = tf.strings.lower(input_data)
    # Keep only alphanumeric, spaces, and common punctuation
    stripped = tf.strings.regex_replace(lowercase, r'[^\w\s\.,\!\?\'"]', '')
    return stripped

train_dir = 'data/train'
test_dir = 'data/test'

batch_size = 10
seed = 67

raw_train_ds = tf.keras.utils.text_dataset_from_directory(
    train_dir,
    batch_size=batch_size,
    seed=seed,
    labels='inferred')

raw_test_ds = tf.keras.utils.text_dataset_from_directory(
    test_dir,
    batch_size=batch_size)

max_features = 10000
sequence_length = 250

vectorize_layer = layers.TextVectorization(
    standardize=custom_standardization,  # Add standardization
    max_tokens=max_features,
    output_mode='int',
    output_sequence_length=sequence_length)

# Adapt the vectorization layer
train_text = raw_train_ds.map(lambda x, y: x)
vectorize_layer.adapt(train_text)

embedding_dim = 16

# Build the complete model
complete_model = tf.keras.Sequential([
    vectorize_layer,
    layers.Embedding(max_features, embedding_dim),
    layers.Dropout(0.2),
    layers.GlobalAveragePooling1D(),
    layers.Dropout(0.2),
    layers.Dense(3, activation='softmax')
])

# Compile the model
complete_model.compile(loss=losses.SparseCategoricalCrossentropy(),
                       optimizer='adam',
                       metrics=[tf.metrics.SparseCategoricalAccuracy()])

# Train the complete model
epochs = 20
history = complete_model.fit(
    raw_train_ds,
    epochs=epochs)

# Evaluate
loss, accuracy = complete_model.evaluate(raw_test_ds)
print(f"Loss: {loss}, Accuracy: {accuracy}")

# Save the complete model including preprocessing
complete_model.save('trained_model.keras')

# ALSO save just the text vectorization layer for debugging
import pickle
vocab = vectorize_layer.get_vocabulary()
with open('vectorizer_vocab.pkl', 'wb') as f:
    pickle.dump(vocab, f)
print(f"Vocabulary saved with {len(vocab)} words")
