# utils.py
import os

high_score_file = "high_score.txt"

def read_high_score():
    if os.path.exists(high_score_file):
        with open(high_score_file, "r") as file:
            return int(file.read())
    return 0

def save_high_score(high_score):
    with open(high_score_file, "w") as file:
        file.write(str(high_score))
