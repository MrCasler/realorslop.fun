import json
import os
import random
from pathlib import Path

#pairs = env.get("PAIRS_FILE", "data/pairs.json")

PROJECT_DIR = Path(__file__).resolve().parents[1]  # realorslop/
IMAGES_FILE = PROJECT_DIR / "services" / "data" / "images.json"

if not IMAGES_FILE.exists():
    raise FileNotFoundError(f"images.json not found at {IMAGES_FILE}")

highscore = 0
score = 0
lives = 3
_images_cache = None


def load_images(filepath=IMAGES_FILE):
    global _images_cache
    if _images_cache is None:
        with open(filepath, "r") as f:
            _images_cache = json.load(f)
    return _images_cache

def get_tags():
    images = load_images()
    tags = set()
    for img in images:
        for tag in img.get("tags", []):
            tags.add(tag)
    return sorted(tags)

def _pools_for_tag(tag=None):
    images = load_images()
    # if tag is None or 'all', don't filter by tag
    def matches_tag(img):
        if not tag or tag == "all":
            return True
        return tag in img.get("tags", [])

    ai_pool   = [img for img in images if img.get("label") == "ai"   and matches_tag(img)]
    real_pool = [img for img in images if img.get("label") == "real" and matches_tag(img)]
    return ai_pool, real_pool

def pick_pair(tag=None):
    ai_pool, real_pool = _pools_for_tag(tag)
    if not ai_pool or not real_pool:
        # Up to you: raise, or return None so the API can handle it gracefully
        return None

    ai_img   = random.choice(ai_pool)
    real_img = random.choice(real_pool)

    # Build a neutral pair object; shuffling is handled next
    pair = {
        "ai_src": ai_img["src"],
        "real_src": real_img["src"],
        "explanation": ai_img.get("explanation", "This looks AI-generated based on texture/structure artifacts.")
    }
    return pair


def shuffle_pair(tag=None):
    pair = pick_pair(tag)
    if pair is None:
        return {"error": "not_enough_images_for_tag"}

    is_left_real = random.choice([True, False])
    if is_left_real:
        left_image  = pair["real_src"]
        right_image = pair["ai_src"]
    else:
        left_image  = pair["ai_src"]
        right_image = pair["real_src"]

    return {
        "left_image": left_image,
        "right_image": right_image,
        "is_left_real": is_left_real,
        "explanation": pair["explanation"]
    }

