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

# Function to create a knowledge graph from cleaned data
def create_knowledge_graph(graph, cleaned_data):
    for row in cleaned_data:
        # Create Post node
        post_title = row['Title']
        sentiment = row['Sentiment']
        sentiment_score = float(row['Sentiment Score'])
        
        # Create a Post node with sentiment properties
        post_node = Node("Post", title=post_title, sentiment=sentiment, sentiment_score=sentiment_score)
        graph.create(post_node)

        # Process entities from NER results
        entities = eval(row['Entities'])  # Convert string back to list of tuples
        for entity in entities:
            entity_name = entity[0]  # First element of tuple is the entity name
            entity_type = entity[1]  # Second element is the entity type

            # Create an Entity node
            entity_node = Node("Entity", name=entity_name, type=entity_type)
            graph.merge(entity_node, "Entity", "name")  # Avoid duplicate nodes

            # Create a relationship between Post and Entity
            relationship = Relationship(post_node, "MENTIONS", entity_node)
            relationship["sentiment"] = sentiment  # Store sentiment in relationship
            relationship["sentiment_score"] = sentiment_score  # Store sentiment score in relationship
            graph.create(relationship)

# Main execution
if __name__ == "__main__":
    # Step 1: Read the cleaned data from CSV
    input_filename = 'cleaned_ner_sentiment_results.csv'
    cleaned_data = read_cleaned_data_from_csv(input_filename)

    # Step 2: Connect to Neo4j
    graph = connect_to_neo4j(uri="bolt://localhost:7687", username="neo4j", password="12345678")

    # Step 3: Create the Knowledge Graph in Neo4j
    create_knowledge_graph(graph, cleaned_data)

    print("Knowledge graph created in Neo4j!")
