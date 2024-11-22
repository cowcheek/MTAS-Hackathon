import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
import re

# Load the Excel file containing the Jira ticket data
df = pd.read_excel("data/raw_data.xlsx")

# Download the necessary NLTK data (if not already downloaded)
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Function to clean and normalize the description
def normalize_error_message(text):
    if not isinstance(text, str):
        return ""
    
    # Remove timestamps (e.g., "2024-10-15T22:19:26.79")
    text = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d+)?", "", text)
    
    # Remove Jenkins links or similar URLs
    text = re.sub(r"https?://[^\s]+", "", text)
    
    # Remove unwanted characters like {noformat}, \xa0
    text = text.replace("{noformat}", "").replace("\xa0", " ").strip()
    
    return text

# Function to clean the description using lemmatization
def clean_description(text):
    if not isinstance(text, str):
        return ""
    
    # Define irrelevant phrases and words to remove
    greetings = ["hi", "hello", "dear", "regards", "thanks", "best", "sincerely", "regards,", "thanks,"]
    
    # Define regex patterns to identify error lines
    error_patterns = [
        r"\[ERROR\]",          # Matches lines with [ERROR]
        r"\[WARNING\]",        # Matches lines with [WARNING]
        r"\[CIFW\]\[ERROR\]",  # Matches specific CIFW error pattern
        r"\b(error|exception|fail|issue|problem|blocked|critical|fatal)\b"  # Matches generic keywords
    ]
    combined_pattern = re.compile("|".join(error_patterns), re.IGNORECASE)
    
    # Split the description into lines
    lines = text.splitlines()
    cleaned_lines = []
    
    # Normalize and process each line
    for i, line in enumerate(lines):
        # Normalize the line
        line = normalize_error_message(line)
        
        # Skip empty or irrelevant lines
        if not line or any(greeting in line.lower() for greeting in greetings):
            continue
        
        # If the line matches any error pattern, include it along with context
        if combined_pattern.search(line):
            # Get the previous and next lines for context
            prev_line = normalize_error_message(lines[i - 1]) if i > 0 else ""
            next_line = normalize_error_message(lines[i + 1]) if i < len(lines) - 1 else ""
            
            # Combine the current line with context
            context_line = f"{prev_line} {line} {next_line}".strip()
            cleaned_lines.append(context_line)
    
    # Join the cleaned lines back into a single string
    cleaned_text = " ".join(cleaned_lines)
    return cleaned_text.strip()



# Apply the cleaning function to the 'Description' column
df['Cleaned_Description'] = df['Description'].apply(clean_description)
print(df['Cleaned_Description'])

# Strip commas from the 'Summary' column
df['Summary'] = df['Summary'].apply(lambda x: x.replace(",", "") if isinstance(x, str) else x)

# Replace 'Description' with 'Cleaned_Description'
df = df.drop(columns=['Description'])
df.rename(columns={'Cleaned_Description': 'Description'}, inplace=True)

# Ensure all columns are preserved and in the correct order
columns_order = ['Key', 'Summary', 'solution', 'Solution_team', 'Solution_component', 'Description']
df = df.reindex(columns=columns_order)

# Filter rows where the 'solution' column is not empty
df = df[df['solution'].notna() & (df['solution'] != "")]
# Replace NaN values in the 'Description' column with empty strings
# Replace empty descriptions with the corresponding summary
df['Description'] = df.apply(
    lambda row: row['Summary'] if row['Description'].strip() == "" else row['Description'], axis=1
)

# Save the cleaned data to a new CSV file
output_file = 'data/cleaned_jira_tickets.csv'
df.to_csv(output_file, index=False)

print(f"Data cleaned and saved to '{output_file}'.")
