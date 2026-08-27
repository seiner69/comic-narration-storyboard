# Test cases

## Normal case: should trigger

Prompt:

> 使用官方漫画第1—5章，生成约20分钟的中文动作型解说，同时提取4:3静态画面、分镜映射、接触表和验收清单。参考视频只学习节奏。

Expected behavior:

- Trigger the Skill.
- Lock the five-chapter boundary and official extractor.
- Produce narration and visuals per unit rather than sequentially by artifact type.
- Re-extract current-edition originals, generate mappings and validate all outputs.
- Report honest duration even if below target.

## Boundary case: should trigger

Prompt:

> 现有分镜里有跨三张JPG的竖长动作画格、手机聊天页和同一人物连续出现四次。保持完整动作，改成1440×1080并重新验收。

Expected behavior:

- Trigger as a repair workflow.
- Inspect all art above and below every candidate.
- Separate independently readable scenes before extraction; never compress several panels into one foreground strip.
- Remove dialogue and SFX bands, then cross-source extract only the shortest complete narrated scene.
- Use same-source blurred background only when that remaining single scene stays readable at preview size.
- Replace the text-majority phone screen with action or reaction evidence.
- Reduce exact-panel use to three or fewer and rebuild derived artifacts.

## Non-trigger case

Prompt:

> 对这一张漫画截图做OCR，把英文对白翻译成中文，不需要脚本、分镜或图片处理。

Expected behavior:

- Do not trigger this Skill.
- Use an OCR or translation workflow instead.
