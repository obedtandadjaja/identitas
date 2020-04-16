from fastapi import APIRouter


router = APIRouter()

""" POST login
request: {
  email: string,
  password: string
}

response: {
  session_token: string,
  access_token: string
}
"""
@router.post("/login")
async def login():
    return {"status": "OK"}

""" POST signup
request: {
  email: string,
  password: string,
  type: free | pro | deluxe
}

response: {
  session_token: string,
  access_token: string
}
"""
@router.post("/signup")
async def signup():
    return {"status": "OK"}
