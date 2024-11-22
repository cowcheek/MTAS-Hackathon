from sentence_transformers import SentenceTransformer, util
import pandas as pd
from app.clean_logs import extract_error_snippets

# Load the pre-trained model
model = SentenceTransformer('all-mpnet-base-v2')

# Function to create embeddings for Jira ticket descriptions
def create_jira_embeddings(jira_csv_path):
    print('trying to read')
    jira_df = pd.read_csv(jira_csv_path) 
    print('read') # Load Jira tickets CSV
    jira_descriptions = jira_df['Description'].tolist()
    print('found jira descriptions')
    return model.encode(jira_descriptions), jira_df

# Function to create embeddings for log errors
def create_log_embeddings(log_content):
    # Extract errors (you can modify the pattern depending on the log format)
    errors = []
    for log in log_content:
        errors.append(log['context'])
    
    return model.encode(errors), errors

# Function to match errors with Jira tickets using cosine similarity
def match_errors_to_tickets(log_content):
    # Load Jira tickets and their embeddings
    print('creating jira embeddings')
    jira_embeddings, jira_df = create_jira_embeddings('data/cleaned_jira_tickets.csv')
    print('finished creating jira embeddings')
    
    # Generate embeddings for the log errors
    log_embeddings, log_errors = create_log_embeddings(log_content)
    
    results = []
    
   # Define a threshold for similarity score (e.g., 0.8 for good matches)
    SIMILARITY_THRESHOLD = 0.8
    common_paths = ['/local/scratch/mtasbin/slave/workspace/', '/usr/', '/var/log/']

    for log_error in log_errors:
    #     if any(common_path in log_error for common_path in common_paths):
    #         print(f"Skipping due to common path match: {log_error[:50]}...")
    #         continue
        
        # Generate the embedding for the log_error
        error_embedding = model.encode(log_error)
        
        # Calculate similarities between error embedding and jira embeddings
        similarities = util.cos_sim(error_embedding, jira_embeddings)
        
        # Get the top match (index of the highest similarity)
        top_match_idx = similarities.argmax().item()  # Convert to an integer index
        
        # Get the highest similarity score for the top match
        top_match_score = similarities[0, top_match_idx].item()
        print(str(top_match_score)+" for "+jira_df.iloc[top_match_idx]['Key'])
        
        # Only include the match if the score is above the threshold
        if top_match_score >= SIMILARITY_THRESHOLD:
            print('found top score'+str(top_match_score))
            # Fetch the matched ticket details
            matched_ticket = {
                "ticket_id": f"https://eteamproject.internal.ericsson.com/browse/{jira_df.iloc[top_match_idx]['Key']}",
                "solution": jira_df.iloc[top_match_idx]['solution'],
                "solution_team": jira_df.iloc[top_match_idx]['Solution_team'],
                "solution_component": jira_df.iloc[top_match_idx]['Solution_component']
            }
            
            # Append result with the top match
            results.append({"matched_ticket": matched_ticket})
    return results


