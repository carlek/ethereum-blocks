import json
from pathlib import Path

import fastapi
import uvicorn
from api import etherscan_api
from services import etherscan_service

api = fastapi.FastAPI()


def configure():
    configure_routers()
    configure_api_keys()


def configure_api_keys():
    file = Path('settings.json').absolute()
    if not file.exists():
        print(f"WARNING: {file} file not found, you cannot continue, please see settings_template.json")
        raise Exception("settings.json file not found, you cannot continue, please see settings_template.json")

    with open(file) as f:
        settings = json.load(f)
        etherscan_service.api_key = settings.get('api_key')


def configure_routers():
    api.include_router(etherscan_api.router)

if __name__ == '__main__':
    configure()
    uvicorn.run(api, port=8000, host='127.0.0.1')
else:
    configure()
