from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def read_health():
    return {"status": "OK"}

""" POST processKTP
request: {
  bytes: string base64,
  api: string,
  retain: bool,
  donate_for_training: bool
}

response: {
  result: {
    data: {
        -- consider having the result be in Indonesian
        nik: ...,
        name: ...,
        date_of_birth: ...,
        place_of_birth: ...,
        gender: ...,
        blood_type: ...,
        address: {
        },
        religion: ...,
        marriage_status: ...,
        job: ...,
        citizenship: ...,
        valid_until: ...
    },
    confidence: float
  },
  error: {
    message: string,
    details: string
  }
}
"""

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
