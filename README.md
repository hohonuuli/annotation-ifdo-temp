# Marine image annotation standard: working revision

A working draft that refines the annotation and label standard proposed in *United metadata
standards to enhance the interoperability of marine image annotation data* (Durden et al., in
preparation). The standard describes **label sets**, **annotation sets** and **annotations** made
on marine imagery. It builds on the [image FAIR Digital Object (iFDO)](https://ifdo-schema.org/)
standard, and maps to Darwin Core and to the VARS, BIIGLE and SQUIDLE+ annotation platforms.

**Status:** draft, revision 0.12. Attribute names, requirement levels and the schema may still
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
| [dwc_alignment.md](dwc_alignment.md) | Exploration notes: how the standard aligns with Darwin Core, and possible changes |
| [ac_alignment.md](ac_alignment.md) | Exploration notes: how the standard aligns with Audiovisual Core, and possible changes |

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
- [Tables 1–10](refined_standard.md#table-1-label-set-attributes): every attribute, for label sets,
  labels, annotation sets, annotations, models, images, reviews, masks, `{name, uri}` objects and
  the top-level containers. Each has its requirement level and its Darwin Core, iFDO, BIIGLE,
  VARS and SQUIDLE+ equivalents where they exist.
- [VARS: corrected notes](refined_standard.md#vars-corrected-notes): how VARS (annosaurus)
  actually stores annotations.
- [Open issues](refined_standard.md#open-issues-for-later-revisions): what is still to be decided.

## Alignment with TDWG standards

Two exploration documents compare every attribute in Tables 1–10 with a TDWG standard. They
list where the standard already matches and where it doesn't, and suggest changes: corrected
mappings, possible new attributes and a few renames. They are proposals for discussion; none
of them has been applied to [refined_standard.md](refined_standard.md) yet.

- [dwc_alignment.md](dwc_alignment.md) compares the standard with the
  [Darwin Core term list](https://dwc.tdwg.org/terms/), including the Humboldt Extension (`eco:`)
  Survey terms. Its main findings:
  - image-based records are always `MachineObservation`;
  - labels map to `dwc:verbatimIdentification`, not `dwc:organismName`;
  - annotators are `dwc:identifiedBy`, not `dwc:recordedBy`;
  - Humboldt terms can record the biological scope and whether absences can be inferred;
  - `dwc:Assertion` fits model confidences and reviews.
- [ac_alignment.md](ac_alignment.md) compares the standard with the
  [Audiovisual Core term list](https://github.com/tdwg/ac/blob/master/docs/termlist/2026-01-23.md)
  (version 2026-01-23), the TDWG standard for media and regions of interest, formerly Audubon
  Core. Its main findings:
  - the region-of-interest rules already match;
  - AC regions support only rectangles and circles;
  - AC has terms for the image hash, variant, format, derivation and capture time;
  - labels map to `ac:CVtermLiteral`, with the label set as the vocabulary;
  - AC's time terms could support video annotation.

## Validating a file

You need [uv](https://docs.astral.sh/uv/). From this folder:

```bash
uv run tools/validate_schema.py annotation-standard.schema.json annotation-standard-sample.yaml
```

```bash
uv run tools/validate_rules.py check annotation-standard-sample.yaml
```

A file needs to pass both checks. See [tools/README.md](tools/README.md) for all commands.
