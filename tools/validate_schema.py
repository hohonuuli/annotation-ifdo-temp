# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml", "jsonschema[format]"]
# ///
"""Validate YAML or JSON annotation files against annotation-standard.schema.json.

usage: uv run tools/validate_schema.py <schema.json> <file> [<file> ...]
YAML timestamps are kept as strings, as they would be in JSON.
"""
import json
import sys

import yaml
from jsonschema import Draft202012Validator, FormatChecker


class StringTimestampLoader(yaml.SafeLoader):
    pass


StringTimestampLoader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def main():
    schema = json.load(open(sys.argv[1]))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    bad = 0
    for path in sys.argv[2:]:
        text = open(path).read()
        doc = json.loads(text) if path.endswith(".json") else yaml.load(text, Loader=StringTimestampLoader)
        errs = sorted(validator.iter_errors(doc), key=lambda e: list(e.absolute_path))
        print(f"{path}: {'OK' if not errs else str(len(errs)) + ' error(s)'}")
        for e in errs:
            loc = "/".join(str(p) for p in e.absolute_path) or "(root)"
            print(f"  {loc}: {e.message[:160]}")
        bad += bool(errs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
