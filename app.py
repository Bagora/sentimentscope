from flask import Flask, render_template, request, jsonify
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import pickle
import string

app = Flask(__name__)

nltk.download('punkt')

# Load the English tokenizer from the pickle file
def load_tokenizer(pickle_path):
    try:
        with open(pickle_path, 'rb') as f:
            tokenizer = pickle.load(f)
        return tokenizer
    except Exception as e:
        print("Error loading tokenizer:", e)
        return None

# Load the tokenizer
english_pickle_path = os.path.join(os.getcwd(), 'english.pickle')
tokenizer = load_tokenizer(english_pickle_path)

# Initialize the sentiment analyzer (VADER lexicon is already included)
sid = SentimentIntensityAnalyzer()

import string

def analyze_text_parts(text):
    try:
        # Split text into sentences and words
        sentences = nltk.sent_tokenize(text)
        words = text.split()  # Split entire text into words
        positive = []
        neutral = []
        negative = []
        
        # Analyze each sentence
        for sentence in sentences:
            sentence_clean = sentence.translate(str.maketrans('', '', string.punctuation))
            scores = sid.polarity_scores(sentence_clean)
            compound_score = scores['compound']
            
            if compound_score > 0.05:
                positive.append(sentence)
            elif compound_score < -0.05:
                negative.append(sentence)
            else:
                neutral.append(sentence)
        
        # Analyze each word separately
        for word in words:
            word_clean = word.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation from word
            scores = sid.polarity_scores(word_clean)
            compound_score = scores['compound']
            
            # Add words to the correct category if not already part of the sentences
            if compound_score > 0.05 and word_clean not in positive:
                positive.append(word)
            elif compound_score < -0.05 and word_clean not in negative:
                negative.append(word)
            elif compound_score >= -0.05 and compound_score <= 0.05 and word_clean not in neutral:
                neutral.append(word)

        return {
            'positive': " ".join(positive) if positive else "No positive sentiment detected.",
            'neutral': " ".join(neutral) if neutral else "No neutral sentiment detected.",
            'negative': " ".join(negative) if negative else "No negative sentiment detected."
        }
    except Exception as e:
        print("Error analyzing text parts:", e)
        return {'positive': 'Error', 'neutral': 'Error', 'negative': 'Error'}


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    text = request.json.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided for analysis.'}), 400
    
    try:
        sentiment_scores = sid.polarity_scores(text)
        overall_sentiment = 'neutral'

        if sentiment_scores['compound'] > 0.05:
            overall_sentiment = 'positive'
        elif sentiment_scores['compound'] < -0.05:
            overall_sentiment = 'negative'
        
        text_parts = analyze_text_parts(text)
        
        return jsonify({
            'sentiment': overall_sentiment,
            'scores': sentiment_scores,
            'text_parts': text_parts
        })
    
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
