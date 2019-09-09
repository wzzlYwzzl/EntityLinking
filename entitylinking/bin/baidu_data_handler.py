import json

def handle_json_data(json_data, spo_file, mention_file):
    """处理百度提供的json格式的数据，将其处理为SPO的形式
    """
    with open(json_data, mode='r', encoding='utf-8') as f_json:
        with open(spo_file, mode='w+', encoding='utf-8') as f_spo:
            with open(mention_file, mode='w+', encoding='utf-8') as f_mention: 
                for line in f_json:
                    data = json.loads(line)