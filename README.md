# Document Retrieval System 21BCE11234

This is a Flask-based backend for a document retrieval system that scrapes news articles from multiple websites, stores them in MongoDB, and allows users to search through the articles. It includes rate limiting, health checks, and article search functionalities.
![image](https://github.com/user-attachments/assets/9c885efb-ff2f-48d0-91c5-f1106e8b4dcf)


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
