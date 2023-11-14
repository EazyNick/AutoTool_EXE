import json

def Json(data_to_save1, data_to_save2):

    data_to_save = dict(zip(data_to_save1, data_to_save2))
    # 데이터를 JSON 파일에 저장
    with open('data.json', 'w') as json_file:
        json.dump(data_to_save, json_file)

    # JSON 파일에서 데이터 불러오기
    with open('data.json', 'r') as json_file:
        loaded_data = json.load(json_file)

    loaded_keys = list(loaded_data.keys())
    loaded_values = list(loaded_data.values())

    return loaded_keys, loaded_values

def Json_Get():
    with open('data.json', 'r') as json_file:
        loaded_data = json.load(json_file)

    loaded_keys = list(loaded_data.keys())
    loaded_values = list(loaded_data.values())

    return loaded_keys, loaded_values