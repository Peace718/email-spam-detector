from flask import Flask, render_template, request, make_response
import joblib

app = Flask(__name__)

# Load the trained model
model = joblib.load('mnb_email_spam_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    email_text = request.form['email']

    # Predict class
    prediction = model.predict([email_text])[0]

    # Predict probability
    proba = model.predict_proba([email_text])[0]
    confidence = round(max(proba) * 100, 2)

    # Map label
    label_map = {0: "Not Spam", 1: "Spam"}
    result = label_map[prediction]

    return render_template('result.html', prediction=result, confidence=confidence, email=email_text)

@app.route('/download', methods=['POST'])
def download():
    email_text = request.form['email']
    prediction = request.form['prediction']
    confidence = request.form['confidence']

    content = f"""Email Spam Detection Result

Original Email:
--------------------
{email_text}

Prediction: {prediction}
Confidence: {confidence}%
"""

    response = make_response(content)
    response.headers['Content-Disposition'] = 'attachment; filename=spam_result.txt'
    response.mimetype = 'text/plain'
    return response

if __name__ == '__main__':
    app.run(debug=True)

    

