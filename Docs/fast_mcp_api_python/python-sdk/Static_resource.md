@server.resource("file://config.json")
def get_config() -> dict:
    return {"setting": "value"}