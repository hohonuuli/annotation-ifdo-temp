# Darwin Core alignment: exploration notes

Exploration only. Nothing in [refined_standard.md](refined_standard.md) has been changed. These
notes compare the standard (revision 0.12, Tables 1–10) with the full Darwin Core term list at
<https://dwc.tdwg.org/terms/>, read on 2026-10-22. That list has 531 terms in 33 classes. It
includes:

- the Humboldt Extension terms (`eco:`) for **Survey** and **SurveyTarget**;
- the newer **Agent**, **Assertion**, **Identification**, **Provenance**, **Protocol** and
  **UsagePolicy** classes.

Namespaces below: `dwc:` Darwin Core, `eco:` Humboldt Extension, `dcterms:` Dublin Core,
`ac:` Audubon Core, `exif:` EXIF.

## Summary

The biggest findings:

1. **Image-based records are `MachineObservation`.** Darwin Core's examples of a
   MachineObservation are "a photograph" and "a video". HumanObservation is a record "without
   physical evidence or evidence captured with a machine". So every annotation should export as
   `dwc:basisOfRecord = MachineObservation`, *even when a human made it*. The standard currently
   maps `human` to HumanObservation, which is wrong. Whether a person or a model identified the
   organism belongs in the Identification terms (`dwc:identifiedBy`, `dwc:identificationType`),
   not in `basisOfRecord`.
2. **A label is a classification, not an `organismName`.** `dwc:organismName` is a name for one
   individual organism, such as "Huberta" or "J pod". A project label such as "Holothurian
   morphotype 1" should map to `dwc:verbatimIdentification`, whose examples include
   "Ministrymon sp. nov. 1". The taxon should map to `dwc:scientificName`, and the AphiaID to
   `dwc:scientificNameID`.
3. **Annotators are identifiers, not recorders.** `dwc:recordedBy` is the agent that recorded the
   *event*, and its examples include "ROV SuBastian". The person or model that drew or labelled an
   annotation is `dwc:identifiedBy` / `dwc:identifiedByID`. `dwc:recordedBy` should come from the
   iFDO (platform or image creators).
