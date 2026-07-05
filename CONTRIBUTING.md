# 贡献指南

感谢你对 BizTrip Agent 的兴趣！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复或新功能
- 🌐 新增平台解析器

---

## 快速开始

### 1. Fork 并克隆

```bash
# Fork 本仓库，然后克隆你的 fork
git clone https://github.com/<your-username>/BizTrip-Agent.git
cd BizTrip-Agent
```

### 2. 安装依赖

```bash
pip install python-dotenv PyPDF2 openpyxl

# 如果需要 LLM 功能
pip install openai
```

### 3. 配置邮箱

```bash
cp .env.example .env
# 编辑 .env，填入你的邮箱和授权码
```

### 4. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

---

## 贡献方式

### 🐛 报告 Bug

请使用 [Bug Report 模板](../../issues/new?template=bug_report.md) 创建 Issue，并包含：

- 复现步骤
- 预期行为
- 实际行为
- 环境信息（操作系统、Python 版本、邮箱服务商）
- 相关日志或截图

### 💡 功能建议

请使用 [Feature Request 模板](../../issues/new?template=feature_request.md) 创建 Issue，并说明：

- 这个功能解决了什么问题
- 你期望的实现方式
- 有没有备选方案

### 🔧 提交代码

1. 确保你的代码遵循现有代码风格
2. 添加必要的注释和文档
3. 测试你的修改
4. 提交 PR，使用 PR 模板填写详细信息

### 🌐 新增平台解析器

这是最受欢迎的贡献方式！在 `classify_emails.py` 的 `DOMAIN_RULES` 中添加域名规则，然后在 `extract_emails.py` 中添加对应的解析函数。

---

## 代码规范

- 使用 Python 3.8+ 语法
- 遵循 PEP 8
- 函数和变量使用 snake_case
- 添加 docstring 说明函数用途、输入和输出
- 敏感信息（邮箱、授权码、API Key）**绝不**提交到代码中

---

## 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/zh-hans/v1.0.0/) 格式：

```
feat: 新增XX平台火车票解析
fix: 修复滴滴金额提取错误
docs: 更新安装指南
chore: 升级依赖版本
```

---

## 常见问题

**Q: 我需要什么权限才能贡献？**
A: 任何人都可以提交 Issue 和 PR，不需要特殊权限。

**Q: 多久会收到回复？**
A: 我们会在 3 个工作日内回复所有 Issue 和 PR。

**Q: 可以只提交想法不写代码吗？**
A: 当然可以！好的想法和 Bug 报告同样有价值。

---

## 行为准则

参与本项目请遵守 [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct.html) 行为准则，保持友善和尊重。

---

再次感谢你的贡献！ 🙌
