# app/utils.py
def detect_scam(message):
    """
    Basic logic for scam detection.
    Returns True if 'scam' is in the message, else False.
    """
    return "scam" in message.lower()

def process_new_messages(messages):
    """
    Process a list of messages and detect scams.
    Returns a dictionary with messages and their scam status.
    """
    results = {}
    for message in messages:
        results[message] = detect_scam(message)
    return results

async def fetch_facebook_listing(link, access_token):
    """
    Simulated async function to fetch a Facebook listing.
    Returns success or error based on the input.
    """
    if link and access_token:
        return {"status": "success", "data": "sample data"}
    else:
        return {"error": "Invalid link or access token"}
