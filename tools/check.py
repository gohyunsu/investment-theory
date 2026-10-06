"""Check slide mapping, numeric examples, and publication exclusions."""
from __future__ import annotations

import json
import math
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
print("66 slide mappings, image dimensions, publication exclusions and calculations passed")
