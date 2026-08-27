---
name: comic-narration-storyboard
description: Create or revise synchronized Chinese comic narration and visual storyboards from sequential comic chapters, including source-grounded narration units, full-panel or cross-source extraction, still-frame composition, visual-semantic QC, mapping files, contact sheets, and deterministic delivery validation. Use when a user asks for end-to-end comic recap or explainer scripting plus matching visual assets, or asks to repair an existing delivery for hook rhythm, scene-to-script mismatch, clipped panels, text-heavy frames, or repeated visuals. Do not use for prose-only rewriting, OCR-only extraction, single-image cropping, AI comic generation, voice, subtitle or video production, or tasks without an authoritative comic source.
---

# Comic Narration Storyboard

Produce the narration and its supporting comic frame as one synchronized unit. Treat the authoritative comic as the only source of plot facts; treat references and older deliveries only as style or workflow evidence.

## Load the right references

- Read [references/input-output-contract.md](references/input-output-contract.md) before preflight or delivery setup.
- Read [references/narration-visual-rules.md](references/narration-visual-rules.md) before writing or selecting frames.
- Read [references/failure-prevention.md](references/failure-prevention.md) when revising an existing delivery or after any user correction.
- Read [references/validation.md](references/validation.md) before the final pass.
- Read [references/gold-standard.md](references/gold-standard.md) when examples are needed.
- Read [references/test-cases.md](references/test-cases.md) only when testing or changing this Skill.

## Execute the workflow

1. Lock the factual boundary.
   - Record the canonical chapter root, inclusive chapter range, extractor, output path, protected older version, target frame, target duration, and optional style references.
   - Inspect the canonical source and extractor before writing.
   - Refuse to infer events from references or older versions.
   - Never read outside the requested chapter range.

2. Inventory the source.
   - Read chapters in order.
   - Identify story beats, character names, relationships, action order, panel boundaries, source-file boundaries, warning or credit pages, and text-only regions.
   - Build review views that include the current candidate plus all nearby art above and below it. Do not audit selected crops in isolation.

3. Draft and select synchronously.
   - Work in short narration units, not a completed full script.
   - For every unit, immediately write the narration, identify visible evidence, choose the official source region, decide whether cross-source extraction is required, render the visual, and save the mapping.
   - If no frame supports a sentence, rewrite the sentence or choose a better frame. Never fill with merely adjacent or attractive art.

4. Shape the narration.
   - Open with the strongest direct identity contrast or emotional cost, then return immediately to the story start.
   - Sustain the chain: action, result, reaction, new obstacle.
   - Prefer concrete verbs and short semantic units. Keep analysis and explanation subordinate to visible events.
   - Learn cadence from references without copying language, facts, names, coordinates, or scene order.
   - Do not pad to a requested duration. Report the duration implied by the final Han count.

5. Extract complete visual evidence.
   - Use scans only for reading and positioning when an official extractor is supplied.
   - Generate final originals through the supplied extractor at native width.
   - Identify scene and panel boundaries before expanding a crop. Treat two independently readable locations, moments, or compositions as two shots even when they are vertically adjacent.
   - Expand to the complete person, action, result, object, or single composed panel when art continues above or below the initial region.
   - Merge consecutive source files when one person, action, object, or composition crosses a boundary.
   - Crop to the shortest region that still preserves the narrated person, action, result, object, or one coherent composition. Never compress a multi-panel sequence into one narrow foreground strip.
   - Exclude detached dialogue, narration, phone UI, SFX, and decorative white bands from art boundaries. Do not repair or preserve text merely because it is clipped.
   - Use a centered clear foreground over a same-source blurred background only after scene splitting and text-band removal. If the named subject or action is still too small in the final preview, shorten the crop, split the shot, or select another panel.

6. Perform standalone semantic review.
   - Judge who is visible, what happens, what result appears, how others react, which object matters, where the scene occurs, and whether the frame appears in the correct story order.
   - Use OCR only as secondary evidence. A frame must not depend on dialogue text to justify the match.
   - Replace or expand any weak match, clipped subject, incomplete action, text-majority screen, pure SFX crop, or unsupported inference.
   - Review the rendered preview at delivery size without zooming. Reject a technically complete frame when its clear foreground is too narrow for the named subject and current action to be read immediately.
   - Limit one exact complete panel to at most three displays. Avoid consecutive reuse unless distinct framing or editor motion has a real narrative purpose.

7. Regenerate derived artifacts.
   - Generate `script.md` only from storyboard narration with `scripts/build_script_from_storyboard.py`.
   - Rebuild previews, processed frames, contact sheets, source lists, QC rows, and metrics after every mapping change.
   - Keep superseded assets recoverable outside the final inventory. Do not overwrite a protected prior version.

8. Validate and stop.
   - Run `scripts/validate_delivery.py` against the final output.
   - Inspect all contact sheets after automated validation; automation cannot certify narrative meaning.
   - Stop after the requested script, still images, mappings, QC artifacts, and metrics exist. Do not create voice, subtitles, timelines, or video unless separately requested.

## Use deterministic resources

- Run `scripts/init_delivery.py` to scaffold a delivery from `assets/output-template/`.
- Run `scripts/build_script_from_storyboard.py STORYBOARD SCRIPT` after narration changes.
- Run `scripts/build_contact_sheets.py OUTPUT` after preview or mapping changes.
- Run `scripts/audit_frame_legibility.py OUTPUT` before manual contact-sheet review to flag overlong foreground strips and text-heavy candidates.
- Run `scripts/validate_delivery.py OUTPUT` for objective checks. Pass target dimensions, allowed chapters, and protected-file hashes as needed.

The bundled gold-standard fixture under `assets/gold-standard/` demonstrates structure only. Never reuse its fictional facts in a real episode.
