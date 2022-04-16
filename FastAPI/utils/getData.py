import random
from pymongo import MongoClient
from bson.objectid import ObjectId
import re

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
    for chapter in chuong.find({}):
        if chapter["_id"] == content["id_chuong"]:
            data["ten_chuong"] = chapter["ten_chuong"]
    for index in phan_muc.find({}):
        if index["id_noi_dung"] == content["_id"]:
            data_index =  {
                "ten_muc" : index["ten_muc"],
                "noi_dung" : index["noi_dung"],
                "media" : [],
                "code" : [],
                "table" : []
            }
            for m in media.find({}):
                if m["id_muc"] == index["_id"]:
                    data_index["media"].append({
                        "Link" : m["Link"],
                        "Loai" : m["Loai"]
                    })
            for c in code.find({}):
                if c["id_muc"] == index["_id"]:
                    data_index["code"].append({"" : c["Code"]})
            for t in table.find({}):
                if t["id_muc"] == index["_id"]:
                    data_index["table"].append({"" : t["table"]})
            data["Phan_muc"].append(data_index)

    return data

def getIndexById(strId):
    index = phan_muc.find({"_id": ObjectId(strId)})[0]
    data_index =  {
        "ten_noi_dung" : "",
        "ten_muc" : index["ten_muc"],
        "noi_dung" : index["noi_dung"],
        "media" : [],
        "code" : [],
        "table" : []
    }
    for nd in noi_dung.find({}):
        if nd["_id"] == index["id_noi_dung"]:
            data_index["ten_noi_dung"] = nd["ten_noi_dung"]
    for m in media.find({}):
        if m["id_muc"] == index["_id"]:
            data_index["media"].append({
                "Link" : m["Link"],
                "Loai" : m["Loai"]
            })
    for c in code.find({}):
        if c["id_muc"] == index["_id"]:
            data_index["code"].append({"" : c["Code"]})
    for t in table.find({}):
        if t["id_muc"] == index["_id"]:
            data_index["table"].append({"" : t["table"]})
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
        # data.pop('Dap_an', None)
        data.pop("id_muc", None)
    return list_data

