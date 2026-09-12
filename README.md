# WeatherCalculator CLI

一个面向气象计算的交互式命令行工具。

WeatherCalculator CLI 旨在将一些常用的气象计算封装为简单的命令，通过统一的交互式 CLI 进行调用，并采用模块化结构，方便后续继续添加新的计算功能。

> 当前项目仍处于早期开发阶段，功能和接口可能发生变化。

## 功能

目前支持：

- 风向、风速 → U/V 风分量
- U/V 风分量 → 风向、风速
- 根据海拔计算气压
- 交互式命令行操作
- Windows 独立可执行文件
- 模块化的计算函数与命令注册机制

## 使用

### 从 Python 运行

需要 Python 环境。

```powershell
python main.py
```

启动后，可以输入：

```text
~ > help
```

查看当前支持的命令。

### 使用预编译版本

从 GitHub Releases 下载：

```text
weathercalculator.exe
```

Windows 用户无需单独安装 Python，直接运行即可。

## 当前命令

| 命令 | 功能 |
|---|---|
| `cal-uv_wind` | 根据风向和风速计算 U/V 风分量 |
| `cal-dir-speed` | 根据 U/V 风分量计算风向和风速 |
| `cal-prs` | 根据海拔计算气压 |
| `help` | 显示可用命令 |
| `exit` | 退出程序 |

### 示例

#### 风向、风速 → U/V

```text
~ > cal-uv_wind
~/uv_wind.dir > 45
~/uv_wind.speed > 1
~return.u > -0.7071
~return.v > -0.7071
~ >
```

这里采用气象学中的风向定义：

> 风向表示“风从哪里来”。

因此，45° 表示东北风，1 m/s 的东北风对应负的 U、V 分量。

#### U/V → 风向、风速

```text
~ > cal-dir-speed
~/uv_dir.u > -0.7071
~/uv_dir.v > -0.7071
~return.dir > 45
~return.speed > 1
```

## 项目结构

```text
weathercalculator_cli/
├── main.py          # 程序入口
├── cli.py           # 交互式 CLI
├── press.py         # 气压相关计算
├── uv_wind.py       # U/V 风计算
├── build.ps1        # Windows 构建脚本
├── .gitignore
└── README.md
```

项目采用计算逻辑与用户交互分离的设计。

例如，`uv_wind.py` 只负责计算：

```python
u, v = calculate_uv_windspeed(direction, speed)
```

而 `cli.py` 负责：

- 接收用户输入
- 转换参数类型
- 调用计算函数
- 输出计算结果
- 处理输入错误

这样可以在不修改核心计算函数的情况下继续扩展 CLI。

## 添加新的计算功能

WeatherCalculator CLI 使用命令注册表管理 CLI 命令。

例如：

```python
COMMANDS = {
    "cal-example": {
        "description": "示例计算",
        "function": example.calculate,
        "parameters": [
            ("value", "~/example.value > ", float),
        ],
        "returns": [
            "result",
        ],
    },
}
```

因此，添加新的计算功能时，可以主要关注两个部分：

1. 在对应模块中实现计算函数
2. 在 `COMMANDS` 中注册命令

无需为每一个新功能重新编写一套 CLI 流程。

## 构建

项目使用 PyInstaller 构建 Windows 独立可执行文件。

使用 PyInstaller：

```powershell
pyinstaller -F --clean --name weathercalculator main.py
```

由于项目入口为 `main.py`，PyInstaller 会自动分析 Python 模块之间的 `import` 关系，并将项目所需的 Python 代码打包到可执行文件中。

## 开发环境

当前主要面向：

- Windows 10 / 11
- Python 3.x
- PyInstaller

项目本身目前主要依赖 Python 标准库，因此不需要复杂的第三方运行环境。

## 开发计划

后续可能加入：

- 更多气象计算公式
- 位势高度与气压层相关计算
- 风场及热力参数计算
- 更完善的参数验证
- 更丰富的 CLI 输出
- 配置文件支持
- 更完善的帮助系统
- 更多独立计算模块

具体功能将根据实际使用需求逐步增加。

## 版本

当前版本：

**v0.2.0**

这是 WeatherCalculator CLI 的首个公开版本。

项目目前处于早期开发阶段，因此未来版本可能会调整命令名称、交互方式以及内部接口。

## License

MIT License
