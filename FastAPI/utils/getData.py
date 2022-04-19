import json
from turtle import position
import numpy as np
from pymongo import MongoClient
from bson.objectid import ObjectId
import re
import random

CONNECTION_STRING = "mongodb+srv://kun09:khongbiet@cluster0.7vq6c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

database = client["database"]
chuong = database["chuong"]
noi_dung = database["noi dung"]
phan_muc = database["phan muc"]
media = database["media"]
code = database["code"]
table = database["table"]
keyphrase = database["keyphrase"]
cau_hoi = database["cau hoi"]

def findOccurrences(str_, substr):
    return [m.start() for m in re.finditer(substr, str_)]
def ignoreABCD(str):
    return str.replace("A.","").replace("B.","").replace("C.","").replace("D.","").strip()

def getChapter():
    list_data = []
    for chapter in chuong.find({}):
        list_data.append({
            "id": str(chapter["_id"]),
            "ten" : chapter["ten_chuong"]
        })
    return list_data   

def getIdContentByIdChapter(strId):
    list_data = []
    for content in noi_dung.find({"id_chuong": ObjectId(strId)}):
        list_data.append({
            "id": str(content["_id"]),
        })
    return list_data  


def getContentById(strId):
    content = noi_dung.find({"_id": ObjectId(strId)})[0]
    data = {
        "ten_chuong" : "",
        "ten_noi_dung" : content["ten_noi_dung"],
        "Phan_loai" : content["Phan_loai"],
        "Mo_ta" : content["Mo_ta"],
        "Phan_muc" : []
    }

    data["ten_chuong"] = chuong.find({"_id" : ObjectId(content["id_chuong"])})[0]["ten_chuong"]
    for index in phan_muc.find({"id_noi_dung" : ObjectId(content["_id"])}):
        position = []
        position.append({
            "pos" : 0,
            "type" : ""
        })

        data_index =  {
            "ten_muc" : index["ten_muc"],
            "noi_dung" : [],
            "bo_sung" : []
        }

        for type in ["code","img","href","table"]:
            for pos in findOccurrences(index["noi_dung"], f"\|{type}\|"):
                position.append({
                    "pos" : pos,
                    "type" : f"|{type}|\n"
                })

        position.append({
            "pos" : len(index["noi_dung"]),
            "type" : ""
        })

        #print(index["noi_dung"])
        position = sorted(position, key=lambda d: d['pos']) 
        # for pos in position:
        #     print(pos)
        
        list_img = []
        list_code = []
        list_table = []
        list_href = []

        for m in media.find({"id_muc" : ObjectId(str(index["_id"]))}):
            if m["Loai"] == "img":
                list_img.append(m["Link"])
            else:
                list_href.append(m["Link"])
        for c in code.find({"id_muc" : ObjectId(str(index["_id"]))}):
            list_code.append(c["Code"])
        for t in table.find({"id_muc" : ObjectId(str(index["_id"]))}):
            list_table.append(t["table"])

        for pos in position:
            if pos["type"] == "|code|\n":
                data_index["bo_sung"].append({
                    "noi_dung" : list_code[0][1:],
                    "Loai" : "code"
                })
                list_code = np.delete(list_code, 0, None)
            if pos["type"] == "|img|\n":
                data_index["bo_sung"].append({
                    "noi_dung" : list_img[0],
                    "Loai" : "img"
                })
                list_img = np.delete(list_img, 0, None)
            if pos["type"] == "|href|\n":
                data_index["bo_sung"].append({
                    "noi_dung" : list_href[0],
                    "Loai" : "href"
                })
                list_href = np.delete(list_href, 0, None)
            if pos["type"] == "|table|\n":
                data_index["bo_sung"].append({
                    "noi_dung" : list_table[0],
                    "Loai" : "table"
                })
                list_table = np.delete(list_table, 0, None)


        while len(position) != 1:
            data_index["noi_dung"].append(index["noi_dung"][position[0]["pos"]+len(position[0]["type"]):position[1]["pos"]])
            position = np.delete(position, 0, None)
        
        data["Phan_muc"].append(data_index)
    return data

        

