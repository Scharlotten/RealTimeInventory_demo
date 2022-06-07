import requests
from ccloud_lib import read_ccloud_config


def get_address(id : int, config_file: str = "./shipping_service/ksql_secret.config", ksql_topic: str = "CUSTOMERS"):
    conf = read_ccloud_config(config_file)
    headers = {
        'Accept': 'application/vnd.ksql.v1+json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = """{ "ksql": "SELECT * FROM """ + ksql_topic + """ WHERE my_key -> id =""" + str(id) + """;" }"""
    response = requests.post(conf["ksql.endpoint"], headers=headers, data=data,
                             auth=(conf["ksql.auth.api.key"], conf["ksql.auth.secret"]))
    ksql_response = response.json()
    try:
        address = ksql_response[1].get("row", {}).get("columns", {})[2].get("ADDRESS")
    except Exception as e:
        print(f"Could not resolve address from message: {ksql_response}, reason: {e}")
        address = "No address found"

    return address


