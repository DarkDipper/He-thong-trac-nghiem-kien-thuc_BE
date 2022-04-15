from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY
import os
import re
import json
import numpy as np
from pymongo import MongoClient

def findOccurrences(str_, substr):
    return [m.start() for m in re.finditer(substr, str_)]

def escape(data):
    return data.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;'," ")

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def replaceWithLink(data):
    regex = r"<a href=\"(.*?\")>|<(?:img|video).*?(src=\"(.*?\"))>"
    match = re.finditer(regex, data, re.MULTILINE|re.IGNORECASE)
    d = data
    for i in match:
        if i.group(1) is not None:
            d = d.replace(i.group(0), i.group(1))
        if i.group(3) is not None:
            d = d.replace(i.group(0), i.group(3))
    return d


def dirMultiFile(filename):
    list_dir_file = []
    for root, dirs, files in os.walk(filename, topdown=False):
        for name in files:
            dir_file = str(os.path.join(root, name)).replace("\\","/")
            list_dir_file.append(dir_file)

    return list_dir_file


CONNECTION_STRING = "mongodb+srv://kun09:khongbiet@cluster0.7vq6c.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(CONNECTION_STRING)

database = client["database"]
chuong = database["chuong"]
noi_dung = database["noi dung"]
phan_muc = database["phan muc"]
media = database["media"]
code = database["code"]
table = database["table"]

# ----Xử lý

list_path = dirMultiFile("D:\Code\He-thong-trac-nghiem-kien-thuc_BE\data\T.Phong")

list_data = []


for path in list_path:
    with open(path, encoding='utf-8') as myfile:
        list_data.append(json.load(myfile))

# chapter = np.unique([i["chapter"] for i in list_data])
# for ch in chapter:
#     chuong.insert_one({"ten_chuong" : ch}) 