# rgx = re.compile(f'.*Tham chiếu.*', re.IGNORECASE)
# content = noi_dung.find({"ten_noi_dung" : rgx})[0]
# data = getContentById(str(content["_id"]))


    # return data

def getIndexById(strId):
    index = phan_muc.find({"_id": ObjectId(strId)})[0]
    position = []
    position.append({
        "pos" : 0,
        "type" : ""
    })

    data_index =  {
        "ten_muc" : index["ten_muc"],
        "noi_dung" : [],
        "bo_sung" : []
    }

    for type in ["code","img","href","table"]:
        for pos in findOccurrences(index["noi_dung"], f"\|{type}\|"):
            position.append({
                "pos" : pos,
                "type" : f"|{type}|\n"
            })

    position.append({
        "pos" : len(index["noi_dung"]),
        "type" : ""
    })

    #print(index["noi_dung"])
    position = sorted(position, key=lambda d: d['pos']) 
    # for pos in position:
    #     print(pos)
    
    list_img = []
    list_code = []
    list_table = []
    list_href = []

    for m in media.find({"id_muc" : ObjectId(str(index["_id"]))}):
        if m["Loai"] == "img":
            list_img.append(m["Link"])
        else:
            list_href.append(m["Link"])
    for c in code.find({"id_muc" : ObjectId(str(index["_id"]))}):
        list_code.append(c["Code"])
    for t in table.find({"id_muc" : ObjectId(str(index["_id"]))}):
        list_table.append(t["table"])

    for pos in position:
        if pos["type"] == "|code|\n":
            data_index["bo_sung"].append({
                "noi_dung" : list_code[0][2:],
                "Loai" : "code"
            })
            list_code = np.delete(list_code, 0, None)
        if pos["type"] == "|img|\n":
            data_index["bo_sung"].append({
                "noi_dung" : list_img[0],
                "Loai" : "img"
            })
            list_img = np.delete(list_img, 0, None)
        if pos["type"] == "|href|\n":
            data_index["bo_sung"].append({
                "noi_dung" : list_href[0],
                "Loai" : "href"
            })
            list_href = np.delete(list_href, 0, None)
        if pos["type"] == "|table|\n":
            data_index["bo_sung"].append({
                "noi_dung" : list_table[0],
                "Loai" : "table"
            })
            list_table = np.delete(list_table, 0, None)


    while len(position) != 1:
        data_index["noi_dung"].append(index["noi_dung"][position[0]["pos"]+len(position[0]["type"]):position[1]["pos"]])
        position = np.delete(position, 0, None)
        
    return data_index

def findWithKeyphrase(keyph):
    list_data = []
    keyph = keyph.lower()
    for key in keyphrase.find({}):
        if key["from"] == keyph or key["to"] == keyph:
            rgx = re.compile(f'.*{key["from"]}.*|.*{key["to"]}.*', re.IGNORECASE)
            break
        else:
            rgx = re.compile(f'.*{keyph}.*', re.IGNORECASE)
    list_find_index = [idx["_id"] for idx in phan_muc.find({"ten_muc":rgx})]
    for idx in list_find_index:
        data = getIndexById(str(idx))
        list_data.append(data)
    return list_data

def getQuestionRandom(number_of_question):
    list_question = list(cau_hoi.find({}))
    list_data = [list_question[idx] for idx in random.sample(range(len(list_question)), number_of_question)]
    for data in list_data:
        data["_id"] = str(data["_id"])
        data["Cau_tra_loi"] = [ignoreABCD(c) for c in  data["Cau_tra_loi"]] 
        data.pop('Dap_an', None)
        data.pop("id_muc", None)
    return list_data

with open('data_question.json', 'w', encoding='utf-8') as f:
    json.dump(getQuestionRandom(20), f, ensure_ascii=False)



# data = findWithKeyphrase("const")
