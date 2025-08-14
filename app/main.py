from app import create_app
from dotenv import load_dotenv
load_dotenv()
app = create_app()

@app.get("/")
async def root():
    return {"message": "Hello World"}