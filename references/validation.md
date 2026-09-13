# Objective validation

Pass all applicable checks before delivery.

## Contract routing

For a rendered delivery, use the image/provenance checks and tools below. For an approved-panel prose revision, validate ordered narration, paragraph separation, existing approved IDs and PNG paths, allowed scope and protected hashes. Rendering, extraction and image-metric checks are not applicable when those artifacts were not requested; do not claim the full rendered-schema validator passed.

## Script and mapping

- For the legacy rendered schema, `script.md` equals the ordered, line-flattened `storyboard.csv.narration` exactly; paragraph-mode rules are below.
- Segment order is contiguous and every segment has narration and at least one source.
- Character names and relationships are consistent with the canonical source.
- No unit states an event outside the allowed chapters.
- For paragraph rows generated with `--paragraphs`, script text equals the ordered narration with the chosen paragraph separators. Do not count each paragraph as one semantic unit or each repeated panel reference as a new display.
- Read the prose without images: essential relationships, requests, responses and consequences remain understandable. Review emotional flourishes against source art/dialogue/context, not solely against an isolated image.
- Character judgments, including rhetorical questions, stay attributable; demands and contested accounts do not become established outcomes. Do not invent a cause to remove a known ambiguity.
- A repetition retained for emotional effect changes perspective, meaning or response, rather than only restating the same state. This is an editorial check, not a regex ban on repeated words.
- For a file-ordered paragraph CSV without `order`, generate with `--paragraphs --file-order`. Validate any paragraph IDs as nonempty and unique. Do not treat physical file order as an accidental fallback or the number of rows as an editing cadence.

## Provenance

- Every selected original and processed frame exists.
- Every source path in `visual-sources.csv` exists and belongs to an allowed chapter.
- Final originals come from the current canonical edition and supplied extractor when required.
- No old-edition image, coordinate, chapter or generated comic art appears.
- Protected prior-version hashes remain unchanged.

## Visual integrity

- Every processed JPG has the requested dimensions and an sRGB ICC profile.
- Every clear foreground region lies inside its selected original.
- Complete-panel compositions use the entire selected original as foreground.
- Cross-source art is extracted as one continuous original.
- Dialogue-only margins are not treated as mandatory panel content.
- One selected original contains one coherent scene; independently readable stacked scenes are split into separate shots.
- The 720×540 preview remains readable without zooming. A vertical clear foreground below 32% of canvas width is explicitly repaired or justified in QC.
- No adjacent rendered frames are byte-identical.
- Each exact complete panel is displayed no more than the configured limit, normally three.

## Semantic QC

- Every segment passes the applicable visible-action and contextual factual checks described in `narration-visual-rules.md`.
- Current subject, action, result, reaction or key object supports the narration.
- Visuals follow the telling; any time shift stays within the explicitly agreed spoiler and source scope.
- No subject or action is clipped.
- No pure text, isolated SFX or dialogue-majority foreground remains when a visual alternative exists.
- Detached dialogue, narration, SFX, phone UI and decorative white bands are removed from the useful foreground even when they occupy less than half of the frame.
- OCR is not the sole evidence for a match.
- A source speech bubble may establish an essential fact without being shown. A metaphor does not require a literal image, but must not smuggle in an event, motive or outcome.
- All contact sheets are manually reviewed after generation.

## Metrics

Calculate the requested metrics from final artifacts; do not fabricate render metrics for a prose/mapping-only contract:

- pure Han count;
- duration at each requested Han-per-minute rate;
- semantic-unit count;
- visual-segment count;
- final visual-source count;
- cross-source count;
- contact-sheet count;
- maximum exact-panel display count;
- any factual or name differences found against a protected older version.

Run:

```powershell
python scripts/audit_frame_legibility.py <output> --min-foreground-width-fraction 0.32
python scripts/validate_delivery.py <output> --width 1440 --height 1080 --chapters ch_001,ch_002,ch_003,ch_004,ch_005
```

Add `--protected-file PATH=SHA256` for each file that must not change. A passing script validates structure and pixels, not narrative meaning; retain the manual semantic pass.
