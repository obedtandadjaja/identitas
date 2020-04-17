from fastapi import Depends, FastAPI, Header, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.api.v1.api import api_router as api_v1_router
from app.db.session import Session


app = FastAPI(title="Identitas")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow everything for now. Change later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response

# async def get_token_header(authorization: str = Header(...)):
#     if authorization != "secret":
#         raise HTTPException(status_code=400, detail="Authorization header invalid")

app.include_router(api_v1_router, prefix="/api/v1/")

@app.get("/health")
def read_health():
    return {"status": "OK"}
