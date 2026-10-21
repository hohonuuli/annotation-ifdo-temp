# Marine image annotation standard: working revision

A working draft that refines the annotation and label standard proposed in *United metadata
standards to enhance the interoperability of marine image annotation data* (Durden et al., in
preparation). The standard describes **label sets**, **annotation sets** and **annotations** made
on marine imagery. It builds on the [image FAIR Digital Object (iFDO)](https://ifdo-schema.org/)
standard, and maps to Darwin Core and to the VARS, BIIGLE and SQUIDLE+ annotation platforms.

**Status:** draft, revision 0.11. Attribute names, requirement levels and the schema may still
change.

## Contents

| Path | What it is |
| --- | --- |
| [refined_standard.md](refined_standard.md) | The standard. It is a living document with a change log and a list of open issues. |
| [annotation-standard.schema.json](annotation-standard.schema.json) | Draft JSON Schema (2020-12) for the standard's prefixed form |
| [annotation-standard-sample.yaml](annotation-standard-sample.yaml) | Sample label set and annotation set, using every feature of the standard |
| [annotation-standard-sample-nested.yaml](annotation-standard-sample-nested.yaml) | The same sample with short nested names, generated from the one above |
| [annotation-standard-sample-no-ifdo.yaml](annotation-standard-sample-no-ifdo.yaml) | Sample annotation set for images that have no iFDO |
| [tools/](tools/README.md) | Scripts that validate files against the schema and the standard's other rules |

## The standard at a glance

- [Naming rules](refined_standard.md#naming-rules) and [File structure](refined_standard.md#file-structure):
  how attributes are named, the top-level `label-set` and `annotation-set` containers,
  requirement levels, and the [JSON Schema](refined_standard.md#json-schema).
- [Annotation shapes and coordinates](refined_standard.md#annotation-shapes-and-coordinates) and
  [Pixel masks](refined_standard.md#pixel-masks): shape names and coordinate encodings, aligned
  with iFDO, plus masks stored as COCO RLE.
- [Referencing the annotated image](refined_standard.md#referencing-the-annotated-image): how
  annotations name images by UUID, record pixel size and [capture time](refined_standard.md#capture-time),
  and handle [images without an embedded UUID or an iFDO](refined_standard.md#images-without-an-embedded-uuid-or-without-an-ifdo).
- [Machine-generated annotations](refined_standard.md#machine-generated-annotations-models-and-confidence)
  and [Review provenance](refined_standard.md#review-provenance): which model did each step, its
  confidence, and who reviewed the result.
- [Tables 1–4](refined_standard.md#table-1-label-set-attributes): every attribute, with its
  requirement level and its Darwin Core, BIIGLE, VARS and SQUIDLE+ equivalents.
- [VARS: corrected notes](refined_standard.md#vars-corrected-notes): how VARS (annosaurus)
  actually stores annotations.
- [Open issues](refined_standard.md#open-issues-for-later-revisions): what is still to be decided.

## Validating a file

You need [uv](https://docs.astral.sh/uv/). From this folder:

```bash
uv run tools/validate_schema.py annotation-standard.schema.json annotation-standard-sample.yaml
```

```bash
uv run tools/validate_rules.py check annotation-standard-sample.yaml
```

A file needs to pass both checks. See [tools/README.md](tools/README.md) for all commands.
