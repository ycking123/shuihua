# 结束前提问规则

你必须遵守以下规则：

1. 在每一次 assistant 回合中，只要你准备结束当前回复，或者没有明确可继续执行的下一步，就必须先调用工具 `vscode_askQuestions`。
2. 即使你在本轮或上一轮已经调用过 `vscode_askQuestions`，只要当前仍准备结束回复，且用户没有明确表示“结束”“不用再问”“停止提问”，你就必须再次调用 `vscode_askQuestions`。
3. 用户如果是在回答上一轮 `vscode_askQuestions`，而该回答没有形成一个明确、可直接执行的新任务，你不能直接结束，必须继续调用 `vscode_askQuestions`。
4. 不允许把“已经调用过一次 `vscode_askQuestions`”视为后续回合的豁免条件。
5. 只有在用户明确表示“结束对话”“不用再问”“停止”“就这样”时，才可以不再调用 `vscode_askQuestions`。
6. 如果 `vscode_askQuestions` 工具不可用，必须明确说明该工具不可用，而不能静默结束回复。
7. 每次提问应尽量简短，优先只问 1 个最关键的问题。