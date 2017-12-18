from config import *
debug = config["debugging"]


def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)
