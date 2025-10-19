
===========================================================================

workers的脚本剖析：

实际上脚本按操作用途分，无非就这几种：
读写执行型（为了完成功能点，比如增删改，移动复制文件等等）、
读写体检型（将数据收敛成完成功能点前的理想状态，如控制只有某几个类型文件，其他文件移动掉；但似乎很多AI生成的执行型脚本在一开始就加了很多检查的动作，例如检查是不是合法规范的路径）、
只读型（通常为统计数据，然后用于数据分析）
这里在计算机领域有什么俗称吗？



===========================================================================

对于schemas的类命名规则，直接无脑复制避免浪费过多时间在命名上：

通用的schemas在/apis里直接用，非常规的在对应的模块里找对应的schemas

拿到一个worker函数 (例如 decompress_recursively)。
机械地创建Request Schema -> DecompressRecursiveRequest。
决定Response类型：
只需要成功/失败信息？ -> response_model=StatusResponse。
需要返回特定数据结构？ -> 创建一个 DecompressRecursiveResponse。
编写API Endpoint，连接 Request 和 Response。


Schema 的主要作用是简化和规范化 POST 请求。
你的场景核心是处理本地文件路径。
你需要一个既通用又能处理特殊参数的方案。


===========================================================================

data_processing_service/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI应用入口，非常轻量
│   ├── core/               # 核心配置与共享模块
│   │   ├── __init__.py
│   │   └── schemas.py      # Pydantic模型，定义API的输入输出契约
│   │
│   ├── apis/               # API路由层 (唯一的外部入口)
│   │   ├── __init__.py
│   │   ├── router_v1.py    # 所有v1版本的API路由
│   │   └── deps.py         # (可选) 依赖注入项
│   │
│   └── workers/            # 真正的“大脑”：所有的数据处理脚本
│       ├── __init__.py
│       ├── phase1_preprocessing/  # 环节一：预处理
│       │   ├── __init__.py
│       │   ├── 01_clean_data.py   # 原1.py，处理数据清洗
│       │   └── 02_format_convert.py # 原2.py，处理格式转换
│       │
│       └── phase2_modeling/       # 环节二：模型处理
│           ├── __init__.py
│           ├── 03_run_inference.py  # 原3.py，运行模型推理
│           └── 04_evaluate_results.py # 原4.py，评估结果
│
├── tests/                  # ⭐ 测试验证脚本的家
│   ├── __init__.py
│   ├── test_phase1_workers.py     # 专门测试环节一的worker函数
│   ├── test_phase2_workers.py     # 专门测试环节二的worker函数
│   └── test_api_endpoints.py      # (可选) 对API接口进行端到端测试
│
├── playground/             # ⭐ 探索性、一次性的测试脚本放在这里
│   ├── temp_test_script.py
│   └── exploring_new_data.ipynb
│
├── .gitignore
├── requirements.txt
└── README.md

运行测试: 在你的项目根目录（data_processing_service/）打开终端，然后简单地输入：
pytest
pytest 会自动发现并运行所有 tests/ 目录下 test_*.py 文件中的 test_* 函数。



===========================================================================