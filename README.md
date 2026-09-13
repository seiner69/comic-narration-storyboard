# 漫画解说与视觉分镜

这是一个 Codex Skill 与 Python 工具集：依据权威漫画原画和对白撰写中文解说，支持自然段与审核画格的多对多映射，并可按需生成静帧、接触表和交付验证。

事实依据与画面呈现需要分别检查：对白可以提供必要背景，即使它不显示在成片画面中；具体动作仍应使用正确的行动者、动作或结果画格。段落、句子、镜头和原作画格不是同一种单位。

## 主要能力

- 先理解完整冲突，再组织连贯、有情绪变化的自然段；不强制每句配一图。
- 区分全新重写、已确认稿的局部修订、明确要求的先图后文流程。
- 只需文案和映射时保留审核 PNG、边界与 ID，不额外运行提取或渲染。
- 从最终 CSV 生成脚本，支持数字顺序、显式文件顺序和自然段模式。
- 新制图时检查完整画格、跨源提取、文字带、最终尺寸下的可读性。
- 使用完全虚构的示意夹具验证渲染结构，使用合成 CSV 验证文字生成。

## 前置条件与安装

- Python 3.10+。
- 仅运行脚本生成器时只使用 Python 标准库。
- 图片构建、审计和端到端测试需要支持 `ImageCms` 的 Pillow 12.3.0 或更新的 12.x 版本。

```bash
python -m pip install --upgrade -r requirements.txt
```

已有环境也应升级依赖。版本下限排除了已披露的相关越界写入问题，参见 [ImageCms 安全公告](https://github.com/advisories/GHSA-9hw9-ch79-4vh6)与[裁切安全公告](https://github.com/advisories/GHSA-6r8x-57c9-28j4)。这不表示本工具已证实存在可利用路径；处理外部图片前仍需更新依赖并限制输入规模。Pillow 13 尚未验证。

作为 Skill 使用时，将仓库放到个人 Skill 目录下的 `comic-narration-storyboard` 文件夹，再调用：

```text
$comic-narration-storyboard
```

参见 [SKILL.md](SKILL.md)。漫画原画与对白须由使用者提供并具有使用权；旧稿和参考视频不能取代事实来源。本仓库不提供漫画内容。

## 生成自然段正文

有 `order` 列的 CSV 按整数排序，顺序必须从 1 开始连续，每行 `narration` 非空：

```csv
order,narration
1,灯塔失去了主电源。
2,“备用灯还亮着。”守灯人说。
```

```bash
python scripts/build_script_from_storyboard.py ./work/storyboard.csv ./work/script.md --paragraphs
```

如果 CSV 明确按文件行顺序组织，且没有 `order` 列，则显式使用：

```bash
python scripts/build_script_from_storyboard.py ./work/storyboard.csv ./work/script.md --paragraphs --file-order
```

`paragraph_id` 可选；存在时必须非空且唯一，工具不会按 ID 排序。有 `order` 列时不能使用 `--file-order`。其他映射字段可保留，但生成器只负责文字与顺序，不验证画格 ID、图片路径或审批状态。

自然段模式保留单元格内部换行，在单元格之间加一个空行；CR、CRLF 和 LF 均归一为 UTF-8/LF，文件末尾保留一个换行。省略 `--paragraphs` 时沿用逐行拼接、去除空行的旧行为。控制台的行数不是语义单元数或镜头数。

**输出路径会被覆盖。请使用新的输出路径，不要指向输入 CSV 或受保护的旧稿。** 工具不会自动修改旁白措辞，也不会生成配音、字幕或视频。

## 新制图交付

只有需要制作图片时才初始化完整交付目录：

```bash
python scripts/init_delivery.py ./work/episode-001
python scripts/build_script_from_storyboard.py ./work/episode-001/storyboard.csv ./work/episode-001/script.md
python scripts/build_contact_sheets.py ./work/episode-001
python scripts/audit_frame_legibility.py ./work/episode-001 --min-foreground-width-fraction 0.32
python scripts/validate_delivery.py ./work/episode-001 --width 1440 --height 1080 --chapters ch_001,ch_002
```

初始化不会静默覆盖已有模板。完整验证器针对渲染交付 schema；自定义“自然段＋审核画格”CSV 应检查实际字段、文字一致性、图像与来源范围、受保护文件哈希，不能声称它通过了不兼容的渲染验证器。结构或像素检查通过也不代表叙事语义正确。

## 验证方式

```bash
python scripts/test_build_script_from_storyboard.py
python -m unittest -v tests.test_end_to_end
python scripts/create_gold_standard_fixture.py --output ./work/gold-standard
```

第一项检查排序、显式文件顺序、段落、换行、异常输入与输入保护。端到端测试连续构建两次虚构夹具，比对文件哈希，并检查交付结构和可读性。图片为代码绘制的示意形状，不含第三方漫画；ICC 时间戳已冻结。

[行为场景](references/test-cases.md)供人工审核 Skill 的范围与编辑判断，不是已经执行的独立模型行为测试。自动测试不能认证文案的情绪效果或受众反馈。

## 目录结构

```text
agents/       Skill 界面元数据
assets/       空交付模板与虚构渲染夹具
references/   叙事方法、来源与映射契约、验证规则和行为场景
scripts/      构建、审计、验证工具及文字生成回归测试
tests/        确定性渲染端到端测试
SKILL.md      Skill 指令与模式选择
```

## 已知限制

- 无法自动证明剧情事实、动机归属、句画匹配或叙事质量；仍需依据原作人工审核。
- OCR 只能辅助检查，本仓库不提供 OCR 实现。
- 最终原图依赖使用者有权使用的来源与提取流程；超高图片可能消耗大量内存。
- 自定义段落映射不等于渲染交付，脚本生成器不会替你验证外部图片与审批状态。
- 不会自动保护任意已存在的输出文件；测试和修订应写入独立输出路径。

## 来源日期与所有权

工具源于 2026-08-19 的 Codex 辅助创作，于 2026-08-27 整理为公开副本。2026-09-13 同步通用的自然段写作、审核画格映射和局部修订方法，并修复独立 CR 换行处理。

公开包仅保留通用工具、方法和独立虚构测试；不包含真实漫画、生产文案、私人验收记录、聊天历史、本机路径或项目素材。依赖由包管理器安装，不复制第三方源码。

## 许可证

本仓库目前没有授予开源许可证，默认版权限制仍然有效。本次更新不新增许可证，也不授予第三方漫画或其他输入素材的使用权。
