from sentence_transformers import SentenceTransformer, util
import pandas as pd

# Load the pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')

# Function to create embeddings for Jira ticket descriptions
def create_jira_embeddings(jira_csv_path):
    jira_df = pd.read_csv(jira_csv_path)  # Load Jira tickets CSV
    jira_descriptions = jira_df['Description'].tolist()
    return model.encode(jira_descriptions), jira_df

# Function to create embeddings for log errors
def create_log_embeddings(log_content):
    # Extract errors (you can modify the pattern depending on the log format)
    errors = []
    for line in log_content.splitlines():
        if "ERROR" in line:  # Adjust pattern if necessary
            error_message = line.split("ERROR")[1].strip()
            print("error found: "+error_message)
            errors.append(error_message)

    return model.encode(errors), errors

# Function to match errors with Jira tickets using cosine similarity
def match_errors_to_tickets(log_content):
    # Load Jira tickets and their embeddings
    jira_embeddings, jira_df = create_jira_embeddings('data/cleaned_jira_tickets.csv')
    print('finished creating jira embeddings')
    
    # Generate embeddings for the log errors
    log_embeddings, log_errors = create_log_embeddings(log_content)
    
    results = []
    
    for log_error in log_errors:
        print(log_error)
        error_embedding = model.encode(log_error)
        similarities = util.cos_sim(error_embedding, jira_embeddings)
        
        # Get the top match (index of the highest similarity)
        top_match_idx = similarities.argmax().item()  # Convert to an integer index

        # Fetch the matched ticket details
        matched_ticket = {
            "ticket_id": jira_df.iloc[top_match_idx]['Key'],
            "description": jira_df.iloc[top_match_idx]['Description'],
            "solution": jira_df.iloc[top_match_idx]['solution']
        }

        # Append result with one top match
        results.append({"error": log_error, "matched_ticket": matched_ticket})
        print(results)
    
    return results


