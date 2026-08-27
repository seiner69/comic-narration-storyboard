# Comic Narration Storyboard

A Codex skill and Python toolkit for producing synchronized Chinese comic narration, source-grounded visual mappings, processed still frames, contact sheets, and objective delivery validation.

The central rule is simple: narration and visual evidence are built together. If a sentence is not supported by the authoritative comic frame, the sentence or the frame must change.

## Highlights

- Source-bounded narration with explicit chapter limits
- One narration unit mapped to one reviewable visual source
- Full-panel and cross-source extraction rules
- Dialogue/SFX/text-band removal without inventing comic pixels
- Final-size foreground legibility audit
- Contact-sheet generation for manual semantic review
- Structural, provenance, image-profile, dimension, repetition, and metric validation
- Reproducible fictional gold-standard fixture generated entirely with Pillow

## Requirements

- Python 3.10 or newer
- Pillow with ImageCms support

```bash
python -m pip install -r requirements.txt
```

## Use as a Codex skill

Clone or copy this repository into your personal Codex skills directory under the name `comic-narration-storyboard`, then invoke:

```text
$comic-narration-storyboard
```

Read `SKILL.md` for the complete agent workflow. The skill requires an authoritative comic source; references and older deliveries may guide style but must not supply plot facts.

## Scaffold a delivery

```bash
python scripts/init_delivery.py ./work/episode-001
```

The scaffold contains the required CSV/Markdown/JSON files and directories. Existing template files are never overwritten silently.

## Rebuild derived artifacts

```bash
python scripts/build_script_from_storyboard.py \
  ./work/episode-001/storyboard.csv \
  ./work/episode-001/script.md

python scripts/build_contact_sheets.py ./work/episode-001
```

## Audit and validate

```bash
python scripts/audit_frame_legibility.py \
  ./work/episode-001 \
  --min-foreground-width-fraction 0.32

python scripts/validate_delivery.py \
  ./work/episode-001 \
  --width 1440 \
  --height 1080 \
  --chapters ch_001,ch_002
```

A passing validator confirms structure and pixels, not narrative meaning. Contact sheets still require human semantic review.

## Rebuild the fictional fixture

```bash
python scripts/create_gold_standard_fixture.py \
  --output ./work/gold-standard
```

The fixture contains only schematic shapes drawn by the script. It does not contain third-party comic artwork. The ICC profile timestamp is frozen so identical runs produce byte-identical artifact trees.

## Test

```bash
python -m unittest -v tests.test_end_to_end
```

The test generates the fixture twice, compares every file hash, runs delivery validation, and checks the final-size legibility audit.

## Repository structure

```text
agents/       Codex skill metadata
assets/       Empty delivery template and fictional gold standard
references/   Narration, visual, provenance, and validation rules
scripts/      Scaffold, build, audit, validation, and fixture tools
tests/        Deterministic end-to-end test
SKILL.md      Codex skill instructions
```

## Known limits

- Narrative truth and visual-semantic fit cannot be certified by automation alone.
- OCR is only secondary evidence and is not included in this repository.
- Final originals still depend on the user's authorized comic source and extraction pipeline.
- Processed-frame generation can consume substantial memory for very tall source art.

## Provenance

Created from a Codex-assisted workflow on 2026-08-19 and prepared as a clean public snapshot on 2026-08-27. Authoritative comic inputs, private delivery files, machine-specific paths, and conversation history are not included.

## License

No open-source license has been granted for this repository yet. The absence of a license means normal copyright restrictions apply.
