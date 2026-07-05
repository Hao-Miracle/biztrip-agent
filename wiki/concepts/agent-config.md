## 🤖 Agent 配置说明（通用 LLM 接入）

> 不配 LLM 也能完整使用规则引擎。配了 LLM 则自动启用 AI 增强模式。

### 架构：两层降级策略

```
用户请求
  ├── LLM 可用？ ──→ 是 ──→ 🧠 AI 增强模式
  │                         ├── LLM 路由分类
  │                         ├── LLM 专用提取
  │                         └── LLM 出差聚合
  │                              │
  │                         单条失败？──→ 📋 自动降级正则兜底
  │
  └── LLM 不可用？──→ 📋 规则模式
                        ├── 域名匹配分类
                        ├── 正则提取
                        └── 规则聚合
```

### 支持的服务商

| 服务商 | 模型示例 | 获取 Key |
|--------|---------|---------|
| DeepSeek | `deepseek-chat` | [platform.deepseek.com](https://platform.deepseek.com/) |
| 阿里云百炼（通义千问） | `qwen-plus` | [bailian.console.aliyun.com](https://bailian.console.aliyun.com/) |
| 智谱 AI（GLM） | `glm-4-flash` | [open.bigmodel.cn](https://open.bigmodel.cn/) |
| 月之暗面（Kimi） | `moonshot-v1-8k` | [platform.moonshot.cn](https://platform.moonshot.cn/) |
| SiliconFlow（模型聚合） | `Qwen/Qwen2.5-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn/) |
| 火山引擎（豆包） | `ep-xxxxxxxxxx` | [console.volcengine.com](https://console.volcengine.com/ark) |
| **Ollama 本地模型** | `qwen2.5:7b` | 完全本地，零成本 |

### 三步配置

```bash
# 1. 复制配置模板
cp .env.example .env

# 2. 编辑 .env，填入你的选择
# 例如用 DeepSeek：
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 或用本地 Ollama：
LLM_API_KEY=ollama
LLM_BASE_URL=http://localhost:11434/v1
LLM_MODEL=qwen2.5:7b

# 3. 运行
python3 phase2/agent_report.py
```

### 降级行为

| 场景 | 行为 |
|------|------|
| 没配 `LLM_API_KEY` | 全部走规则引擎，零成本 |
| LLM 分类置信度 < 0.7 | 该封邮件降级为域名/关键词匹配 |
| LLM 提取关键字段缺失 > 50% | 该条记录降级为正则提取 |
| LLM 聚合调用失败 | 降级为基于目的地的简单规则聚合 |

### 成本参考

| 模型 | 输入 | 输出 | 一次扫描（~5封差旅邮件）|
|------|------|------|------|
| DeepSeek V3 | 2元/百万Tokens | 8元/百万Tokens | < 0.05 元 |
| GLM-4-Flash | 免费 | 免费 | 0 元 |
| Ollama 本地 | 0 | 0 | 0 元 |

> GLM-4-Flash 有免费额度，Ollama 完全本地运行零成本——不花钱也能用 AI 增强。

### 角色说明

- **Agent 角色**：邮件分类器 + 信息提取器 + 出差聚合器，三层 LLM prompt 各有分工
- **工作流**：IMAP 获取 → LLM 路由分类 → LLM 品类专用提取 → LLM 出差聚合 → Excel 输出
- **工具依赖**：IMAP 邮件获取（内置）+ PDF/ZIP 解析（PyPDF2/zipfile）+ Excel 生成（openpyxl）