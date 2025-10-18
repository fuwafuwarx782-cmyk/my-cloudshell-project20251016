# ファイル名はmain.py
import datetime
def generate_log_message(location = "Gifu", user = "Fuwa"):
    """
    現在時刻と位置情報を含むログメッセージを生成する。
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"[{now}] User'{user}' logged in from '{location}'."
    return message

if __name__ == "__main__":
    # 練習用のログメッセージを生成して出力する
    log1 = generate_log_message(location="Lambda-Test", user="DevUser")
    log2 = generate_log_message(location="Nagoya", user="Hideyosi")

    print("--- Location Log ---")
    print(log1)
    print(log2)