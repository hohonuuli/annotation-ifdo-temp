# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Reference COCO RLE encoder and decoder (column-major), written from the encoding rules in
refined_standard.md ("Pixel masks"). No numpy needed. Used by validate_rules.py.

usage: uv run tools/rle.py
           print the example ring mask from the standard (counts, compressed string, extent, area)
       uv run --with numpy --with pycocotools tools/rle.py --check-pycocotools
           also encode the same mask with pycocotools and compare
"""
import json
import sys


def encode(inside, width, height):
    """inside(x, y) -> bool for pixel column x, row y. Returns uncompressed counts."""
    counts, cur, run = [], 0, 0
    for x in range(width):
        for y in range(height):
            v = 1 if inside(x, y) else 0
            if v != cur:
                counts.append(run)
                cur, run = v, 0
            run += 1
    counts.append(run)
    return counts


def to_string(counts):
    """pycocotools rleToString: delta from counts[i-2] for i > 2, 5-bit groups, offset 48."""
    out = []
    for i, x in enumerate(counts):
        if i > 2:
            x -= counts[i - 2]
        more = True
        while more:
            c = x & 0x1F
            x >>= 5
            more = (x != -1) if (c & 0x10) else (x != 0)
            if more:
                c |= 0x20
            out.append(chr(c + 48))
    return "".join(out)


def from_string(s):
    counts, p = [], 0
    while p < len(s):
        x, k, more = 0, 0, True
        while more:
            c = ord(s[p]) - 48
            x |= (c & 0x1F) << (5 * k)
            more = bool(c & 0x20)
            p += 1
            k += 1
            if not more and (c & 0x10):
                x |= -1 << (5 * k)
        if len(counts) > 2:
            x += counts[-2]
        counts.append(x)
    return counts


def extent(counts, width, height):
    """Bounding rectangle [xmin, ymin, xmax, ymax] in corner coordinates."""
    xs, ys, pos = [], [], 0
    for i, n in enumerate(counts):
        if i % 2 == 1:
            for p in range(pos, pos + n):
                xs.append(p // height)
                ys.append(p % height)
        pos += n
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


if __name__ == "__main__":
    W, H = 6000, 4000
    cx, cy = 4500.5, 2800.5

    def ring(x, y):
        d2 = (x + 0.5 - cx) ** 2 + ((y + 0.5 - cy) / 0.7) ** 2
        return 4 ** 2 < d2 <= 12 ** 2

    counts = encode(ring, W, H)
    s = to_string(counts)
    assert from_string(s) == counts
    print(json.dumps({"counts": counts, "string": s, "extent": extent(counts, W, H),
                      "area": sum(counts[1::2]), "n": len(counts)}))
    if "--check-pycocotools" in sys.argv[1:]:
        import numpy as np
        from pycocotools import mask as m
        arr = np.zeros((H, W), dtype=np.uint8, order="F")
        for x in range(4480, 4521):
            for y in range(2780, 2821):
                arr[y, x] = ring(x, y)
        ref = m.encode(arr)
        same = ref["counts"].decode() == s
        print("pycocotools string matches:", same)
        print("pycocotools area:", int(m.area(ref)), "bbox xywh:", m.toBbox(ref).tolist())
        sys.exit(0 if same else 1)
