# 学生发布包暂存区

本目录只存放可能发给学生的材料，不放参考答案。

当前四个 Lab 均处于“待修订/待实机验证”状态，不能直接把本目录整体发布。各实验的材料状态和发布前待办统一维护在 [`当前材料状态.md`](../当前材料状态.md)，不再在每个 Lab 目录重复维护 README。

正式发布时，应从对应 Lab 目录中挑选已验证的文件，建立单个实验的独立压缩包。学生包只包含：

1. 最终 PDF 指导书；
2. 不含答案的 starter；
3. 必要数据；
4. 学生需要的课件；
5. 简短的提交说明。

不得包含 TA 参考实现、往届学生报告、运行产物、缓存文件或其他实验的材料。

## Coding agent 规则

本仓库对 coding agent 的强制规则写在 [`AGENTS.md`](AGENTS.md)。根目录和工具目录下的适配文件只负责让各工具自动加载这份政策，**不要在适配文件里改政策本身**。

已适配：Cursor、Claude Code、GitHub Copilot、Gemini CLI、Aider、Windsurf、Cline、Trae Code、腾讯云 CodeBuddy、通义灵码 / Qoder CN、Qoder、百度文心快码 Comate、心流 iFlow。华为云码道 CodeArts 与 Qwen Code 会直接读取根目录 `AGENTS.md`，无需额外文件。

若更新规则，请改 `AGENTS.md`，并同步全文镜像：`.github/copilot-instructions.md`、`.trae/rules/follow-agents.md`、`CODEBUDDY.md`、`.lingma/rules/follow-agents.md`、`.comate/rules/follow-agents.mdr`。
