import os
import sys
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from flask import Flask, request, render_template

# Replace with your Azure Text Analytics endpoint and key
endpoint = "https://commoncognitiveservice.cognitiveservices.azure.com/"
key = "6e026ea53ae947afba3e7a1e587cb3cc"

# Initialize the Text Analytics client
credential = AzureKeyCredential(key)
text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def analyze_and_categorize_text():
    if request.method == 'POST':
        text = request.form['text']
        result, category = analyze_text(text)
        return render_template('index.html', text=text, result=result, category=category)
    return render_template('index.html', text='', result='', category='')

def analyze_text(text):
    try:
        documents = [text]
        response = text_analytics_client.extract_key_phrases(documents=documents)
        key_phrases = response[0].key_phrases
        category = categorize_key_phrases(key_phrases)
        return text, category
    except Exception as e:
        print("Error:", str(e))
        return "Error", "Uncategorized"

def categorize_key_phrases(key_phrases):
    performance_keywords = ["slow"]
    security_keywords = ["security"]
    technical_keywords = ["javascript", "page"]

    for phrase in key_phrases:
        phrase = phrase.lower()  # Convert to lowercase for case-insensitive matching
        if any(keyword in phrase for keyword in performance_keywords):
            return "Performance Related"
        elif any(keyword in phrase for keyword in security_keywords):
            return "Security Related"
        elif any(keyword in phrase for keyword in technical_keywords):
            return "Technical Related"

    return "Uncategorized"

if __name__ == '__main__':
    app.run(debug=True)
