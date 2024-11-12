from datetime import datetime


def basic_status() -> str:
    now = datetime.now()
    return f"""<status>Today is {now.month} {now.day} {now.year}. The time is {now.hour}:{now.minute}. All systems are operational.</status>"""
