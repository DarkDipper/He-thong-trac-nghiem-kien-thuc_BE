from pymongo import MongoClient
from bson.objectid import ObjectId
from FastAPI.utils.getData import getIndexById
# from getData import getIndexById

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
    list_detail = []
    list_check = []
    for ans in list_ans:
        list_id_noi_dung = [phan_muc.find({"_id" : ObjectId(id_muc)})[0]["id_noi_dung"] for id_muc in cau_hoi.find({"_id" : ObjectId(ans["id"])})[0]["id_muc"]]
        for id in list_id_noi_dung:
            if str(id) not in dict_detail.keys():
                dict_detail[str(id)] = {
                    "ten_noi_dung" : noi_dung.find({"_id":id})["ten_noi_dung"],
                    "total" : 1,
                    "correct" : 0,
                    "content" : []
                }
            else:
                dict_detail[str(id)]["total"] = dict_detail[str(id)]["total"] + 1

            if ans["ans"] == cau_hoi.find({"_id" : ObjectId(ans["id"])})[0]["Dap_an"]:
                dict_detail[str(id)]["correct"] = dict_detail[str(id)]["correct"] + 1
            else:
                content_index = [getIndexById(str(id_muc)) for id_muc in cau_hoi.find({"_id" : ObjectId(ans["id"])})[0]["id_muc"]]
                for ci in content_index:
                    if ci["id_muc"] not in list_check:
                        list_check.append(ci["id_muc"])
                        ci.pop("id_muc", None)
                        dict_detail[str(id)]["content"].append(ci)
                        
    for r in dict_detail:
        list_detail.append(dict_detail[r])

    list_data["detail"] = list_detail

    return list_data

# import json
# f = open("D:/Code/He-thong-trac-nghiem-kien-thuc_BE/SL/FastAPI/utils/data.json", "r", encoding='utf-8')
# data = json.load(f)
# data_result = resultOfAnswer(data)
# print(data_result)
# # # for r in data_result["detail"]:
# # # print(data_result["detail"][r])
# with open('data_question.json', 'w', encoding='utf-8') as f:
#     json.dump(data_result, f, ensure_ascii=False)