from django_tasks import task


from icecream import ic
import time
from typing import List, Generator


@task()
def calculate_meaning_of_life():
    halo: List[int] = []
    for i in range(1, 10):
        time.sleep(2)
        halo.append(i)
        i += 1

    return halo
