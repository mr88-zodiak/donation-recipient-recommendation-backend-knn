from fastapi import FastAPI
from app.router.user import router
from app.router.donasi import donasi_router
from app.router.sr_rekomendasi import sr

def create_app():
    app = FastAPI()
 
    @app.get("/testing/{testing}")
    def testing(testing: str):
        return {"message": f"{testing}"}
    app.include_router(router)
    app.include_router(donasi_router)
    app.include_router(sr)
    
    return app