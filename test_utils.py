import random as rnd
import os.path

STRESS_WORDS = []

with open(os.path.join("tests_sources", "stress_words_fix.txt"), "r", encoding="utf-8") as f:
    STRESS_WORDS = f.read().strip().split("\n")

def get_stress_word():
    r = rnd.randint(0, len(STRESS_WORDS)-1)
    return STRESS_WORDS[r]