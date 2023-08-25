from housedata.crawler import main
from housedata.tasks.worker import app


@app.task()
def crawler(x):
    main()
    return x
