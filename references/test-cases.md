# Test cases

These are fictional behavior scenarios for an editorial review, not automated model-evaluation results. Never use a real production draft as a public fixture.

## Normal rendered delivery: should trigger

Request: 使用指定漫画第 1—5 章，生成中文解说、4:3 静帧、分镜映射、接触表和验收清单。参考视频只用于节奏。

Expected behavior: lock source scope and extractor; understand complete conflicts before composing and mapping; do not force one sentence per panel; generate only the requested artifacts and report honest duration.

## Visual repair: should trigger

Request: 现有分镜有跨三张切片的长动作画格、手机聊天页和同一人物连续出现四次。保持完整动作，重新制作 1440×1080 画面并验收。

Expected behavior: inspect source context; split independently readable scenes before extraction; remove detached text bands; preserve complete source art across file boundaries; inspect readability after composition; reduce unjustified reuse and regenerate derived outputs.

## Approved-panel prose revision: should trigger

Request: 已有审核通过的灯塔画格和对白，只修订停电后启用备用灯的段落。写成自然段，保留紧张感，不改 PNG，交付正文和画格映射。

Fictional evidence: the main lamp fails; the keeper places a working backup lamp in the window; the apprentice asks whether it is bright enough. No source establishes that a ship received the signal or that the outage was deliberate.

Expected behavior:

- Preserve approved IDs, boundaries and image bytes; no new rendering, extraction, audio or video.
- Keep the question as uncertainty; do not announce rescue success or sabotage.
- Use contrast between darkness and the small light without inventing a result.
- Allow multiple sentences per panel and multiple panels per paragraph; a paragraph break need not be a cut.
- Derive final script from the mapping, with unresolved facts outside narration.

## Focused feedback: should trigger

Request: 保留已确认段落的结构，只删去重复三次的“灯很暗”，明确亮度担忧是学徒的看法。不改原画。

Expected behavior: perform a targeted revision, not a new source-research or render project. Attribute the concern using established evidence rather than invented speech. Keep a later mention of brightness only if a changed situation gives it new meaning. Update affected mappings and remove obsolete replays.

## Fresh rewrite and an unknown cause: should trigger

Request: 重读当前范围再写，不沿用旧稿。停电原因并不明确；对白中学徒承认担心被扣报酬，别把这个理由改成无私奉献。

Expected behavior: reread the source, distinguish a stated material concern from an invented flattering motive, explain known requests and responses without inventing an outage cause. Note uncertainty outside the prose; do not stop useful writing merely because one fact is unresolved.

## Explicit visual-first order: should trigger

Request: 先排叙事节点、选图并验收静帧，再写这一小段的解说。

Expected behavior: honor the requested order, retain dialogue-grounded context and allow multiple sentences per visual. Do not substitute the default prose-first workflow.

## OCR-only and reference-only analysis: should not trigger

- 只翻译这一张截图的对白，不写旁白或分镜。
- 只分析几篇视频稿的信息安排，不修改漫画稿或生成画面。

Use the requested translation or analysis workflow. These requests do not authorize comic production, unrelated source inspection or Skill edits.

## Deterministic script regressions

Run `python scripts/test_build_script_from_storyboard.py`:

- Sort numbered rows and require contiguous order starting at 1.
- Use physical CSV order only with explicit `--file-order` and no conflicting `order` column.
- Validate optional paragraph IDs as nonempty and unique; do not sort them.
- Preserve quotations and internal lines, separate paragraph cells with one blank line.
- Normalize CR, CRLF and LF to UTF-8/LF output with one final newline.
- Reject empty narration and invalid schemas before modifying an output.
- Reproduce fictional paragraph text without changing source CSV or a protected prior script.

These checks do not validate creative quality, factual accuracy or audience response.
