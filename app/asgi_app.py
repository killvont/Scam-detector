import os
import re
import logging
import aiohttp
from flask import Flask, request, jsonify  # Use Flask instead of Quart
from flask_cors import CORS  # Use Flask-CORS for CORS support
from flask_limiter import Limiter
from flasgger import Swagger
from dotenv import load_dotenv
from cachetools import cached, TTLCache
from custom_exceptions import FacebookAPIError

# Load environment variables
load_dotenv()

# Initialize Flask app and configurations
app = Flask(__name__)
CORS(app)  # CORS support
limiter = Limiter(key_func=lambda: request.remote_addr)
swagger = Swagger(app)

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG, filename='data/spam_detection.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# In-memory cache with a Time-To-Live of 10 minutes
cache = TTLCache(maxsize=100, ttl=600)

# List of suspicious keywords for spam detection
suspicious_keywords = ["free", "win", "guarantee", "urgent", "act now"]

def detect_scam(message):
    """Check if the message contains suspicious keywords."""
    message = message.lower()
    return any(re.search(r'\b' + re.escape(keyword) + r'\b', message) for keyword in suspicious_keywords)

def log_event(event):
    """Log events related to spam detection with structured data."""
    logger.info(event)

@cached(cache)
async def fetch_facebook_listing(link, access_token):
    """Fetch Facebook listing data asynchronously."""
    listing_id = extract_listing_id(link)
    if not listing_id:
        raise FacebookAPIError("Invalid Facebook link.")

    url = f"https://graph.facebook.com/v12.0/{listing_id}?access_token={access_token}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise FacebookAPIError(await response.text())
            return await response.json()

@limiter.limit("5 per minute")  # Example rate limit
@app.route('/scan_listing', methods=['POST'])
def scan_listing():
    """Scan a Facebook listing for potential scams."""
    data = request.get_json()
    logger.debug(f"Received data: {data}")

    link = data.get('link')
    access_token = data.get('access_token')

    if not link or not access_token:
        logger.error("Link and access token are required.")
        return jsonify({'error': 'Link and access token are required.'}), 400

    try:
        result = fetch_facebook_listing(link, access_token)  # Call sync function for now
        logger.debug(f"Fetched result: {result}")
        return jsonify(result)
    except FacebookAPIError as e:
        logger.error(f"Facebook API error: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.exception("Error fetching Facebook listing")
        return jsonify({'error': 'An unexpected error occurred.'}), 500

def extract_listing_id(link):
    """Extract the listing ID from a Facebook Marketplace link."""
    parts = link.split('/')
    return parts[-2] if len(parts) > 2 else None

if __name__ == "__main__":
    app.run(debug=True)
