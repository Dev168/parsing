import pandas as pd

def get_forks():
    with open("forks_searching\handicap_search.sql", "r") as f:
        sql_code = f.read()

