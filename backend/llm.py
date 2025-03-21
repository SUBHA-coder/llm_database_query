import requests
import json

# Set your Groq API key
GROQ_API_KEY = "api"
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

def generate_mongo_query(natural_language_query):
    """Convert natural language to MongoDB query using Llama via Groq API"""
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"Convert this natural language query into a valid MongoDB query in JSON format: {natural_language_query}"
    
    data = {
        "model": "llama-3-8b-instruct",
        "messages": [
            {"role": "system", "content": "You are an AI that translates natural language into MongoDB queries in strict JSON format."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise error for HTTP issues

        response_json = response.json()
        mongo_query = response_json.get("choices", [{}])[0].get("message", {}).get("content", "{}")

        # Ensure the response is valid JSON
        return json.loads(mongo_query)

    except json.JSONDecodeError:
        print("Error: Could not parse JSON response from LLM")
        return {}

    except requests.RequestException as e:
        print(f"Error communicating with Groq API: {e}")
        return {}
