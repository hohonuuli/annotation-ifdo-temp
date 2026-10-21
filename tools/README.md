# Tools for the annotation standard

Scripts that check files against [refined_standard.md](../refined_standard.md) and the draft
[JSON Schema](../annotation-standard.schema.json). They are drafts, written to check the samples
while the standard is being revised.

| Script | What it does |
| --- | --- |
| `validate_schema.py` | Validates YAML or JSON files against `annotation-standard.schema.json`. |
| `validate_rules.py` | Checks the rules the schema can't express, and generates the nested form of a file. |
| `test_schema.py` | Makes one deliberate mistake at a time in the samples, and confirms the schema rejects each. |
| `rle.py` | Encodes and decodes COCO RLE masks. `validate_rules.py` uses it. |

`validate_rules.py` checks these rules, which the schema can't express:

- references resolve: images, models, labels, and a bundled label set;
- the review status matches the last review, and reviews are oldest first;
- polygons are closed, and rectangle and ellipse geometry is valid;
- vertices are inside the image;
- a mask's size and run total are right, and its bounding rectangle matches;
- a hash-derived UUID matches its hash.

## Requirements

[uv](https://docs.astral.sh/uv/). Each script declares its own dependencies (PyYAML, jsonschema),
so `uv run` installs them in a temporary environment. Nothing is installed globally.

## Running

Run these from the folder that holds `refined_standard.md`, the folder above this one.

Check the samples against the schema:

```bash
uv run tools/validate_schema.py annotation-standard.schema.json annotation-standard-sample.yaml annotation-standard-sample-no-ifdo.yaml
```

Check the main sample against the rules the schema can't express, and confirm that the nested
sample matches it:

```bash
uv run tools/validate_rules.py check annotation-standard-sample.yaml --nested annotation-standard-sample-nested.yaml
```

The no-iFDO sample has no label set of its own. Give it the main sample's label set, so that its
labels can be checked:

```bash
uv run tools/validate_rules.py check annotation-standard-sample-no-ifdo.yaml annotation-standard-sample.yaml
```

After editing the main sample, regenerate the nested sample from it:

```bash
uv run tools/validate_rules.py nest annotation-standard-sample.yaml annotation-standard-sample-nested.yaml
```

Confirm the schema still rejects common mistakes:

```bash
uv run tools/test_schema.py annotation-standard.schema.json annotation-standard-sample.yaml annotation-standard-sample-no-ifdo.yaml
```

Print the example mask from the standard, and check the encoder against pycocotools (this needs
numpy and pycocotools):

```bash
uv run --with numpy --with pycocotools tools/rle.py --check-pycocotools
```

Each script prints `OK` or lists the problems it found. It exits with status 0 if everything
passes and 1 if anything failed, so it can be used in CI.

## Notes

- A file needs to pass both `validate_schema.py` and `validate_rules.py`. Neither covers
  everything on its own.
- `validate_schema.py` reads YAML date-times as text, as they would be in JSON. A date-time
  written without the trailing `Z`, or with a space instead of `T`, is rejected.
- The schema covers the prefixed form only. To check a nested-form file, convert it to the
  prefixed form first.
