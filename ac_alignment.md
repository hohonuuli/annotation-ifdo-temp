# Audiovisual Core alignment: exploration notes

Exploration only. Nothing in [refined_standard.md](refined_standard.md) has been changed. This
is a companion to [dwc_alignment.md](dwc_alignment.md).

**Sources compared:**
- The standard: revision 0.12, Tables 1–10.
- The **Audiovisual Core (AC) term list, version 2026-01-23**
  (<https://github.com/tdwg/ac/blob/master/docs/termlist/2026-01-23.md>), with 165 terms.
- The live list at <https://ac.tdwg.org/termlist/>, version 2026-02-24, which replaces it. The
  only difference is one added class, `ac:Media`, matching Darwin Core's new `ac:Media` class. No
  term relevant here changed.

Prefixes: `ac:` Audiovisual Core; `dc:` / `dcterms:` Dublin Core; `exif:`, `xmp:`, `xmpRights:`
from XMP/EXIF (borrowed by AC); `dwc:` Darwin Core.

## Summary

1. **The name has changed.** "Audubon Core" is now **Audiovisual Core**. The standard says
   "Audubon Core" in several places, most visibly the "Mapping to Darwin Core / Audubon Core"
   heading in the shapes section.
2. **The region-of-interest rules already match AC.** The origin is the top-left, coordinates
   convert to fractions of width and height, the radius is a fraction of the *width*, a point is a
   zero radius, zero-size rectangles aren't allowed, and circles may extend past the image. AC
   still supports only **rectangles and circles**, as its own text says, so our polygons,
   polylines, ellipses, rotated rectangles and masks can only be exported as bounding
   rectangles. That is what revision 0.2 already says.
3. **AC fixes the pixel grid on the "Best Quality" variant.** AC's precision rules multiply the
   fractions by the pixel size of the **Best Quality variant** of the media item. Our coordinates
   are on the exact file named by `image-uuid`, which may be a lower-quality copy. When the two
   differ, an exporter must scale. A way to say which variant an image entry is (`ac:variant`)
   would make this explicit.
4. **AC has terms for things the standard has with no mapping:**
   - the image hash: `ac:hashValue` + `ac:hashFunction`;
   - derived images: `ac:derivedFrom`;
   - the media type: `dc:type`, `StillImage` / `MovingImage`;
   - the file format: `dc:format`;
   - the capture time: `xmp:CreateDate`.
5. **A label maps well to `ac:CVtermLiteral` + `ac:subjectCategoryVocabulary`.** AC's way to say
   "this image or region shows *X*, from controlled vocabulary *V*" fits project labels,
   including non-taxonomic ones such as habitat or litter labels. The label set is the
   vocabulary. This complements the Darwin Core mapping (`dwc:verbatimIdentification`), which
   only suits organisms.
6. **AC already has terms for video regions.** `ac:startTime` / `ac:endTime` are offsets in seconds
   (iFDO `frames`, VARS `elapsed_time_millis`). `ac:startTimestamp` / `ac:endTimestamp` are UTC
   clock times (VARS `recorded_timestamp`). With `ac:frameRate` and `ac:mediaDuration`, these
   give open issue 1 a ready vocabulary.
7. **An annotation can export as an AC region of interest.** AC states that features in a region
   "can be taxonomically identified or linked to occurrence records". So each annotation can be
   an `ac:RegionOfInterest` (linked with `ac:isROIOf`). It can carry `dwc:scientificName`,
   `dwc:identifiedBy`, `dwc:dateIdentified` and `dwc:identificationQualifier` from AC's
   Taxonomic Coverage vocabulary. That works alongside, or instead of, a Darwin Core Occurrence.

## How the standard's objects map to AC

| Standard | AC | Notes |
| --- | --- | --- |
| Image (Table 6) | `ac:Media` + one `ac:ServiceAccessPoint` | The image entry is one specific file, i.e. one access point (variant) of a media item |
| Annotation (Table 4) | `ac:RegionOfInterest`, `ac:isROIOf` the media item | Shape → `ac:xFrac` … `ac:radius`; identity → Taxonomic Coverage terms |
| Label set (Tables 1–2) | `ac:subjectCategoryVocabulary` | The vocabulary that labels are drawn from |
| Label | `ac:CVtermLiteral` (and `dwc:scientificName` if taxonomic) | |
| Annotation set | An AC collection (`dc:type` = Collection) | Only loosely. Set-level metadata mostly belongs in EML or Darwin Core. |

## Where the standard already aligns

| Attribute | AC term | Comment |
| --- | --- | --- |
| image-uuid | dcterms:identifier | Exact. Required in AC. |
| image-handle | ac:accessURI | Exact |
| image-width-pixels, image-height-pixels | exif:PixelXDimension, exif:PixelYDimension | Exact, for that access point |
| annotation-image-uuid | ac:isROIOf | Exact |
| annotation-coordinates (`rectangle`, axis-aligned) | ac:xFrac, ac:yFrac, ac:widthFrac, ac:heightFrac | Exact after dividing by the image size |
| annotation-coordinates (`circle`) | ac:xFrac, ac:yFrac, ac:radius | Exact. The radius is a fraction of the width in both. |
| annotation-coordinates (`single-pixel`) | ac:xFrac, ac:yFrac, ac:radius = 0 | Exact. AC adds that nothing can be assumed about the object's bounds, which matches. |
| annotation-coordinates (`whole-image`) | no ROI; the record refers to the media item | Matches 0.2 |
| label-set-funding, annotation-set-funding | ac:fundingAttribution | Exact. AC is where the term comes from. |
| label-identification-qualifier | dwc:identificationQualifier (in AC's Taxonomic Coverage) | Exact |
| annotation-creation-datetime | dwc:dateIdentified | Exact |

## Where we might change the standard to align

"Mapping only" means the attribute stays as it is and only the mapping changes.

| Attribute | Problem | Suggestion |
| --- | --- | --- |
| (document text) | Says "Audubon Core" | Rename to Audiovisual Core everywhere, and cite the term list version |
| image-hash-sha256 | No AC mapping given | `ac:hashValue`, with `ac:hashFunction` = `SHA-256`. Mapping only. |
| image-datetime | Only `dwc:eventDate` given | Also `xmp:CreateDate`. For an absolute time range, `ac:startTimestamp` on the media item. Mapping only. |
| image-filename | No mapping | `ac:providerManagedID`. Mapping only. |
| annotation-label-name | Only Darwin Core terms given | `ac:CVtermLiteral` on the region of interest, with `ac:subjectCategoryVocabulary` = the label set's DOI or catalogue. Mapping only. |
| label-set-doi / label-set-catalogue | | `ac:subjectCategoryVocabulary` (a stable URL for the vocabulary) |
| label-set-objective | | `ac:taxonCoverage` when the scope is one higher taxon (e.g. Echinodermata). It complements `eco:targetTaxonomicScope` (see the Darwin Core notes). |
| label-set-copyright, annotation-set-copyright | The Darwin Core notes suggest `dcterms:rightsHolder` | AC keeps a *sentence* in `dc:rights` and the owners' names in `xmpRights:Owner`. **Keep the sentence**, mapped to `dc:rights`. Add an optional owner `{name, uri}` for `xmpRights:Owner` / `dcterms:rightsHolder`. |
| label-set-license, annotation-set-license | | `uri` → `dcterms:rights` (AC requires `dcterms:rights` or `dc:rights`) and `xmpRights:WebStatement`; `name` → `xmpRights:UsageTerms` |
| annotation-reviews (accepted) | | `ac:reviewerLiteral` / `ac:reviewer` with `ac:reviewerComments` on the region of interest. AC's reviewer means an expert approved the item's metadata, which fits an accepted review. Modified reviews still map to `dwc:identifiedBy` (new identification). |
| annotation-human-creators, annotation-classification-model | | `dwc:identifiedBy`, as in AC's Taxonomic Coverage vocabulary. This agrees with the Darwin Core notes. **Not** `dcterms:creator`, which is the creator of the media. |
| model entries (Table 5) | | No AC terms. The Darwin Core Agent and Protocol classes cover them. |

## New attributes worth adding

| Possible attribute | Level | AC term | Why |
| --- | --- | --- | --- |
| image-variant | image | ac:variant / ac:variantLiteral (`bestQuality`, `goodQuality`, `mediumQuality`, `lowerQuality`, `thumbnail`, `offline`, `trailer`) | Says which representation the coordinates are on. AC's fractions assume `bestQuality`. |
| image-format | image | dc:format (MIME type) | Distinguishes the PNG and JPEG versions of a frame grab. VARS already stores `image_references.format`. |
| image-type | image (or fixed export) | dc:type (`StillImage`, `MovingImage`) | Required in AC. It would also mark video entries for open issue 1. |
| image-derived-from-uuid | image | ac:derivedFrom | Records that a derived copy (0.3 rule) came from another image, so annotations can be traced across copies |
| image-capture-device | image (from the iFDO) | ac:captureDevice | Usually taken from iFDO `image-sensor`. Listed for export completeness only. |
| For video (open issue 1) | annotation | ac:startTime / ac:endTime, ac:startTimestamp / ac:endTimestamp | Offsets and clock times for a temporal region. They match iFDO `frames` and VARS `elapsed_time_millis` / `recorded_timestamp`. |
| For video (open issue 1) | image | ac:frameRate, ac:mediaDuration | Needed to convert between frame numbers, offsets and clock times |
| annotation-subject-part, annotation-subject-orientation (optional) | annotation | ac:subjectPartLiteral, ac:subjectOrientationLiteral | Which part of the organism is shown, and from which view. These are common VARS associations, with AC controlled vocabularies. |

## What AC can't express (proposal candidates)

- **Shapes other than rectangles and circles.** AC regions are limited to these. Polygon,
  polyline, ellipse, rotated rectangle and mask regions would need an AC extension. A joint
  proposal with iFDO, which has the same gap for masks, could cover both.
- **Per-region machine provenance.** AC has no model, confidence or score terms. Darwin Core's
  `Assertion` class (see the Darwin Core notes) is the natural place.
- **Rejected or uncertain reviews.** `xmp:Rating = -1` means "rejected", but it rates the media
  file, not an identification. It should not be used for review outcomes.

## How this interacts with the Darwin Core findings

- **They agree** on `dwc:identifiedBy` for annotators and models. AC's Taxonomic Coverage
  vocabulary uses the Darwin Core identification terms directly.
- **They agree** that the region of interest belongs to the media record, and the occurrence to
  Darwin Core. An exporter can produce both from one annotation: an `ac:RegionOfInterest`
  linked to an `ac:Media`, and a `dwc:Occurrence` whose `dwc:associatedMedia` points to the
  media.
- **Copyright differs.** Darwin Core uses `dcterms:rightsHolder` (an agent), while AC keeps the
  copyright sentence in `dc:rights`. Keeping our sentence and adding an optional owner satisfies
  both.
- **Labels:** AC's `ac:CVtermLiteral` is the general mapping for any label.
  `dwc:verbatimIdentification` is the organism-specific mapping. Non-organism labels (habitat,
  substrate, litter) only fit AC, or a Darwin Core MeasurementOrFact.
