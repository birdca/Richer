from housedata.tasks.worker import app
from housedata.crawler import main


@app.task()
def crawler(x):
    main()
    return x
