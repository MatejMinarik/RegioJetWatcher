import random
from retrying import retry


@retry(stop_max_attempt_number=7, stop_max_delay=10000, wait_fixed=2000)
def pick_one():
    print("not")
    raise Exception("1 was not picked")

pick_one()