from django_tasks import task
from django_tasks import default_task_backend
from icecream import ic

import time


@task()
def fix_returned_stocks(sales_id):
    time.sleep(3)
    ic("fixed")
