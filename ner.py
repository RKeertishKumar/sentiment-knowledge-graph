from transformers import pipeline
import csv

# Function to read the cleaned news titles from a CSV file
def read_cleaned_titles_from_csv(filename):
    titles = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Check if the row is not empty
                titles.append(row[0])  # Assuming titles are in the first column
    return titles

# Load pre-trained NER model
ner_model = pipeline("ner", model="xlm-roberta-large-finetuned-conll03-english")

# Load sentiment analysis model
sentiment_model = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Function to perform NER and Sentiment Analysis and save results to CSV
def analyze_and_save_to_csv(titles, output_filename):
    with open(output_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Entities', 'Sentiment', 'Sentiment Score'])

        for title in titles:
            # Perform NER using the fine-tuned model
            ner = ner_model(title)
            entities = [(entity['word'], entity['entity']) for entity in ner]

            # Perform Sentiment Analysis using the sentiment model
            sentiment = sentiment_model(title)[0]

            # Write the results to the CSV file
            writer.writerow([title, entities, sentiment['label'], sentiment['score']])

# Main execution
if __name__ == "__main__":
    # Step 1: Read titles from the CSV file
    input_filename = 'cleaned_news_titles.csv'
    cleaned_titles = read_cleaned_titles_from_csv(input_filename)

    # Step 2: Perform NER and Sentiment Analysis and save to CSV
    output_filename = 'ner_sentiment_results.csv'
    analyze_and_save_to_csv(cleaned_titles, output_filename)

    print(f"NER and sentiment analysis results saved to {output_filename}")
