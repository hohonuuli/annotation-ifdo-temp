# Refined standard for marine image annotation data

Living document for iterating on the standard proposed in *United metadata standards to enhance the
interoperability of marine image annotation data* (Durden, J. M., Wright, D., Ferreira, T.,
Duncan, G., Lear, D., Savage, J., Schlining, B. & Schoening, T., in preparation; target journal
*Scientific Data*). Throughout this document, "the draft" means that manuscript.

Sample files that follow the draft:

- Paper attribute names: <https://gist.github.com/hohonuuli/6d2729cd34ce6598a0e2829b837d07e6>
- Shorter nested names: <https://gist.github.com/hohonuuli/fe2173f6a07fa1ebcc6b812a13bc3726>

Since revision 0.7, attribute names follow the [naming rules](#naming-rules) below. The draft's
names are listed in the [rename table](#renamed-attributes). Sections written before 0.7 describe
changes from the draft using the draft's names.

## Change log

| Revision | Date | Change |
| --- | --- | --- |
| 0.1 | 2026-10-21 | Started from the draft paper. Corrected the VARS descriptions and the VARS column of Table 4, using the annosaurus source code (`mbari-org/annosaurus`, commit `213e62bb`). Tables 1–3 are copied from the draft unchanged. |
| 0.2 | 2026-10-21 | Defined `annotation-shape-name` and `annotation-coordinates` precisely: shape names, units, origin, vertex order and per-shape encodings, aligned with iFDO v2.2.1. Added conversions from VARS, BIIGLE, COCO and Audubon Core. Replaced the DarwinCore mapping `ac:pixelX, ac:pixelY`, which are not Audubon Core terms. |
| 0.3 | 2026-10-21 | Defined how an annotation names its image. Each annotation now carries `annotation-image-uuid`, which is the iFDO `image-uuid`, instead of `image-filename`. A new set-level `annotation-images` list records each annotated image once, with its filename, image set and pixel width and height. |
| 0.4 | 2026-10-21 | Allowed images whose UUID is not embedded in the file, and images with no iFDO. Added `image-uuid-source` (`embedded` or `assigned`) and the set-level `annotation-image-metadata` (`ifdo` or `none`). The SHA-256 hash is required when a UUID is assigned. Existing platform UUIDs are kept. Otherwise a UUID v5 is derived from the hash, with a namespace UUID for this standard. |
| 0.5 | 2026-10-21 | Added per-annotation machine provenance. A set-level `annotation-machine-models` list (with identity, task, score meaning, threshold and per-model training and validation data) replaces `annotation-machine-algorithm` and the set-level training and validation links. Annotations name the model and confidence (0–1) separately for detection and for classification. `annotation-machine-detect-or-classify` is now derived, and `annotation-human-or-machine` must agree with the model fields. |
| 0.6 | 2026-10-21 | Added review provenance. A per-annotation `annotation-reviews` list (reviewer, time, outcome `accepted` / `modified` / `rejected` / `uncertain`, what changed, previous values) replaces `annotation-human-reviewer` and `annotation-human-reviewer-ID`. Added a summary field, `annotation-review-status`, mapped to Darwin Core. Rejected annotations may be kept, but are never occurrences. |
| 0.7 | 2026-10-21 | Cleaned up attribute names (open issue 6). Added [naming rules](#naming-rules): lowercase, a prefix for each level (`label-set-`, `label-`, `annotation-set-`, `annotation-`, `image-`, `model-`, `review-`), plural names for lists, and `{name, uri}` objects for people and named things, as in iFDO. Gave the unnamed rows names. Chose `annotation-set-machine-scope` over `annotation-machine-use`. Named the containers (open issue 7). Rewrote Tables 1–4 with the new names, and added a [rename table](#renamed-attributes). |
| 0.8 | 2026-10-21 | Added pixel masks (open issue 8). The new shape `mask` keeps its bounding rectangle in `annotation-coordinates`. The mask itself is a new `annotation-mask` object holding a full-image COCO RLE, in either the integer-list or the compressed-string form. Spelled out the encoding rules, and added conversions from COCO, SAM and VARS. Added open issue 10 (dense label maps). |
| 0.9 | 2026-10-21 | Added an optional `image-datetime` (capture time) to `annotation-set-images` entries. It is the same instant as iFDO's `image-datetime` and VARS's `recorded_timestamp`, and maps to Darwin Core `eventDate`. It is optional with an iFDO and recommended without one. The general video case is not covered. |
| 0.10 | 2026-10-21 | Formally defined the top-level containers `label-set` and `annotation-set` in a new [File structure](#file-structure) section: at most one of each per file, a bundled label set must be one the annotation set uses, other top-level keys are reserved, and each container has a minimum set of required attributes. Added `label-set-standard-version` and `annotation-set-standard-version`. Added serialization rules and the reasons for not using iFDO's header and items layout. Added open issue 11 (requirement levels and a schema). |
| 0.11 | 2026-10-21 | Added a Level column (REQUIRED / RECOMMENDED / OPTIONAL / conditional) to every attribute in Tables 1–4, replacing the 0.10 minimum. Added a draft JSON Schema, [annotation-standard.schema.json](annotation-standard.schema.json), and listed the checks it cannot make. Resolved open issue 11, and added open issue 12 (local extensions). |
| 0.12 | 2026-10-21 | Gathered every attribute into the tables at the end of the document. Added [Table 5](#table-5-model-attributes) (model attributes), [Table 6](#table-6-image-attributes) (image attributes), [Table 7](#table-7-review-attributes) (review attributes), [Table 8](#table-8-mask-keys) (mask keys) [Table 9](#table-9-name-and-uri-object) (`{name, uri}` object) and [Table 10](#table-10-top-level-containers) (top-level containers), with levels and Darwin Core, iFDO, COCO and VARS terms where they apply. The attribute tables inside the sections, including the model, image, review and mask tables and the per-section annotation tables, are replaced by links to the end tables. Their extra detail was merged into Table 4. No attribute rules changed. |

## Structure

The standard has three components. An **annotation set** is made by observing one or more
**image sets** using one or more **label sets**. Image sets and image metadata are defined by
iFDO. Label sets, labels, annotation sets and annotations are defined below.

---

## Naming rules

The draft's names have mixed capitalization (`Label-set-abstract`, `lowest-AphiaID`) and a stray
space (`label-name- is-lowest`). Several table rows have no name at all: the creator and PI IDs,
and the project and context URIs. The same prefix is used at two levels. For example,
`annotation-license` describes the set, but `annotation-uuid` describes one annotation. The rules
below fix this. They follow iFDO v2.2.1 wherever iFDO has a convention.

1. **Characters.** Names use lowercase letters, digits and hyphens only. Acronyms are lowercase,
   as in iFDO (`image-hash-sha256`, `image-set-uuid`): `uuid`, `doi`, `obis`, `aphia-id`.
2. **The prefix gives the level.**

   | Prefix | Level | Defined in |
   | --- | --- | --- |
   | `label-set-` | The label set | Table 1 |
   | `label-` | One label | Table 2 |
   | `annotation-set-` | The annotation set | Table 3 |
   | `annotation-` | One annotation | Table 4 |
   | `image-` | One entry in `annotation-set-images` (same names as iFDO) | [Table 6](#table-6-image-attributes) |
   | `model-` | One entry in `annotation-set-models` | [Table 5](#table-5-model-attributes) |
   | `review-` | One entry in `annotation-reviews` | [Table 7](#table-7-review-attributes) |

   This is the same split as iFDO's `image-set-` (set level) and `image-` (item level).
3. **References** to another object end in `-uuid`, or `-uuids` for a list. Examples:
   `annotation-image-uuid`, `annotation-set-label-set-uuids`.
4. **Lists have plural names**, for example `-creators`, `-images`, `-models`, `-reviews` and
   `-uuids`. Mass nouns are the exception: `-related-material` and `-funding` hold lists but stay
   singular.
5. **People and named things are `{name, uri}` objects**, as in iFDO (`image-pi`,
   `image-creators`, `image-project`, `image-license`). `name` is REQUIRED and `uri` is optional.
   - For a person, `uri` SHOULD be an ORCID. If there is no ORCID, it MAY be a `mailto:` URI.
   - This replaces the draft's unnamed second rows (IDs and URIs) and its parallel name and ID
     lists.
   - The object is defined in [Table 9](#table-9-name-and-uri-object).
6. **Values.** Controlled values are lowercase tokens with hyphens, such as `presence-absence` or
   `detection+classification`. Booleans are `true` and `false`, not Yes and No.
7. **Containers.** These are defined formally in [File structure](#file-structure).
   - A file holds a top-level `label-set` object, a top-level `annotation-set` object, or both.
   - Labels are listed in `label-set-labels`, and annotations in `annotation-set-annotations`.
   - Image, model and review entries are listed in `annotation-set-images`,
     `annotation-set-models` and `annotation-reviews`.
8. **Prefixed and nested forms.** The prefixed names are the normative names. They keep their
   meaning when flattened into CSV columns or database fields. Because the prefixes are
   systematic, the shorter nested form (second gist) follows mechanically: a nested key is the
   prefixed name with its container's prefix removed. For example, `annotation-set` > `name` is
   `annotation-set-name`. Both forms carry the same information.

**`machine-scope` or `machine-use`?** The draft's Table 3 says `annotation-machine-scope`, and its
Results text says `annotation-machine-use`. This revision uses `annotation-set-machine-scope`.
That matches the table, which defines the attribute, and its description, which is about the
scope of machine use. The draft's Results text should change to match.

### Renamed attributes

| Draft name | Name since 0.7 | Other change |
| --- | --- | --- |
| label-set-project, plus an unnamed URI row | label-set-project | `{name, uri}` |
| label-set-context, plus an unnamed URI row | label-set-context | `{name, uri}` |
| Label-set-abstract | label-set-abstract | |
| Label-set-objective | label-set-objective | |
| label-set-creators, plus an unnamed IDs row | label-set-creators | List of `{name, uri}` |
| label-set-pi, plus an unnamed ID row | label-set-pi | `{name, uri}` |
| Label-set-license | label-set-license | `{name, uri}`, as iFDO `image-license` |
| Label-set-copyright | label-set-copyright | |
| Label-set-uuid | label-set-uuid | |
| Label-set-version | label-set-version | Text instead of Number, as in Table 3 |
| Label-set-related-material | label-set-related-material | |
| Label-set-DOI | label-set-doi | |
| Label-set-catalogue | label-set-catalogue | |
| Label-set-funding | label-set-funding | |
| (container, not named) | label-set-labels | New |
| annotation-label-name (Table 2) | label-name | `annotation-label-name` is now only the Table 4 attribute |
| parent-label-name | label-parent-name | |
| lowest-taxonomic-name | label-lowest-taxonomic-name | |
| lowest-AphiaID | label-lowest-aphia-id | |
| label-name- is-lowest | label-is-lowest-taxon | `true` / `false` instead of Yes / No |
| identification-qualifier | label-identification-qualifier | |
| label-name-uuid | label-uuid | |
| annotation-project, plus an unnamed URL row | annotation-set-project | `{name, uri}` |
| annotation-context, plus an unnamed URL row | annotation-set-context | `{name, uri}` |
| annotation-abstract, -objective, -target-environment, -target-timescale, -curation-protocol, -copyright, -related-material, -quantitative-or-qualitative, -quantification-type, -biological-metrics, -biological-stats, -funding | annotation-set-… (same ending) | `quantification-type` values become tokens: `presence-absence`, `count`, `linear-measurement`, `area-measurement`, `volume-measurement`, `rate` |
| annotation-human-creators, plus an unnamed IDs row (Table 3) | annotation-set-creators | List of `{name, uri}` |
| annotation-pi, plus an unnamed ID row | annotation-set-pi | `{name, uri}` |
| annotation-license | annotation-set-license | `{name, uri}` |
| annotation-set-uuid | annotation-set-uuid | Type UUID instead of Text |
| annotation-image-set-name | annotation-set-image-set-names | |
| annotation-image-set-uuid | annotation-set-image-set-uuids | |
| annotation-image-set-handle (Results text only) | annotation-set-image-set-handles | Added to Table 3 |
| label-set-name (Table 3) | annotation-set-label-set-names | List |
| label-set-UUID (Table 3) | annotation-set-label-set-uuids | List |
| annotation-set-connections | annotation-set-connected-set-uuids | |
| annotation-machine-scope / annotation-machine-use | annotation-set-machine-scope | |
| annotation-OBIS-data | annotation-set-obis-datasets | List |
| annotation-images (0.3) | annotation-set-images | |
| annotation-image-metadata (0.4) | annotation-set-image-metadata | |
| annotation-machine-models (0.5) | annotation-set-models | |
| (container, not named) | annotation-set-annotations | New |
| annotation-human-creator, plus an unnamed ID row (Table 4) | annotation-human-creators | List of `{name, uri}`, because a reviewer who modifies an annotation is added (0.6) |
| Annotation-additional-info | annotation-additional-info | |
| review-reviewer and review-reviewer-ID (0.6) | review-reviewer | `{name, uri}` |

All other attribute names are unchanged.

---

## File structure

This section formally defines the top-level containers. Before revision 0.10 they were named only
in naming rule 7.

### Top-level containers

A file following this standard is a single object with at most two keys, `label-set` and
`annotation-set`. Each holds at most one set. They are defined in
[Table 10](#table-10-top-level-containers).

Rules:

1. **At least one is present.** A file MUST contain `label-set`, `annotation-set` or both.
2. **One set of each kind per file.** Each set can be published separately, with its own UUID,
   version, license and DOI. Keeping one per file makes the file the unit of publication. An
   annotation set that uses several label sets references them all in
   `annotation-set-label-set-uuids`. At most one of them may be in the same file; the others are
   published separately.
3. **A bundled label set must be used.** If a file contains both, `label-set-uuid` MUST be one of
   the annotation set's `annotation-set-label-set-uuids`.
4. **No other top-level keys.** Other top-level keys are reserved for later revisions. Readers
   SHOULD ignore keys they don't recognise and SHOULD warn about them.
5. **The names are the same in every form.** `label-set` and `annotation-set` are kept as they are
   in both the prefixed form and the nested form (naming rule 8).

### Requirement levels

Every attribute in Tables 1–10 has a **Level**. Tables 1–4 gained one in revision 0.11. Tables 5–9
gather the model, image, review, mask and `{name, uri}` attributes, which already had
requirement levels, at the end of the document (0.12). The levels are:

| Level | Meaning |
| --- | --- |
| REQUIRED | MUST be present. It MUST NOT be null, unless the level says "(may be null)". |
| RECOMMENDED | SHOULD be present. Leave it out only for a reason, such as the information not existing. |
| OPTIONAL | MAY be present. |
| REQUIRED if … / REQUIRED unless … | REQUIRED when the stated condition holds, and as stated otherwise. |

The levels were chosen as follows:

- **Identity, provenance and reuse are REQUIRED.** For both sets these are the name, UUID,
  standard version, creators and license. An annotation set's abstract and PI are also REQUIRED,
  as in iFDO's header. An annotation's identity and provenance are REQUIRED: its UUID, image,
  label, shape, coordinates, creation time, and whether a human or a machine made it.
- **Model fields on an annotation are REQUIRED, but may be null.** Null means a human did that
  step. An absent field would be ambiguous, and `annotation-human-or-machine` must be checked
  against these fields.
- **Scope and interpretation are RECOMMENDED.** These include the project, objective, curation
  protocol and quantification type. They make the data reusable, but older data often lacks them.
- **Publication links are OPTIONAL until published.** `label-set-doi` and `annotation-set-handle`
  are RECOMMENDED once a set is published.
- **Conditional rules come from earlier revisions.** For example, `annotation-mask` is REQUIRED
  for the `mask` shape (0.8), and `annotation-set-machine-scope` is REQUIRED when models are
  listed (0.5).

### JSON Schema

[annotation-standard.schema.json](annotation-standard.schema.json) is a JSON Schema (draft
2020-12) for the prefixed form. YAML files are checked the same way, after loading. Date-times
must be read as strings, not converted to dates. The schema checks:

- the top-level containers and the REQUIRED attributes at every level;
- types, patterns and controlled values: UUIDs, UTC date-times, quoted standard versions, SHA-256
  hashes, DOIs, `{name, uri}` objects, confidences in [0, 1], and every enumerated value;
- the number of coordinate values for each shape, and exactly one inner array for a still image;
- these conditional rules:
  - a mask is required for the `mask` shape and not allowed otherwise;
  - there is no confidence without a model;
  - `annotation-human-or-machine` agrees with the model fields, and human creators are listed
    exactly when a human did a step;
  - a `modified` review has `review-changed`, and no other review does;
  - an assigned UUID has a hash, and an image that can't be hashed has a handle;
  - an annotation set with `annotation-set-image-metadata: none` has no image set UUIDs;
  - machine scope is given when models are listed;
  - a review status is given once there are reviews;
- **no unknown attributes.** Each object rejects names it does not define. This catches typos and
  the draft's old names, such as `Label-set-abstract`. A way to add local attributes is open
  issue 12.

**What the schema does not check.** JSON Schema cannot compare values across the document or
compute with them. A validator must check these separately:

- Each `annotation-image-uuid` is in `annotation-set-images`, and each model field is a
  `model-id` in `annotation-set-models`.
- Each `annotation-label-name` is a `label-name` in one of the label sets used.
- A bundled label set's UUID is in `annotation-set-label-set-uuids`.
- `annotation-review-status` equals the last review's outcome, and reviews are oldest first.
- A reviewer who modified an annotation is in `annotation-human-creators`.
- Polylines and polygons have an even number of values. Polygons are closed. Rectangle sides are
  perpendicular. Ellipse axes bisect each other at right angles.
- Vertices lie inside the image.
- A mask's width and height equal the image's, its counts add up to width × height, and its
  bounding rectangle equals `annotation-coordinates`.
- A hash-derived UUID matches its hash. Values copied from an iFDO match the iFDO.

The schema covers the prefixed form only. A nested-form file can be checked by converting it to the
prefixed form first, by adding each container's prefix back.

### Standard version

Each container records the revision of this standard it follows:

- `label-set-standard-version` (Table 1)
- `annotation-set-standard-version` (Table 3)

This is the equivalent of iFDO's `image-set-ifdo-version`.

- **Value.** The revision number as text, for example `"0.11"`. It MUST be quoted in YAML,
  because an unquoted `0.10` would be read as the number 0.1. Once the standard is published, the
  value will be its released version number, such as `"1.0"`.
- **Each set carries its own.** A label set and an annotation set are published and versioned
  separately, and may follow different revisions of this standard.
- **Not the set's version.** `label-set-version` and `annotation-set-version` give the version of
  the *data*. `-standard-version` gives the version of the *rules* the data follows.
- **Readers** SHOULD check it. A reader that does not support the stated revision SHOULD warn
  rather than fail. It MAY still read the attributes it knows.

### Serialization

- **Formats.** Files are JSON or YAML, encoded as UTF-8. The extension is `.json`, `.yaml` or
  `.yml`.
- **Nulls.** Null values MAY be written out, or the attribute MAY be left out. Both mean "not
  recorded". The exception is attributes whose rules give null a meaning of its own, such as a
  model field that is null because a human did that step. Those SHOULD be written out.
- **Tabular forms.** A CSV export flattens the annotations to one row per annotation, with
  prefixed names as columns. A CSV export cannot hold set-level attributes or the image, model
  and label lists, so it MUST come with the JSON or YAML file it was exported from.

### Why not iFDO's header and items?

iFDO's top level is `image-set-header`, which holds defaults for the set, plus `image-set-items`,
which holds per-image records keyed by filename. This standard keeps each set's attributes and its
lists side by side in one object. There are three reasons:

- **Annotations are not keyed by image.** An image can have many annotations, or none.
  Annotations refer to images by UUID instead.
- **Image-level data already has its own list.** The images are recorded in
  `annotation-set-images`, so per-image records are not needed under the annotations.
- **Nothing is overridden.** iFDO's header supplies defaults that items can override. Here,
  set-level attributes describe the set, and they are never overridden at the annotation level.

The two structures map directly onto each other. An `annotation-set` without its lists
corresponds to iFDO's header. `annotation-set-images` and `annotation-set-annotations` correspond
to iFDO's items.

### Skeleton

```yaml
label-set:
  label-set-standard-version: "0.11"
  label-set-name: ...
  label-set-uuid: ...
  # ... other Table 1 attributes
  label-set-labels:
    - label-name: ...
      label-uuid: ...
      # ... other Table 2 attributes

annotation-set:
  annotation-set-standard-version: "0.11"
  annotation-set-name: ...
  annotation-set-uuid: ...
  annotation-set-label-set-uuids: [...]   # includes the label-set-uuid above
  # ... other Table 3 attributes
  annotation-set-models: [...]            # model entries
  annotation-set-images: [...]            # image entries
  annotation-set-annotations:
    - annotation-uuid: ...
      # ... other Table 4 attributes
      annotation-reviews: [...]           # review entries
```

---

## VARS: corrected notes

This section replaces what the draft says about VARS. The draft cites the 2006 OCEANS paper
(Schlining & Stout). Current VARS is a set of services:

- **annosaurus** stores the annotations.
- **oni** is the knowledgebase of concepts.
- **vampire-squid** is the catalog of video assets.

The notes below describe annosaurus, which is where annotation data lives.

### VARS annotation data model

VARS is built around video. An image is a frame grab of a moment in a video. Every record is keyed
by a UUID. New rows get UUIDv7.

| Entity (table) | Purpose | Key fields |
| --- | --- | --- |
| ImagedMoment (`imaged_moments`) | A moment in a video | `uuid`, `video_reference_uuid`, plus at least one time index: `recorded_timestamp` (UTC wall-clock time the frame was captured), `elapsed_time_millis` (time since the video started), `timecode` (`HH:MM:SS:FF`) |
| Observation (`observations`) | One identification at that moment. This is the VARS "annotation" | `uuid`, `concept`, `observer`, `observation_timestamp`, `activity`, `observation_group` (`group` in the JSON), `duration_millis` |
| Association (`associations`) | Extra information about an observation, stored as a triple | `uuid`, `link_name`, `to_concept`, `link_value`, `mime_type` |
| ImageReference (`image_references`) | An image of the moment, such as a frame grab | `uuid`, `url` (unique), `format`, `width_pixels`, `height_pixels`, `description` |
| CachedAncillaryDatum (`ancillary_data`) | Position and sensor data for the moment (1:1) | `latitude`, `longitude`, `depth_meters`, `altitude`, `temperature_celsius`, `salinity`, `oxygen_ml_per_l`, `pressure_dbar`, `light_transmission`, and others |
| CachedVideoReferenceInfo (`video_reference_information`) | Cached deployment information for the video | `mission_id` (the dive), `platform_name`, `mission_contact` |

Things to know about this model:

- **Images belong to the moment, not to the observation.** One moment can have several images,
  for example a PNG and a JPEG of the same frame grab. There is no image filename field. An image is
  identified by its `url`.
- **`concept` is a plain string.** annosaurus does not check it against the knowledgebase and does
  not record a knowledgebase version. The concept hierarchy (parents and descendants) comes from oni,
  not from annosaurus.
- **There is no label-set entity and no annotation-set entity.** Annotations are grouped by video
  (`video_reference_uuid`). Through vampire-squid, a video belongs to a deployment (dive) and a
  platform. Project-level metadata in Tables 1 and 3 has no VARS equivalent.
- **`observation_timestamp` is when the annotation was made.** `recorded_timestamp` is when the
  frame was *captured*. The draft maps annotation creation time to `RECORDEDDATE`, which is wrong.
- **`observer` is a VARS username.** It is not a full name, an ORCID or an email.
- **Change history** is kept by Hibernate Envers in `observations_AUD` and `associations_AUD`. It is
  not exposed as provenance fields.

### Associations

An association has the form `link_name | to_concept | link_value` and a `mime_type` (default
`text/plain`). Examples from the annosaurus README:

```
eating          | Aegina | nil
surface-color   | self   | red
audio-comment   | nil    | first sighting on this mission
```

Associations hold behaviour, interactions between organisms, substrate, free-text comments and
localizations. The knowledgebase's link templates offer users a controlled list of link names.

### Localizations (shapes and coordinates)

VARS has no dedicated shape or coordinate fields. Each shape is one association on the observation,
by convention:

- The **shape type is the `link_name`**: `bounding box`, `localization-point`,
  `localization-line` or `localization-polygon`.
- The **coordinates are JSON in the `link_value`**, with `mime_type = application/json`.
- Coordinates are **pixels with the origin at the top left**.

| `link_name` | `link_value` (examples from the annosaurus localization proposal) |
| --- | --- |
| `bounding box` | `{"x": 982, "y": 1, "width": 97, "height": 132, "generator": "mbari452k_yolov8", "confidence": 43.0}` |
| `bounding box` | `{"x": 0, "y": 266, "width": 26, "height": 23, "generator": "mbari452k_yolov8", "confidence": 17.0, "verifier": "kwalz"}` |
| `localization-point` | `{"x": [2128], "y": [2529]}` |
| `localization-line` | `{"x": [1630, 4381], "y": [2312, 1645]}` |
| `localization-polygon` | `{"x": [2208, 1167, ..., 4252], "y": [1525, 1263, ..., 1449]}` |

How the JSON is laid out:

- A bounding box is `x`, `y`, `width`, `height`. `x, y` is the top-left corner.
- Points, lines and polygons are two parallel arrays, `x` and `y`. They are not interleaved
  x,y pairs.

Optional keys in the JSON:

| Key | Meaning |
| --- | --- |
| `generator` | The model that made the box. Its presence marks a machine-generated box. |
| `confidence` | Model confidence, on a 0–100 scale. |
| `verifier` | Username of the person who confirmed the box. |
| `tags` | For example `["training"]`. |
| `image_reference_uuid` | The image whose pixels the coordinates refer to. |

Limits of this convention:

- Nothing enforces that the JSON is valid or complete.
- `link_value` holds at most 1024 characters. That limits a polygon to roughly 90–100 vertices.
- Without `image_reference_uuid`, nothing says which image the pixels refer to.

**Planned change, not yet implemented.** A proposal in annosaurus
(`docs/proposals/2026-08-25-localizations.md`) replaces this convention with a `localizations`
table. In that table:

- Each observation has at most one localization of each type: `bounding_box`, `point`, `line`,
  `polygon` or `mask`.
- Coordinates are normalized to [0, 1]. Vertices are interleaved as `[x0, y0, x1, y1, ...]`.
  Masks are COCO RLE.
- Confidence is on a 0–1 scale.
- Provenance columns are `generator`, `observer`, `observation_timestamp`, `verifier`,
  `verification_timestamp` and `comment`, plus `training` and `truncated` flags.

If this ships, the VARS column of Table 4 must be updated.

### Corrections to the draft's text

| Draft section | Draft text (summary) | Correction |
| --- | --- | --- |
| Methods | Cites VARS (Schlining & Stout 2006) | Also cite or describe the current service-based VARS (annosaurus, oni, vampire-squid). The 2006 paper describes the older system. |
| Mapping to platforms, ¶1 | "VARS includes labels in its Knowledgebase, but without delineating the bounds of the labels for a particular project as a label set." | Keep the point, and be precise. VARS concepts come from a single hierarchical knowledgebase. Observations store the concept name as free text, with no link to a label set or a knowledgebase version. VARS has no label-set or annotation-set entity. |
| Mapping to platforms, ¶2 | "VARS documents the series of x and y coordinates denoting the polygon shape within its ASSOCIATIONS, rather than in one or more dedicated attributes." | Each shape (bounding box, point, line, polygon) is one association. The `link_name` names the shape. The `link_value` holds JSON in pixel coordinates (origin top left): `x, y, width, height` for boxes, parallel `x[]` and `y[]` arrays for the other shapes. The same JSON can carry `generator`, `confidence`, `verifier` and `image_reference_uuid`. A dedicated localization table is proposed. |
| Future expansion | "VARS includes controlled lists and formats for some of these, and also allows users to make text comments; both are stored in the ASSOCIATIONS attribute." | Correct in substance. Associations are `link_name | to_concept | link_value` triples. Link names offered to users come from knowledgebase link templates. `to_concept` can point to another concept, for example `eating | Aegina`. |
| Table 4 | VARS column | See the corrected Table 4 below. The draft's last row also appears to have the VARS and SQUIDLE+ values swapped. |

---

## Annotation shapes and coordinates

This section defines `annotation-shape-name` and `annotation-coordinates`. The draft says only
"X and Y values of pixel location in the image of vertices of shape", as "Numbers, comma
separated". That leaves the order, units and per-shape layout undefined, and the platforms
disagree on all three.

**Decision: adopt the iFDO v2.2.1 encoding.** The standard already builds on iFDO, and iFDO v2.2.1
(`ifdo-schema.org/schemas/v2.2.1/annotation.json`) defines shape names and coordinate arrays. It
is also close to BIIGLE's encoding. The rules below follow iFDO and fill in what iFDO leaves
unstated. Each of those additions is marked **(addition)**. They should be offered back to iFDO.

The key words MUST, SHOULD and MAY are used as in RFC 2119.

### Coordinate system

1. Coordinates are **pixels** of the image file named by the annotation's `annotation-image-uuid`
   (see [Referencing the annotated image](#referencing-the-annotated-image)). They refer to that
   file at its full stored resolution. They are not normalized to [0, 1].
2. The **origin (0, 0) is the top-left corner of the image**. x increases to the right and y
   increases downwards.
3. **(addition)** Coordinates are continuous. Pixel *(i, j)*, counted from zero, covers
   *i ≤ x < i + 1* and *j ≤ y < j + 1*, so its centre is *(i + 0.5, j + 0.5)*. An image *W*
   pixels wide and *H* pixels high spans *0 ≤ x ≤ W* and *0 ≤ y ≤ H*.
   - Fractional values are allowed.
   - Tools that record integer pixel indices (most do, including VARS) MAY write them unchanged.
     The error is at most half a pixel.
   - iFDO's camera calibration fields (`calibration-principal-point-xy-pixel`) use a different
     origin: the *centre* of the top-left pixel. To convert a calibration point to annotation
     coordinates, add 0.5 to both x and y.
4. **(addition)** Vertices SHOULD lie inside the image. A circle or ellipse MAY extend beyond the
   image edges.
5. **(addition)** The image's pixel width and height MUST be recorded. They are needed to check
   coordinates and to convert to fractional schemes such as Audubon Core. They are recorded in the
   annotation set's `annotation-set-images` list (see
   [Referencing the annotated image](#referencing-the-annotated-image)).

### Value format

`annotation-coordinates` is an **array of arrays of numbers**:
`[[x1, y1, x2, y2, ..., xn, yn]]`.

- Each inner array holds one shape's vertices as **interleaved x, y pairs**. It is not two
  separate x and y lists.
- For a still image, the outer array MUST have exactly one inner array.
- For video, iFDO allows one inner array per frame, paired by position with a `frames` array of
  times in seconds. Video is open issue 1, so this revision covers still images only.
- In JSON or YAML the value is a real array, not a string. **(addition)** In CSV or another
  tabular format, the cell holds the same array written as JSON text, e.g.
  `"[[1204,811,1388,811,1388,902,1204,902]]"`.

### Shapes

`annotation-shape-name` MUST be one of the iFDO shape names below.

| `annotation-shape-name` | Meaning | Numbers per inner array | Layout |
| --- | --- | --- | --- |
| `single-pixel` | A point | exactly 2 | `[x, y]` |
| `polyline` | An open line: a length, a path, or a boundary that is not closed | even, ≥ 4 (≥ 2 vertices) | `[x1, y1, ..., xn, yn]` in order along the line |
| `polygon` | A closed outline | even, ≥ 8 (≥ 3 distinct vertices plus the closing vertex) | `[x1, y1, ..., xn, yn, x1, y1]`. The last vertex MUST repeat the first. |
| `rectangle` | A bounding box. It MAY be rotated. | exactly 8 | Four corners in order around the perimeter |
| `circle` | A bounding circle | exactly 3 | `[cx, cy, r]`: centre and radius, in pixels |
| `ellipse` | A bounding ellipse | exactly 8 | `[a1x, a1y, a2x, a2y, b1x, b1y, b2x, b2y]` |
| `whole-image` | The whole image; no region | 0 | `[]` |
| `mask` **(addition, 0.8)** | A per-pixel mask, which may have holes or several parts | exactly 8 | The mask's axis-aligned bounding `rectangle`. The mask itself is in `annotation-mask`; see [Pixel masks](#pixel-masks). |

Rules for each shape that iFDO does not state **(addition)**:

- **Vertex order.** For `polygon` and `rectangle`, vertices go around the perimeter. The direction
  (clockwise or anticlockwise) is not significant.
- **Rectangle corners.** An axis-aligned bounding box SHOULD start at the top-left corner and go
  clockwise on screen:
  `[[xmin, ymin, xmax, ymin, xmax, ymax, xmin, ymax]]`.
  Readers MUST NOT assume that order. They MUST take the box's extent from the minimum and maximum
  of the x and y values. Adjacent sides MUST be perpendicular, within rounding. A shape whose sides
  are not perpendicular is a `polygon`.
- **Ellipse.** `a1` and `a2` are the two ends of one axis, and `b1` and `b2` are the two ends of
  the other. The two axes MUST cross at their midpoints, which is the centre, and MUST be
  perpendicular, within rounding. This is BIIGLE's ellipse layout.
- **Polygon.** It SHOULD NOT intersect itself. Holes are not supported. Use a
  [mask](#pixel-masks) for shapes with holes.
- **Degenerate shapes.** Rectangles and circles of zero size are not allowed. Use `single-pixel`
  for a point.

### Changes from the draft

| Draft | This revision |
| --- | --- |
| point | `single-pixel` |
| line | `polyline` |
| polygon | `polygon` (now closed: the first vertex is repeated at the end) |
| bounding box | `rectangle` (4 corners, not 2 points or x, y, width, height) |
| centrexy | Not defined in the draft. If it means a centre point, use `single-pixel`. If it means a centre plus radius, use `circle`. |
| (none) | `circle`, `ellipse` and `whole-image` added from iFDO |
| "Controlled list based on svg shape standard" | iFDO shape list. The names differ from SVG (`rect`, `polyline`, `polygon`, `circle`, `ellipse`). SVG has no point or whole-image shape. |

### Converting from other formats

In this table, *W* and *H* are the image's pixel width and height.

| Source | Source encoding | To this standard |
| --- | --- | --- |
| VARS `bounding box` | `{"x", "y", "width", "height"}`, pixels, top-left corner | `rectangle` `[[x, y, x+width, y, x+width, y+height, x, y+height]]` |
| VARS `localization-point` | `{"x": [x], "y": [y]}` | `single-pixel` `[[x, y]]` |
| VARS `localization-line` | `{"x": [x1, ..., xn], "y": [y1, ..., yn]}` | `polyline`: interleave to `[[x1, y1, ..., xn, yn]]` |
| VARS `localization-polygon` | `{"x": [...], "y": [...]}`, not closed | `polygon`: interleave, then repeat the first vertex at the end |
| VARS proposed `localizations` table | Normalized to [0, 1]. Vertices interleaved. Box as x, y, width, height. | Multiply x values by *W* and y values by *H*, then as above |
| BIIGLE | `[x1, y1, ...]`. Circle is `[x, y, r]`. Rectangle and ellipse have 4 vertices. | Same layout. Wrap in an outer array. Close polygons if BIIGLE does not (to confirm). Line string → `polyline`. Point → `single-pixel`. Whole frame → `whole-image`. |
| COCO | `bbox` `[x, y, w, h]`; `segmentation` polygons interleaved, not closed | `rectangle` as for VARS; `polygon`: close it |
| SQUIDLE+ | x, y appear to be fractions of image width and height, with a polygon field (to confirm with SQUIDLE+ authors) | Multiply by *W* and *H*; polygon layout to confirm |

### Mapping to Darwin Core / Audubon Core

The draft maps coordinates to `ac:pixelX, ac:pixelY`. Those are not Audubon Core terms.

Audubon Core's region-of-interest terms use fractions of the media item, measured from its top-left:
`ac:xFrac`, `ac:yFrac`, `ac:widthFrac`, `ac:heightFrac` and `ac:radius`. The radius is a fraction
of the *width*. The image size is given by `exif:PixelXDimension` and `exif:PixelYDimension`.

| Shape | Audubon Core |
| --- | --- |
| `single-pixel` | `xFrac = x/W`, `yFrac = y/H`, `radius = 0` |
| `circle` | `xFrac = cx/W`, `yFrac = cy/H`, `radius = r/W` |
| `rectangle`, axis-aligned | `xFrac = xmin/W`, `yFrac = ymin/H`, `widthFrac = (xmax−xmin)/W`, `heightFrac = (ymax−ymin)/H` |
| `polygon`, `polyline`, `ellipse`, rotated `rectangle` | No exact equivalent. Export the axis-aligned bounding rectangle, and keep the full shape in `annotation-coordinates`. |
| `whole-image` | No region of interest. Link the occurrence to the whole media item. |
| `mask` | Export the bounding rectangle in `annotation-coordinates`, as for an axis-aligned `rectangle` |

### Examples

```yaml
annotation-set-annotations:
  - annotation-shape-name: rectangle          # axis-aligned bounding box
    annotation-coordinates: [[1204, 811, 1388, 811, 1388, 902, 1204, 902]]
  - annotation-shape-name: polygon            # closed: last vertex repeats the first
    annotation-coordinates: [[882, 640, 951, 612, 1040, 655, 1012, 731, 905, 720, 882, 640]]
  - annotation-shape-name: single-pixel
    annotation-coordinates: [[2048, 1536]]
  - annotation-shape-name: polyline           # e.g. a length measurement
    annotation-coordinates: [[1630, 2312, 4381, 1645]]
  - annotation-shape-name: circle             # centre (512.5, 300), radius 40 px
    annotation-coordinates: [[512.5, 300, 40]]
  - annotation-shape-name: ellipse            # axis a: (100,200)-(300,200); axis b: (200,150)-(200,250)
    annotation-coordinates: [[100, 200, 300, 200, 200, 150, 200, 250]]
  - annotation-shape-name: whole-image        # one inner array, empty
    annotation-coordinates: [[]]
```

The bounding box and polygon in the gist samples (`"1204,811,1388,902"` and an unclosed polygon
string) are now written as in the first two entries above.

---

## Pixel masks

### The problem

Some shapes are not polygons. An organism may have a hole in its outline, be split into several
pieces by an occluding object, or be traced pixel by pixel by a segmentation model. Segment
Anything (SAM), Mask R-CNN and most segmentation tools output a per-pixel mask, not a polygon.
iFDO v2.2.1 has no mask shape. The draft has none either, and revision 0.2 rules out holes in
polygons.

What other formats use:

- **COCO** stores a mask as run-length encoding (RLE) over the whole image. It allows two forms:
  a list of integers, and a compressed string. pycocotools reads and writes both, and so do SAM,
  Detectron2 and most segmentation tools.
- **The VARS localizations proposal** has chosen COCO RLE, with the columns `mask_encoding`
  (`coco_rle`), `mask_data`, `mask_width_pixels` and `mask_height_pixels`.
- **Dense label maps** are PNG images in which each pixel's value is a class. They are used for
  habitat or substrate cover. They describe the whole image at once, not one object, so they are
  a different kind of data (see open issue 10).

### Decision

1. **New shape: `mask` (addition).** It is the eighth value of `annotation-shape-name`. This
   should be proposed to iFDO.
2. **The mask is stored in a new attribute, `annotation-mask`, encoded as COCO RLE.** That is the
   encoding the tools already produce, and the one VARS has chosen.
3. **`annotation-coordinates` holds the mask's bounding rectangle.** For a `mask`, the coordinates
   are an axis-aligned `rectangle` (8 numbers) that MUST equal the mask's extent. Tools that cannot
   decode masks still get a box, and the Audubon Core export works without decoding.
4. **The mask covers the whole image, at full resolution.** Its width and height MUST equal the
   image's `image-width-pixels` and `image-height-pixels`. A mask computed at a lower resolution,
   as SAM does internally, MUST be scaled to the image before it is stored. In RLE, a full-image
   mask costs little: the empty area before and after the object is one number each.
5. **One mask is one object.** A mask MAY have holes and MAY be in several disconnected parts,
   for example when the object is partly hidden. Separate objects get separate annotations.

### `annotation-mask`

`annotation-mask` is an object. It is REQUIRED when `annotation-shape-name` is `mask`, and MUST be
absent otherwise. Its keys are `encoding`, `width`, `height` and `counts`, defined in
[Table 8](#table-8-mask-keys).

Like `{name, uri}`, it is a small object with plain keys, so the prefix rules don't apply to them.
`width` and `height` are written out instead of COCO's `size: [height, width]`, because COCO's
order is the reverse of the x, y order used everywhere else in this standard.

### Encoding rules (addition)

These rules restate COCO's, so they don't depend on reading pycocotools' source.

- **Pixel order is column-major.** Runs go down column x = 0 from top to bottom, then down
  column x = 1, and so on. Pixel *(x, y)* is at position *x × height + y*.
- **Runs alternate, starting with background.** The first count is the number of background (0)
  pixels before the first mask (1) pixel. It MAY be 0. Counts then alternate between mask and
  background runs.
- **The counts MUST add up to width × height.**
- **The pixel grid is the image's pixel grid.** In coordinate terms, mask pixel *(x, y)* covers
  *x ≤ X < x + 1* and *y ≤ Y < y + 1* (see [Coordinate system](#coordinate-system)). So the
  bounding rectangle in `annotation-coordinates` is `[[xmin, ymin, xmax+1, ymin, xmax+1, ymax+1,
  xmin, ymax+1]]`, where `xmin`…`ymax` are the smallest and largest mask pixel columns and rows.
- **The compressed form** is the string pycocotools produces (`rleToString`). Each count except
  the first three is replaced by its difference from the count two places before it. Each value
  is then written as a little-endian variable-length signed integer in 5-bit groups. Each group is
  written as the character with code *48 + group*. Bit 0x20 of a group means more groups follow.
  In the last group, bit 0x10 is the sign.
- **Writers** SHOULD use `coco-rle-compressed`, which is usually 2–5 times smaller. **Readers**
  MUST accept both forms.
- **In CSV**, the `annotation-mask` cell holds the object as JSON text, as for coordinates.

**More encodings may be added later.** `coco-rle` and `coco-rle-compressed` are the only encodings
in this revision. Later revisions may add more `encoding` values, for example a reference to an
external PNG mask file, or another compressed format. Each will keep the same `width` and `height`
rules. A reader that meets an `encoding` it does not recognise MUST NOT guess at `counts`. It
SHOULD treat the annotation as its bounding rectangle in `annotation-coordinates`, and SHOULD say
that the mask was not decoded.

`annotation-measurement` stays an explicit, optional value. A mask's area in pixels is the sum of
its mask runs (the 2nd, 4th, 6th, … counts), so it need not be stored.

### Converting to and from other formats

| Source or target | Conversion |
| --- | --- |
| COCO `segmentation` with RLE | `size: [h, w]` → `height: h, width: w`. A `counts` list → `coco-rle`; a `counts` string → `coco-rle-compressed`. `bbox` `[x, y, w, h]` → the rectangle in `annotation-coordinates`. |
| SAM, Detectron2, pycocotools | `pycocotools.mask.encode` on a column-major (Fortran-order) array gives `coco-rle-compressed` directly. |
| VARS proposed `localizations` | `mask_encoding: coco_rle` → `encoding`; `mask_data` → `counts`; `mask_width_pixels` and `mask_height_pixels` → `width` and `height`. Which of the two COCO forms VARS stores in `mask_data` is to confirm. If the mask is not the image's size, it must be scaled. |
| iFDO v2.2.1 | No mask shape. Export the outer boundary of each part as a `polygon`. This loses holes, and gives one polygon per part. Or export the bounding `rectangle`. |
| Audubon Core | Export the bounding rectangle, as for other shapes with no exact equivalent. |
| BIIGLE, SQUIDLE+ | (to confirm whether either stores masks) |

### Example

An annotation of a coiled holothurian. The mask is a ring with a hole, in a 6000 × 4000 image. It
covers 284 pixels, and its extent is columns 4488–4512 and rows 2792–2808. The same mask is
written in both forms. (Generated, and checked against pycocotools, by the script that validates
the samples.)

```yaml
- annotation-shape-name: mask
  annotation-coordinates: [[4488, 2792, 4513, 2792, 4513, 2809, 4488, 2809]]
  annotation-mask:
    encoding: coco-rle-compressed
    width: 6000
    height: 4000
    counts: '`omSa01ll36L2N2N2O0O2O00H`SL0_l30cSL0\l3OfSL0Zl30fSL0Zl30fSL0Zl30fSL0Zl30fSL0Zl31dSL0]l30aSL0`l38001N101N2N2N4Jck]e5'

# The same mask as a list of integers:
#   annotation-mask:
#     encoding: coco-rle
#     width: 6000
#     height: 4000
#     counts: [17954800, 1, 3996, 7, 3992, 9, 3990, 11, 3988, 13, 3987, 13, 3986, 15, 3985, 15,
#              3985, 7, 1, 7, 3984, 7, 3, 7, 3983, 6, 5, 6, 3983, 6, 5, 6, 3983, 6, 5, 6, 3983,
#              6, 5, 6, 3983, 6, 5, 6, 3983, 7, 3, 7, 3984, 7, 1, 7, 3985, 15, 3985, 15, 3986,
#              13, 3987, 13, 3988, 11, 3990, 9, 3992, 7, 3996, 1, 5949199]
```

---

## Referencing the annotated image

### The problem

The draft has each annotation name its image with `image-filename` alone. That is not enough, for
four reasons:

- **A filename is not unique.** Two image sets can both contain `IMG_0001.jpg`. An annotation set
  can reference several image sets, so a filename alone can be ambiguous.
- **Names change.** Files are renamed and moved when they are copied, archived or published.
- **An image can exist in several versions.** One frame can be stored as a full-resolution PNG, a
  JPEG and a thumbnail, and VARS can store several images for one moment. Pixel coordinates are
  only correct for the version they were drawn on.
- **Pixel dimensions are missing.** Coordinates can't be checked or converted without the image's
  width and height. iFDO v2.2.1 has no pixel width or height field. It has
  `image-pixel-magnitude`, which is the size of one pixel on the ground, not the image size.

What iFDO v2.2.1 does provide:

- Every image item MUST have an `image-uuid`, "a (random) UUID for the individual image file
  (still or moving)". iFDO says it is embedded in the file's own metadata. Each item also MUST
  have an `image-hash-sha256` and an `image-handle`.
- iFDO's own `image-annotations` sit inside an image item, so they don't need an image reference.
  The annotation sets in this standard are separate from the iFDO, so they do.

### Decision

1. **Each annotation names its image by UUID.** `annotation-image-uuid` is REQUIRED. Its value is
   the `image-uuid` of the exact file whose pixel grid the coordinates use. That is the iFDO
   `image-uuid` when there is an iFDO, and an assigned UUID when there is not (see
   [Images without an embedded UUID, or without an iFDO](#images-without-an-embedded-uuid-or-without-an-ifdo)).
2. **Each annotated image is described once, in the annotation set.** The set gets a new
   `annotation-set-images` list with one entry per annotated image. This keeps image-level data at the
   image level instead of repeating it on every annotation. It works the same way as COCO's
   `images` list and Audubon Core's media records.
3. **The width and height are REQUIRED in that list.** They duplicate image metadata, but an
   annotation set must be usable without its iFDO, for example once it has been published to OBIS.
4. **The filename is kept, but only for people to read.** `image-filename` moves to the image
   entry. It is RECOMMENDED there, but software MUST NOT use it to look up an image.

### Annotated image attributes

Each entry in `annotation-set-images` describes one annotated image: its UUID and where that UUID
is recorded, its image set, filename, handle, hash, pixel width and height, and capture time. The
attributes are defined in [Table 6](#table-6-image-attributes).

Rules:

- Each `annotation-image-uuid` MUST match the `image-uuid` of exactly one entry in
  `annotation-set-images`.
- An image entry with no annotations MAY be included. That is how an annotation set says an image
  was examined and nothing was found (see the draft's discussion of recording absence).
- **Derived images.** A resized, cropped or re-encoded copy is a different file with a different
  pixel grid. It needs its own `image-uuid`. If annotations are moved onto it, their coordinates
  MUST be transformed to its grid. Copying a file unchanged keeps its UUID.
- **Video.** `image-uuid` names the video file. The frame within it is defined by video support,
  which is open issue 1.

**Proposal to iFDO.** Add image-level `image-pixel-width` and `image-pixel-height` fields,
equivalent to `exif:PixelXDimension` and `exif:PixelYDimension`. If iFDO adopts them, the width
and height in `annotation-set-images` stay REQUIRED, and MUST equal the iFDO values.

### Capture time

`image-datetime` records when the image was captured. It is the same field as iFDO's
`image-datetime`, the "full UTC datetime of image acquisition (or start time of a video)". In VARS
it is the imaged moment's `recorded_timestamp`.

- **It describes the image, not the annotation.** Every annotation on an image shares the image's
  capture time, so it is recorded once, in the image entry. It is not repeated on each annotation.
- **It is not the annotation time.** `annotation-creation-datetime` is when the annotation was
  made, and maps to Darwin Core `dateIdentified`. `image-datetime` is when the organism was
  observed, and maps to Darwin Core `eventDate`. The draft confused the two by mapping annotation
  creation time to VARS `RECORDEDDATE`.
- **With an iFDO, it is optional.** The iFDO already holds the capture time. A copy makes the
  annotation set usable without its iFDO, for example once it has been exported to OBIS. If both
  are present, they MUST be the same instant.
- **Without an iFDO, it is recommended.** It is then the only source of the occurrence date, which
  OBIS and GBIF need.
- **Format.** It is written in the same ISO 8601 UTC form as every other date-time in an
  annotation set (`YYYY-MM-DDThh:mm:ss.sssZ`), so readers parse one format. iFDO's default is
  `YYYY-MM-DD hh:mm:ss.sss`, with a space, and iFDO allows other formats through
  `image-datetime-format`. When copying from an iFDO, convert the value to this format. The
  instant MUST NOT change.
- **VARS.** For each VARS image entry, `image-datetime` is the `recorded_timestamp` of the imaged
  moment the image belongs to. VARS annotations on video moments are also handled with
  `image-datetime`, using the moment's `recorded_timestamp`. General video support is open issue 1.

### Images without an embedded UUID, or without an iFDO

iFDO requires the `image-uuid` to be embedded in the image file, so a copy of the file found on its
own still identifies itself. Many existing images can't meet that rule:

- legacy archives, including VARS frame grabs;
- read-only collections;
- files owned by someone else;
- images that are only available through a web service.

Some images have no iFDO at all. This standard accepts both cases. When the UUID is not in the
file, the link between a UUID and its file is kept in the record, and the file's SHA-256 hash
confirms that the record and the file belong together.

#### Case 1: there is an iFDO, but the UUID is not in the file

1. **Say where the UUID comes from.** Every `annotation-set-images` entry records `image-uuid-source`:
   - `embedded`: the UUID is in the file's metadata, as iFDO requires.
   - `assigned`: the UUID is recorded only outside the file. It may be in the iFDO, in this
     annotation set, or in the platform the image came from.
2. **The hash links the UUID to the file.** When `image-uuid-source` is `assigned`,
   `image-hash-sha256` is REQUIRED. To resolve an image, software MUST look it up by `image-uuid`
   and SHOULD confirm the file by its hash. It MUST NOT resolve an image by `image-filename`.
3. **Keep identifiers that already exist.** If the source platform has a stable UUID for the
   exact file, that UUID MUST be used. It MUST NOT be replaced with a new one. For VARS, that is
   `image_references.uuid`.
4. **Otherwise, derive the UUID from the hash.** If no UUID exists, one SHOULD be created as a
   UUID version 5 (RFC 9562):
   - Namespace: `8fb66ecc-ce0d-45ff-b8ab-23bd7774d760`. This is the namespace of this standard,
     and is provisional until the standard is published.
   - Name: the file's SHA-256, as 64 lowercase hexadecimal characters, encoded as UTF-8.

   Anyone can recompute this UUID, so two groups that annotate the same file get the same UUID
   without coordinating. For example, a file whose bytes are `example` has SHA-256
   `50d858e0985ecc7f60418aaf0cc5ab587f42c2570a884095a9e8ccacd0f6545c` and UUID
   `06a5dc4e-1641-57c5-8fcf-800527bec2ff`.
   - **Create the UUID once.** After that it is only an identifier. If the UUID is later embedded
     in the file, the file's bytes and hash change. The UUID MUST stay the same,
     `image-hash-sha256` MUST be updated, and `image-uuid-source` becomes `embedded`. Software MUST
     NOT require a derived UUID to match the file's current hash.
   - **Hash the file's bytes, not its decoded pixels.** Different decoders do not always produce
     identical pixels, especially for JPEG, so a pixel hash would not be reproducible.

#### Case 2: there is no iFDO

The `annotation-set-images` entry serves as the minimal record of the image.

1. The annotation set sets `annotation-set-image-metadata` to `none`. (Its other value, `ifdo`, is the
   default.)
2. Each image entry MUST have `image-uuid` (with `image-uuid-source: assigned`),
   `image-hash-sha256`, `image-handle`, `image-width-pixels` and `image-height-pixels`. They
   SHOULD have `image-datetime`, because without an iFDO it is the only source of the occurrence
   date.
3. `image-set-uuid` and `annotation-set-image-set-uuids` are omitted. `annotation-set-image-set-names` MAY
   describe the images in words.
4. **What is lost.** iFDO records where, when and how each image was taken. Without it, the
   annotations have no position, time, platform or sensor. This makes them much less useful
   downstream; OBIS, for example, needs a location. An iFDO SHOULD be written later. If it is,
   it MUST use the UUIDs already assigned. `annotation-set-image-metadata` then changes to `ifdo`,
   and the image set UUIDs are added.

#### Edge cases

- **Images that cannot be hashed.** Some images are only available through a service, such as a
  tiled or IIIF image server, so their bytes cannot be hashed. Use `image-uuid-source: assigned`
  and `image-hash-sha256: null`. `image-handle`, `image-width-pixels` and `image-height-pixels`
  are then REQUIRED. Nothing can confirm that the coordinates match the image the service returns.
- **Video frames that are not saved as files.** A frame that only exists inside a video is
  identified by the video's UUID plus a time within the video, not by a UUID of its own. This is
  part of open issue 1.

### How existing platforms map

| Platform | Image identifier | Pixel dimensions | Notes |
| --- | --- | --- | --- |
| VARS | `image_references.uuid` for one stored file (one URL) | `image_references.width_pixels`, `height_pixels` (nullable; fill in on export) | `image-datetime` is the `recorded_timestamp` of the image's imaged moment. The file named by the localization's `image_reference_uuid` key. If that key is missing, the exporter must choose the image of the moment whose pixel size matches the coordinates. VARS UUIDs are not embedded in the files. Export them unchanged as `image-uuid`, with `image-uuid-source: assigned` and the file's SHA-256. The proposed VARS `localizations` table has normalized coordinates and no image link, so its exporter can choose any image of the moment and scale to that image's size. |
| BIIGLE | Internal image ID and filename (to confirm whether a UUID is exported) | Image width and height attributes (to confirm) | |
| SQUIDLE+ | Media object (to confirm) | (to confirm) | Coordinates appear to be fractions, so the dimensions are needed to convert them to pixels. |
| COCO | `images[].id` (integer), `file_name` | `images[].width`, `height` | Same structure as `annotation-set-images`. |
| Audubon Core | Media record identifier; an ROI links to it with `ac:isROIOf` | `exif:PixelXDimension`, `exif:PixelYDimension` | |

### Example

```yaml
annotation-set:
  annotation-set-image-set-uuids:
    - 4b30f1c8-d061-40e0-9d3a-8a971a3c1b45
    - 7f68599d-05a0-4a53-abca-c0aebf3a5143
  annotation-set-images:
    - image-uuid: 0d1f6a52-8c2e-4f0b-9a4e-3b7c51e2d9a1
      image-uuid-source: embedded
      image-set-uuid: 4b30f1c8-d061-40e0-9d3a-8a971a3c1b45
      image-filename: JC999_M42_20260612T031522Z_0187.jpg
      image-width-pixels: 6000
      image-height-pixels: 4000
    - image-uuid: 9a3e2c17-5b48-4d6f-8e01-c2f4a7b6d530     # legacy file: UUID kept in the iFDO only
      image-uuid-source: assigned
      image-hash-sha256: 3f9a1c0e7b2d4a6f8e1c5b9d0a7e3f2c6b8d1e4a9c0f7b3e5d2a8c6f1b4e9d07
      image-set-uuid: 7f68599d-05a0-4a53-abca-c0aebf3a5143
      image-filename: JC999_M43_20260614T224907Z_0042.jpg
      image-width-pixels: 6000
      image-height-pixels: 4000
    - image-uuid: 5e7b9d04-21c3-4a8f-b6d2-0f9e8c3a1b77     # examined, nothing found
      image-uuid-source: embedded
      image-set-uuid: 7f68599d-05a0-4a53-abca-c0aebf3a5143
      image-filename: JC999_M43_20260614T225012Z_0043.jpg
      image-width-pixels: 6000
      image-height-pixels: 4000

  annotation-set-annotations:
    - annotation-image-uuid: 0d1f6a52-8c2e-4f0b-9a4e-3b7c51e2d9a1
      annotation-shape-name: rectangle
      annotation-coordinates: [[1204, 811, 1388, 811, 1388, 902, 1204, 902]]
    - annotation-image-uuid: 9a3e2c17-5b48-4d6f-8e01-c2f4a7b6d530
      annotation-shape-name: single-pixel
      annotation-coordinates: [[2048, 1536]]
```

---

## Machine-generated annotations: models and confidence

### The problem

The draft records machine provenance in two places, and neither is enough:

- **Set level.** `annotation-machine-algorithm` is a single text field. A real annotation set
  often uses several models, or several versions of one model, or a detector followed by a
  separate classifier. Each model also has its own training and validation data, but the draft has
  one set of training and validation links for the whole set.
- **Annotation level.** `annotation-machine-detect-or-classify` says *what* a machine did, but not
  *which* machine did it or how confident it was. VARS records both for each box (`generator` and
  `confidence`), and so do iFDO (`annotator` and `confidence` on each label) and COCO results files
  (`score`).

Many machine annotations are made in two steps, and the two steps can come from different sources:

- The **detection** produces the shape. It can come from a human, a detector model, or a combined
  model.
- The **classification** produces the label. It can come from a human, a classifier model, or
  the same combined model.

Recording a single "generator" can't describe, for example, a box from a detector with a label
from a separate classifier. It also can't describe a box from a detector with a label chosen by a
human.

### Decision

1. **Describe each model once, in the annotation set.** A new `annotation-set-models` list
   replaces `annotation-machine-algorithm`. Each entry describes one model version: its identity,
   its task, what its scores mean, and the threshold applied. The entry also holds that model's
   training and validation data.
2. **Record each step separately on the annotation.** Each annotation names the model that
   produced its shape and the model that produced its label, each with its own confidence.
   - A model is named by its `model-id` from the set's list.
   - A field left null means a human did that step.
3. **Confidence is a number from 0 to 1.** It is the model's score for this annotation, exactly as
   the model output it, before any human review. This is the scale used by iFDO, COCO and the
   proposed VARS table. Legacy VARS scores on a 0–100 scale are divided by 100.
4. **Scores from different models are not comparable.** Each model entry says what its score
   means (`model-score-type`). Readers MUST NOT compare or pool confidences across models unless
   the scores are described as calibrated probabilities.
5. **`annotation-machine-detect-or-classify` is no longer a field.** It is derived from which model
   fields are filled (see the rules below).

### Model attributes

Each model entry in `annotation-set-models` describes one model version: its identity, its task,
what its scores mean, the threshold applied, and its training and validation data. The attributes
are defined in [Table 5](#table-5-model-attributes).

The set-level fields `annotation-machine-training-images`, `-training-annotations`,
`-validation-images` and `-validation-annotations` are replaced by the per-model fields in
Table 5. `annotation-set-machine-scope` stays at set level. It describes the role of machine annotation in the
study as a whole.

### Annotation attributes

Each annotation names the model that produced its shape and the model that produced its label,
each with its own confidence, and may list the model's other top-ranked labels. These are
`annotation-detection-model`, `annotation-detection-confidence`,
`annotation-classification-model`, `annotation-classification-confidence` and
`annotation-classification-alternatives`, defined in [Table 4](#table-4-annotation-attributes).

### Rules

- **Model references.** Every model field that is not null MUST match a `model-id` in
  `annotation-set-models`. A confidence MUST be null when its model field is null.
- **Single-pass models.** A model that detects and classifies in one pass and gives one score,
  such as YOLO, is named in *both* model fields. Its score goes in
  `annotation-classification-confidence`. `annotation-detection-confidence` is filled only if the
  model reports a separate detection score. If a human or another model later replaces the label,
  the first model's score MAY be moved to `annotation-detection-confidence`, because it is still
  the only score for the shape.
- **Human edits.** The fields describe the annotation as it is now. If a human redraws the shape,
  the detection model and confidence are set to null. If a human changes the label, the
  classification model and confidence are set to null. A human review that accepts the annotation
  without changes leaves the fields as they are. Reviews are recorded in `annotation-reviews` (see
  [Review provenance](#review-provenance)).
- **Deriving the old fields.**

  | Detection model | Classification model | `annotation-machine-detect-or-classify` | `annotation-human-or-machine` | DwC `basisOfRecord` |
  | --- | --- | --- | --- | --- |
  | null | null | (none) | `human` | HumanObservation |
  | set | set | `detection/classification` | `algorithm` | MachineObservation |
  | set | null | `detection` | `combination` | MachineObservation |
  | null | set | `classification` | `combination` | MachineObservation |

  `annotation-human-or-machine` is kept because it maps directly to Darwin Core. It MUST agree with
  this table.
- **Human creators.** `annotation-human-creators` lists the people who did whichever steps were
  done by a human. It is empty when both steps were done by a model.

### How existing formats map

| Source | Model identity | Confidence | Notes |
| --- | --- | --- | --- |
| VARS (current) | `generator` key in the localization JSON → `model-id`, used for both detection and classification | `confidence` ÷ 100 → `annotation-classification-confidence` | No model registry. The exporter creates one model entry per distinct `generator`, with `model-version: unknown` unless it is known. If the observer changed the concept after detection, the classification model is null. |
| VARS (proposed `localizations`) | `generator` | `confidence`, already 0–1 | As above, without rescaling |
| iFDO v2.2.1 | `annotation-label.annotator` (an ORCID or a model handle) | `annotation-label.confidence` (0–1) | iFDO records the annotator on the label only. It has no field for who made the shape. |
| COCO results | One results file per model; no model field | `score` | Each results file becomes one model entry. |
| BIIGLE (MAIA) | (to confirm) | (to confirm) | |
| SQUIDLE+ | (to confirm) | (to confirm) | |
| Darwin Core | `identifiedBy` MAY carry the model name and version | No term. Could use the MeasurementOrFact extension (`measurementType: classification confidence`) | `basisOfRecord: MachineObservation` |

### Example

```yaml
annotation-set:
  annotation-set-machine-scope: >-
    Detector run on all images. Every detection was reviewed by a human, who accepted it or
    changed its label.
  annotation-set-models:
    - model-id: pap-det-v3
      model-name: YOLOv8m
      model-version: "3.1.0"
      model-task: detection+classification
      model-handle: https://doi.org/10.5072/example.pap-det-v3
      model-score-type: YOLOv8 class confidence after NMS
      model-confidence-threshold: 0.25
      model-training-annotations: c53b9646-2dfd-4a66-bb7f-3df999874d54
      model-validation-annotations: 15fcf0f7-c216-46d5-9ab3-e5429712c9df
    - model-id: pap-cls-v1
      model-name: ViT-B/16
      model-version: "1.0"
      model-task: classification
      model-score-type: softmax class probability
  annotation-set-annotations:
    - annotation-uuid: 3340ab0f-b891-42d6-a0a3-9ea48e187268     # single-pass YOLO, accepted by a reviewer
      annotation-human-or-machine: algorithm
      annotation-detection-model: pap-det-v3
      annotation-detection-confidence: null
      annotation-classification-model: pap-det-v3
      annotation-classification-confidence: 0.81
      annotation-label-name: Asteroid morphotype 2
    - annotation-uuid: 7c1e2f9a-6b3d-4e8a-9f20-5d4c3b2a1e0f     # YOLO box, relabelled by a separate classifier
      annotation-human-or-machine: algorithm
      annotation-detection-model: pap-det-v3
      annotation-detection-confidence: 0.64
      annotation-classification-model: pap-cls-v1
      annotation-classification-confidence: 0.92
      annotation-label-name: Holothurian morphotype 1
      annotation-classification-alternatives:
        - {label-name: Asteroid morphotype 2, confidence: 0.05}
    - annotation-uuid: 2b7b5a13-13f9-4873-a4e1-378541321ce5     # machine box, label chosen by a human
      annotation-human-or-machine: combination
      annotation-human-creators: [{name: Jo Sample, uri: "https://orcid.org/0000-0002-1825-0097"}]
      annotation-detection-model: pap-det-v3
      annotation-detection-confidence: 0.47
      annotation-classification-model: null
      annotation-classification-confidence: null
      annotation-label-name: Holothurian morphotype 1
```

---

## Review provenance

### The problem

The draft has two review fields per annotation: `annotation-human-reviewer` and
`annotation-human-reviewer-ID`. That leaves out:

- **When** the review happened.
- **What the reviewer decided.** They might have confirmed the annotation, corrected it, rejected
  it as a false positive, or been unable to decide.
- **What it was before** a correction.
- **More than one review.** Many curation protocols involve several reviews, for example a second
  annotator, then an expert, then a consensus decision. The sample curation protocol in the gists
  is one.

VARS records a little of this: a `verifier` key in the box JSON, and the planned
`verification_timestamp`. Darwin Core has `identificationVerificationStatus`.

### Decision

1. **Each annotation has a list of reviews.** A new `annotation-reviews` list replaces
   `annotation-human-reviewer` and `annotation-human-reviewer-ID`. Each entry records one review:
   who did it, when, and what they decided. Entries are in order, oldest first.
2. **The annotation's other fields show its state after the latest review.** Reviews do not hide
   the current values behind history. A reader who ignores `annotation-reviews` still gets the
   current shape and label.
3. **A review that changes something records the old values.** The entry's `review-previous`
   holds the values of the fields that changed, as they were before the review. This keeps the
   original machine output, which open issue 4 asked for.
4. **A summary field for simple use.** `annotation-review-status` is the outcome of the latest
   review, or `unreviewed` if there has been none. It maps to Darwin Core.
5. **Rejected annotations may be kept.** A rejected annotation is a record that the model or
   annotator was wrong. That is useful for measuring model precision and as hard negatives for
   training.
6. **Reviews are by humans.** A model that re-scores or relabels an annotation is a
   classification step and is recorded with the model fields, not as a review.

### Review attributes

Each entry in `annotation-reviews` records one review: the reviewer, the time, the outcome, what
changed, the previous values and any remarks. The attributes are defined in
[Table 7](#table-7-review-attributes).

What each outcome means:

| `review-outcome` | Meaning | Effect on the annotation |
| --- | --- | --- |
| `accepted` | The shape and label are correct as they stand | None. Model fields and confidences stay as they are. |
| `modified` | The reviewer changed the label, the shape, or both | Changed fields hold the new values. For each changed step, the model and confidence are set to null (see [Rules](#rules)). The reviewer is added to `annotation-human-creators`. |
| `rejected` | Not an object of interest: a false positive, a duplicate, or out of scope | None to the other fields. The annotation stays as it was, marked rejected. |
| `uncertain` | The reviewer could not decide, and the annotation is flagged for an expert | None |

### Annotation attributes

Each annotation has `annotation-reviews`, a list of review entries (Table 7), and
`annotation-review-status`, the outcome of the latest review. Both are defined in
[Table 4](#table-4-annotation-attributes).

### Review rules

- **The status must match the list.** `annotation-review-status` MUST equal the `review-outcome`
  of the last entry in `annotation-reviews`, or be `unreviewed` if the list is empty.
- **The creation time doesn't change.** `annotation-creation-datetime` stays the time the
  annotation was first made. Review times are in the review entries.
- **Rejected annotations are not occurrences.** An annotation whose status is `rejected` MUST NOT
  be counted in abundance, presence or any other biological result. It MUST NOT be exported to
  OBIS, GBIF or any other occurrence repository. An annotation set MAY leave rejected annotations
  out, and its `annotation-set-curation-protocol` SHOULD say whether it did.
- **Say what was reviewed.** `annotation-set-curation-protocol` SHOULD say which annotations were
  reviewed and how they were chosen. For example: "all machine detections" or "a random 10% of
  human annotations". A reader can't interpret `unreviewed` without knowing this.
- **Reviewers are recorded every time.** A reviewer who reviews the same annotation more than once
  gets one entry per review.

### How existing formats map

| Source | Mapping | Notes |
| --- | --- | --- |
| VARS (current) | `verifier` key in the box JSON → one review with that `review-reviewer`, `review-outcome: accepted`, `review-datetime: null` | VARS has no outcome field. It is assumed that a verifier means "confirmed". Earlier concept names can be found in the Envers audit table (`observations_AUD`) and could fill `review-previous`. |
| VARS (proposed `localizations`) | `verifier` and `verification_timestamp` → one review with `accepted` | |
| iFDO v2.2.1 | A review that accepts or changes the label can be written as an additional `annotation-label` entry, with the reviewer as `annotator` and the review time as `created-at` | iFDO has no review outcome and cannot express `rejected` or `uncertain`. |
| Darwin Core | `annotation-review-status` → `identificationVerificationStatus`: `accepted` and `modified` → `verified`; `unreviewed` → `unverified`; `uncertain` → `questionable`. `rejected` is not exported. `review-remarks` → `identificationRemarks`. After a `modified` review, `identifiedBy` and `dateIdentified` are the reviewer and the review time. | Darwin Core recommends a controlled vocabulary for `identificationVerificationStatus` but doesn't define one. The values used here are a proposal. |
| BIIGLE (Largo re-evaluation) | (to confirm) | |
| SQUIDLE+ | (to confirm) | |

### Example

```yaml
annotation-set-annotations:
  - annotation-uuid: 3340ab0f-b891-42d6-a0a3-9ea48e187268     # machine annotation, accepted
    annotation-label-name: Asteroid morphotype 2
    annotation-classification-model: pap-det-v3
    annotation-classification-confidence: 0.81
    annotation-review-status: accepted
    annotation-reviews:
      - review-reviewer: {name: Jo Sample, uri: https://orcid.org/0000-0002-1825-0097}
        review-datetime: 2026-09-05T09:12:00Z
        review-outcome: accepted

  - annotation-uuid: 2b7b5a13-13f9-4873-a4e1-378541321ce5     # machine label corrected by a reviewer
    annotation-human-or-machine: combination
    annotation-human-creators: [{name: Jo Sample, uri: "https://orcid.org/0000-0002-1825-0097"}]
    annotation-label-name: Holothurian morphotype 1
    annotation-detection-model: pap-det-v3
    annotation-detection-confidence: 0.47
    annotation-classification-model: null
    annotation-classification-confidence: null
    annotation-review-status: modified
    annotation-reviews:
      - review-reviewer: {name: Jo Sample, uri: https://orcid.org/0000-0002-1825-0097}
        review-datetime: 2026-09-05T09:14:30Z
        review-outcome: modified
        review-changed: [label]
        review-previous:
          annotation-label-name: Asteroid morphotype 2
          annotation-classification-model: pap-det-v3
          annotation-classification-confidence: 0.47

  - annotation-uuid: 8d2f4b61-0c7e-4a93-b5d8-1e6f9a3c7b20     # false positive, kept for training
    annotation-label-name: Asteroid morphotype 2
    annotation-classification-model: pap-det-v3
    annotation-classification-confidence: 0.31
    annotation-review-status: rejected
    annotation-reviews:
      - review-reviewer: {name: Jo Sample}
        review-datetime: 2026-09-05T09:20:05Z
        review-outcome: rejected
        review-remarks: Sediment mound, not an organism.

  - annotation-uuid: 51602484-ee63-4f66-b4b7-9f88f4af2962     # flagged, then settled by an expert
    annotation-label-name: Holothurian morphotype 1
    annotation-review-status: accepted
    annotation-reviews:
      - review-reviewer: {name: Sam Placeholder}
        review-datetime: 2026-09-05T10:02:44Z
        review-outcome: uncertain
        review-remarks: Could be morphotype 1 or 3; needs expert.
      - review-reviewer: {name: Alex Example, uri: https://orcid.org/0000-0002-1825-0097}
        review-datetime: 2026-09-12T15:40:10Z
        review-outcome: accepted
```

---

## Table 1. Label set attributes

Names follow the [naming rules](#naming-rules) (revision 0.7). The draft's names are in the
[rename table](#renamed-attributes). VARS has no label-set equivalent.

| Attribute name | Description | Allowed value(s) | Level | DarwinCore term |
| --- | --- | --- | --- | --- |
| label-set-standard-version | **New in 0.10.** The revision of this standard the label set follows. See [Standard version](#standard-version). | Quoted text, e.g. `"0.11"` | REQUIRED | |
| label-set-name | A unique name for the label set. | Text | REQUIRED | |
| label-set-project | The overarching project context within which the label set was created | `{name, uri}` | RECOMMENDED | projectTitle (name) |
| label-set-context | The more specific project or expedition or cruise or experiment within which the label set was created. | `{name, uri}` | OPTIONAL | |
| label-set-abstract | Description of what, when, where, why and how the labels were created. Includes aims, purpose of labels. | Text | RECOMMENDED | |
| label-set-objective | A general description of the aims and objectives or scope of the label set. | Text | RECOMMENDED | organismScope |
| label-set-creators | The people who created the label set | List of `{name, uri}` | REQUIRED | |
| label-set-pi | The principal investigator | `{name, uri}` | RECOMMENDED | |
| label-set-license | License to use the data (should be FAIR) | `{name, uri}`, e.g. `{name: CC-BY-4.0, uri: https://creativecommons.org/licenses/by/4.0/}` | REQUIRED | UsagePolicy |
| label-set-copyright | Copyright sentence / contact person or office | Text | RECOMMENDED | |
| label-set-uuid | A UUID for the label set | UUID | REQUIRED | |
| label-set-version | Version of the label set | Text, e.g. `"2"` or `"2.1"` | RECOMMENDED | |
| label-set-related-material | Papers, websites, software or other documentation associated with the label set | List of DOIs and/or URIs | OPTIONAL | |
| label-set-doi | DOI for the label set | DOI | OPTIONAL; RECOMMENDED once published | |
| label-set-catalogue | Link to the catalogue or vocabulary used | URI or DOI | OPTIONAL | |
| label-set-funding | Funding attribution | Text | OPTIONAL | fundingAttribution |
| label-set-labels | The labels in the set (Table 2) | List of label entries | REQUIRED | |

## Table 2. Label attributes

One entry per label in `label-set-labels`. For VARS, a label corresponds to a knowledgebase concept,
and the concept's parent in the knowledgebase hierarchy corresponds to `label-parent-name`. VARS
does not store AphiaIDs, identification qualifiers or per-label UUIDs on annotations.

| Attribute name | Description | Allowed value(s) | Level | DarwinCore term |
| --- | --- | --- | --- | --- |
| label-name | Name of the label (can be project-specific) | Text | REQUIRED | organismName |
| label-parent-name | `label-name` of the parent label in the same label set | Text | OPTIONAL (absent or null for a top-level label) | |
| label-lowest-taxonomic-name | Most detailed taxonomic identification possible without open nomenclature terms | Text | RECOMMENDED | identification or scientificName |
| label-lowest-aphia-id | AphiaID of `label-lowest-taxonomic-name` | Integer | RECOMMENDED when `label-lowest-taxonomic-name` is in WoRMS | |
| label-is-lowest-taxon | `true`: the label is `label-lowest-taxonomic-name` itself. `false`: the label is a category below it, such as a morphotype. | `true`, `false` | REQUIRED when `label-lowest-taxonomic-name` is given | |
| label-identification-qualifier | Open nomenclature term qualifying `label-lowest-taxonomic-name` | Text | OPTIONAL | identificationQualifier |
| label-uuid | UUID to tell apart similar label names used in different projects | UUID | REQUIRED | identificationID |

## Table 3. Annotation set attributes

VARS has no annotation-set entity. The nearest grouping is the video (`video_reference_uuid`) and
its cached deployment information (`mission_id`, `platform_name`, `mission_contact`).

| Attribute name | Description | Allowed values | Level | DarwinCore term |
| --- | --- | --- | --- | --- |
| annotation-set-standard-version | **New in 0.10.** The revision of this standard the annotation set follows. See [Standard version](#standard-version). | Quoted text, e.g. `"0.11"` | REQUIRED | |
| annotation-set-name | A unique name for the annotation set. | Text | REQUIRED | datasetName |
| annotation-set-project | The overarching project context within which the annotation set was created | `{name, uri}` | RECOMMENDED | Event |
| annotation-set-context | The more specific project or expedition or cruise or experiment within which the annotation set exists. | `{name, uri}` | RECOMMENDED | |
| annotation-set-abstract | Description of what, when, where, why and how the annotations were created. Includes aims, purpose of annotation, selection of images/image sets, etc. | Text | REQUIRED | |
| annotation-set-objective | The aims and objectives, pertaining to biology and method scope. Define the primary and secondary data to be measured and to what precision. | Text | RECOMMENDED | |
| annotation-set-target-environment | A definition of the habitat or environment to be annotated, including boundaries thereof | Text | OPTIONAL | |
| annotation-set-target-timescale | A definition of the period, interval or temporal environment to be annotated | Text | OPTIONAL | |
| annotation-set-curation-protocol | A description of the annotation curation/QAQC steps and results, including which annotations were reviewed and how they were chosen | Text | RECOMMENDED | |
| annotation-set-creators | The people who made annotations in the set | List of `{name, uri}` | REQUIRED | identifiedBy |
| annotation-set-pi | The principal investigator | `{name, uri}` | REQUIRED | |
| annotation-set-license | License to use the data (should be FAIR) | `{name, uri}` | REQUIRED | UsagePolicy |
| annotation-set-copyright | Copyright sentence / contact person or office | Text | RECOMMENDED | |
| annotation-set-uuid | Unique identifier | UUID | REQUIRED | datasetID |
| annotation-set-handle | Persistent URI for the annotation set | URI | OPTIONAL; RECOMMENDED once published | |
| annotation-set-version | Version of the annotation set | Text | RECOMMENDED | |
| annotation-set-image-set-names | Names of the image sets examined | List of Text | RECOMMENDED | eventID |
| annotation-set-image-set-uuids | UUIDs of the image sets examined | List of UUIDs | REQUIRED unless `annotation-set-image-metadata` is `none`; then absent | |
| annotation-set-image-set-handles | Handles of the image sets examined, in the same order as the UUIDs | List of URIs | OPTIONAL | |
| annotation-set-image-metadata | Whether the annotated images are described by an iFDO. `ifdo` (the default): yes. `none`: no iFDO exists, and the `annotation-set-images` entries are the only image records. | `ifdo`, `none` | OPTIONAL (default `ifdo`) | |
| annotation-set-images | One entry per annotated image, with its UUID, image set, filename and pixel width and height. See [Referencing the annotated image](#referencing-the-annotated-image). | List of image entries | REQUIRED | |
| annotation-set-label-set-names | Names of the label sets used | List of Text | RECOMMENDED | |
| annotation-set-label-set-uuids | UUIDs of the label sets used | List of UUIDs | REQUIRED | |
| annotation-set-connected-set-uuids | UUIDs of connected annotation sets, for example sets for habitats or litter | List of UUIDs | OPTIONAL | |
| annotation-set-machine-scope | A description of the scope of machine use, including how it relates to the scope and objectives of the study | Text | REQUIRED if `annotation-set-models` is not empty | |
| annotation-set-models | One entry per model version used, with the attributes in [Table 5](#table-5-model-attributes). See [Machine-generated annotations](#machine-generated-annotations-models-and-confidence). | List of model entries | REQUIRED if any annotation names a model | |
| annotation-set-related-material | Papers, websites, software or other documentation associated with the annotation set | List of DOIs and/or URIs | OPTIONAL | associatedReferences |
| annotation-set-quantitative-or-qualitative | Scope of observations | `qualitative`, `semi-quantitative`, `quantitative` | RECOMMENDED | samplingProtocol |
| annotation-set-quantification-type | Planned type of quantification | `presence-absence`, `count`, `linear-measurement`, `area-measurement`, `volume-measurement`, `rate` | RECOMMENDED | organismQuantityType |
| annotation-set-biological-metrics | Planned derived metrics (e.g., abundance, diversity, biomass, rate) | Text | OPTIONAL | |
| annotation-set-biological-stats | Description of desired statistical comparison (including sampling units, replicates, etc.) | Text | OPTIONAL | |
| annotation-set-obis-datasets | DOIs of OBIS datasets archived from these annotations | List of DOIs | OPTIONAL | associatedReferences |
| annotation-set-funding | Details of the funding for the annotations | Text | OPTIONAL | |
| annotation-set-annotations | The annotations in the set (Table 4) | List of annotation entries | REQUIRED (may be empty) | |

## Table 4. Annotation attributes

The descriptions, DarwinCore terms and BIIGLE terms are from the draft, updated by revisions
0.2–0.6. VARS names are annosaurus database columns. In the API's JSON they are the same in
snake_case, except `observation_group`, which is `group`.

| Attribute name | Description | Allowed value(s) | Level | DarwinCore term | BIIGLE term | VARS term (corrected) | SQUIDLE+ term |
| --- | --- | --- | --- | --- | --- | --- | --- |
| annotation-uuid | Unique identifier of the annotation | UUID | REQUIRED | occurrenceID | Annotation ID | `observations.uuid` (`observation_uuid` in the API). Each localization association also has its own `uuid`. | |
| annotation-image-uuid | The `image-uuid` of the annotated file. It MUST match an entry in the set's `annotation-set-images`. | UUID | REQUIRED | ac:isROIOf → the media record's identifier | Image filename | `image_references.uuid`, taken from the localization JSON's `image_reference_uuid` key. The filename corresponds to `image_references.url`. The image belongs to the imaged moment, not the observation. For video, the frame is identified by `video_reference_uuid` plus `recorded_timestamp`, `elapsed_time_millis` or `timecode`. | MediaObject |
| annotation-human-or-machine | Whether the annotation was made by a human, a machine or a combination. It MUST agree with the model fields (see [Rules](#rules)). | `human`, `algorithm`, `combination` | REQUIRED | basisOfRecord: HumanObservation or MachineObservation | | No field. Machine-generated localizations carry a `generator` key in their JSON. | |
| annotation-detection-model | `model-id` of the model that produced the shape ([Table 5](#table-5-model-attributes)). Null if a human drew it, or if the shape is `whole-image`. | Text (a `model-id`) or null | REQUIRED (may be null) | | | `generator` key in the localization JSON | |
| annotation-detection-confidence | The detection model's score for the shape (e.g. objectness) | Number in [0, 1] or null | OPTIONAL; null or absent when the model is null | | | | |
| annotation-classification-model | `model-id` of the model that produced the label ([Table 5](#table-5-model-attributes)). Null if a human chose it. | Text (a `model-id`) or null | REQUIRED (may be null) | identifiedBy (model name) | | `generator`, if the concept was not changed by a human | |
| annotation-classification-confidence | The classification model's score for the assigned label | Number in [0, 1] or null | RECOMMENDED when the model is set; null or absent otherwise | | | `confidence` in the localization JSON ÷ 100 | |
| annotation-classification-alternatives | The model's other top-ranked labels, best first, each with its score. Useful for review and for training. | List of `{label-name, confidence}`; `label-name` is text and `confidence` is a number in [0, 1], both REQUIRED | OPTIONAL | | | | |
| annotation-human-creators | The people who did the human steps of the annotation | List of `{name, uri}` | REQUIRED unless `annotation-human-or-machine` is `algorithm`; then empty or absent | recordedBy; recordedByID | firstname, lastname; ID of the user who created/attached the annotation label | `observations.observer` (a VARS username, not a name or ORCID) | |
| annotation-creation-datetime | Date and time the annotation was made | ISO 8601 date-time, UTC | REQUIRED | dateIdentified | Creation date | `observations.observation_timestamp`. **Not** `recorded_timestamp`, which is when the frame was captured and maps to `image-datetime`. | |
| annotation-label-name | Label assigned to the annotation: a `label-name` from one of the set's label sets | Text | REQUIRED | organismName | Label name | `observations.concept` (knowledgebase concept name, stored as free text) | Label |
| annotation-shape-name | Shape of the annotation. See [Annotation shapes and coordinates](#annotation-shapes-and-coordinates). | `single-pixel`, `polyline`, `polygon`, `rectangle`, `circle`, `ellipse`, `whole-image`, `mask` | REQUIRED | measurementType (under review, open issue 9) | Annotation shape name | `associations.link_name`: `bounding box`, `localization-point`, `localization-line`, `localization-polygon` | |
| annotation-coordinates | Pixel coordinates of the shape's vertices in the referenced image. The origin (0, 0) is the top-left corner of the image; x is to the right and y is down. See [Annotation shapes and coordinates](#annotation-shapes-and-coordinates). | Array of arrays of numbers, `[[x1, y1, x2, y2, ...]]`; one inner array for a still image | REQUIRED | Derived: ac:xFrac, ac:yFrac, ac:widthFrac, ac:heightFrac, ac:radius | Annotation points | `associations.link_value` JSON, in pixels with origin at top left. Bounding box: `{"x", "y", "width", "height"}`. Other shapes: `{"x": [...], "y": [...]}` | Point, Polygon, x, y, t |
| annotation-mask | The per-pixel mask, as COCO RLE. Required when the shape is `mask`, and absent otherwise. See [Pixel masks](#pixel-masks). | `{encoding, width, height, counts}` | REQUIRED when the shape is `mask`; absent otherwise | | | Proposed `localizations` columns `mask_encoding`, `mask_data`, `mask_width_pixels`, `mask_height_pixels` | |
| annotation-measurement | A measurement of the object, in pixels | Number | OPTIONAL | measurementValue | | No dedicated field. Could be an association. | |
| annotation-reviews | The human reviews of this annotation, oldest first, with the attributes in [Table 7](#table-7-review-attributes). An empty list or an absent attribute means it has not been reviewed. See [Review provenance](#review-provenance). | List of review entries | OPTIONAL | identifiedBy and dateIdentified after a `modified` review; identificationRemarks | | `verifier` key in the localization JSON → one `accepted` review with no time | |
| annotation-review-status | The `review-outcome` of the latest review, or `unreviewed` | `unreviewed`, `accepted`, `modified`, `rejected`, `uncertain` | REQUIRED if `annotation-reviews` is not empty; otherwise OPTIONAL (absent means `unreviewed`) | identificationVerificationStatus | | `accepted` if `verifier` is present; otherwise `unreviewed` | |
| annotation-machine-training-validation | Whether this annotation was used to train or validate a model | `training`, `validation` | OPTIONAL | | | `tags: ["training"]` in some bounding-box JSON. No validation marker. | |
| annotation-additional-info | Additional comments or observations | Text | OPTIONAL | identificationRemarks or occurrenceRemarks | Additional attributes of the image | `associations` (`link_name \| to_concept \| link_value`), e.g. `audio-comment \| nil \| <text>` | Tags; Comment for annotations (draft shows `ASSOCIATIONS` here, which appears swapped with VARS; SQUIDLE+ authors to confirm) |

VARS observation fields with no attribute in the standard: `activity` (e.g. descent, transect),
`observation_group` (e.g. ROV, AUV, images), `duration_millis`, the video time indices, and the
ancillary position and sensor data.

## Table 5. Model attributes

One entry per model version, in `annotation-set-models` (Table 3). Annotations refer to an entry
by its `model-id`, in `annotation-detection-model` and `annotation-classification-model`
(Table 4). Added in revision 0.5; see
[Machine-generated annotations](#machine-generated-annotations-models-and-confidence) for the
rules. The four `model-training-*` and `model-validation-*` attributes replace the draft's
set-level `annotation-machine-training-images`, `-training-annotations`, `-validation-images` and
`-validation-annotations`. Training and validation data belong to each model, not to the set.
BIIGLE (MAIA) and SQUIDLE+ equivalents are to confirm.

| Attribute name | Description | Allowed value(s) | Level | DarwinCore term | VARS term |
| --- | --- | --- | --- | --- | --- |
| model-id | Identifier that annotations use to refer to this entry. Unique within the annotation set. | Text, e.g. `mbari452k_yolov8` | REQUIRED | | `generator` key in the localization JSON (one entry per distinct value) |
| model-name | Name of the model or architecture | Text, e.g. `YOLOv8m` | REQUIRED | identifiedBy (with `model-version`), when the model chose the label | No field. The exporter uses the `generator` value. |
| model-version | Version of the trained weights. Use `unknown` only when converting legacy data that did not record it. | Text | REQUIRED | identifiedBy (with `model-name`) | No field. `unknown` unless known. |
| model-task | What the model produces | `detection`, `classification`, `detection+classification`, `segmentation` | REQUIRED | | No field. Usually `detection+classification`. |
| model-handle | Persistent link to the weights or the model card (DOI, Hugging Face, FathomNet model zoo, etc.) | URI or DOI | RECOMMENDED | identificationReferences | |
| model-weights-sha256 | Hash of the weights file, to identify the exact weights | 64 lowercase hexadecimal characters | OPTIONAL | | |
| model-description | How the model was applied: inference settings, image size, non-maximum suppression (NMS) settings, tiling, post-processing | Text | OPTIONAL | | |
| model-score-type | What the confidence means, e.g. "softmax class probability", "YOLO objectness × class probability", "calibrated probability" | Text | REQUIRED if any annotation reports a confidence from this model | | No field. Scores are on a 0–100 scale and are divided by 100 on export. |
| model-confidence-threshold | Minimum score kept; detections below it were discarded. Needed to interpret absences, because anything scored below the threshold is not in the data. | Number in [0, 1] | RECOMMENDED | | |
| model-label-set-uuid | The label set the model's output classes belong to, if it differs from the annotation set's label set | UUID | OPTIONAL | | |
| model-training-images | UUID or link to the training images | UUID or URI | RECOMMENDED | | |
| model-training-annotations | UUID or link to the training annotations | UUID or URI | RECOMMENDED | | |
| model-validation-images | UUID or link to the validation images | UUID or URI | OPTIONAL | | |
| model-validation-annotations | UUID or link to the validation annotations | UUID or URI | OPTIONAL | | |

## Table 6. Image attributes

One entry per annotated image, in `annotation-set-images` (Table 3). Annotations refer to an
entry by its `image-uuid`, in `annotation-image-uuid` (Table 4). Added in revision 0.3, and
extended in 0.4 and 0.9. See [Referencing the annotated image](#referencing-the-annotated-image)
for the rules. Names follow iFDO wherever iFDO has the field. BIIGLE and SQUIDLE+ equivalents are
to confirm.

| Attribute name | Description | Allowed value(s) | Level | iFDO field | DarwinCore / Audubon Core term | VARS term |
| --- | --- | --- | --- | --- | --- | --- |
| image-uuid | The UUID of the annotated file. Annotations refer to it with `annotation-image-uuid`. When there is an iFDO, this is the iFDO `image-uuid`. | UUID | REQUIRED | `image-uuid` | dcterms:identifier of the media record | `image_references.uuid` |
| image-uuid-source | Where the UUID is recorded. `embedded`: in the file's metadata. `assigned`: only outside the file. See [Images without an embedded UUID, or without an iFDO](#images-without-an-embedded-uuid-or-without-an-ifdo). | `embedded`, `assigned` | REQUIRED | | | `assigned`: VARS does not embed UUIDs in files |
| image-set-uuid | The image set the image belongs to. It MUST be one of the set's `annotation-set-image-set-uuids`. | UUID | REQUIRED if the annotation set references more than one image set; absent when `annotation-set-image-metadata` is `none` | `image-set-uuid` | | No field |
| image-filename | The image's key in the iFDO `image-set-items` (a filename or relative path), or its original filename when there is no iFDO. For people to read; not for lookup. | Text | RECOMMENDED | key of `image-set-items` | | Last part of `image_references.url` |
| image-handle | A URI to download the image | URI | REQUIRED when `annotation-set-image-metadata` is `none` or `image-hash-sha256` is null; otherwise OPTIONAL | `image-handle` | ac:accessURI | `image_references.url` |
| image-hash-sha256 | The SHA-256 hash of the file. Confirms that the coordinates apply to these exact bytes, and links an assigned UUID to its file. | 64 lowercase hexadecimal characters, or null if the bytes cannot be hashed | REQUIRED when `image-uuid-source` is `assigned`; otherwise OPTIONAL | `image-hash-sha256` | | No field. Computed on export. |
| image-width-pixels | Width of the file in pixels | Integer > 0 | REQUIRED | none (proposed `image-pixel-width`) | exif:PixelXDimension | `image_references.width_pixels` (nullable; fill in on export) |
| image-height-pixels | Height of the file in pixels | Integer > 0 | REQUIRED | none (proposed `image-pixel-height`) | exif:PixelYDimension | `image_references.height_pixels` (nullable; fill in on export) |
| image-datetime | When the image was captured, or when a video started. See [Capture time](#capture-time). | ISO 8601 date-time in UTC, e.g. `2026-06-12T03:15:22.000Z` | OPTIONAL when there is an iFDO, and then MUST be the same instant as the iFDO value; RECOMMENDED when `annotation-set-image-metadata` is `none` | `image-datetime` | eventDate | `imaged_moments.recorded_timestamp` |

## Table 7. Review attributes

One entry per review, in an annotation's `annotation-reviews` (Table 4), oldest first. Added in
revision 0.6. See [Review provenance](#review-provenance) for what each outcome means and for the
rules. BIIGLE (Largo) and SQUIDLE+ equivalents are to confirm.

| Attribute name | Description | Allowed value(s) | Level | DarwinCore term | VARS term |
| --- | --- | --- | --- | --- | --- |
| review-reviewer | The reviewer | `{name, uri}` ([Table 9](#table-9-name-and-uri-object)) | REQUIRED | identifiedBy and identifiedByID, after a `modified` review | `verifier` key in the localization JSON (a username, so `name` only) |
| review-datetime | When the review was made | ISO 8601 date-time in UTC; null only for legacy data that did not record it | REQUIRED (may be null) | dateIdentified, after a `modified` review | No field, so null. The proposed `localizations` table has `verification_timestamp`. |
| review-outcome | What the reviewer decided | `accepted`, `modified`, `rejected`, `uncertain` | REQUIRED | identificationVerificationStatus, through `annotation-review-status` | `accepted` when `verifier` is present (assumed; open issue 5) |
| review-changed | Which parts the reviewer changed | List of `label`, `shape` | REQUIRED if `review-outcome` is `modified`; absent otherwise | | No field |
| review-previous | The changed attributes' values before this review | Object holding any of `annotation-label-name`, `annotation-shape-name`, `annotation-coordinates`, `annotation-mask`, `annotation-detection-model`, `annotation-detection-confidence`, `annotation-classification-model`, `annotation-classification-confidence` | RECOMMENDED if `review-outcome` is `modified`; absent otherwise | | Earlier concept names are in the Envers audit table `observations_AUD` |
| review-remarks | Free-text notes, e.g. why an annotation was rejected | Text | OPTIONAL | identificationRemarks | No field |

## Table 8. Mask keys

The keys of the `annotation-mask` object (Table 4), which is REQUIRED when
`annotation-shape-name` is `mask` and absent otherwise. Added in revision 0.8. See
[Pixel masks](#pixel-masks) for the encoding rules. Like `{name, uri}`, it is a small object with
plain keys, so the naming prefixes don't apply.

| Key | Description | Allowed value(s) | Level | COCO term | VARS term (proposed `localizations` table) |
| --- | --- | --- | --- | --- | --- |
| encoding | The form of `counts`. More encodings may be added later. | `coco-rle` (a list of integers) or `coco-rle-compressed` (a string) | REQUIRED | Whether `segmentation.counts` is a list or a string | `mask_encoding` (`coco_rle`) |
| width | Mask width in pixels. MUST equal `image-width-pixels`. | Integer > 0 | REQUIRED | `segmentation.size[1]` | `mask_width_pixels` |
| height | Mask height in pixels. MUST equal `image-height-pixels`. | Integer > 0 | REQUIRED | `segmentation.size[0]` | `mask_height_pixels` |
| counts | The run lengths: column-major, starting with background, adding up to width × height | List of non-negative integers (`coco-rle`), or a string (`coco-rle-compressed`) | REQUIRED | `segmentation.counts` | `mask_data` (which form is to confirm) |

## Table 9. Name and URI object

The `{name, uri}` object used for people and named things, as in iFDO. Added in revision 0.7
(naming rule 5). It is the value of these attributes:

- label sets: `label-set-project`, `label-set-context`, `label-set-creators` (list),
  `label-set-pi`, `label-set-license`;
- annotation sets: `annotation-set-project`, `annotation-set-context`, `annotation-set-creators`
  (list), `annotation-set-pi`, `annotation-set-license`;
- annotations: `annotation-human-creators` (list);
- reviews: `review-reviewer`.

| Key | Description | Allowed value(s) | Level | iFDO term |
| --- | --- | --- | --- | --- |
| name | Name of the person, project, context or license | Text, not empty | REQUIRED | `name` |
| uri | Link to details. For a person, an ORCID, or a `mailto:` URI if there is no ORCID. For a license, the license text, e.g. `https://creativecommons.org/licenses/by/4.0/`. | URI | RECOMMENDED for people and licenses; OPTIONAL otherwise | `uri` |

No other keys are allowed.

## Table 10. Top-level containers

The keys at the top level of a file. Added in revision 0.10. See
[File structure](#file-structure) for the rules. This table comes last so that Tables 1–4 keep the
draft's numbering, even though the containers come first in a file.

| Key | Contents | Allowed value(s) | Level | Names in the nested form |
| --- | --- | --- | --- | --- |
| label-set | One label set: the Table 1 attributes, with its labels (Table 2) in `label-set-labels` | Object | OPTIONAL, but a file MUST have at least one of `label-set` and `annotation-set` | Unchanged |
| annotation-set | One annotation set: the Table 3 attributes, with its annotations (Table 4) in `annotation-set-annotations`, its images (Table 6) in `annotation-set-images`, and its models (Table 5) in `annotation-set-models` | Object | OPTIONAL, but a file MUST have at least one of `label-set` and `annotation-set` | Unchanged |

No other top-level keys are allowed. They are reserved for later revisions.

---

## Open issues for later revisions

Items noticed while revising the standard. Resolved items are struck through and keep their numbers.

1. **Video.** VARS annotates video. The standard has no way to identify a frame or time in a video
   (video reference plus timestamp, elapsed time or timecode), and no duration for an observation.
   The draft lists video as future expansion. Since 0.9, VARS video moments are handled with
   `image-datetime` (the moment's `recorded_timestamp`; see [Capture time](#capture-time)). That
   leaves general video support open: iFDO's `frames`, elapsed time, timecode and duration.
2. ~~**Coordinate encoding.**~~ Resolved in revision 0.2. See
   [Annotation shapes and coordinates](#annotation-shapes-and-coordinates). Still to do:
   - Propose the **(addition)** rules to the iFDO maintainers.
   - Confirm the BIIGLE polygon closure and the SQUIDLE+ encoding with those teams.
3. ~~**Which image the coordinates refer to.**~~ Resolved in revision 0.3. See
   [Referencing the annotated image](#referencing-the-annotated-image). Still to do:
   - Propose `image-pixel-width` and `image-pixel-height` to the iFDO maintainers.
   - Confirm the BIIGLE and SQUIDLE+ image identifiers and dimension fields.
   - ~~Decide how a VARS export assigns iFDO image UUIDs.~~ Resolved in 0.4: the export keeps
     `image_references.uuid` as an assigned UUID.
   - Propose `image-uuid-source` and the hash-derived UUID rule to the iFDO maintainers.
   - Register the namespace UUID `8fb66ecc-ce0d-45ff-b8ab-23bd7774d760` when the standard is
     published.
4. ~~**Machine confidence and generator.**~~ Resolved in revision 0.5. See
   [Machine-generated annotations](#machine-generated-annotations-models-and-confidence). Still to
   do:
   - Confirm how BIIGLE (MAIA) and SQUIDLE+ record model identity and scores.
   - ~~Decide whether to keep the original machine values when a human edits an annotation.~~
     Resolved in 0.6. A review keeps them in `review-previous`. Edits made outside a review still
     lose them.
   - Propose separate attribution for the shape (detection) to iFDO, which has none.
   - Review the Darwin Core mapping for confidence: MeasurementOrFact, or an extension term.
5. ~~**Review provenance.**~~ Resolved in revision 0.6. See
   [Review provenance](#review-provenance). Still to do:
   - Confirm how BIIGLE (Largo) and SQUIDLE+ record reviews.
   - Agree a controlled vocabulary for Darwin Core `identificationVerificationStatus` with OBIS.
   - Decide whether the VARS `verifier` key always means "confirmed".
6. ~~**Names.**~~ Resolved in revision 0.7. See [Naming rules](#naming-rules). Still to do:
   - Update the draft's Results text to use `annotation-set-machine-scope`.
   - Regenerate the gist samples with the new names.
7. ~~**Container names.**~~ Resolved in revision 0.7. The containers are top-level `label-set` and
   `annotation-set`, with `label-set-labels` and `annotation-set-annotations` inside them.
8. ~~**Masks.**~~ Resolved in revision 0.8. See [Pixel masks](#pixel-masks). Still to do:
   - Propose the `mask` shape to iFDO.
   - Confirm which COCO form the VARS proposal stores in `mask_data`.
   - Confirm whether BIIGLE or SQUIDLE+ store masks.
9. **`annotation-shape-name` DarwinCore term.** The draft maps the shape name to
   `measurementType`. The shape describes a region of interest, not a measurement, so this mapping
   needs review.
10. **Dense label maps.** Habitat and substrate cover is often a per-pixel class map of the whole
    image, usually a PNG whose pixel values are label indices. Such a map is not one annotation per
    object, so `annotation-mask` is not the right fit. It may need its own image-level attribute,
    one that references the map file, the value-to-label table and the file's hash.
11. ~~**Requirement levels and a schema.**~~ Resolved in revision 0.11. See
    [Requirement levels](#requirement-levels) and [JSON Schema](#json-schema). Still to do:
    - Review the levels with the co-authors, especially which Table 1 and Table 3 attributes are
      REQUIRED.
    - Publish the schema at a permanent `$id`.
    - Publish a validator for the checks the schema can't make. A draft is in
      [tools/](tools/README.md) (`validate_rules.py`).
12. **Local extensions.** The schema rejects attributes it doesn't define. The draft wants the
    standard to be "expandable to include additional attributes". One option is a reserved
    prefix, such as `x-`, for local attributes that readers ignore. Another is a single
    `…-extensions` object at each level.
