# Examples and their limits

## Fictional prose examples

[narrative-craft.md](narrative-craft.md) uses an independently invented lighthouse scene to illustrate emphasis without inventing facts. The builder tests use small in-memory CSV examples, including quoted speech, multiline paragraphs, physical row order and protected inputs.

These examples do not contain production scripts, private acceptance records or copyrighted story excerpts. They establish neither audience performance nor a mandatory voice, word count, opening or number of images.

When a user supplies an approved draft in their own project, preserve that approval's scope. Focused feedback can retain its structure; a fresh rewrite can return to the authoritative source. A project preference does not become a general rule for other stories.

## Synthetic rendering fixture

The fixture in `assets/gold-standard/` is fictional and deliberately short. It demonstrates a rendered-delivery contract, not reusable plot content.

1. Map narration to complete schematic panels.
2. Keep `script.md` derived from storyboard narration.
3. Include native originals, 4:3 processed frames, previews, contact sheets and metrics.
4. Verify source paths, allowed chapters, geometry and final-size legibility.

Its one-panel-per-row layout and short action sequence are not requirements for prose paragraphs. Dialogue may supply essential facts in real work even when bubbles are not displayed.

```bash
python scripts/validate_delivery.py assets/gold-standard --width 1440 --height 1080 --chapters ch_001
python scripts/test_build_script_from_storyboard.py
```

Builder tests use temporary outputs and verify that inputs remain unchanged. They check deterministic bytes and invalid-input handling, not narrative taste. Rendering tests do not certify factual or emotional interpretation.

Do not copy fixture names, events or wording into another story or promote unreviewed prose to an accepted example.
