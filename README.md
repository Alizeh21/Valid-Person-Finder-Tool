# Valid-Person-Finder-Tool


A tool that finds the person holding a given role (e.g., **Facebook – CEO**) using only free, publicly available sources and
returns a structured JSON response.

This project:

- builds multiple search queries automatically
- expands designation aliases (CEO → Chief Executive Officer, etc.)
- uses DuckDuckGo Search (no API key)
- extracts names from public web pages
- validates company + role context
- stores results in MongoDB
- exposes a REST API
- includes a simple frontend UI

---

## Project Structure

```

Person-Finder/
│
├── backend/
│   ├── main.py
│   ├── search.py
│   ├── extractor.py
│   ├── db.py
│   └── requirements.txt
│
└── frontend/
└── index.html

```

---

## Prerequisites

- Python 3.10 or newer (Python 3.12 supported)
- MongoDB installed locally
- Visual Studio Code

---

## Open the project in VS Code

Open the root folder:

```

D:\Person-Finder

```

Open a terminal inside VS Code.

---

## Backend Setup (Windows – PowerShell)

Move into the backend directory:

```

cd backend

```

---

### Create virtual environment

Because some Windows installations have a broken global `pywin32` package,
this project uses a safe workaround:

```

python -S -m venv venv

```

---

### Activate the virtual environment

```

.\venv\Scripts\Activate.ps1

```

You should see:

```

(venv)

```

at the start of the terminal line.

---

### Install dependencies

If your network is restricted, use:

```

pip install -r requirements.txt --timeout 120 --trusted-host pypi.org --trusted-host files.pythonhosted.org

```

If that still fails, use the official mirror:

```

pip install -r requirements.txt -i [https://pypi.python.org/simple](https://pypi.python.org/simple) --trusted-host pypi.python.org --timeout 120

```

---

## Start MongoDB

Open a separate terminal window and run:

```

mongod

```

Leave this window running.

The application uses:

- database: `person_finder`
- collection: `results`

They are created automatically.

---

## Run the Backend API

In the backend terminal (with venv activated):

```

uvicorn main:app --reload

```

You should see:

```

Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000)

```

---

## Verify the API

Open in a browser:

```

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

```

You should see the Swagger UI with:

```

POST /find-person

```

---

## Run the Frontend

Open the file:

```

frontend/index.html

````

in your browser  
(or right-click in VS Code → Open with Live Server).

---

## How to Use

In the web interface:

- Company  
  `Facebook`

- Designation  
  `CEO`

Click **Search**.

---

## Example Output

The UI will display JSON similar to:

```json
{
  "first_name": "Mark",
  "last_name": "Zuckerberg",
  "current_title": "CEO",
  "company": "Facebook",
  "source_url": "https://en.wikipedia.org/wiki/Mark_Zuckerberg",
  "confidence_score": 0.8
}
````

---

## MongoDB Storage

Every successful lookup is stored in MongoDB:

* database: `person_finder`
* collection: `results`

Example document:

```json
{
  "first_name": "Mark",
  "last_name": "Zuckerberg",
  "current_title": "CEO",
  "company": "Facebook",
  "source_url": "...",
  "confidence_score": 0.8
}
```

---

## API Usage

### Endpoint

```
POST /find-person
```

### Request body

```json
{
  "company": "Facebook",
  "designation": "CEO"
}
```

---

## Internal Processing Pipeline

1. Build multiple search queries using designation aliases
   (e.g. CEO → CEO, Chief Executive Officer).
2. Perform searches using DuckDuckGo.
3. Filter for credible public sources.
4. Download public page content using `requests`.
5. Parse text using BeautifulSoup.
6. Extract possible person names.
7. Score each candidate using:

   * company match
   * designation match
   * name relevance
8. Select the highest-scoring candidate.
9. Store the result in MongoDB.
10. Return structured JSON.

---

## No-Result Handling

If no valid person is found, the API returns:

```json
{
  "status": "no_result",
  "message": "No valid person found"
}
```

---

## Important Notes

* The tool does not scrape private or logged-in LinkedIn pages.
* Only public and indexed pages and search snippets are used.
* A small delay is applied between page fetches to reduce aggressive crawling.

---

## Common Issues

### MongoDB connection error

Ensure `mongod` is running before starting the API.

---

### Import errors in VS Code

Make sure VS Code uses the virtual environment interpreter:

```
backend/venv/Scripts/python.exe
```

Use:

```
Ctrl + Shift + P → Python: Select Interpreter
```

---

### Slow searches

Public page fetching and HTML parsing can be slow, especially on restricted networks.
This is expected behavior.

---

## Stopping the System

* Stop backend:
  `Ctrl + C` in the uvicorn terminal
* Stop MongoDB:
  `Ctrl + C` in the mongod terminal

---

## Technologies Used

* FastAPI
* DuckDuckGo Search (duckduckgo-search)
* Requests
* BeautifulSoup
* RapidFuzz
* MongoDB (PyMongo)
* HTML + JavaScript frontend

```

