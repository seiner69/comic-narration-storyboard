# Narration and visual rules

## Narration

- Use third-person, causal, continuously advancing Chinese narration.
- Start with a simple, direct contrast: formidable identity versus present humiliation, sacrifice or constraint.
- End the hook quickly and return to the first chronological scene. Do not preview later chapters to manufacture suspense.
- Express one action, result or turn per semantic unit. Treat 10–18 Han characters as a useful default, not a quota.
- After three to five concrete actions, add at most one concise judgment when it changes interpretation.
- Preserve a few decisive lines at identity reveals, danger escalations and emotional recovery points.
- Remove greetings, repeated dialogue, redundant explanation and side plots that do not change the main chain.
- Do not add motives, powers, events, relationships or outcomes absent from the canonical comic.
- Do not force a target length. Density outranks duration.

Preferred progression:

```text
person acts → result appears → opponent reacts → new obstacle arrives
```

Avoid analysis-first language such as abstract system commentary, cost theories or institutional generalization unless the comic visibly establishes it and the point is indispensable.

## Visual selection

- Show the person named by the current narration whenever available.
- For emotion, prefer face and body reaction. For action, prefer occurrence and result. For identity reveals, show the subject and other characters' reaction.
- Do not show future events before narration reaches them.
- Reject advertisements, credits, warnings, Discord promotions, signature pages and unrelated blank space.
- Reject pure text screens, large dialogue regions and isolated SFX when character, action, reaction or object evidence is available.
- Permit a dialogue box to be clipped. Dialogue completeness is not an extraction goal.

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

## Standalone semantic test

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

Keep scores 2–3. For scores 0–1, reselect, enlarge to the complete panel, inspect for boundary clipping, or rewrite the narration to visible facts.

OCR can disprove a match but cannot by itself prove a match. Dialogue or text must not occupy most of the useful clear foreground.

Run the standalone test again after dialogue and SFX bands are removed. If the art no longer supports the line, reselect the panel or rewrite the narration; do not restore the text block to make the match work.

## Repetition

- Use one exact panel no more than three times.
- Avoid three consecutive displays when another direct frame exists.
- Reuse only for a real editorial phase such as establishing, reaction and result.
- Vary scale or editor motion while retaining the full art; do not simulate variety with destructive crops.
- Reject adjacent frames with identical rendered hashes.
