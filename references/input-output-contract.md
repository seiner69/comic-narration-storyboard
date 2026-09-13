# Input and output contract

## Required inputs

Obtain or discover these before production:

- Canonical comic root and inclusive chapter range.
- Authoritative source format or reviewed library plus its approval state and corresponding dialogue/source context.
- Writable output directory.
- Language and requested artifact contract; platform, frame ratio and pixel dimensions only when producing images.
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
7. In approved-panel-only mode, use the approved PNGs; an extractor is not required and may not be used to alter approved boundaries without authorization.

## Paragraph / approved-panel revision

When the user requests prose and mapping without new images, deliver only the requested files, commonly `script.md`, `storyboard.csv` and a brief `comparison.md` or `notes.md`. Do not scaffold the rendered-delivery template, render images or require its metrics.

Useful fields are `paragraph_id`, `order`, `chapter`, `narration`, `panel_ids_in_order`, `presentation`, `panel_pngs_in_order`, with optional `text_evidence_ids` and factual notes. Record the ordered panels and where narration changes the framing or hold. Multiple sentences can share a panel, and one paragraph can use several panels.

Finalize narration cells after prose composition, then generate the final script with `build_script_from_storyboard.py STORYBOARD SCRIPT --paragraphs`. If an existing approved schema uses physical CSV order and has no `order` column, explicitly add `--file-order`; preserve any `paragraph_id` and validate that IDs are present and unique. Do not silently sort those IDs or guess a missing order. The builder rejects conflicting order modes. This preserves paragraph separation without maintaining an independently rewritten script. Count semantic units separately if asked; CSV rows are not automatically sentences or visual cuts.

The builder emits UTF-8 with LF line endings and one final newline on every platform. It does not modify the input CSV or an accepted example during tests.

For focused feedback, change only what the feedback warrants and synchronize affected mapping/presentation notes. A reduced paragraph does not need its former number of panels. Preserve the accepted draft separately; distinguish a provisional user preference from a fully validated universal standard.

## Rendered delivery

For new visual production, create these artifacts unless the user specifies another contract:

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

Keep narration multiline inside one CSV cell. A visual segment may contain multiple semantic units. Derive `script.md` from narration cells in storyboard order, without duplicating a whole paragraph across rows just to map extra panels.

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
- Writing viewpoint, narrative order within the spoiler contract, emotional register and optional literary techniques.
- Scene-first versus explicit visual-first workflow; approved-only mapping versus new rendering.

Never let parameter changes weaken the factual, provenance, completeness, semantic-match or version-protection constraints.
