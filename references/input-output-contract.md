# Input and output contract

## Required inputs

Obtain or discover these before production:

- Canonical comic root and inclusive chapter range.
- Authoritative source format and, when available, the official region extractor.
- Writable output directory.
- Target platform, language, frame ratio and pixel dimensions.
- Protected previous delivery path when revising an existing version.

Treat the following as optional parameters:

- Reference video, transcript or subtitles for rhythm and opening style.
- Previous script for tone comparison.
- Target duration, Han-per-minute range, preferred semantic-unit length, frame-change cadence, motion labels and output filename variants.

## Missing-input handling

1. Search the explicitly named roots before asking the user.
2. Infer chapter IDs, page order, image dimensions and extractor CLI from local metadata or `--help` when safe.
3. Use sensible defaults only for reversible presentation parameters such as contact-sheet layout.
4. Stop and request input when the authoritative comic root, chapter range or output destination cannot be established.
5. Do not substitute an older delivery, a scan preview, a reference transcript or internet summaries for a missing canonical source.
6. If no official extractor exists, preserve source pixels with a documented local crop pipeline; never upscale before extraction.

## Default delivery

Create these artifacts unless the user specifies a compatible schema:

```text
output/
├─ script.md
├─ storyboard.csv
├─ visual-sources.csv
├─ visual-semantic-validation.csv
├─ full-panel-qc.csv
├─ delivery-metrics.json
├─ selected-originals/
├─ visual-segment-previews/
├─ processed/
└─ contact-sheets/
```

Use `assets/output-template/` for headers and baseline JSON. Extra internal audit files are allowed when they support verification, but do not replace required outputs.

## Storyboard minimum fields

- `segment_id`, `order`, `chapter`, `narration`
- `source_id`, `selected_original`, `processed_image`, `preview_image`
- `crop_coordinates`, `full_frame_region`, `composition_mode`
- `motion`, `visual_subject`

Keep narration multiline inside one CSV cell. Derive `script.md` by flattening the narration cells in storyboard order.

## Variable parameters

Allow these to change per project:

- Chapter count and IDs.
- Canonical source width and image format.
- Target resolution and aspect ratio.
- Target duration, speech rate and unit-length preference.
- Ordinary and action frame-change cadence.
- Number and naming of motion labels.
- Output schema extensions.
- Whether an existing version may supply stylistic hints.

Never let parameter changes weaken the factual, provenance, completeness, semantic-match or version-protection constraints.
