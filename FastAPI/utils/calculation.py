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

def resultOfAnswer(list_ans):
    list_data = {
        "number_of_question" : len(list_ans),
        "number_of_correct" : len([i for i in list_ans if i["ans"] == cau_hoi.find({"_id" : ObjectId(i["id"])})[0]["Dap_an"]]),
    }

    dict_detail = {}

    for ans in list_ans:
        list_id_noi_dung = [phan_muc.find({"_id" : ObjectId(id_muc)})[0]["id_noi_dung"] for id_muc in cau_hoi.find({"_id" : ObjectId(ans["id"])})[0]["id_muc"]]
        for id in list_id_noi_dung:
            if str(id) not in dict_detail.keys():
                dict_detail[str(id)] = {
                    "total" : 1,
                    "correct" : 0,
                }
            else:
                dict_detail[str(id)]["total"] = dict_detail[str(id)]["total"] + 1

            if ans["ans"] == cau_hoi.find({"_id" : ObjectId(ans["id"])})[0]["Dap_an"]:
                dict_detail[str(id)]["correct"] = dict_detail[str(id)]["correct"] + 1

    list_data["detail"] = dict_detail

    return list_data