4. **The Humboldt Extension models the draft's "biological scope" and "recording absence".** The
   label set's objective and target environment, plus whether every target organism was
   annotated, map to `eco:targetTaxonomicScope`, `eco:targetHabitatScope`,
   `eco:isTaxonomicScopeFullyReported`, `eco:isAbsenceReported` and `eco:SurveyTarget`. This is the
   strongest fit in Darwin Core for what the draft calls the "biological scope". The standard is
   missing a few of these flags. They matter for absence inference and for machine-learning
   training data (see [New attributes worth adding](#new-attributes-worth-adding)).
5. **Confidence, alternative labels and review decisions fit `dwc:Assertion`.** Darwin Core now
   has a general class for "a statement about a resource", with a type, value, author, date and
   protocol. That suits model confidences and review outcomes better than MeasurementOrFact.
6. **Several mappings name a class instead of a term.** Examples are `UsagePolicy` and `Event`. Others
   are under-specified, such as "identification or scientificName", or name the wrong level, such as
   `eventID` for an image set *name*. All mappings should name one namespaced term.
7. **Much set-level metadata isn't Darwin Core at all.** The abstract, PI, creators, copyright
   and version normally go in the dataset's EML metadata when published to OBIS or GBIF, not in
   Darwin Core terms. The mapping column could say "EML" for these, rather than leaving them blank
   or forcing a term.

## How the standard's objects map to Darwin Core classes

| Standard | Darwin Core class | Notes |
| --- | --- | --- |
| Annotation set | `eco:Survey` (plus dataset metadata in EML) | `dwc:datasetID` / `dwc:datasetName` |
| Image set (iFDO) | `dwc:Event`, parent of the image events | The draft already says image set ≈ Event |
| Image (Table 6) | `dwc:Event` (one image) and `ac:Media` | `dwc:eventDate` from `image-datetime` |
| Annotation (Table 4) | `dwc:Occurrence` + `dwc:Identification` + an `ac:Media` region of interest | One annotation = one occurrence record |
| Label set (Tables 1–2) | `eco:SurveyTarget`s + the taxon concept source (`dwc:nameAccordingTo`) | Each label is a target scope |
| Model (Table 5) | `dcterms:Agent` (`dwc:agentType` such as software) + `dwc:Protocol` | Darwin Core lists "a software instance" as an Agent |
| Review (Table 7) | A new `dwc:Identification` (if modified) or a `dwc:Assertion` | See below |
| `{name, uri}` (Table 9) | `dcterms:Agent` (`dwc:agentID` = `uri`) | For people and organizations |
| Confidence | `dwc:Assertion` | `assertionType`, `assertionValue`, `assertionBy` |

## Where the standard already aligns

These mappings match the Darwin Core definitions and can stay. Some need a small addition.

| Attribute | Darwin Core term | Comment |
| --- | --- | --- |
| annotation-set-name | dwc:datasetName | Exact |
| annotation-set-uuid | dwc:datasetID | Exact |
| annotation-uuid | dwc:occurrenceID | Good. See the note on repeat sightings below. |
| annotation-creation-datetime | dwc:dateIdentified | Exact. Both are ISO 8601. |
| image-datetime | dwc:eventDate | Exact |
| label-identification-qualifier | dwc:identificationQualifier | Exact |
| label-lowest-taxonomic-name | dwc:scientificName | Pick this term. Drop "identification or" from the mapping. |
| annotation-review-status | dwc:identificationVerificationStatus | Term is right. Vocabulary needs agreeing (below). |
| review-remarks | dwc:identificationRemarks | Exact |
| review-reviewer, after `modified` | dwc:identifiedBy, dwc:identifiedByID | Exact. A modifying review is a new identification. |
| annotation-classification-model | dwc:identifiedBy | Darwin Core's own example is "MegaDetector V5" |
| annotation-measurement | dwc:measurementValue | Add `dwc:measurementUnit` = pixels and a `dwc:measurementType` |
| label-set-funding, annotation-set-funding | ac:fundingAttribution | Exact. It is in the Provenance class. Table 3 has the term missing. |
| annotation-set-related-material | dwc:associatedReferences | Acceptable. See below for a dataset-level choice. |
| annotation-additional-info | dwc:occurrenceRemarks / dwc:identificationRemarks | Fine |
| image-handle | ac:accessURI | Audubon Core, exact |
| image-width-pixels, image-height-pixels | exif:PixelXDimension, exif:PixelYDimension | Audubon Core, exact |
| annotation-coordinates | ac:xFrac, ac:yFrac, ac:widthFrac, ac:heightFrac, ac:radius (derived) | Audubon Core regions of interest, as in 0.2 |

## Where we might change the standard to align

Each row is a mapping that is wrong or weak, with a suggested fix. "Mapping only" means the
attribute stays as it is and only the Darwin Core column changes.

| Attribute | Current mapping | Problem | Suggestion |
| --- | --- | --- | --- |
| annotation-human-or-machine | basisOfRecord: Human/MachineObservation | Images are always MachineObservation | Export `dwc:basisOfRecord = MachineObservation` for all. Express human or machine through `dwc:identifiedBy` and an Agent's `dwc:agentType`. Mapping only. |
| annotation-label-name, label-name | dwc:organismName | organismName names an individual | `dwc:verbatimIdentification`. Mapping only. |
| label-lowest-aphia-id | (none) | OBIS expects an identifier | `dwc:scientificNameID` as `urn:lsid:marinespecies.org:taxname:<AphiaID>`. Mapping only. Or store the LSID directly. |
| label-uuid | dwc:identificationID | identificationID names one identification act, not a label category | `dwc:taxonConceptID`. A project label is a taxon concept defined by its label set. |
| label-set-doi, label-set-catalogue | (none) | The label set is the "sensu" source for its labels | `dwc:nameAccordingTo` / `dwc:nameAccordingToID` for the label set, and `dwc:identificationReferences` for the catalogue (a field guide in Darwin Core terms) |
| label-parent-name | (none) | Not equivalent to `dwc:parentNameUsage`, which is taxonomic only | Leave unmapped. Note that it maps only when the hierarchy is taxonomic. |
| label-set-objective | dwc:organismScope | organismScope is the *kind* of organism instance (colony, virus), not the study scope | `eco:targetTaxonomicScope` / `eco:excludedTaxonomicScope`. Use `eco:verbatimTargetScope` for free text. |
| annotation-set-target-environment | (none) | | `eco:targetHabitatScope` / `eco:excludedHabitatScope` |
| annotation-human-creators | dwc:recordedBy; recordedByID | recordedBy is who recorded the event, e.g. "ROV SuBastian" | `dwc:identifiedBy` / `dwc:identifiedByID`. Take `dwc:recordedBy` from the iFDO platform or image creators. Consider renaming the attribute `annotation-identified-by`. |
| annotation-set-creators | dwc:identifiedBy | Fine in Survey context (Darwin Core says identifiedBy then covers all identifications) | Keep. Also EML creators. |
| label-set-project, annotation-set-project | projectTitle (name) / Event | `Event` is a class | `dwc:projectTitle` (name) and `dwc:projectID` (uri), for both |
| annotation-set-context | (none) | | Parent `dwc:Event` with `dwc:eventType` = expedition; or `dwc:parentEventID` |
| label-set-license, annotation-set-license | UsagePolicy | UsagePolicy is a class | `dcterms:license` (use `uri`, e.g. the CC legal code) |
| label-set-copyright, annotation-set-copyright | (none) | | `dcterms:rightsHolder`. Consider changing the value from a sentence to `{name, uri}`. |
| annotation-set-image-set-names | dwc:eventID | A name isn't an ID | Map **`annotation-set-image-set-uuids`** to `dwc:parentEventID` of each image event. Leave the names unmapped. |
| annotation-set-quantitative-or-qualitative | dwc:samplingProtocol | samplingProtocol is the method name | `eco:isAbundanceReported` (quantitative ⇒ true). Consider replacing with Humboldt booleans. |
| annotation-set-quantification-type | dwc:organismQuantityType | That term is per occurrence ("individuals", "% cover"), and our values mix in measurement types | Per occurrence, export `dwc:organismQuantity` = 1 and `dwc:organismQuantityType` = individuals (or % cover for masks used as cover). Align the value list with Darwin Core's. |
| annotation-set-obis-datasets | dwc:associatedReferences | That term is for references about an occurrence | `dcterms:references`, or record it only in EML |
| annotation-shape-name | dwc:measurementType | Not a measurement (open issue 9) | Drop the Darwin Core mapping. The shape is Audubon Core region-of-interest information. |
| annotation-image-uuid | ac:isROIOf | Fine for Audubon Core | Also export `dwc:associatedMedia` (the image's `image-handle`) |
| model-handle | dwc:identificationReferences | Workable | Better: `dwc:identifiedByID` (the model as an Agent). Keep identificationReferences for the model card or paper. |
| annotation-reviews (accepted) | (only modified reviews map) | | `dwc:Assertion` (`assertionType` = identification review, `assertionBy`, `assertionMadeDate`). Or keep the identification and set `dwc:identificationVerificationStatus`. |
| review-previous | (none) | | `dwc:previousIdentifications` for earlier labels. Or export each superseded label as a `dwc:Identification` with `dwc:isAcceptedIdentification` = false. |
| annotation-review-status vocabulary | verified / unverified / questionable (proposed in 0.6) | Darwin Core recommends the HISPID/ABCD vocabulary (example "0" = unverified) | Adopt the HISPID/ABCD codes, or agree a TDWG/OBIS IRI vocabulary (open issue 5) |
| annotation-detection-confidence, annotation-classification-confidence, -alternatives | (none) | | `dwc:Assertion`: `assertionType` (e.g. classificationConfidence), `assertionValue`, `assertionBy` (model), `assertionProtocols` (`model-score-type`) |
| annotation-set-curation-protocol | (none) | | `dwc:Protocol` (`protocolType` = curation, `protocolDescription`) |
| model-description, model-score-type | (none) | | `dwc:Protocol` / `dwc:protocolDescription`. `assertionProtocols` for the score. |

## New attributes worth adding

These Darwin Core terms have no counterpart in the standard yet, but they record things that
imaging studies know and that downstream users need.

| Possible attribute | Level | Darwin Core term | Why |
| --- | --- | --- | --- |
| annotation-set-is-taxonomic-scope-fully-reported | annotation set | eco:isTaxonomicScopeFullyReported | Says whether *every* instance of every target label was annotated in each examined image. Needed to infer absence and to use the set as exhaustive training data. |
| annotation-set-is-absence-reported | annotation set | eco:isAbsenceReported, eco:absentTaxa | The draft's "Recording the absence" section asks for this |
| label-is-fully-reported (per label) | label | eco:SurveyTarget with eco:isSurveyTargetFullyReported | Lets some labels be exhaustive and others opportunistic, which is common in practice |
| annotation-set-inventory-type | annotation set | eco:inventoryTypes (restrictedSearch, openSearch, …) | Distinguishes systematic annotation from opportunistic annotation |
| annotation-set-sampling-effort | annotation set | eco:samplingEffortValue / eco:samplingEffortUnit | e.g. the number of images examined, or annotator-hours |
| annotation-set-total-area-sampled | annotation set | eco:totalAreaSampledValue / eco:totalAreaSampledUnit | Can be summed from iFDO `image-area-square-meters` over `annotation-set-images` |
| annotation-organism-id | annotation | dwc:organismID | Links annotations of the *same individual* across overlapping images or video frames, so counts aren't inflated. Each annotation stays its own occurrence. |
| annotation-identification-type | annotation (or a fixed export value) | dwc:identificationType (example "media") | Darwin Core now records the evidence basis. For image annotation this is always `media`. |
| annotation-occurrence-status | export only | dwc:occurrenceStatus (detected / notDetected) | Detected for every annotation. With the "fully reported" flags, notDetected records can be generated for target labels absent from examined images. |

The draft's future-expansion list also maps directly to existing Darwin Core terms. Its VARS
associations (behavior, interactions, substrate) could export as:

- `dwc:behavior`;
- `dwc:substrate`;
- `dwc:associatedTaxa`;
- `dwc:OrganismInteraction` (`dwc:organismInteractionType`);
- `dwc:causeOfDeath`.

## Should we rename attributes to Darwin Core names?

**Recommendation: no, keep the iFDO-style names, but make every mapping exact.** The standard
builds on iFDO, whose kebab-case, prefixed names (`image-…`) the standard follows, and a single
annotation record spans several Darwin Core classes. Renaming to Darwin Core camelCase would
break the naming rules without making export any easier. What helps instead:

- **Every mapping names exactly one namespaced term**, or "EML", or "none". Never a class, and
  never "X or Y".
- **A rename only where our name suggests the wrong meaning:**
  - `annotation-human-creators` → `annotation-identified-by`, because they identify; they don't
    record the event;
  - possibly `label-set-objective` → `label-set-target-scope`.
- **A "Darwin Core export" section** listing the fixed values (`basisOfRecord`,
  `identificationType`, `occurrenceStatus`, `organismQuantity`/`Type`) and where each exported
  term comes from, including terms taken from the iFDO, such as `dwc:recordedBy`, location and
  depth.

## Questions to settle

1. **Can an annotation set be an `eco:Survey`?** Several sets can annotate the same images, and
   Humboldt surveys are usually defined by the sampling design.
2. **Should a review that accepts an annotation export at all?** It could export as a
   `dwc:Assertion`, or only through `dwc:identificationVerificationStatus`.
3. **Which verification vocabulary?** The HISPID/ABCD integer codes, or a new IRI vocabulary
   agreed with OBIS.
4. **Should the AphiaID be stored as an LSID?** Storing the LSID, which is what OBIS uses in
   `scientificNameID`, would make the export exact.
5. **How should annotation-level confidence be represented?** One `dwc:Assertion` per value
   could be heavy for large machine-generated sets. `dwc:dynamicProperties` (JSON) is a lighter
   alternative.
