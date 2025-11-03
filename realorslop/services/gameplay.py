import json
import os
import random
from pathlib import Path

#pairs = env.get("PAIRS_FILE", "data/pairs.json")
BASE_DIR = Path(__file__).resolve().parent  # realorslop/
PAIRS_FILE = BASE_DIR / "data" / "pairs.json"

highscore = 0
score = 0
lives = 3

def load_pairs(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def pick_pair():
    pair = load_pairs(PAIRS_FILE)
    return random.choice(pair)

def shuffle_pair():
    pair = pick_pair()
    true_or_false = random.choice([True,False])  # 0 means real is left, 1 means ai is left
    if true_or_false == True:
        left_image = pair["real"]
        right_image = pair["ai"]
    elif true_or_false == False:
        left_image = pair["ai"]
        right_image = pair["real"]
    else:
        raise ValueError("Random value must be 0 or 1")

    return {
        "left_image": left_image,
        "right_image": right_image,
        "is_left_real": true_or_false == True,
        "explanation": pair["explanation"]
    }


def score_guess(is_left_real, user_guess):
    update_score(is_left_real == user_guess)

    return is_left_real == user_guess

def update_score(correct):
    global score
    global highscore
    if correct:
        score += 1
        if score > highscore:
            highscore = score
    else:
        lives -= 1
        health_check(lives)
        score = 0

def health_check(lives):
    if lives <= 0:
        return {"status": "game over", "highscore": highscore}
    else:
        return {"status": "ok"}

