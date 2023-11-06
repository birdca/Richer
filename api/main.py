import pandas as pd
from fastapi import FastAPI
from sqlalchemy import create_engine, engine
from api import config
import ipaddress
import json
import os
import subprocess
from enum import Enum

import uvicorn
from dotenv import load_dotenv
from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    Header,
    HTTPException,
    Request,
    status,
)
from httpx import AsyncClient
from loguru import logger

import hmac
import hashlib


def get_mysql_financialdata_conn() -> engine.base.Connection:
    address = (
        f"mysql+pymysql://{config.MYSQL_DATA_USER}:{config.MYSQL_DATA_PASSWORD}"
        f"@{config.MYSQL_DATA_HOST}:{config.MYSQL_DATA_PORT}/{config.MYSQL_DATA_DATABASE}"
    )
    engine = create_engine(address)
    connect = engine.connect()
    return connect


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/taiwan_stock_price")
def taiwan_stock_price(
        stock_id: str = "",
        start_date: str = "",
        end_date: str = "",
):
    sql = f"""
    select * from taiwan_stock_price
    where StockID = '{stock_id}'
    and Date>= '{start_date}'
    and Date<= '{end_date}'
    """
    mysql_conn = get_mysql_financialdata_conn()
    data_df = pd.read_sql(sql, con=mysql_conn)
    data_dict = data_df.to_dict("records")
    return {"data": data_dict}


def deploy_application(script_name):
    # subprocess.run(["ls", "-l"]) test
    # give_permission = "chmod +x "
    # result = subprocess.run([script_name, config.DOCKER_HUB_TOKEN])
    # my_env = os.environ.copy()
    # print(my_env)
    # my_env = {'DOCKER_HUB_TOKEN': config.GITHUB_SECRET}
    subprocess.Popen(script_name)
    # process = subprocess.Popen([script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # process.wait()  # Wait for process to complete.
    #
    # # iterate on the stdout line by line
    # for line in process.stdout.readlines():
    #     print(line)
    # logger.info("result:{}".format(result))


async def gate_by_github_secret(request: Request):
    # See if github secret matched test
    secret = config.GITHUB_SECRET
    body = await request.body()
    local_signature = hmac.new(secret.encode('utf-8'), msg=body, digestmod=hashlib.sha1)
    expected_signature = "sha1=" + local_signature.hexdigest()
    if request.headers['X-Hub-Signature'] == expected_signature:
        return
    else:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "No access permission"
        )


@app.post("/deployimage", dependencies=[Depends(gate_by_github_secret)])
async def receive_payload(
        request: Request,
        background_tasks: BackgroundTasks,
        x_github_event: str = Header(...),
):
    # test upgrade test
    if x_github_event == "push":
        payload = await request.json()
        logger.info("get payload:{}".format(payload))

        default_branch = payload["repository"]["default_branch"]

        script_name = "scripts/deploy_image.sh"
        # script_name = "ls /usr/local"
        background_tasks.add_task(deploy_application, script_name)
        return {"message": "Deployment test"}
        # check if event is referencing the default branch
        if "ref" in payload and payload["ref"] == f"refs/heads/{default_branch}":
            # check if app_name is declared in config
            script_name = "/usr/bin/Richer/scripts/deploy_image.sh"
            background_tasks.add_task(deploy_application, script_name)
            return {"message": "Deployment started"}

    elif x_github_event == "ping":
        return {"message": "pong"}

    else:
        return {"message": "Unable to process action"}


def calc_signature(payload):
    secret = config.GITHUB_SECRET
    digest = hmac.new(
        key=secret.encode("utf-8"), msg=payload, digestmod="sha1"
    ).hexdigest()
    return f"sha1={digest}"
