# Document Retrieval System

This is a Flask-based backend for a document retrieval system that scrapes news articles from multiple websites, stores them in MongoDB, and allows users to search through the articles. It includes rate limiting, health checks, and article search functionalities.

#Backend Output :
![image](https://github.com/user-attachments/assets/9c885efb-ff2f-48d0-91c5-f1106e8b4dcf)

#Frontend Output :
![image](https://github.com/user-attachments/assets/262dfc18-1320-4630-8955-d62070624439)


# 🛠️ Technology Stack

Backend: Python 3.7+, Flask
Database: MongoDB
Caching: Built-in MongoDB caching
Containerization: Docker
Web Scraping: BeautifulSoup4, Requests
Text Processing: PyMongo text search capabilities

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [GET /health](#get-health)
  - [POST /search](#post-search)
- [Scraping Logic](#scraping-logic)
- [Rate Limiting](#rate-limiting)
- [Logging](#logging)

---

## Features
- **News Scraping:** Periodically scrapes news articles from popular websites and stores them in MongoDB.
- **Article Search:** Allows users to search for articles based on keywords with relevance scoring.
- **Rate Limiting:** Limits the number of search requests a user can make per minute to prevent API abuse.
- **Health Check:** Provides a health check endpoint to verify the status of the application.
- **Logging:** Captures important actions and errors in logs for easier debugging.

## Installation


### Prerequisites
- **Python 3.8+**
- **MongoDB** (You can use a local MongoDB or a cloud-based one like MongoDB Atlas)

### Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/document-retrieval-system.git
    cd document-retrieval-system
    ```
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configure MongoDB:
   - Set up a MongoDB instance (local or cloud) and update the connection string in your `database.py` file or you can use the given file aslo:
     ```python
     MONGO_URI = "mongodb://localhost:27017/yourdbname"
     ```
![image](https://github.com/user-attachments/assets/7d2d649b-5fcf-4544-b906-94d97e2cf6c3)


5. Initialize the database:
    ```bash
    python -c "from database import init_db; init_db()"
    ```

## Configuration

- **Database**: Modify the MongoDB connection in `database.py` if necessary.
- **Rate Limiting**: You can adjust the rate limits in the `app.py` file:
  ```python
  limiter = Limiter(
      get_remote_address,
      app=app,
      default_limits=["5 per minute"],  # Adjust the limits here
      storage_uri="memory://",
  )


## API Endpoints

### GET `/health`
Returns a random health status message to check the application status.

#### Sample Request:
```bash
curl http://127.0.0.1:5000/health
```

#### Sample Response:
"Healthy"

### POST /search
Searches for documents in the database based on the provided text.

Request Parameters:
user_id: Unique identifier for the user.
text: Search keyword(s).
top_k: Number of top results to return (default: 5).
threshold: Minimum score threshold for filtering search results.

```bash
curl -X POST http://127.0.0.1:5000/search -H "Content-Type: application/json" -d '{
  "user_id": "12345",
  "text": "technology",
  "top_k": 5,
  "threshold": 0.5
}'
```
```bash
{
  "results": [
    {
      "id": "614cf29b1fdfab12345",
      "content": "Article Title",
      "score": 1.5,
      "source": "https://timesofindia.indiatimes.com/"
    }
  ],
  "inference_time": 0.0824
}
```

Scraping Logic
The system scrapes articles from predefined news websites every 60 seconds and stores them in MongoDB. Scraping is handled by the scrape_news function, which fetches and parses HTML content to extract article titles.

Rate Limiting
The system limits users to 5 search requests per minute to prevent abuse. This is implemented using the Flask-Limiter library.

Logging
The application logs scraping activities and errors using the logging module. These logs help monitor scraping activities and troubleshoot issues.


THANKYOU!!!
