from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
html: str
with open('frontend/index.html', 'r') as file:
    html = file.read()


@app.get("/")
async def root():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json(get_all_names())
    while True:
        data = await websocket.receive_text()
        dict = json.loads(data)
        names = ''
        func = dict.keys()
        if"name" in func:
            names = add_name(dict["name"])
        elif"decline" in func:
            names = decline(dict["decline"])
        await websocket.send_json(names)


@app.get("/names/")
async def return_json():
    return get_all_names()


@app.get("/names/{letters}")
async def get_advice(letters: str):
    return letter(letters)


@app.post("/names/{name}", )
async def post_name(name: str):
    return add_name(name)


@app.post("/names/decline/")
async def post_decline(to_decline: list):
    return decline(to_decline)


def calculation(prev, new):
    return_value = prev + (1 - prev) * new
    return return_value


def get_all_names():
    f = open("DB.json", "r")
    string = json.load(f)
    f.close()
    return string


def add_name(name: str):
    f = open("DB.json", "r")
    content = json.load(f)
    f.close()
    if name in content:
        content[name] = round(calculation(content[name], 0.2), 3)
    else:
        content[name] = 0.3

    content = dict(sorted(content.items(), key=lambda elem: elem[1], reverse=True))
    f = open("DB.json", "w")
    f.write(json.dumps(content))
    f.close()
    return content


def letter(letters: str):
    f = open("DB.json", "r")
    content = json.load(f)
    f.close()
    advice = {name: content[name] for name in content.keys() if letters in name}
    return advice


def decline(to_decline: list):
    f = open("DB.json", "r")
    content = json.load(f)
    f.close()
    for name in to_decline:
        if name in content:
            val = round(calculation(content[name], -0.2), 3)
            if val<0.1:
                del content[name]
            else:
                content[name] = val
    content = dict(sorted(content.items(), key=lambda elem: elem[1], reverse=True))
    f = open("DB.json", "w")
    f.write(json.dumps(content))
    f.close()
    return content
