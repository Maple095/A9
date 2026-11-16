import os


def run_user_command():
    user_input = input("Enter command: ")
    # 刻意將使用者輸入直接交給 eval 或 os.system 執行（會觸發 CodeQL 高風險警報）
    os.system("echo " + user_input)
