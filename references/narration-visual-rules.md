# Narration and visual rules

## Narration

- Use the requested viewpoint and natural, understandable Chinese prose. Read [narrative-craft.md](narrative-craft.md) for composition and emotional emphasis.
- Choose a fitting opening rather than requiring every story to start with an identity contrast. Keep any approved baseline and spoiler/time-order constraints.
- Write coherent conflict paragraphs; sentence length, commentary frequency and cutting rhythm are not fixed quotas.
- Allow source-grounded psychological narration, contrast, metaphor, selective repetition, summary and lingering reactions. Do not make every line ornate or give every line a reversal.
- Preserve dialogue that changes a relationship or decision. Remove redundant restatement, but retain background needed to understand the characters' actions.
- Do not add motives, powers, events, relationships or outcomes absent from the canonical comic.
- Do not force a target length. Density outranks duration.

Continuity check, not a prose template:

```text
person acts → result appears → opponent reacts → new obstacle arrives
```

Do not let abstract system commentary replace the characters' experience. Explanation is useful when it supplies an indispensable cause or relationship; a lack of single-frame proof is not a reason to delete dialogue-grounded context.

## Visual selection

- Show the person named by the current narration whenever available.
- For emotion, prefer face and body reaction. For action, prefer occurrence and result. For identity reveals, show the subject and other characters' reaction.
- Visual order must follow the current telling. Use a flashforward or flashback only within the agreed narrative/spoiler scope, and signal the shift clearly.
- Reject advertisements, credits, warnings, Discord promotions, signature pages and unrelated blank space.
- Reject pure text screens, large dialogue regions and isolated SFX when character, action, reaction or object evidence is available.
- Permit a dialogue box to be clipped. Dialogue completeness is not an extraction goal.
- In approved-panel-only mode, keep approved boundaries and PNGs unchanged. Write framing/hold advice, and flag an unsuitable boundary rather than silently repairing it.

## Complete-panel rule

Inspect the current candidate together with all art immediately above and below it.

First identify whether the candidate contains one coherent scene or several independently readable scenes. A new location, time, camera setup, bordered panel, reaction panel, or action phase may define a new scene. If two scenes are present, split them into separate shots and, when necessary, split the narration mapping. Do not preserve a continuous webtoon strip merely because every pixel is chronologically adjacent.

Expand the region when any of these continues outside the candidate:

- head, torso, limbs or another essential character;
- weapon, vehicle, phone, rope or other decisive object;
- attack wind-up, contact, trajectory or result;
- reaction that completes the composition;
- a designed vertical or horizontal single panel.

Do not expand only to include a detached speech bubble, narration gutter, SFX field, phone UI, or decorative blank area. Remove those bands from the selected original whenever the narrated art remains complete. A bubble may be clipped or omitted. If one coherent composition crosses consecutive source files, extract it as one cross-source original.

After scene splitting and text-band removal, crop to the shortest self-contained art region that preserves the narrated subject, action, result, or key object. Then, if that single scene is still too tall or wide for the output ratio, keep the remaining source art visible in the clear foreground and fill the canvas with a blurred, darkened version of the same source. Never generate missing comic pixels.

## Final-size legibility gate

- Inspect the actual 720×540 preview without zooming.
- The named subject, current action, and decisive object must be immediately readable.
- For a vertical clear foreground centered on a 4:3 canvas, treat a foreground width below 32% of the canvas as a mandatory review flag, not as an automatic pass.
- When the flag fires, shorten the crop, split independent scenes, or select another panel. A blurred background does not cure an unreadably narrow foreground.
- Keep an exception only for a deliberate single-scene scale reveal whose subject remains obvious at preview size; record the reason in QC.

## Standalone visual test and contextual factual test

An isolated frame tests visible subjects and actions, not whether every sentence of a story is a literal image description. Verify relationships, motives, past context and spoken threats with the official dialogue/context separately. Do not delete that information when cropping away bubbles. Figurative emotional language can be supported by the correct character state and established conflict rather than a literal image of the metaphor.

Evaluate a frame without relying on adjacent narration. Score each applicable item:

- subject identity is visually plausible;
- current action is visible;
- action result is visible;
- reaction or emotion is visible;
- key object or location is visible;
- chronology matches the current unit;
- OCR, when present, does not contradict the narration.

Use this decision scale:

- `3 direct`: the central action, result or reaction is visible.
- `2 supporting`: the correct person and state are visible, though the exact action is implied.
- `1 weak`: only location, text or adjacency supports the line.
- `0 mismatch`: wrong person, event, order or unsupported claim.

For a concrete key action/result, require direct visual evidence; a merely plausible face is insufficient. For dialogue, background or emotional interpretation, a correct speaker/listener/state can be supporting evidence when the factual source and reason are recorded. For a weak or wrong visual, reselect, inspect clipping, or correct the actual mismatch; do not mechanically rewrite all narration into visible actions.

OCR cannot by itself prove a visible action. An apparent OCR contradiction requires checking the original and speaker attribution, not automatic rejection. Dialogue or text must not occupy most of a newly rendered useful clear foreground.

Run the visual test again after text-band removal when rendering. Reselect a relevant speaker, listener, reaction or action if needed; do not restore a large text block to prove visual support, or discard the underlying dialogue as a fact source.

## Repetition

- Use one exact panel no more than three times.
- Avoid three consecutive displays when another direct frame exists.
- Reuse only for a real editorial phase such as establishing, reaction and result.
- Vary scale or editor motion while retaining the full art; do not simulate variety with destructive crops.
- Reject adjacent frames with identical rendered hashes.
- Count displays, not narration clauses or repeated CSV references: a continuous hold across paragraphs is one display. A callback in the prose does not require a visual replay.
