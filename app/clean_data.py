import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer

# Load the Excel file containing the Jira ticket data
df = pd.read_excel("data/raw_data.xlsx")

# Download the necessary NLTK data (if not already downloaded)
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# Function to clean the description using lemmatization
def clean_description(text):
    if not isinstance(text, str):
        return ""
    
    # Define irrelevant phrases and words to remove
    greetings = ["hi", "hello", "dear", "regards", "thanks", "best", "sincerely", "regards,", "thanks,"]
    
    # Split the description into lines
    lines = text.splitlines()
    
    # Normalize the lines by lemmatizing the words and filtering out irrelevant lines
    filtered_lines = []
    for line in lines:
        # Remove all commas from the line to avoid CSV issues
        line = line.replace(",", "")
        
        # Remove lines containing greetings and irrelevant phrases
        if any(greeting in line.lower() for greeting in greetings):
            continue
        
        # Lemmatize the words in the line
        words = line.split()
        normalized_words = [lemmatizer.lemmatize(word.lower()) for word in words]
        
        # Keep lines that mention relevant keywords
        if any(word in ['error', 'exception', 'fail', 'issue', 'problem', 'blocked'] for word in normalized_words):
            filtered_lines.append(line)
    
    # Join the filtered lines back into a single string
    cleaned_text = " ".join(filtered_lines)
    return cleaned_text.strip()

# Apply the cleaning function to the 'Description' column
df['Cleaned_Description'] = df['Description'].apply(clean_description)

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

# Save the cleaned data to a new CSV file
df.to_csv('data/cleaned_jira_tickets.csv', index=False)

print("Data cleaned and saved to 'cleaned_jira_tickets.csv'.")
