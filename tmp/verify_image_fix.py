import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from core.fetcher import get_wikimedia_image

def test_player(name):
    print(f"Testing {name}...")
    url = get_wikimedia_image(name)
    if url:
        print(f"Result URL: {url}")
    else:
        print(f"Result URL: NONE (Initials will show)")
    print("-" * 20)

if __name__ == "__main__":
    # 1. Elliot Anderson - Should find the footballer, not the city or other person
    test_player("Elliot Anderson")
    
    # 2. Ngal'Ayel Mukau - Should handle apostrophe/casing
    test_player("Ngal'Ayel Mukau")
    
    # 3. Known "bad" name that should return nothing (no footballer match)
    test_player("Anderson South Carolina")
