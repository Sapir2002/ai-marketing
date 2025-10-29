from fastapi import FastAPI

# import the modules, then access .router off each
from app.routes import gbp_fetch, gbp_analyze, gbp_apply

app = FastAPI(title="GBP Optimizer")

app.include_router(gbp_fetch.router)
app.include_router(gbp_analyze.router)
app.include_router(gbp_apply.router)
