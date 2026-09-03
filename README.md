# Comic Narration Storyboard（漫画解说与视觉分镜）

这是一个 Codex Skill 与 Python 工具集，用于同步生成中文漫画解说、基于来源的画面映射、处理后的静帧、接触表和客观交付验证。

核心规则只有一条：旁白与视觉证据必须同时构建。如果一句旁白得不到权威漫画画面的支持，就必须修改旁白或更换画面。

## 主要能力

- 明确章节边界、以来源为准的旁白生成
- 每个旁白单元映射到可复核的视觉来源
- 完整画格与跨源提取规则
- 在不虚构漫画像素的前提下处理对白、拟声词和文字带
- 按最终输出尺寸执行前景可读性审计
- 生成接触表，供人工进行语义检查
- 验证结构、来源、图片配置、尺寸、重复率和交付指标
- 使用 Pillow 生成完全虚构、可重复构建的金标准夹具

## 前置条件

- Python 3.10+
- 支持 `ImageCms` 的 Pillow 12.3.0 或更新的 12.x 版本

安装或升级依赖（已有环境也需要执行）：

```bash
python -m pip install --upgrade -r requirements.txt
```

版本下限用于排除 Pillow 12.3.0 之前已披露的 `ImageCms` 和裁切相关越界写入问题，参见 [ImageCms 安全公告](https://github.com/advisories/GHSA-9hw9-ch79-4vh6)与[裁切安全公告](https://github.com/advisories/GHSA-6r8x-57c9-28j4)。这不表示本工具已证实存在可利用路径；处理外部图片前仍应更新依赖，并限制输入规模。Pillow 13 尚未验证，因此暂不纳入支持范围。

## 作为 Codex Skill 使用

将本仓库克隆或复制到个人 Codex Skill 目录，并保持目录名为 `comic-narration-storyboard`，然后调用：

```text
$comic-narration-storyboard
```

完整工作流程见 `SKILL.md`。该 Skill 必须有权威漫画来源；参考稿和旧交付只能提供节奏参考，不能提供剧情事实。

## 初始化交付目录

```bash
python scripts/init_delivery.py ./work/episode-001
```

生成的目录包含所需 CSV、Markdown、JSON 文件和子目录。已有模板文件不会被静默覆盖。

## 重建派生产物

```bash
python scripts/build_script_from_storyboard.py \
  ./work/episode-001/storyboard.csv \
  ./work/episode-001/script.md

python scripts/build_contact_sheets.py ./work/episode-001
```

## 审计与验收

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

验证器通过只代表结构和像素符合要求，不代表叙事语义已经正确。接触表仍需人工复核。

## 重建虚构金标准

```bash
python scripts/create_gold_standard_fixture.py \
  --output ./work/gold-standard
```

夹具只包含脚本绘制的示意形状，不含第三方漫画。ICC 配置的时间戳已冻结，因此相同输入会生成字节级一致的文件树。

## 验证

```bash
python -m unittest -v tests.test_end_to_end
```

测试会连续生成两次夹具、比较每个文件哈希、执行交付验证，并检查最终尺寸下的可读性。

## 目录结构

```text
agents/       Codex Skill 元数据
assets/       空交付模板与虚构金标准
references/   旁白、视觉、来源和验证规则
scripts/      初始化、构建、审计、验证和夹具工具
tests/        确定性端到端测试
SKILL.md      Codex Skill 指令
```

## 已知限制

- 叙事事实和句画语义匹配无法完全依靠自动化认证。
- OCR 只能作为辅助证据，本仓库不包含 OCR 实现。
- 最终原图仍依赖用户有权使用的漫画来源和提取流程。
- 处理超高源图时可能占用较多内存。

## 来源

项目来自 2026-08-19 的 Codex 辅助工作流，并于 2026-08-27 整理为干净公开副本。仓库不包含权威漫画输入、私人交付文件、本机路径或对话历史。

## 许可证

本仓库目前没有授予开源许可证。没有许可证意味着默认版权限制仍然有效。
