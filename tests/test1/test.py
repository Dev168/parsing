import os
import json

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def load_test_data():
    with open(os.path.join(DIRNAME, "data.json"), "r", encoding="utf8") as f:
        data = json.loads(f.read())
    return data



def save_test_data(data):
    with open(os.path.join(DIRNAME, "data.json"), "w", encoding="utf8") as f:
        f.write(json.dumps(data, sort_keys=True, indent=4))

