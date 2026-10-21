# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Check annotation files against the rules in refined_standard.md that JSON Schema cannot
express, and generate the nested form of a prefixed file.

usage: uv run tools/validate_rules.py check <prefixed.yaml> [<label-set.yaml>] [--nested <nested.yaml>]
       uv run tools/validate_rules.py nest <prefixed.yaml> <nested.yaml>

check: <label-set.yaml> supplies the label set when the file being checked has none of its own.
       --nested also confirms that <nested.yaml> is the nested form of <prefixed.yaml>.
nest:  writes the nested form (Naming rule 8) and confirms it round-trips.
"""
import math
import re
import sys
import uuid

import yaml

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import rle  # noqa: E402

PREFIXES = ["label-set-", "label-", "annotation-set-", "annotation-", "image-", "model-", "review-"]
NAMESPACE = uuid.UUID("8fb66ecc-ce0d-45ff-b8ab-23bd7774d760")

NESTED_HEADER = """\
# Nested form of annotation-standard-sample.yaml (refined_standard.md, revision 0.11, Naming rule 8).
#
# Generated from the prefixed sample: each key is the prefixed name with its container's prefix
# removed (label-set-, label-, annotation-set-, annotation-, image-, model-, review-).
# For example annotation-set > name == annotation-set-name, and annotation-set > annotations >
# image-uuid == annotation-image-uuid. The prefixed file is the normative form; both carry the
# same information.
"""


def strip(key):
    if key in ("label-set", "annotation-set"):
        return key
    for p in PREFIXES:
        if key.startswith(p):
            return key[len(p):]
    return key


def nest_obj(o):
    if isinstance(o, dict):
        return {strip(k): nest_obj(v) for k, v in o.items()}
    if isinstance(o, list):
        return [nest_obj(v) for v in o]
    return o


KEY_RE = re.compile(r"^(\s*(?:- )?)([a-z][a-z0-9+-]*)(:(?:\s|$))")


def nest_text(text):
    lines = text.split("\n")
    # drop the prefixed file's header comment block
    i = 0
    while i < len(lines) and (lines[i].startswith("#") or lines[i] == ""):
        i += 1
    out = []
    for line in lines[i:]:
        m = KEY_RE.match(line)
        if m and m.group(2) not in ("label-set", "annotation-set"):
            line = m.group(1) + strip(m.group(2)) + line[m.end(2):]
        out.append(line)
    return NESTED_HEADER + "\n" + "\n".join(out)


errors = []


def err(where, msg):
    errors.append(f"{where}: {msg}")


SHAPES = {
    "single-pixel": lambda n: n == 2,
    "polyline": lambda n: n >= 4 and n % 2 == 0,
    "polygon": lambda n: n >= 8 and n % 2 == 0,
    "rectangle": lambda n: n == 8,
    "circle": lambda n: n == 3,
    "ellipse": lambda n: n == 8,
    "whole-image": lambda n: n == 0,
    "mask": lambda n: n == 8,
}


def check_mask(where, a, w, h):
    m = a.get("annotation-mask")
    if a["annotation-shape-name"] != "mask":
        if m is not None:
            err(where, "annotation-mask only allowed when the shape is mask")
        return
    if m is None:
        return err(where, "mask shape needs annotation-mask")
    if (m.get("width"), m.get("height")) != (w, h):
        return err(where, f"mask size {m.get('width')}x{m.get('height')} is not the image size {w}x{h}")
    enc, counts = m.get("encoding"), m.get("counts")
    if enc == "coco-rle-compressed":
        if not isinstance(counts, str):
            return err(where, "compressed counts must be a string")
        counts = rle.from_string(counts)
    elif enc == "coco-rle":
        if not (isinstance(counts, list) and all(isinstance(c, int) and c >= 0 for c in counts)):
            return err(where, "coco-rle counts must be non-negative integers")
    else:
        return err(where, f"unknown mask encoding {enc}")
    if sum(counts) != w * h:
        return err(where, f"mask counts sum to {sum(counts)}, not {w * h}")
    if not any(counts[1::2]):
        return err(where, "mask is empty")
    x0, y0, x1, y1 = rle.extent(counts, w, h)
    if a["annotation-coordinates"] != [[x0, y0, x1, y0, x1, y1, x0, y1]]:
        err(where, f"coordinates are not the mask's bounding rectangle [{x0}, {y0}]-[{x1}, {y1}]")


def check_shape(where, shape, coords, w, h):
    if shape not in SHAPES:
        return err(where, f"unknown shape {shape}")
    if not isinstance(coords, list) or len(coords) != 1:
        return err(where, "still image needs exactly one inner coordinate array")
    c = coords[0]
    if not SHAPES[shape](len(c)):
        return err(where, f"{shape} has wrong number of values ({len(c)})")
    pts = list(zip(c[0::2], c[1::2])) if shape != "circle" else [(c[0], c[1])]
    if shape not in ("circle", "ellipse"):
        for x, y in pts:
            if not (0 <= x <= w and 0 <= y <= h):
                err(where, f"vertex ({x}, {y}) outside {w}x{h} image")
    if shape == "polygon":
        if pts[0] != pts[-1]:
            err(where, "polygon is not closed")
        if len(set(pts[:-1])) < 3:
            err(where, "polygon needs 3 distinct vertices")
    if shape in ("rectangle", "mask"):
        for i in range(4):
            a, b, d = pts[i - 1], pts[i], pts[(i + 1) % 4]
            v1 = (a[0] - b[0], a[1] - b[1])
            v2 = (d[0] - b[0], d[1] - b[1])
            if abs(v1[0] * v2[0] + v1[1] * v2[1]) > 1e-6 * (math.hypot(*v1) * math.hypot(*v2) + 1):
                err(where, "rectangle sides not perpendicular")
                break
    if shape == "ellipse":
        a1, a2, b1, b2 = pts
        mid_a = ((a1[0] + a2[0]) / 2, (a1[1] + a2[1]) / 2)
        mid_b = ((b1[0] + b2[0]) / 2, (b1[1] + b2[1]) / 2)
        va = (a2[0] - a1[0], a2[1] - a1[1])
        vb = (b2[0] - b1[0], b2[1] - b1[1])
        if mid_a != mid_b or abs(va[0] * vb[0] + va[1] * vb[1]) > 1e-6:
            err(where, "ellipse axes must bisect each other at right angles")
    if shape == "circle" and c[2] <= 0:
        err(where, "circle radius must be > 0")


def check_utc(where, name, value):
    """ISO 8601 UTC: PyYAML gives an aware datetime for values ending in Z."""
    off = getattr(value, "utcoffset", lambda: None)()
    if off is None or off.total_seconds() != 0:
        err(where, f"{name} must be an ISO 8601 date-time in UTC (got {value!r})")


HOM = {(False, False): "human", (True, True): "algorithm", (True, False): "combination",
       (False, True): "combination"}


REQUIRED = {
    "label-set": ["label-set-standard-version", "label-set-name", "label-set-uuid", "label-set-labels"],
    "annotation-set": ["annotation-set-standard-version", "annotation-set-name", "annotation-set-uuid",
                       "annotation-set-label-set-uuids", "annotation-set-images",
                       "annotation-set-annotations"],
    "label": ["label-name", "label-uuid"],
    "annotation": ["annotation-uuid", "annotation-image-uuid", "annotation-label-name",
                   "annotation-shape-name", "annotation-coordinates",
                   "annotation-creation-datetime", "annotation-human-or-machine"],
}


def check_file(doc):
    """File structure rules (revision 0.11)."""
    keys = set(doc)
    if not keys & {"label-set", "annotation-set"}:
        err("file", "needs a top-level label-set or annotation-set")
    for k in keys - {"label-set", "annotation-set"}:
        err("file", f"unknown top-level key {k}")
    for kind in ("label-set", "annotation-set"):
        if kind not in doc:
            continue
        for k in REQUIRED[kind]:
            if k not in doc[kind]:
                err(kind, f"missing {k}")
        v = doc[kind].get(f"{kind}-standard-version")
        if not isinstance(v, str):
            err(kind, f"{kind}-standard-version must be quoted text (got {v!r})")
    for lab in doc.get("label-set", {}).get("label-set-labels", []):
        for k in REQUIRED["label"]:
            if k not in lab:
                err(f"label {lab.get('label-name')}", f"missing {k}")
    for a in doc.get("annotation-set", {}).get("annotation-set-annotations", []):
        for k in REQUIRED["annotation"]:
            if k not in a:
                err(f"annotation {a.get('annotation-uuid')}", f"missing {k}")
    if "label-set" in doc and "annotation-set" in doc:
        if doc["label-set"].get("label-set-uuid") not in doc["annotation-set"].get(
                "annotation-set-label-set-uuids", []):
            err("file", "bundled label set is not in annotation-set-label-set-uuids")


def check(doc, label_names):
    check_file(doc)
    if errors or "annotation-set" not in doc:
        return
    aset = doc["annotation-set"]
    meta = aset.get("annotation-set-image-metadata", "ifdo")
    set_uuids = aset.get("annotation-set-image-set-uuids", [])
    if meta == "none" and set_uuids:
        err("annotation-set", "image set UUIDs must be omitted when image-metadata is none")
    images = {}
    for im in aset["annotation-set-images"]:
        u = im["image-uuid"]
        where = f"image {u}"
        images[u] = im
        for k in ("image-uuid-source", "image-width-pixels", "image-height-pixels"):
            if k not in im:
                err(where, f"missing {k}")
        if im.get("image-uuid-source") == "assigned" and "image-hash-sha256" not in im:
            err(where, "assigned UUID needs image-hash-sha256 (null if unhashable)")
        if "image-datetime" in im:
            check_utc(where, "image-datetime", im["image-datetime"])
        hsh = im.get("image-hash-sha256")
        if hsh is not None and not re.fullmatch(r"[0-9a-f]{64}", hsh):
            err(where, "hash must be 64 lowercase hex characters")
        if (meta == "none" or ("image-hash-sha256" in im and hsh is None)) and "image-handle" not in im:
            err(where, "image-handle required")
        if meta == "ifdo":
            if len(set_uuids) > 1 and im.get("image-set-uuid") not in set_uuids:
                err(where, "image-set-uuid must be one of the set's image set UUIDs")
        elif "image-set-uuid" in im:
            err(where, "image-set-uuid must be omitted when image-metadata is none")
    models = {m["model-id"]: m for m in aset.get("annotation-set-models", [])}
    for mid, m in models.items():
        for k in ("model-name", "model-version", "model-task"):
            if k not in m:
                err(f"model {mid}", f"missing {k}")
    used_conf = set()
    for a in aset["annotation-set-annotations"]:
        where = f"annotation {a['annotation-uuid']}"
        im = images.get(a["annotation-image-uuid"])
        if im is None:
            err(where, "annotation-image-uuid not in annotation-set-images")
            continue
        check_shape(where, a["annotation-shape-name"], a["annotation-coordinates"],
                    im["image-width-pixels"], im["image-height-pixels"])
        check_mask(where, a, im["image-width-pixels"], im["image-height-pixels"])
        check_utc(where, "annotation-creation-datetime", a.get("annotation-creation-datetime"))
        if label_names is not None and a["annotation-label-name"] not in label_names:
            err(where, f"label {a['annotation-label-name']!r} not in the label set")
        det, cls = a.get("annotation-detection-model"), a.get("annotation-classification-model")
        for step, mdl in (("detection", det), ("classification", cls)):
            conf = a.get(f"annotation-{step}-confidence")
            if mdl is not None and mdl not in models:
                err(where, f"{step} model {mdl} not in annotation-set-models")
            if mdl is None and conf is not None:
                err(where, f"{step} confidence without a model")
            if conf is not None:
                used_conf.add(mdl)
                if not 0 <= conf <= 1:
                    err(where, f"{step} confidence outside [0, 1]")
        if a.get("annotation-human-or-machine") != HOM[(det is not None, cls is not None)]:
            err(where, "annotation-human-or-machine disagrees with the model fields")
        creators = a.get("annotation-human-creators", [])
        if det is not None and cls is not None and creators:
            err(where, "human creators listed although both steps were by a model")
        if (det is None or cls is None) and not creators:
            err(where, "a human step but no human creators")
        reviews = a.get("annotation-reviews", [])
        status = reviews[-1]["review-outcome"] if reviews else "unreviewed"
        if a.get("annotation-review-status") != status:
            err(where, f"review status should be {status}")
        times = [r["review-datetime"] for r in reviews if r.get("review-datetime") is not None]
        if times != sorted(times):
            err(where, "reviews not oldest first")
        for r in reviews:
            if "name" not in r.get("review-reviewer", {}):
                err(where, "review-reviewer needs a name")
            if r["review-outcome"] == "modified":
                if not r.get("review-changed"):
                    err(where, "modified review needs review-changed")
                if "label" in r.get("review-changed", []) and any(
                        p["name"] == r["review-reviewer"]["name"] for p in creators) is False:
                    err(where, "reviewer who modified must be in annotation-human-creators")
            elif "review-changed" in r:
                err(where, "review-changed only allowed on modified reviews")
    for mid in used_conf:
        if "model-score-type" not in models[mid]:
            err(f"model {mid}", "model-score-type required when confidences are reported")


def main():
    if sys.argv[1] == "nest":
        text = open(sys.argv[2]).read()
        nested = nest_text(text)
        if yaml.safe_load(nested) != nest_obj(yaml.safe_load(text)):
            sys.exit("nested text does not match the structural transform")
        open(sys.argv[3], "w").write(nested)
        print(f"wrote {sys.argv[3]}")
        return
    args = sys.argv[2:]
    nested_path = None
    if "--nested" in args:
        i = args.index("--nested")
        nested_path = args[i + 1]
        del args[i:i + 2]
    doc = yaml.safe_load(open(args[0]))
    ls_doc = yaml.safe_load(open(args[1])) if len(args) > 1 else doc
    labels = ({lab["label-name"] for lab in ls_doc["label-set"].get("label-set-labels", [])}
              if "label-set" in ls_doc else None)
    check(doc, labels)
    for im in doc.get("annotation-set", {}).get("annotation-set-images", []):
        h = im.get("image-hash-sha256")
        if h and str(uuid.uuid5(NAMESPACE, h)) == im["image-uuid"]:
            print(f"  {im['image-uuid']}: hash-derived UUID matches its SHA-256")
    if nested_path and yaml.safe_load(open(nested_path)) != nest_obj(doc):
        err("nested", "nested file is not the nested form of the prefixed file")
    print(f"{args[0]}: {'OK' if not errors else str(len(errors)) + ' problem(s)'}")
    for e in errors:
        print("  " + e)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
