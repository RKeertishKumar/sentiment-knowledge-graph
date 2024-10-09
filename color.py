from py2neo import Graph, Node, Relationship
import csv

# Function to read the cleaned NER and sentiment results from CSV
def read_cleaned_data_from_csv(filename):
    cleaned_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cleaned_data.append(row)
    return cleaned_data

# Connect to the Neo4j database
def connect_to_neo4j(uri="bolt://localhost:7687", username="neo4j", password="password"):
    graph = Graph(uri, auth=(username, password))
    return graph

# Function to update the knowledge graph from cleaned data
def update_knowledge_graph(graph, cleaned_data):
    for row in cleaned_data:
        post_title = row['Title']
        sentiment = row['Sentiment']
        sentiment_score = float(row['Sentiment Score'])
        
        # Assign color based on sentiment
        if sentiment == 'positive':
            color = 'blue'
        elif sentiment == 'negative':
            color = 'red'
        else:
            color = 'gray'  # For neutral or other sentiments
        
        # Merge Post node based on title (update existing nodes)
        post_node = graph.nodes.match("Post", title=post_title).first()

        # If the post node exists, update its sentiment and color
        if post_node:
            post_node['sentiment'] = sentiment
            post_node['sentiment_score'] = sentiment_score
            post_node['color'] = color
            graph.push(post_node)  # Push changes to Neo4j

# Main execution
if __name__ == "__main__":
    # Step 1: Read the cleaned data from CSV
    input_filename = 'cleaned_ner_sentiment_results.csv'
    cleaned_data = read_cleaned_data_from_csv(input_filename)

    # Step 2: Connect to Neo4j
    graph = connect_to_neo4j(uri="bolt://localhost:7687", username="neo4j", password="12345678")

    # Step 3: Update the Knowledge Graph in Neo4j
    update_knowledge_graph(graph, cleaned_data)

    print("Knowledge graph updated in Neo4j!")
