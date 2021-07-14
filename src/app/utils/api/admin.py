from app.models.user import STATUS


def manager_name_extract(dic):
    if isinstance(dic, dict) is False:
        return None
    elif isinstance(dic, dict):
        return dic.get("name")


def warning_level_changer(now_level: str):
    level = STATUS.index(now_level)
    if level == len(STATUS)-1:
        return STATUS[len(STATUS)-1]
    return STATUS[level+1]


if __name__ == "__main__":
    print(warning_level_changer("NORMAL"))
