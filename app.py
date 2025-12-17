import tensorflow as tf
from flask import Flask, request, render_template, jsonify
import numpy as np
from keras.saving import register_keras_serializable

app = Flask(__name__)

# IMPORTANT: Define AND register the custom function BEFORE loading the model
@register_keras_serializable()
def custom_standardization(input_data):
    """This must be exactly the same function used during training"""
    lowercase = tf.strings.lower(input_data)
    # Keep only alphanumeric, spaces, and common punctuation
    stripped = tf.strings.regex_replace(lowercase, r'[^\w\s\.,\!\?\'"]', '')
    return stripped

print("Loading model...")
# Now load the model (the function is already registered)
model = tf.keras.models.load_model('trained_model.keras')
print("Model loaded successfully!")

# Define class names
CLASS_NAMES = {
    0: "Compliant (Low Bias)",
    1: "Partially Compliant (Some Bias)", 
    2: "Violates Test (High Bias)"
}

# Helper function to preprocess input text
def preprocess_text(text):
    text_tensor = tf.constant([text])
    return text_tensor

# Simple index route
@app.route('/')
def index():
    return '''
    <html>
        <head><title>Gender Bias Analyzer</title></head>
        <body>
            <h1>Gender Bias Analyzer</h1>
            <p>Paste text to analyze for gender bias in science journalism.</p>
            <form action="/predict" method="post">
                <textarea name="text" rows="10" cols="80" placeholder="Paste article text here..."></textarea><br>
                <input type="submit" value="Analyze">
            </form>
        </body>
    </html>
    '''

@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text', '')
    if not text:
        return "Please enter some text", 400
    
    try:
        processed_text = preprocess_text(text)
        predictions = model.predict(processed_text, verbose=0)
        predicted_class = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_class]) * 100
        
        result = f'''
        <html>
            <body>
                <h2>Analysis Results</h2>
                <p><strong>Text analyzed:</strong> {text[:200]}{'...' if len(text) > 200 else ''}</p>
                <p><strong>Prediction:</strong> {CLASS_NAMES[predicted_class]}</p>
                <p><strong>Confidence:</strong> {confidence:.1f}%</p>
                <p><strong>All probabilities:</strong></p>
                <ul>
                    <li>Compliant: {predictions[0][0] * 100:.1f}%</li>
                    <li>Partially compliant: {predictions[0][1] * 100:.1f}%</li>
                    <li>Biased: {predictions[0][2] * 100:.1f}%</li>
                </ul>
                <p><a href="/">Analyze another</a></p>
            </body>
        </html>
        '''
        return result
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)