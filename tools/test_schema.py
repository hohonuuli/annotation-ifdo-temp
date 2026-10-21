# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "jsonschema[format]"]
# ///
"""Make one deliberate mistake at a time in the samples and confirm the schema rejects each.

usage: uv run tools/test_schema.py <schema.json> <sample.yaml> <sample-no-ifdo.yaml>
"""
import copy
import json
import sys

import yaml
from jsonschema import Draft202012Validator, FormatChecker

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from validate_schema import StringTimestampLoader  # noqa: E402

schema_path, sample_path, noifdo_path = sys.argv[1:4]
v = Draft202012Validator(json.load(open(schema_path)), format_checker=FormatChecker())
base = yaml.load(open(sample_path).read(), Loader=StringTimestampLoader)
noifdo = yaml.load(open(noifdo_path).read(), Loader=StringTimestampLoader)
A = lambda d: d["annotation-set"]["annotation-set-annotations"]  # noqa: E731


def ann(d, uuid_prefix):
    return next(a for a in A(d) if a["annotation-uuid"].startswith(uuid_prefix))


def m1(d): del ann(d, "492aa121")["annotation-mask"]
def m2(d): ann(d, "9ef7f6c2")["annotation-coordinates"] = [[1, 2, 3, 4, 5, 6]]
def m3(d): ann(d, "2b7b5a13")["annotation-human-or-machine"] = "algorithm"
def m4(d): ann(d, "9ef7f6c2")["annotation-detection-confidence"] = 0.5
def m5(d): del ann(d, "2b7b5a13")["annotation-reviews"][0]["review-changed"]
def m6(d): del d["annotation-set"]["annotation-set-images"][1]["image-hash-sha256"]
def m7(d): d["annotation-set"]["annotation-set-image-set-uuids"] = ["4b30f1c8-d061-40e0-9d3a-8a971a3c1b45"]
def m8(d): d["label-set"]["label-set-standard-version"] = 0.1
def m9(d): d["label-set"]["Label-set-abstract"] = d["label-set"].pop("label-set-abstract")
def m10(d): ann(d, "9ef7f6c2")["annotation-creation-datetime"] = "2026-09-03 14:22:10"
def m11(d): ann(d, "3340ab0f")["annotation-classification-confidence"] = 81
def m12(d): del d["annotation-set"]["annotation-set-license"]
def m13(d): ann(d, "9ef7f6c2")["annotation-mask"] = ann(d, "492aa121")["annotation-mask"]
def m14(d): ann(d, "3340ab0f")["annotation-human-creators"] = [{"name": "Jo Sample"}]


cases = [
    ("mask shape without annotation-mask", m1, base),
    ("rectangle with 6 values", m2, base),
    ("human-or-machine disagrees with models", m3, base),
    ("confidence without a model", m4, base),
    ("modified review without review-changed", m5, base),
    ("assigned UUID without hash", m6, base),
    ("image set UUIDs with image-metadata none", m7, noifdo),
    ("unquoted standard version", m8, base),
    ("draft-style capitalized name", m9, base),
    ("date-time with a space, no Z", m10, base),
    ("confidence on a 0-100 scale", m11, base),
    ("missing license", m12, base),
    ("annotation-mask on a rectangle", m13, base),
    ("human creators on an algorithm annotation", m14, base),
]
failed = 0
for name, mutate, doc in cases:
    d = copy.deepcopy(doc)
    mutate(d)
    n = len(list(v.iter_errors(d)))
    print(f"{'caught' if n else 'MISSED'}: {name} ({n} error(s))")
    failed += not n
sys.exit(1 if failed else 0)
