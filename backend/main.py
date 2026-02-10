# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
import uvicorn

app = FastAPI(title="Gemini Code Explainer API")

# --- CONFIGURATION ---
API_KEY = "AIzaSyBxWDBiqeEAyMWcwuDiMNCJIf51lhKBil4"

# Use the new Client initialization with explicit versioning if needed
client = genai.Client(api_key=API_KEY)

# UPDATED: Use a more recent stable model ID
# Options: "gemini-2.0-flash", "gemini-2.5-flash", or "gemini-1.5-flash-8b"
MODEL_ID = "gemini-2.5-flash" 

class CodeRequest(BaseModel):
    code: str
    concise: bool = False

@app.get("/models")
async def list_models():
    """Debug helper: Run this to see exactly which models you can use."""
    try:
        models = client.models.list()
        return {"available_models": [m.name for m in models]}
    except Exception as e:
        return {"error": str(e)}

@app.post("/explain")
async def explain_code(request: CodeRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Please paste some code first.")

    try:
        verbosity = "in one single clear sentence" if request.concise else "in a detailed, step-by-step breakdown"
        
        prompt = (
            f"Act as a Senior Software Architect. Explain the following code {verbosity}:\n\n"
            f"```\n{request.code}\n```"
        )

        # Call using the updated model ID
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )

        return {"explanation": response.text}

    except Exception as e:
        # If the 404 persists, the specific error will be printed here
        print(f"Detailed Error: {e}")
        raise HTTPException(status_code=500, detail=f"Model Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)