from celery import Celery

from financialdata.config import (
    MESSAGE_QUEUE_HOST,
    MESSAGE_QUEUE_PORT,
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
)

broker = (
    f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@"
    f"{MESSAGE_QUEUE_HOST}:{MESSAGE_QUEUE_PORT}/"
)
app = Celery(
    "task",
    include=["housedata.tasks.task"],
    broker=broker,
)
