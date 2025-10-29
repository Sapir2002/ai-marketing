from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import gbp_routes, gbp_analyze  # ✅ Add this

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can limit this to ["http://127.0.0.1:8001"] later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(gbp_routes.router)
app.include_router(gbp_analyze.router)  # ✅ Add this too

@app.get("/")
def root():
    return {"message": "GBP Optimizer API running!"}
