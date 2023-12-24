import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from challenge import encrypt, decrypt


FLAG = open('flag.txt', 'r').read()
assert len(FLAG) == 31


users = [
    {
        'username': 'Azantis',
        'secret': os.urandom(8).hex()
    },
    {
        'username': 'Byzantine',
        'secret': os.urandom(8).hex()
    },
    {
        'username': 'Carian',
        'secret': FLAG
    },
]

app = FastAPI()

class SecretObject(BaseModel):
    username: str
    secret: str
    

@app.post("/store")
def store_secret(secret_object: SecretObject):
    combined_secret = [{
        'username': secret_object.username,
        'secret': secret_object.secret
    }]
    for user in users:
        combined_secret.append(user)

    return {"token": encrypt(json.dumps(combined_secret))}

@app.get("/verify/{token}")
def verify_token(token: str):
    data = decrypt(token)
    if data:
        users = []
        for content in data:
            users.append(content.get('username'))

        return {"users": users}
    
    raise HTTPException(403, 'Invalid token')

app.mount("/", StaticFiles(directory="static", html = True), name="static")