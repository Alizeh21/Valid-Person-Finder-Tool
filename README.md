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

Below is a **ready-to-paste section** you can add to your existing GitHub `README.md`.

Just place this under your **Common Issues** section.

---

```markdown
## Common MongoDB Problems and Fixes

During development and testing, the following MongoDB-related issues are commonly encountered.

---

### 1. `ServerSelectionTimeoutError`

Example error:

```

pymongo.errors.ServerSelectionTimeoutError

```

**Cause**

MongoDB server is not running.

**Fix**

Open a new terminal and start MongoDB:

```

mongod

```

Leave this terminal running while the backend API is running.

---

### 2. Connection refused (ECONNREFUSED / WinError 10061)

Example:

```

Connection refused

```

or

```

WinError 10061

```

**Cause**

MongoDB is not running or is running on a different port.

**Fix**

Start MongoDB using:

```

mongod

```

Make sure it is listening on the default port:

```

27017

```

---

### 3. Wrong MongoDB URI

The project uses the following default URI in `db.py`:

```

mongodb://localhost:27017

````

If your MongoDB server is running on a different host or port, update:

```python
MONGO_URI = "mongodb://localhost:27017"
````

accordingly.

---

### 4. MongoDB service not running (Windows service install)

On some systems MongoDB is installed as a Windows service.

If `mongod` does not start, open **Services** and make sure:

```
MongoDB Server
```

is running.

You can also start it manually from Services.

---

### 5. MongoDB data directory permission error

Sometimes MongoDB fails to start with errors related to the data directory.

Example:

```
Data directory ... not found or not accessible
```

**Fix**

Create the data directory manually (only if required by your installation):

```
C:\data\db
```

Then start MongoDB again:

```
mongod
```

---

### 6. Authentication failed

If you see an error similar to:

```
Authentication failed
```

**Cause**

Your MongoDB server is running with authentication enabled.

**Fix**

Update the connection string in `db.py` to include username and password:

```python
mongodb://username:password@localhost:27017
```

(If you are using a local default installation, authentication is usually not enabled.)

---

### 7. Database or collection not visible in MongoDB Compass

This is normal behavior.

The database and collection:

* `person_finder`
* `results`

are created only after the first successful insert.

**Fix**

Run at least one successful search from the UI or API, then refresh MongoDB Compass.

---

### 8. Firewall or antivirus blocking MongoDB

In some environments, local firewall or antivirus software blocks port `27017`.

**Fix**

Allow inbound connections for:

```
mongod.exe
```

or allow port:

```
27017
```

in the firewall settings.

---

### 9. Verifying MongoDB connectivity quickly

You can verify that MongoDB is reachable by running the backend and checking that
no error appears when this line is executed:

```python
from pymongo import MongoClient
```

If the backend starts without MongoDB-related errors and successfully inserts results,
the connection is working correctly.

```
```


### About inbound connections (Windows Firewall)

MongoDB runs as a local server process (`mongod.exe`) and listens for connections on the default port:

```

27017

```

When the FastAPI backend connects to MongoDB, it is treated by Windows as an **inbound connection to MongoDB**.

If Windows Firewall or antivirus software blocks inbound connections for `mongod.exe`, the backend will fail to connect and may raise errors such as:

```

ServerSelectionTimeoutError

```

or

```

Connection refused

```

To fix this, allow inbound connections for the MongoDB server executable:

```

mongod.exe

```

(or allow inbound traffic on port `27017`) in Windows Defender Firewall.

This project only connects to:

```

mongodb://localhost:27017

```

so allowing inbound connections only enables local communication between the backend API and the MongoDB server on the same machine.
It does not expose MongoDB to the public internet.


