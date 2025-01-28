import os

from fastapi import FastAPI
from pydantic import BaseModel

import google.auth
from google.cloud import storage


instance_counter = 0

app = FastAPI(
    description="Test application for Cloud Run/GKE"
)

class MainResponse(BaseModel):
    local_counter: int
    host_name: str
    project_id: str


class PingResponse(BaseModel):
    request: str
    response: str

@app.get("/", response_model=MainResponse, summary="Pong to your ping")
def ping():
    """
    Main info endpoint
    """
    global instance_counter
    instance_counter += 1

    _, project_id = google.auth.default()


    return MainResponse(
        local_counter = instance_counter, 
        host_name = os.uname().nodename,
        project_id = project_id
    )


@app.get("/test", summary="Test endpoint")
def test():
    """
    Test endpoint
    """
    return PingResponse(request = 'test', response = 'works')

@app.get("/buckets")
def buckets():

    try:
        client = storage.Client()
        return [bucket.name for bucket in client.list_buckets()]
    except Exception as e:
        return {'error': str(e)}


@app.get("/{request}", summary="Pong to your ping")
def ping(request: str):
    """
    Ping endpoint - response with pong to any request
    """
    return PingResponse(request = request, response = 'pong')

