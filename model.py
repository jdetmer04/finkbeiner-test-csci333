import matplotlib.pyplot as plt
import os
import re
import shutil
import string
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
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


# calculate precision and recall, comment this out if you dont want it
'''
# Get predictions for precision/recall calculation
print("\n" + "="*60)
print("PRECISION AND RECALL ANALYSIS")
print("="*60)

# Collect all true labels and predictions
y_true = []
y_pred = []

for text_batch, label_batch in raw_test_ds:
    # Get predictions for this batch
    predictions = complete_model.predict(text_batch, verbose=0)
    # Convert softmax outputs to class predictions (0, 1, or 2)
    pred_classes = np.argmax(predictions, axis=1)
    
    y_true.extend(label_batch.numpy())
    y_pred.extend(pred_classes)

# Convert to numpy arrays
y_true = np.array(y_true)
y_pred = np.array(y_pred)

# Calculate and print detailed metrics
print("\nClassification Report:")
print(classification_report(y_true, y_pred, 
                           target_names=['Not Biased (0)', 'Little Biased (1)', 'Very Biased (2)']))

# Calculate confusion matrix
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)
print("\nRows = True Labels, Columns = Predicted Labels")
print("Format: [[TN, FN, FN], [FP, TP, FP], [FP, FN, TP]] for each class")

# Calculate precision and recall manually for each class
for class_idx, class_name in enumerate(['Not Biased', 'Little Biased', 'Very Biased']):
    # For each class, treat it as "positive" and others as "negative"
    TP = np.sum((y_true == class_idx) & (y_pred == class_idx))
    FP = np.sum((y_true != class_idx) & (y_pred == class_idx))
    FN = np.sum((y_true == class_idx) & (y_pred != class_idx))
    
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    
    print(f"\n{class_name} (Class {class_idx}):")
    print(f"  Precision: {precision:.3f} ({TP}/{TP+FP})")
    print(f"  Recall:    {recall:.3f} ({TP}/{TP+FN})")
    print(f"  TP: {TP}, FP: {FP}, FN: {FN}")'''