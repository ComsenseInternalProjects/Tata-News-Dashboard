import spacy
from textblob import TextBlob
# Load the SpaCy model for Named Entity Recognition
nlp = spacy.load("en_core_web_sm")

# List of keywords for Tata Motors and competitors
tata_keywords = ["Tata Motors", "Tata Commercial Vehicles", "Tata Trucks", "Tata", "commercial vehicles","automotive industry", "automobile industry","automobile sector"]
competitor_keywords = ["Ashok Leyland", "Mahindra", "Volvo Eicher", "BharatBenz", "Eicher Motors", "MAN Trucks", "Isuzu", "SML Isuzu"]

# Function to perform sentiment analysis and filter based on sentiment score
def analyze_sentiment(article_body):
    # print("************************************")
    # print(article_body)

    blob = TextBlob(article_body)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.2 or sentiment_score < 0:
        return True
    else:
        return False

# Function to check if an article is relevant to Tata Motors or its competitors
def is_relevant(article_body):

    # Named Entity Recognition
    doc = nlp(article_body)
    for ent in doc.ents:
        if ent.text.lower() in [keyword.lower() for keyword in tata_keywords + competitor_keywords]:
            return True
            
    return False

if __name__ == "__main__":
    # Example usage 
    article_title = "Tata Motors to launch new electric vehicle in 2023"
    article_body = "Tata Motors, a leading Indian automobile manufacturer, is set to launch a new electric vehicle in 2023. The company has been investing heavily in electric vehicle technology and is expected to introduce a range of electric vehicles in the coming years."
    print(is_relevant(article_title, article_body))



