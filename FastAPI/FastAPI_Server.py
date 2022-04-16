import json
import numpy as np
from fastapi import FastAPI
import FastAPI.utils.getData as mgGet
import FastAPI.utils.calculation as cal
from FastAPI.model.Client import Client

app = FastAPI()

@app.get("/")
async def root(name: str):
    return{f"Hello World {name}"}

@app.post("/find")
async def create_upload_file(key:str):
    return {
        "list_data": mgGet.findWithKeyphrase(key)
    }
@app.post("/chapter")
async def create_upload_file():
    return {
        "list_data": mgGet.getChapter()
    }
@app.post("/content")
async def create_upload_file(id_chapter:str):
    return {
        "list_data": mgGet.getIdContentByIdChapter(id_chapter)
    }

@app.post("/content/id")
async def create_upload_file(id_content:str):
    return {
        "list_data": mgGet.getContentById(id_content)
    }

@app.post("/question")
async def create_upload_file(number_of_question: int):
    return {
        "list_data": mgGet.getQuestionRandom(number_of_question)
    }
@app.post("/submit")
async def create_upload_file(client: Client):
    return {
        "list_data": cal.resultOfAnswer(client.list_ans)
    }

