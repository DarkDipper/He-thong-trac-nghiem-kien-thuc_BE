from pymongo import MongoClient
from bson.objectid import ObjectId
import json
import numpy as np

CONNECTION_STRING = "mongodb+srv://kun09:khongbiet@cluster0.7vq6c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)
database = client["database"]

cau_hoi = database["cau hoi"]
questions = []
for i in range(1,9):
    f = open(f"400-cau-hoi-trac-nghiem-lap-trinh-c++/De-{i}.txt", encoding='utf-8')
    list_data = f.read().split("@")
    f.close()

    def ignoreABCD(str):
        return str.replace("A.","").replace("B.","").replace("C.","").replace("D.","").strip()
    for data in list_data:
        line = data.split("\n")
        for r in ["",''," ",' ']: 
            while r in line:
                line.remove(r)
        #print(line)
        # for l in line:
        #     print(f"{l}\n")
        question = {
            "id_muc" : [id for id in line[-1].split(";")],
            "Cau_hoi" : line[:-6],
            "Cau_tra_loi" : [ans for ans in line[-6:-2]],
            "Dap_an" : ignoreABCD(line[-2])
        }
        d = 0
        for q in question["Cau_tra_loi"]:
            if "A." in q: d+=1 
            if "B." in q: d+=1 
            if "C." in q: d+=1 
            if "D." in q: d+=1 
        if d!= 4:
            print(question["Cau_hoi"])
        questions.append(question)
        #cau_hoi.insert_one(question)
# with open('data_question.json', 'w', encoding='utf-8') as f:
#     json.dump(questions, f, ensure_ascii=False)