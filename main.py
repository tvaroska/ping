import os
import requests

from fastapi import FastAPI, HTTPException
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

@app.get("/file/{name}")
def get_file(name: str):
    fname = os.getenv(name)
    if fname:
        with open(fname) as f:
            content = f.read()
        return {'file_name': fname, 'content': str(content)}
    else:
        raise HTTPException(status_code=404, detail="Name does not exists")

@app.get("/rest/{name}")
def get_rest(name: str):
    hname = os.getent(name)
    if hname:
        response = requests.get(hname)
        return {'resonse': response.text}
    else:
        raise HTTPException(status_code=404, detail="Name does not exists")

@app.get("/{request}", summary="Pong to your ping")
def ping(request: str):
    """
    Ping endpoint - response with pong to any request
    """
    return PingResponse(request = request, response = 'pong')