for data in list_data:
    idx = 0
    list_ten_muc = []
    # for ch in chuong.find({}):
    #     if ch["ten_chuong"] == data["chapter"]:
    #         d = {
    #             "id_chuong" : ch["_id"],
    #             "ten_noi_dung" : data["title"],
    #             "Mo_ta" : data["desicription"],
    #             "Phan_loai" : "Bài tập" if data["title"].find("Bài tập") != -1 else "Bài học"
    #         }
    #         idx += 1
    #         noi_dung.insert_one(d)

    data_0 = data["content"].replace('<sup>','^')

    regex = r"<h2.*?>"
    match = re.finditer(regex, data_0, re.MULTILINE | re.IGNORECASE)
    for i in match:
        data_0 = data_0.replace(i.group(0),"<h2>")
    data_0 = data_0.replace("</h2>","<h2>")
    pos = findOccurrences(data_0,"<h2>")
    data_nd = data_0
    while len(pos) != 0:
        data_nd = data_nd.replace(data_0[pos[0]+4:pos[1]+4], "")
        list_ten_muc.append(escape(data_0[pos[0]+4:pos[1]])[3:])
        pos = np.delete(np.delete(pos, 0, None), 0, None)


    pos1 = findOccurrences(data_nd,"<h2>")
    pos1 = np.append(pos1, len(data_nd))
    
    #print(data_nd)
    data_pm = data_nd
    while len(pos1) != 1:
        for nd in noi_dung.find({}):
            if nd["ten_noi_dung"] == data["title"]:
                id_nd = nd["_id"]

        for muc in phan_muc.find({}):
            if muc["ten_muc"] == list_ten_muc[idx] and  muc["id_noi_dung"] == id_nd:
                id_muc = muc["_id"]
        data_pm = data_nd[pos1[0]+4:pos1[1]]
        # print(escape(striphtml(data_pm)))
        # print('-------------------------------------------------------------')
        regex = r"<?href=(\".*?\")>|<(?:img).*?src=(\".*?\")>"
        match = re.finditer(regex, data_pm, re.MULTILINE | re.IGNORECASE)
        for i1 in match:
            if i1.group(2) is not None:
                data_pm = data_pm.replace(i1.group(0),"\n|img|\n")
                data_media = {
                    "id_muc": id_muc,
                    "Link" :  i1.group(2).split(" ")[0][1:-1],
                    "Loai" : "img"
                }
                #print(data_media)
                #media.insert_one(data_media)
            if i1.group(1) is not None:
                if i1.group(1).split(" ")[0] == '"https://tracnghiem.net/cntt/400-cau-hoi-trac-nghiem-lap-trinh-c-c-co-dap-an-va-loi-giai-chi-tiet-107.html"':
                    data_pm = data_pm.replace(i1.group(0), "")
                else:
                    data_pm = data_pm.replace(i1.group(0), "\n|href|\n")
                    data_media = {
                        "id_muc": id_muc,
                        "Link" :  i1.group(1).split(" ")[0][1:-1],
                        "Loai" : "href"
                    }
                    #print(data_media)
                    #media.insert_one(data_media)
        
        pos1 = np.delete(pos1, 0, None)


        regex = r"<code.*?>(.*)"
        match = re.finditer(regex, data_pm, re.MULTILINE | re.IGNORECASE)
        for i1 in match:
            data_pm = data_pm.replace(i1.group(0), "\n|code|\n" + i1.group(1))
        data_pm = data_pm.replace("</code>", "\n|code|\n")
        pos2 = findOccurrences(data_pm, "\|code\|")
        tmp = data_pm
        while len(pos2) != 0:
            data_pm = data_pm.replace(tmp[pos2[0]:pos2[1]+6], "|code|")
            data_c = tmp[pos2[0]:pos2[1]+6]
            data_c = data_c.replace("|code|", "")
            data_c =escape(striphtml(data_c))
            data_code = {
                "id_muc": id_muc,
                "Code" :  data_c,
            }
            pos2 = np.delete(np.delete(pos2, 0, None), 0, None)
            #code.insert_one(data_code)


        regex = r"<table.*?>"
        match = re.finditer(regex, data_0, re.MULTILINE | re.IGNORECASE)
        for i1 in match:
            data_pm = data_pm.replace(i1.group(0), "\n|table|\n")
        data_pm = data_pm.replace("</table>", "\n|table|\n")
        pos2 = findOccurrences(data_pm, "\|table\|")
        tmp = data_pm
        while len(pos2) != 0:
            data_pm = data_pm.replace(tmp[pos2[0]:pos2[1] + 7], "|table|")
            data_t = tmp[pos2[0]:pos2[1]+7]
            table_0 = {}
            list_col = []
            list_row = []
            data_t = data_t.replace("|table|", "")
            regex = r"<td.*?>"
            match = re.finditer(regex, data_t, re.MULTILINE | re.IGNORECASE)
            for i in match:
                data_t = data_t.replace(i.group(0), "<td>")
            regex = r"<th.*?>"
            match = re.finditer(regex, data_t, re.MULTILINE | re.IGNORECASE)
            for i in match:
                data_t = data_t.replace(i.group(0), "<th>")
            data_t = data_t.replace("</th>", "<th>")
            pos_t = findOccurrences(data_t, "<th>")
            while len(pos_t) != 0:
                list_col.append(escape(striphtml(data_t[pos_t[0]+4:pos_t[1]])))
                pos_t = np.delete(np.delete(pos_t, 0, None), 0, None)

            data_t = data_t.replace("</td>", "<td>")
            pos_t = findOccurrences(data_t, "<td>")
            while len(pos_t) != 0:
                list_row.append(escape(striphtml(data_t[pos_t[0]+4:pos_t[1]])))
                pos_t = np.delete(np.delete(pos_t, 0, None), 0, None)

            if len(list_col) == 0:
                pos_t = findOccurrences(data_t, "<tr>")
                if len(pos_t) != 0:
                    list_col = [str(i) for i in range(len(list_row)//len(pos_t))]
                #print(len(list_row))
            # for c in list_col:
            #     print(c)
            # for r in list_row:
            #     print(r)

            for i in range(len(list_row)):
                if list_col[i%len(list_col)] not in table_0.keys():
                    table_0[list_col[i%len(list_col)]] = [list_row[i]]
                else:
                    table_0[list_col[i%len(list_col)]].append(list_row[i])

            data_table = {
                "id_muc" : id_muc,
                "table" : table_0
            }
            print("<table>")
            #print("\n")
            pos2 = np.delete(np.delete(pos2, 0, None), 0, None)
            # table.insert_one(data_table)

        p = re.compile(r'<.*?>|<.*')
        data_pm = p.sub('', data_pm)
        data_pm = escape(data_pm)
        data_result = ""
        for item in data_pm.split("\n"):
            if item != "" and  item != " ":
                data_result += item + "\n"
        # print(data["title"])
        # print(list_ten_muc[idx])
        # print(data_result)
        # print("--------------------------")
        # for nd in noi_dung.find({}):
        #     if nd["ten_noi_dung"] == data["title"]:
        #         data_muc = {
        #             "id_noi_dung" : nd["_id"],
        #             "ten_muc" : list_ten_muc[idx],
        #             "noi_dung" : data_result
        #         }
        #         phan_muc.insert_one(data_muc)
        idx += 1
    