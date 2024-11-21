from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
from app.embeddings_processor import match_errors_to_tickets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Create the uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    query = request.form.get('query')
    file = request.files.get('file')

    if not query and not file:
        return jsonify({'error': 'Query or file must be provided'}), 400

    response = {}
    if query:
        response['query'] = f'Processed your query: "{query}"'

    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            # Assuming the log file is a text file
            with open(file_path, 'r') as f:
                log_content = f.read()

            # Process the log content and match it with Jira tickets
            results = match_errors_to_tickets(log_content)

            # Format the response
            response['matches'] = results
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
