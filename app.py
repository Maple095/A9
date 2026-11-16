import os
import pickle
from flask import Flask, request

app = Flask(__name__)


@app.route("/run")
def run_cmd():
    # 來自網頁 URL 參數的外部輸入（CodeQL 會判定為高風險不可信來源）
    cmd = request.args.get("cmd", "")
    os.system(cmd)
    return "OK"


@app.route("/load")
def load_data():
    data = request.data
    return str(pickle.loads(data))
