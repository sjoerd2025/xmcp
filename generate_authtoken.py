"""
Create Tweet - X API v2
=======================
Endpoint: POST https://api.x.com/2/tweets
Docs: https://developer.x.com/en/docs/twitter-api/tweets/manage-tweets/api-reference/post-tweets

Authentication: OAuth 2.0 (User Context)
Required env vars: CLIENT_ID, CLIENT_SECRET
"""

import os
import json
from pathlib import Path

from dotenv import load_dotenv
from xdk import Client
from xdk.oauth2_auth import OAuth2PKCEAuth

# Load variables from a local .env file (or existing environment variables).
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if not client_id or not client_secret:
    raise RuntimeError(
        "Missing CLIENT_ID or CLIENT_SECRET. Add them to .env or export them."
    )

# Replace the following URL with your callback URL, which can be obtained from your App's auth settings.
redirect_uri = "https://example.org"

# Set the scopes
scopes = ["tweet.read", "tweet.write", "users.read", "offline.access", "dm.read", "dm.write"]

# Be sure to replace the text with the text you wish to Tweet. 
# You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
payload = {"text": "Hello world!"}

def main():
    # Step 1: Create PKCE instance
    auth = OAuth2PKCEAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scopes
    )
    
    # Step 2: Get authorization URL
    auth_url = auth.get_authorization_url()
    print("Visit the following URL to authorize your App on behalf of your X handle in a browser:")
    print(auth_url)
    
    # Step 3: Handle callback
    callback_url = input("Paste the full callback URL here: ")
    
    # Step 4: Exchange code for tokens
    tokens = auth.fetch_token(authorization_response=callback_url)
    access_token = tokens["access_token"]
    print(access_token)
    
    
    print("Response code: 201")
    print(json.dumps(response.data, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()