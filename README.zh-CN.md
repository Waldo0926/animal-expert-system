# 动物识别专家系统

[![类型](https://img.shields.io/badge/%E7%B1%BB%E5%9E%8B-%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E8%AF%BE%E7%A8%8B-2563eb?style=for-the-badge)](#)
[![技术](https://img.shields.io/badge/%E6%8A%80%E6%9C%AF-Python_%C2%B7_PyQt5-7c3aed?style=for-the-badge)](#)
[![许可证](https://img.shields.io/badge/%E8%AE%B8%E5%8F%AF%E8%AF%81-MIT-16a34a?style=for-the-badge)](LICENSE)


[English](README.md)

这是一个小型的**符号人工智能 / 专家系统**项目。系统根据用户提供的动物特征，通过产生式规则知识库和真正的**正向链式推理（Forward Chaining）**逐步推导并识别动物。

> 本仓库是我在 2026 年基于 2022 年《人工智能导论》实践周团队课程设计思路进行的独立重构。这里没有直接公开当年的团队原始提交文件。课程设计来源和署名说明请见 [Coursework origin and attribution](docs/coursework-origin.md)。

## 项目意义

现代人工智能常常与机器学习、深度学习联系在一起，但经典人工智能还包括**知识表示、规则系统和逻辑推理**。这个项目以一个规模较小、推理过程完全可观察的专家系统展示 Symbolic AI 的基本思想。

当前知识库包含：

- **20 个可观察特征**
- **4 个中间类别**：哺乳类、鸟类、食肉类、有蹄类
- **7 种可识别动物**：金钱豹、虎、长颈鹿、斑马、鸵鸟、企鹅、信天翁
- **15 条产生式规则**

## 主要特点

- 实现真正的、迭代至收敛的 **Forward Chaining**
- 支持多层推理，而不是只匹配用户第一次输入的事实
- 使用结构化 JSON 保存知识库
- 将知识库、推理引擎、CLI 与 GUI 解耦
- 英文 / 简体中文双语标签
- 可选 PyQt5 图形界面
- 推理核心和 CLI 不依赖第三方库
- 7 种目标动物均有自动化测试
- GitHub Actions 持续集成测试

## 正向链式推理示例

假设输入：

```text
有毛发、吃肉、黄褐色、暗斑点
```

系统首先推导：

```text
R01: 有毛发 -> 哺乳类
R05: 吃肉 -> 食肉类
```

随后新得到的“哺乳类”和“食肉类”会被加入 working memory，再继续触发：

```text
R09: 哺乳类 + 食肉类 + 黄褐色 + 暗斑点 -> 金钱豹
```

这正是本次重构最重要的改进：**推导出来的新事实会继续参与后续推理。**

完整设计见 [Architecture](docs/architecture.md)。

## 项目结构

```text
animal-expert-system/
├── src/animal_expert_system/
│   ├── data/knowledge_base.json
│   ├── engine.py
│   ├── knowledge_base.py
│   ├── models.py
│   ├── cli.py
│   └── gui.py
├── tests/
├── docs/
├── .github/workflows/test.yml
├── pyproject.toml
└── README.md
```

## 快速运行

### 1. 安装

```bash
git clone https://github.com/<your-username>/animal-expert-system.git
cd animal-expert-system
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e .
```

### 2. 查看所有输入特征

```bash
animal-expert-system --list-features
```

### 3. 进行一次推理

```bash
animal-expert-system --features 1 6 12 13
```

最终应得到：

```text
leopard / 金钱豹
```

不安装 console command 也可以直接运行：

```bash
PYTHONPATH=src python -m animal_expert_system --features 1 6 12 13
```

## 图形界面

安装 GUI 依赖：

```bash
pip install -e '.[gui]'
animal-expert-gui
```

在界面中可以勾选动物特征、运行推理、查看每一步触发的规则，并一键重置。

## 测试

```bash
python -m unittest discover -s tests -v
```

测试不仅覆盖 7 种目标动物，也专门验证了多跳推理是否真正发生。

## 与 2022 年课程设计的区别

这个公开仓库并不是把当年的课程作业文件夹直接上传。2026 年版本重新实现了核心代码，并移除了原项目中的虚拟环境、EXE、IDE 配置、个人/学生信息、旧 GUI 生成代码和其他不适合公开仓库的文件。

更重要的是，旧版逻辑主要是根据初始输入做规则匹配；当前版本会把每次推导的新结论加入 working memory，并持续运行直到没有新事实产生，因此可以进行真正的多阶段正向推理。

详细说明见 [Coursework origin and attribution](docs/coursework-origin.md)。

## 技术关键词

Python 3.10+ · Symbolic AI · Expert System · Production Rules · Forward Chaining · Knowledge Representation · JSON · PyQt5 · unittest · GitHub Actions

## License

MIT License，详见 [LICENSE](LICENSE)。
