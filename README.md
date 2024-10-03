# SentimentScope

**SentimentScope** is a web-based sentiment analysis tool built with Flask and NLTK. It analyzes the sentiment of user-provided text and categorizes it into positive, neutral, or negative sections based on VADER (Valence Aware Dictionary and sEntiment Reasoner). The app also highlights the respective text fragments that contribute to each sentiment category.

## Features
- Real-time text sentiment classification.
- Sentiment breakdown into positive, neutral, and negative categories.
- User-friendly interface to input text and view results.
- Mobile-responsive and optimized for various screen sizes.

## Technology Stack
- **Frontend**: HTML, CSS, JavaScript (with Fetch API).
- **Backend**: Flask (Python).
- **Sentiment Analysis**: NLTK (VADER SentimentIntensityAnalyzer).

## How it Works
1. Users input a sentence or paragraph.
2. The app uses the VADER sentiment analysis model to compute sentiment scores.
3. Based on the scores, it categorizes each part of the text as positive, neutral, or negative.
4. The respective sentiment percentages and text sections are displayed.

## Installation and Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Bagora/sentimentscope.git
    ```

2. **Navigate to the project directory**:
    ```bash
    cd SentimentScope
    ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app locally**:
    ```bash
    flask run
    ```

## Deployment
The app is deployed on [PythonAnywhere](https://www.pythonanywhere.com), a cloud platform for hosting Python web apps.

## Usage
1. Navigate to the deployed app on PythonAnywhere.
2. Enter a sentence or paragraph in the provided text box.
3. Press "Analyze Sentiment" to view the sentiment breakdown.

## Future Enhancements
- Implement multi-language sentiment analysis.
- Improve accuracy for more complex texts.
- Provide graphical sentiment representation.
