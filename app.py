from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
from app.embeddings_processor import match_errors_to_tickets
from app.clean_logs import extract_error_snippets
from io import StringIO

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
        # Treat query as a file input if no file is uploaded
        if file:
            response = {'error': 'Provide either a file or a query, not both.'}
        else:
            try:
                # Convert the query into a pseudo-file object using StringIO
                query_file = StringIO(query)
                
                # Process the query as if it were a file
                snippets = extract_error_snippets(query_file, 4)
                results = match_errors_to_tickets(snippets)
                
                # Format the response
                response = results
            except Exception as e:
                return jsonify({'error': f'Error processing query: {str(e)}'}), 500

    else:
        # Save the uploaded file and process it
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        print('found file')

        try:
            snippets = extract_error_snippets(file_path, 4)
            results = match_errors_to_tickets(snippets)
            response = results
        except Exception as e:
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    print('Returning response:', response)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
