from typing import Union
from pypdf import PdfReader
import io
from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def read_root():
    return "The health check is successful"


@app.get("/ocr")
def extract_text(url: Union[str, None] = None):
    if url is None:
        return {"error": "Please provide a url"}

    res = requests.get(url)
    buffer = io.BytesIO(res.content)
    reader = PdfReader(buffer)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + " "

    # remove special characters
    text = text.replace("\n", " ").replace("\t", " ").replace(
        "●", " ").replace("■", " ").replace("□", " ").replace("▪", " ")

    # replace multiple spaces with single space
    text = " ".join(text.split())

    return {"text": text}
