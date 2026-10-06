"""Check slide mapping, numeric examples, and publication exclusions."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path

from PIL import Image


root = Path(__file__).resolve().parents[1]
slides = json.loads((root / "data.json").read_text(encoding="utf-8"))
manifest = json.loads((root / "assets/slide-manifest.json").read_text(encoding="utf-8"))
assert len(slides) == len(manifest) == 66
assert len({slide["id"] for slide in slides}) == 66
assert [slide["image"] for slide in slides] == [entry["path"] for entry in manifest]
for slide in slides:
    image = root / slide["image"]
    assert image.is_file(), slide["id"]
    with Image.open(image) as picture:
        assert picture.width >= 1500 and picture.height >= 900, slide["id"]
    assert slide["title"] and slide["html"] and "\ufffd" not in slide["html"]
    assert slide["case"]["title"] and slide["case"]["html"] and "\ufffd" not in slide["case"]["html"]

for chapter_number, chapter_slug in enumerate(("01-intro", "02-risk-return", "03-two-assets"), 1):
    page = (root / "lecture" / f"{chapter_number:02}.html").read_text(encoding="utf-8")
    chapter_slides = [slide for slide in slides if slide["chapter"] == chapter_slug]
    assert len(chapter_slides) == 22
    assert len(re.findall(r'<section class="slide" id="s\d{2}"', page)) == 22
    for slide in chapter_slides:
        assert f'id="s{slide["page"]:02}"' in page
        assert f'../{slide["image"]}' in page
    assert page.count('width="1600" height="1200"') == 22
    assert page.count('class="case-note"') == 22
assert (root / "index.html").read_text(encoding="utf-8").count('<a class="overview-card ') == 3

assert not list(root.rglob("*_original.txt"))
pdfs = [path for path in root.rglob("*.pdf") if "_build" not in path.parts and "_site" not in path.parts]
assert pdfs == [root / "guide.pdf"], pdfs
assert not (root / "slides").exists()
assert not (root / "scripts").exists()
assert not (root / "notes").exists()

cov = .2 * .15 * .2
w_gmv = (.2**2 - cov) / (.15**2 + .2**2 - 2*cov)
var_gmv = w_gmv**2 * .15**2 + (1-w_gmv)**2 * .2**2 + 2*w_gmv*(1-w_gmv)*cov
assert math.isclose(w_gmv, .6732673267326733, abs_tol=1e-12)
assert math.isclose(var_gmv, .01710891089108911, abs_tol=1e-12)
assert math.isclose(.10-1.96*.15, -.194, abs_tol=1e-12)
assert math.isclose((.12166405023547881-.05)/.13942890853347567, .5139827241656482, abs_tol=1e-12)
assert math.isclose(-.10 + .15 * math.exp(-1.96**2 / 2) / math.sqrt(2*math.pi) / .025, .2506456660007088, abs_tol=1e-12)
assert math.isclose(1.5*(-.20)-.5*.07, -.335, abs_tol=1e-12)
assert math.isclose(2*.6*.4*.15*.20, .0144, abs_tol=1e-12)
print("66 slide mappings and questions, image dimensions, publication exclusions and calculations passed")
