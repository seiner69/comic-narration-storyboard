# Gold-standard example

The fixture in `assets/gold-standard/` is fictional and deliberately short. It is drawn entirely by `scripts/create_gold_standard_fixture.py`, contains no third-party comic art, and demonstrates the contract rather than reusable story content.

Gold-standard behavior:

1. Open with an identity-versus-present-cost contrast in two short units.
2. Move immediately to the visible reason for the humiliation.
3. Continue with an action, its result, an opponent response and a new obstacle.
4. Map each narration segment to a different complete schematic panel.
5. Keep `script.md` derived from storyboard narration.
6. Mark dialogue as unnecessary for visual matching.
7. Include native originals, 4:3 processed frames, previews, contact sheets and metrics.

The sample must pass:

```powershell
python scripts/validate_delivery.py assets/gold-standard --width 1440 --height 1080 --chapters ch_001
```

Do not copy its character names, events or wording into a real project.
