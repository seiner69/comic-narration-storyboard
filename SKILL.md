---
name: comic-narration-storyboard
description: Write or revise source-grounded Chinese comic narration as coherent, emotionally engaging conflict passages, with many-to-many approved-panel mapping and optional still-image production. Use with authoritative comic art and dialogue, including focused revisions to an approved draft. Do not use for standalone reference-video analysis, OCR-only translation, panel-library building, unrelated prose, or voice/video production.
---

# Comic Narration Storyboard

Tell an independently understandable story and keep its visual presentation synchronized. A narration sentence, a prose paragraph, a visual segment and a source panel are different units; never force a one-to-one relationship. The authoritative comic, including its dialogue, supplies facts. References supply writing choices, not facts or permission to invent them.

Write for the listener's experience, not as a report explaining the story's logic. Let pressure, choices, dialogue and reactions carry emotion; use narration where it supplies needed understanding or a meaningful change of perspective. Neither emotion nor causality substitutes for the other.

## Load the right references

- Read [references/input-output-contract.md](references/input-output-contract.md) before preflight or delivery setup.
- Read [references/narration-visual-rules.md](references/narration-visual-rules.md) before writing or selecting frames.
- Read [references/narrative-craft.md](references/narrative-craft.md) when writing, rewriting, or transferring a reference style. It governs narrative freedom, emotional emphasis and their factual boundary.
- Read [references/failure-prevention.md](references/failure-prevention.md) when revising an existing delivery or after any user correction.
- Read [references/validation.md](references/validation.md) before the final pass.
- Read [references/gold-standard.md](references/gold-standard.md) when examples are needed. It distinguishes synthetic prose tests from the rendering fixture; neither defines a mandatory writing style.
- Read [references/test-cases.md](references/test-cases.md) only when testing or changing this Skill.

## Choose the requested workflow

- **Fresh rewrite:** when asked to re-read/rebuild from the comic, re-read the complete in-scope conflict before composing. Old prose is not a fact source or a mandatory outline; do not perform synonym substitution on the last draft.
- **Focused revision of an accepted draft:** when revision is requested, retain the accepted structure and effective passages, recheck source evidence relevant to the proposed changes, and repair the identified problems. Do not restart a full rewrite or render pipeline merely because a revision is requested. A user-requested fresh rewrite takes precedence.
- **Scene/narrative revision (default for story writing):** read the complete in-scope conflict and dialogue; understand relationships, pressures and consequences; draft natural paragraphs; then arrange visuals around action, reaction and information changes. Work by a coherent scene or the requested short test passage, not by individual sentences.
- **Explicit visual-first test:** if requested, follow beats → source selection → final rendering → preview inspection → narration. Even here, preserve necessary dialogue-grounded context and allow multiple sentences per visual; do not reduce narration to captions describing a picture.
- **Approved-panel-only delivery:** inspect approved art and corresponding source dialogue, preserve IDs, boundaries and PNGs, and provide mapping/presentation advice only. Do not call an extractor, generate frames, or require render metrics that the user did not request.
- **New visual production:** apply the extraction and final-size review gates below. A full-chapter source read is for comprehension, not an obligation to draft a full script before mapping. Follow a user-specified production order over these defaults.

## Execute and verify

1. Lock scope and inputs.
   - Record the authoritative edition or reviewed library, allowed chapters and scene endpoint, output, protected versions and requested artifacts. Record resolution/extractor only when making images.
   - Read source art and dialogue in context. Confirm names, relationships, requests versus outcomes, and uncertain pronouns. Do not fill gaps from old scripts, references or later chapters.
   - Keep statements, beliefs and narrator-established facts distinct. Explicitly attribute a character's sweeping judgment, including rhetorical questions; retain uncertainty when the source cannot establish who started a conflict or what decision was reached.
   - Hash protected inputs. Preserve an explicitly approved opening unless the user authorizes changes or a factual error is found.

2. Understand before composing.
   - Establish who wants what, what pressure or misunderstanding obstructs them, and how responses change the situation. Keep unresolved facts separate from the prose.
   - At an emotional turn, identify the source-supported expectation, perception or relationship at stake. Do not manufacture one to fit a reference.
   - When using a reference, inspect the specified excerpt and explain the actual choice being transferred. Respect one-excerpt iterations; do not turn every task into a multi-video study.

