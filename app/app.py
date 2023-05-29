from flask import Flask, request, jsonify
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)

# Load the vectorizer and model
vector_form = pickle.load(open('vector.pkl', 'rb'))
load_model = pickle.load(open('multi_model.pkl', 'rb'))

# Preprocessing function
def stemming(content):
    ps = PorterStemmer()
    con = re.sub('[^a-zA-z]', ' ', content)
    con = con.lower()
    con = con.split()
    con = [ps.stem(word) for word in con if not word in stopwords.words('english')]
    con = ' '.join(con)
    return con

@app.route('/predict', methods=['POST'])
def predict():
    # Get the request data
    news = request.json['news']

    # Preprocess the news
    news = stemming(news)

    # Vectorize the input data using the loaded vectorizer
    vector_form1 = vector_form.transform([news])

    # Make the prediction using the loaded model
    prediction = load_model.predict(vector_form1)

    # Return the prediction as a JSON response
    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)