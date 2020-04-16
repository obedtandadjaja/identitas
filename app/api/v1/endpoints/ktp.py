from fastapi import APIRouter


router = APIRouter()

""" POST parseKTP
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
# TODO(obedtandadjaja): double check the path there are a few other alternatives:
# - /parseKTP
# - /parsektp
# - /parseKtp
# - /parse_ktp
@router.post("/v1/ktp/parse")
async def parse_ktp():
    # mocked return
    return True
