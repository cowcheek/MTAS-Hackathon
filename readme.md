# AI Query Assistant

This project is an AI-powered assistant that allows users to submit queries and match errors from log files with relevant Jira tickets. It is built with **Flask** and uses machine learning models to find ticket solutions related to the log errors.

## Prerequisites

Before running the app, make sure you have Python installed on your system. You can download Python from [here](https://www.python.org/downloads/).

### Setup

Follow these steps to set up and run the application:

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/cowcheek/MTAS-Hackathon.git
cd MTAS-Hackathon
2. Set up a Python virtual environment
It is recommended to use a Python virtual environment to manage dependencies:

bash
Copy code
python3 -m venv venv
Activate the virtual environment:

For macOS/Linux:
bash
Copy code
source venv/bin/activate
For Windows:
bash
Copy code
venv\Scripts\activate
3. Install dependencies
Install all the required dependencies using requirements.txt:

bash
Copy code
pip install -r requirements.txt
4. Run the application
Once the environment is set up and dependencies are installed, you can run the application:

bash
Copy code
python app.py
This will start the Flask web server, and you should see the following message in your terminal:

csharp
Copy code
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
5. Access the app
Open your browser and go to http://127.0.0.1:5000/ to access the AI Query Assistant.

6. Upload log file
By default, a sample log file is included in the data directory (data/sample_log.txt). You can upload this file via the web interface to test the application.

To upload a log file: Click the "Choose File" button to select your log file from your local machine.
Query input: Type your query in the input text box.
Once you submit the query, the system will match errors in the log file to relevant Jira tickets based on the descriptions and provide possible solutions.