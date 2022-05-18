CLIENT_ID = "abcd231da"


class CMD:
    JSON_ERR1 = ""

    JSON_ERR2 = "{cmd,12}"

    JSON_ERR3 = '''{ "cmd": "GET-NODE-LOG-FULL",
                        "day": 0
                        "node_from": "12ewde123",
                        "node_to": "1232fddf3f",
                        "msg_id": "0" }'''

    JSON_ERR4 = '''{ "cmd": "GET-NODE-LOG-FULL",
                            "day": 0,
                            "node_from": "12ewde123",
                            "node_to": "1232fddf3f",
                            "msg_id": }'''

    GET_LOG_PROPER = "".join(('''{ "cmd": "GET-NODE-LOG-FULL",
                    "day": 0,
                    "node_from": "12ewde123",
                    "node_to": "'''+CLIENT_ID+'''",
                    "msg_id": "0" }''').splitlines())

    GET_LOG_PROPER_WRONG_NODE = '''{ "cmd": "GET-NODE-LOG-FULL",
                        "day": 0,
                        "node_from": "12ewde123",
                        "node_to": "1232fddf3f",
                        "msg_id": "0" }'''

    GET_LOG_PROPER_ANY = '''{ "cmd": "GET-NODE-LOG-FULL",
                        "day": -1,
                        "node_from": "12ewde123",
                        "node_to": "ANY",
                        "msg_id": "1" }'''

    GET_LOG_ERR_DAY1 = '''{ "cmd": "GET-NODE-LOG-FULL",
                            "day": 1,
                            "node_from": "12ewde123",
                            "node_to": "ANY",
                            "msg_id": "1" }'''

    GET_LOG_ERR_DAY2 = '''{ "cmd": "GET-NODE-LOG-FULL",
                                "day": "abc",
                                "node_from": "12ewde123",
                                "node_to": "ANY",
                                "msg_id": "1" }'''

    GET_LOG_ERR_DAY3 = '''{ "cmd": "GET-NODE-LOG-FULL",
                                "node_from": "12ewde123",
                                "node_to": "ANY",
                                "msg_id": "1" }'''

    GET_LOG_ERR_SRC = '''{ "cmd": "GET-NODE-LOG-FULL",
                    "day": 0,
                    "node_to": "ANY",
                    "msg_id": "0" }'''

    GET_LOG_ERR_DEST = '''{ "cmd": "GET-NODE-LOG-FULL",
                        "day": -1,
                        "node_from": "12ewde123",
                        "msg_id": "1" }'''

    GET_LOG_ERR_MSG_ID = '''{ "cmd": "GET-NODE-LOG-FULL",
                        "day": -1,
                        "node_from": "12ewde123",
                        "node_to": "ANY"}'''