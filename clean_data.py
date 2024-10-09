import re

# Function to clean the text and extract only the relevant news titles
def clean_news_titles(text):
    # Split the text into lines
    lines = text.splitlines()

    # List to hold clean titles
    clean_titles = []

    # Regex pattern to remove tags like [hn], [ai], etc.
    tag_pattern = re.compile(r'\[.*?\]')
    
    # List of terms to ignore (menu items, irrelevant text)
    ignore_terms = [
        'login', 'all', 'tech', 'news', 'business', 'science', 'gaming',
        'culture', 'politics', 'sports', 'wordcloud', 'summarizer', 'premium',
        'about', 'hacker news', 'previous day', 'brutalist network'
    ]

    # Loop through each line and clean
    for line in lines:
        cleaned_line = line.strip().lower()

        # Remove unnecessary lines (ignore menu items and non-news sections)
        if not cleaned_line or cleaned_line in ignore_terms:
            continue

        # Remove any tags like [hn], [ai], etc.
        cleaned_line = tag_pattern.sub('', cleaned_line).strip()

        # Skip lines that are just numbers or irrelevant sections
        if cleaned_line.isdigit() or len(cleaned_line) < 5:
            continue

        # Add the cleaned line to the list if it's valid news
        clean_titles.append(cleaned_line)

    return clean_titles

# Read the raw news data from a file
def read_news_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        raw_text = file.read()
    return raw_text

# Write the clean titles to a new file
def write_clean_titles_to_file(clean_titles, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        for title in clean_titles:
            file.write(f"{title}\n")

# Main execution
if __name__ == "__main__":
    # Read raw text from a file
    input_filename = 'scraped_titles.csv'  # Change this to your actual file path
    raw_text = read_news_file(input_filename)

    # Clean the titles
    clean_titles = clean_news_titles(raw_text)

    # Print the cleaned titles (optional)
    print("Cleaned Titles:")
    for title in clean_titles:
        print(title)

    # Write the cleaned titles to a new file
    output_filename = 'cleaned_news_titles.csv'  # Change this to your desired output file path
    write_clean_titles_to_file(clean_titles, output_filename)

    print(f"\nAll cleaned titles have been written to {output_filename}")
