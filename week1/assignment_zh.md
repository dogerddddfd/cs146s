# 第1周 — 提示技术

你将通过编写提示来完成特定任务，从而练习多种提示技术。每个任务的说明位于其对应的源文件顶部。

## 安装
确保你已经完成了顶层`README.md`中描述的安装。

## Ollama安装
我们将使用一个名为[Ollama](https://ollama.com/)的工具在你的机器上本地运行不同的最先进的LLM。使用以下方法之一：

- macOS（Homebrew）：
  ```bash
  brew install --cask ollama 
  ollama serve
  ```

- Linux（推荐）：
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Windows：
  从[ollama.com/download](https://ollama.com/download)下载并运行安装程序。

验证安装：
```bash
ollama -v
```

在运行测试脚本之前，确保你已经拉取了以下模型。你只需要做一次（除非你以后删除了模型）：
```bash
ollama run mistral-nemo:12b
ollama run llama3.1:8b
```

## 技术和源文件
- K-shot提示 — `week1/k_shot_prompting.py`
- 思维链 — `week1/chain_of_thought.py`
- 工具调用 — `week1/tool_calling.py`
- 自洽性提示 — `week1/self_consistency_prompting.py`
- RAG（检索增强生成） — `week1/rag.py`
- 反思 — `week1/reflexion.py`

## 交付物
- 阅读每个文件中的任务描述。
- 设计并运行提示（查找代码中所有标记为`TODO`的地方）。这应该是你唯一需要更改的内容（即不要修改模型）。
- 迭代改进结果，直到测试脚本通过。
- 保存每种技术的最终提示和输出。
- 确保在你的提交中包含每种提示技术文件的完整代码。***仔细检查所有`TODO`是否已解决。***

## 评估标准（共60分）
- 6种不同提示技术中每种完成的提示得10分