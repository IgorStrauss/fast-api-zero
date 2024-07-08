from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_api_zero.routers import auth, users
from fast_api_zero.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
def read_root() -> dict:
    return {"message": "Olá Mundo!"}


@app.get("/path-html")
def read_html() -> HTMLResponse:
    html_content = """
    <html>
        <head>
            <title>MarquesIgor</title>
        </head>
        <body style="background-color:#1c1c1c;">
            <h1 style="color:red; text-align:center; margin-top:20rem">
            MarquesIgor
            </h1>
            <h1 style="color:red; text-align:center; margin-top:5rem">
            Curso FastAPI Zero com Dunossauro!
            </h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
