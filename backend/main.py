from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

app = FastAPI(title="Drive Speak")

# Setup CORS (Crucial for Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routes
app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"message": "The forge is burning hot. API is live."}