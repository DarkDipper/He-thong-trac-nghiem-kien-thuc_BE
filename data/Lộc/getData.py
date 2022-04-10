from pymongo import MongoClient
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

data = {}

idx = 0
for content in noi_dung.find({}):
    if content["Phan_loai"] == "Bài học":
        data = {
            # "ten_chuong" : "",
            "ten_noi_dung" : content["ten_noi_dung"],
            # "Phan_loai" : content["Phan_loai"],
            "Phan_muc" : []
        }
        # for chapter in chuong.find({}):
        #     if chapter["_id"] == content["id_chuong"]:
        #         data["ten_chuong"] = chapter["ten_chuong"]
        for index in phan_muc.find({}):
            if index["id_noi_dung"] == content["_id"]:
                data_index =  {
                    "idx" : idx,  
                    "ten_muc" : index["ten_muc"],
                    # "noi_dung" : index["noi_dung"],
                    # "media" : [],
                    # "code" : [],
                    # "table" : []
                }
                idx += 1
                # for m in media.find({}):
                #     if m["id_muc"] == index["_id"]:
                #         data_index["media"].append({
                #             "Link" : m["Link"],
                #             "Loai" : m["Loai"]
                #         })
                # for c in code.find({}):
                #     if c["id_muc"] == index["_id"]:
                #         data_index["code"].append({"" : c["Code"]})
                # for t in table.find({}):
                #     if t["id_muc"] == index["_id"]:
                #         data_index["table"].append({"" : t["table"]})
                data["Phan_muc"].append(data_index)


        with open('data_lesson.json', 'a', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
