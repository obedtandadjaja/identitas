from fastapi import Depends, FastAPI, Header, HTTPException

from app.api.v1.endpoints import auth, ktp


app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "OK"}

async def get_token_header(authorization: str = Header(...)):
    if authorization != "secret":
        raise HTTPException(status_code=400, detail="Authorization header invalid")

app.include_router(auth.router)
app.include_router(
        ktp.router,
        prefix="/api/v1/ktp",
        dependencies=[Depends(get_token_header)],
        responses={404: {"description": "Not Found"}},
)