3. Write with selective emphasis.
   - Action → result → reaction → obstacle is a continuity diagnostic, not a sentence template or a compulsory order for every paragraph.
   - Allow contrast, psychological paraphrase, figurative language, suspense, callbacks, dialogue, summary and scene expansion where they serve this story. Leave ordinary transitions plain; let pivotal words or reactions land.
   - Do not impose fixed sentence lengths, action-to-commentary ratios, reversals per line, or a compulsory identity hook. Respect the chosen viewpoint, spoiler limit and any approved baseline.
   - Keep essential causal/relationship information even when it cannot be proven by one isolated image. Do not pad for duration.
   - After an effective action or line, remove a following summary if it adds no understanding, expectation or emotional change. Preserve repetition that changes meaning, such as contrasting an earlier plea with a later inability to answer; do not erase all lingering reactions in the name of speed.
   - Preserve source-supported unflattering grievances. Do not turn material resentment into pure concern, add vindication for the focal character, or force a hero/villain judgment to simplify the conflict.

4. Map the coherent passage.
   - One panel may carry several sentences; a paragraph may need several panels. A paragraph boundary alone is not a cut.
   - Show the actual actor/action/result for concrete claims; use the correct speaker, listener or reaction for dialogue and emotional interpretation. Record source-text evidence separately from displayed imagery.
   - Read narration without images, then review it with the ordered art. Repair mismatches without deleting information merely because it appears in a speech bubble.

5. Extract complete visual evidence, only when requested.
   - Use scans only for reading and positioning when an official extractor is supplied.
   - Generate final originals through the supplied extractor at native width.
   - Identify scene and panel boundaries before expanding a crop. Treat two independently readable locations, moments, or compositions as two shots even when they are vertically adjacent.
   - Expand to the complete person, action, result, object, or single composed panel when art continues above or below the initial region.
   - Merge consecutive source files when one person, action, object, or composition crosses a boundary.
   - Crop to the shortest region that still preserves the narrated person, action, result, object, or one coherent composition. Never compress a multi-panel sequence into one narrow foreground strip.
   - Exclude detached dialogue, narration, phone UI, SFX, and decorative white bands from art boundaries. Do not repair or preserve text merely because it is clipped.
   - Use a centered clear foreground over a same-source blurred background only after scene splitting and text-band removal. If the named subject or action is still too small in the final preview, shorten the crop, split the shot, or select another panel.

6. Perform visual review appropriate to the deliverable.
   - Judge who is visible, what happens, what result appears, how others react, which object matters, where the scene occurs, and whether the frame appears in the correct story order.
   - Do not use OCR or on-screen text to pass an absent literal action. Dialogue remains authoritative evidence for facts, relationships and motives; it need not be visible in the final frame.
   - Replace or expand any weak match, clipped subject, incomplete action, text-majority screen, pure SFX crop, or unsupported inference.
   - For new images, inspect source context above/below and the final preview without zooming; reject an unreadable foreground. For approved-only mappings, inspect the approved art without altering it; flag a real boundary problem for the user.
   - Limit one exact complete panel to the agreed display cap, normally three. A continuous hold across sentences/paragraphs is one display, not a new shot per CSV reference.

7. Regenerate derived artifacts.
   - Finalize narration in the storyboard, then generate `script.md` with `scripts/build_script_from_storyboard.py`; use `--paragraphs` for prose-paragraph rows. For an explicitly file-ordered CSV without an `order` column, also pass `--file-order`. Drafting prose first does not mean maintaining two final versions.
   - Rebuild all affected derived artifacts that belong to the requested contract. Do not create new image deliverables for a mapping-only revision.
   - Keep superseded assets recoverable outside the final inventory. Do not overwrite a protected prior version.

8. Validate and stop.
   - Use the full delivery validator for its supported rendered schema; for a custom approved-panel schema, check text equality, order, approved status, scope, existing paths and protected hashes. Do not claim a schema-incompatible validator passed.
   - Inspect all delivered contact sheets or all ordered mapped panels. Automation cannot certify story meaning, emotion, or popularity.
   - Stop after the requested script, still images, mappings, QC artifacts, and metrics exist. Do not create voice, subtitles, timelines, or video unless separately requested.

## Use deterministic resources

- For rendered deliveries, use `scripts/init_delivery.py`, `scripts/build_contact_sheets.py`, `scripts/audit_frame_legibility.py` and `scripts/validate_delivery.py` with the matching schema and project dimensions.
- For either mode, use `scripts/build_script_from_storyboard.py STORYBOARD SCRIPT [--paragraphs] [--file-order]` after narration changes. Never target a protected accepted script during a test.
- Run `scripts/test_build_script_from_storyboard.py` when changing the builder.

The synthetic `assets/gold-standard/` demonstrates rendering structure only. Prose examples and builder tests use fictional scenarios; no project acceptance records or production scripts are bundled. Examples supply neither facts nor mandatory wording, length or shot counts for another task.
