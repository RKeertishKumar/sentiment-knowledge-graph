import csv

# Function to read the NER and Sentiment results from the CSV file
def read_ner_sentiment_from_csv(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Function to clean the NER entities (merge fragmented tokens)
def clean_ner_entities(entities_string):
    # Convert string representation of entities back to list of tuples
    entities = eval(entities_string)  # This will evaluate the string and convert it back into a list of tuples
    
    cleaned_entities = []
    current_entity = ""
    current_label = ""
    
    for entity, label in entities:
        if label == current_label:
            current_entity += entity
        else:
            if current_entity:
                cleaned_entities.append((current_entity, current_label))
            current_entity = entity
            current_label = label
    
    if current_entity:
        cleaned_entities.append((current_entity, current_label))
    
    return cleaned_entities

# Function to map sentiment labels to more understandable categories
def map_sentiment_label(label):
    sentiment_mapping = {
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive"
    }
    return sentiment_mapping.get(label, "Neutral")

# Function to save cleaned data to a new CSV file
def save_cleaned_data_to_csv(cleaned_data, output_filename):
    with open(output_filename, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Entities', 'Sentiment', 'Sentiment Score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in cleaned_data:
            # Write the cleaned data to the CSV
            writer.writerow({
                'Title': row['Title'],
                'Entities': row['Entities'],
                'Sentiment': row['Sentiment'],
                'Sentiment Score': row['Sentiment Score']
            })

# Main execution
if __name__ == "__main__":
    # Step 1: Read the NER and sentiment results from CSV
    input_filename = 'ner_sentiment_results.csv'
    data = read_ner_sentiment_from_csv(input_filename)

    # Step 2: Clean the data
    cleaned_data = []
    for row in data:
        title = row['Title']
        cleaned_entities = clean_ner_entities(row['Entities'])
        mapped_sentiment = map_sentiment_label(row['Sentiment'])
        sentiment_score = row['Sentiment Score']
        
        cleaned_data.append({
            'Title': title,
            'Entities': cleaned_entities,
            'Sentiment': mapped_sentiment,
            'Sentiment Score': sentiment_score
        })

    # Step 3: Save the cleaned data to a new CSV file
    output_filename = 'cleaned_ner_sentiment_results.csv'
    save_cleaned_data_to_csv(cleaned_data, output_filename)

    print(f"Cleaned data saved to {output_filename}")
