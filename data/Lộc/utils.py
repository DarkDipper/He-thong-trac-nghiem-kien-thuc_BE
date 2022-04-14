from pymongo import MongoClient
from bson.objectid import ObjectId
import re
import json

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


def getContentById(id):
    content = noi_dung.find({"_id": id})[0]
    data = {
        "ten_chuong" : "",
        "ten_noi_dung" : content["ten_noi_dung"],
        "Phan_loai" : content["Phan_loai"],
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

def getIndexById(id):
    index = phan_muc.find({"_id": id})[0]
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
    keyph = keyph.lower()
    for key in keyphrase.find({}):
        if key["from"] == keyph or key["to"] == keyph:
            rgx = re.compile(f'.*{key["from"]}.*|.*{key["to"]}.*', re.IGNORECASE)
            break
        else:
            rgx = re.compile(f'.*{keyph}.*', re.IGNORECASE)
    list_find_index = [idx["_id"] for idx in phan_muc.find({"ten_muc":rgx})]
    return list_find_index

list_find_index =  findWithKeyphrase("toán tử")
for idx in list_find_index:
    data = getIndexById(idx)
    with open('data_index.json', 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)