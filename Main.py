import os
import requests
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables (store API credentials in a .env file)
load_dotenv()
FATSECRET_CLIENT_ID = os.getenv("FATSECRET_CLIENT_ID")
FATSECRET_CLIENT_SECRET = os.getenv("FATSECRET_CLIENT_SECRET")

# FatSecret API URLs
TOKEN_URL = "https://oauth.fatsecret.com/connect/token"
SEARCH_URL = "https://platform.fatsecret.com/rest/server.api"

# Initialize FastAPI app
app = FastAPI()

# OAuth 2.0 - Get Access Token
def get_access_token():
    """Fetch an OAuth 2.0 token from FatSecret."""
    data = {"grant_type": "client_credentials", "scope": "basic"}
    headers = {
        "Authorization": f"Basic {requests.auth._basic_auth_str(FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET)}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    return response.json()["access_token"]

# Dependency for OAuth token
async def oauth_token():
    return get_access_token()

# Pydantic model for request validation
class FoodSearchRequest(BaseModel):
    search_expression: str

@app.get("/")
async def root():
    """Root endpoint - Just a welcome message."""
    return {"message": "Welcome to FatSecret API with FastAPI"}

@app.post("/search-foods")
async def search_foods(request: FoodSearchRequest, token: str = Depends(oauth_token)):
    """Search for foods using FatSecret API."""
    params = {"method": "foods.search", "format": "json", "search_expression": request.search_expression}
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(SEARCH_URL, params=params, headers=headers)
    return response.json()

# Run with: uvicorn filename:app --reload
