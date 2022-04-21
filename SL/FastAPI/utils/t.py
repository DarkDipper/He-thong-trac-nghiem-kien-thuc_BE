import json
import getData as mgGet
import calculation as cal

list_ans = []

list_data = mgGet.getQuestionRandom(20)


for data in list_data:
    list_ans.append({
        "id" : data["_id"],
        "ans": data["Dap_an"]
    })

ans = cal.resultOfAnswer(list_ans)

with open('data_ans.json', 'w', encoding='utf-8') as f:
    json.dump(ans, f, ensure_ascii=False)