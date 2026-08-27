# Objective validation

Pass all applicable checks before delivery.

## Script and mapping

- `script.md` equals the ordered, line-flattened `storyboard.csv.narration` exactly.
- Segment order is contiguous and every segment has narration and at least one source.
- Character names and relationships are consistent with the canonical source.
- No unit states an event outside the allowed chapters.

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

- Every segment passes standalone visual-semantic review.
- Current subject, action, result, reaction or key object supports the narration.
- No future event is shown early.
- No subject or action is clipped.
- No pure text, isolated SFX or dialogue-majority foreground remains when a visual alternative exists.
- Detached dialogue, narration, SFX, phone UI and decorative white bands are removed from the useful foreground even when they occupy less than half of the frame.
- OCR is not the sole evidence for a match.
- All contact sheets are manually reviewed after generation.

## Metrics

Calculate from final artifacts:

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
