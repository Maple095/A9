import html
import json
import subprocess
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

# 1. 建立指令白名單，絕不直接執行使用者輸入的字串
ALLOWED_COMMANDS = {
    "status": ["echo", "System OK"],
    "version": ["python", "--version"],
}


@app.route("/run")
def run_cmd():
    cmd_key = request.args.get("cmd", "")
    if cmd_key not in ALLOWED_COMMANDS:
        abort(400, description="Invalid command")

    # 使用參數陣列且不開啟 shell=True，防止指令注入 (Command Injection)
    result = subprocess.run(
        ALLOWED_COMMANDS[cmd_key],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout


@app.route("/load", methods=["POST"])
def load_data():
    try:
        data = json.loads(request.data.decode("utf-8"))
        # 使用 html.escape() 過濾潛在的惡意腳本標籤，防止反射型 XSS
        safe_data = html.escape(json.dumps(data))
        return jsonify({"received": safe_data})
    except (json.JSONDecodeError, UnicodeDecodeError):
        abort(400, description="Invalid JSON payload")
        
