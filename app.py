from flask import Flask, render_template, request, jsonify
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import string
import pickle

app = Flask(__name__)

# Specify the path to your local nltk_data folder
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
nltk.data.path.append(nltk_data_path)

# Load the English tokenizer manually from the pickle file in your local folder
def load_tokenizer(pickle_path):
    try:
        with open(pickle_path, 'rb') as f:
            tokenizer = pickle.load(f)
        return tokenizer
    except Exception as e:
        print("Error loading tokenizer:", e)
        return None

# Set the local path for the Punkt tokenizer (English)
english_pickle_path = os.path.join(nltk_data_path, 'tokenizers', 'punkt', 'english.pickle')
tokenizer = load_tokenizer(english_pickle_path)

if tokenizer is None:
    raise FileNotFoundError(f"Punkt tokenizer not found at {english_pickle_path}")

# Manually load the VADER lexicon
vader_lexicon_path = os.path.join(nltk_data_path, 'sentiment', 'vader_lexicon', 'vader_lexicon.txt')
if not os.path.exists(vader_lexicon_path):
    raise FileNotFoundError(f"VADER lexicon not found at {vader_lexicon_path}")

# Manually load the VADER lexicon file
def load_vader_lexicon(lexicon_path):
    lexicon = {}
    with open(lexicon_path, 'r') as file:
        for line in file:
            if not (line.strip() and not line.startswith(';')):
                continue
            word, measure = line.strip().split('\t')[0:2]
            lexicon[word] = float(measure)
    return lexicon

# Initialize the sentiment analyzer with the manually loaded lexicon
vader_lexicon = load_vader_lexicon(vader_lexicon_path)
sid = SentimentIntensityAnalyzer()
sid.lexicon.update(vader_lexicon)

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
