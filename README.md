### CDP Chatbot Project Documentation

#### Project Overview
This project is a support agent chatbot designed to answer "how-to" questions related to four Customer Data Platforms (CDPs): Segment, mParticle, Lytics, and Zeotap. The chatbot extracts relevant information from the official documentation of these CDPs to guide users on how to perform tasks or achieve specific outcomes within each platform.

#### Project Structure
```
cdp_chatbot/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   └── index.html
└── utils/
    ├── __init__.py
    ├── document_fetcher.py
    └── question_handler.py
```

#### Dependencies
The project uses the following dependencies:
- FastAPI==0.95.0
- requests==2.26.0
- beautifulsoup4==4.10.0
- fuzzywuzzy==0.18.0
- uvicorn==0.20.0

These dependencies are listed in the `requirements.txt` file.

#### Installation
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd cdp_chatbot
   ```

2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

#### Running the Application
To run the FastAPI application, execute the following command:
```sh
uvicorn app:app --reload
```
Open your browser and navigate to `http://127.0.0.1:8000/docs` to interact with the API.

#### File Descriptions

##### `app.py`
This is the main application file that sets up the FastAPI web server and defines the endpoints for the application.
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import process

app = FastAPI()

# Define the base URLs for each CDP
CDP_DOCS = {
    "segment": "https://segment.com/docs/",
    "mparticle": "https://docs.mparticle.com/",
    "lytics": "https://docs.lytics.com/",
    "zeotap": "https://docs.zeotap.com/home/en-us/"
}

# Function to scrape relevant content from a documentation URL
def scrape_documentation(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = ' '.join([p.get_text() for p in soup.find_all("p")])
        return text
    except Exception as e:
        return str(e)

# Store scraped documentation
DOCUMENTATION_DATA = {cdp: scrape_documentation(url) for cdp, url in CDP_DOCS.items()}

# Define the input model
class QueryModel(BaseModel):
    question: str
    cdp: str

@app.post("/ask")
def ask_question(query: QueryModel):
    cdp = query.cdp.lower()
    
    if cdp not in DOCUMENTATION_DATA:
        raise HTTPException(status_code=400, detail="Invalid CDP specified")
    
    documentation_text = DOCUMENTATION_DATA[cdp]
    best_match = process.extractOne(query.question, documentation_text.split(". "))
    
    if best_match and best_match[1] > 50:  # Confidence threshold
        return {"answer": best_match[0]}
    else:
        return {"answer": "Sorry, I couldn't find relevant information."}
```

##### `requirements.txt`
This file lists the dependencies required for the project.
```plaintext
FastAPI==0.95.0
requests==2.26.0
beautifulsoup4==4.10.0
fuzzywuzzy==0.18.0
uvicorn==0.20.0
```

##### `static/style.css`
This file contains the CSS styles for the web application.
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

.container {
    width: 50%;
    margin: 50px auto;
    background: #fff;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
}

form {
    display: flex;
    flex-direction: column;
}

textarea {
    resize: none;
    height: 100px;
    margin-bottom: 10px;
}

button {
    align-self: flex-end;
    padding: 10px 20px;
    background: #007bff;
    color: #fff;
    border: none;
    cursor: pointer;
}

button:hover {
    background: #0056b3;
}

.response {
    margin-top: 20px;
}
```

##### `utils/document_fetcher.py`
This file contains functions to fetch and parse documentation from the provided URLs.
```python
import requests
from bs4 import BeautifulSoup

def fetch_documentation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def parse_documentation(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()
```

##### `utils/question_handler.py`
This file contains the logic to handle user questions and extract relevant information from the documentation.
```python
from utils.document_fetcher import fetch_documentation, parse_documentation

CDP_DOCS = {
    'segment': 'https://segment.com/docs/?ref=nav',
    'mparticle': 'https://docs.mparticle.com/',
    'lytics': 'https://docs.lytics.com/',
    'zeotap': 'https://docs.zeotap.com/home/en-us/'
}

def handle_question(question):
    for cdp, url in CDP_DOCS.items():
        if cdp in question.lower():
            html_content = fetch_documentation(url)
            if html_content:
                doc_text = parse_documentation(html_content)
                return "Relevant information extracted."
    return "Sorry, I couldn't find the information you are looking for."
```

#### Additional Notes
- The chatbot currently uses simple keyword matching with fuzzy string comparison.
- The project can be extended with NLP enhancements for better question handling.
- Advanced features like cross-CDP comparisons can be implemented in future iterations.
