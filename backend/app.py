from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import random
import time
from database import init_db, get_db
import threading
import requests
from bs4 import BeautifulSoup
import logging

app = Flask(__name__)
CORS(app)

init_db(app)

limiter = Limiter(
    key_func=get_remote_address,  
    app=app,  
    default_limits=["5 per minute"],  
    storage_uri="memory://",  
)


logging.basicConfig(level=logging.INFO)


NEWS_SITES = [
    "https://timesofindia.indiatimes.com/",
    "https://www.hindustantimes.com/",
    "https://indianexpress.com/"
]


def scrape_news():
    while True:
        for site in NEWS_SITES:
            try:
                response = requests.get(site, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(response.content, 'html.parser')
                
                if "timesofindia" in site:
                    articles = soup.find_all('div', class_='w_tle')
                elif "hindustantimes" in site:
                    articles = soup.find_all('h3', class_='hdg3')
                elif "indianexpress" in site:
                    articles = soup.find_all('h2', class_='title')
                
                db = get_db()
                count = 0
                for article in articles:
                    title = article.text.strip()
                    if title:
                        result = db.documents.update_one(
                            {"content": title},
                            {"$set": {"content": title, "source": site}},
                            upsert=True
                        )
                        if result.upserted_id or result.modified_count > 0:
                            count += 1
                
                logging.info(f"Scraped {count} new or updated news articles from {site}")
            except Exception as e:
                logging.error(f"Error scraping news from {site}: {e}")
            
            time.sleep(60)  


@app.route('/health')
def health():
    responses = ["OK", "Healthy", "Running"]
    return random.choice(responses)

@app.route('/search', methods=['POST'])
@limiter.limit("5 per minute")
def search():
    start_time = time.time()
    
    data = request.json
    user_id = data.get('user_id')
    text = data.get('text', '')
    top_k = int(data.get('top_k', 5))
    threshold = float(data.get('threshold', 0.5))

    db = get_db()
    user = db.users.find_one({"_id": user_id})
    if not user:
        db.users.insert_one({"_id": user_id, "request_count": 1})
    else:
        new_count = user['request_count'] + 1
        if new_count > 5:
            return jsonify({"error": "Rate limit exceeded"}), 429
        db.users.update_one({"_id": user_id}, {"$set": {"request_count": new_count}})

    results = list(db.documents.find(
        {"$text": {"$search": text}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})]).limit(top_k))

    results = [{"id": str(doc['_id']), "content": doc['content'], "score": doc['score'], "source": doc.get('source', 'Unknown')} for doc in results if doc['score'] > threshold]

    end_time = time.time()
    inference_time = end_time - start_time

    return jsonify({
        "results": results,
        "inference_time": inference_time
    })

if __name__ == '__main__':
    threading.Thread(target=scrape_news, daemon=True).start()
    app.run(debug=True, host='0.0.0.0')
