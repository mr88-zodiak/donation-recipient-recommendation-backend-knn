from app import create_app
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()
app = create_app()


origins = [
    "http://localhost",
    "http://localhost:5173",  # contoh jika pakai Vite
    "http://127.0.0.1:5173",
    "http://localhost:5173/penerima"
    # tambahkan origin lain jika perlu
]

# Tambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # atau ["*"] untuk semua origin
    allow_credentials=True,
    allow_methods=["*"],  # atau ["GET", "POST", "PUT"]
    allow_headers=["*"],  # atau ["Authorization", "Content-Type"]
)

@app.get("/")
async def root():
    return {"message": "Hello World"}