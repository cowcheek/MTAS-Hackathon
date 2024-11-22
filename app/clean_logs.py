import os
import argparse
import re


def extract_error_snippets(log_file_path, context_lines=4):
    """
    Extracts error snippets from a log file with surrounding context.

    Args:
    - log_file_path (str): Path to the log file.
    - context_lines (int): Number of context lines before and after the error line to include in the snippet.

    Returns:
    - List of dictionaries containing the error line and its context.
    """
    # Define the error keywords and common paths to filter out
    error_keywords = ['[ERROR]', 'EXCEPTION', 'FAILURE', 'FATAL', 'Traceback (most recent call last)', 'FAILED']
    common_paths = ['/local/scratch/mtasbin/slave/workspace/', '/usr/', '/var/log/']

    error_snippets = []

    # Check if the log file exists
    if not os.path.exists(log_file_path):
        print(f"Error: log file {log_file_path} does not exist")
        return []

    # Read the log file
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    # Process each line in the log file
    for i, line in enumerate(lines):
        # If the line contains any error keyword
        if any(keyword in line for keyword in error_keywords):
            start = max(0, i - context_lines)
            end = min(len(lines), i + context_lines + 1)
            snippet_context = lines[start:end]

            # Join the context and remove newlines
            text = ''.join(s.replace("\n", " ") for s in snippet_context).strip()

            # Remove timestamps in formats like "2024-10-15T22:18:52.56" or "22:18:52"
            text = re.sub(r"\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?", "", text)
            text = re.sub(r"\b\d{2}:\d{2}:\d{2}\b", "", text)
            text = re.sub(r"\[\d+\]", "", text)  # Removing any numbers in brackets

            # Filter out snippets containing common paths

            # Append error snippet
            error_snippets.append({
                "error": line.strip(),
                "context": text
            })

    return error_snippets


	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"log_file",
		type = str,
		help = "Path to the log file to process."
	)	


	parser.add_argument(
		"--context",
		type = int,
		default = 4,
		help = "Number of context lines to include."
	)



	args = parser.parse_args()

	log_file_path = args.log_file
	context_lines = args.context
	snippets = extract_eror_snippets(log_file_path,context_lines)

	for id,snippet in enumerate(snippets):
		print(f"Error #{id +1}:")
		#print(f"Error Line: {snippet['error']}")
		print(f"\n{snippet['context']}\n{'-' * 50}")
	
