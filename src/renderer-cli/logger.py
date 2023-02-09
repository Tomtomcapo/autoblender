from datetime import datetime


def log(type: str, content: str, additional: str = ""):
    print(f"{datetime.now().strftime('%H:%M:%S')}|{type}|{content}|{additional}")


def log_action(action_name: str):
    log("action", action_name)


def log_info(content: str, additional: str = ""):
    log("info", content, additional)

def log_warning(content: str, additional: str = ""):
    log("warning", content, additional)