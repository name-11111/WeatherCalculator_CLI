# WeatherCalculator CLI

一个面向气象计算的交互式命令行工具。

WeatherCalculator CLI 旨在将一些常用的气象计算封装为简单的命令，通过统一的交互式 CLI 进行调用，并采用模块化结构，方便后续继续添加新的计算功能。

> 当前项目仍处于早期开发阶段，功能和接口可能发生变化。

## 功能

目前支持：

- 风向、风速 → U/V 风分量
- U/V 风分量 → 风向、风速
- 根据海拔计算气压
- 根据气压和温度计算位温
- 根据温度和露点计算相对湿度
- 交互式命令行操作，结果、警告与错误使用不同颜色区分
- 参数校验：参数为空或格式错误时会提示并重新输入
- 参数与返回值均带有单位提示
- 模块化的计算函数与命令注册机制
- Windows 独立可执行文件

## 使用

### 从 Python 运行

需要 Python 3.x 环境（开发环境使用 Python 3.13）。运行时仅依赖 Python 标准库，无需安装第三方依赖。

```powershell
python main.py
```

启动后，可以输入：

```text
~ > help
```

查看当前支持的命令。

### 使用预编译版本

如果 Release 中提供了构建好的可执行文件，可以直接下载：

```text
weathercalculator.exe
```

Windows 用户无需单独安装 Python，直接运行即可。也可以参考下方的「构建」一节自行构建。

## 当前命令

| 命令 | 功能 | 参数 | 返回 |
|---|---|---|---|
| `cal-uv_wind` | 风向、风速 → U/V 风分量 | `dir`（度）、`speed`（m/s） | `u`、`v`（m/s） |
| `cal-dir-speed` | U/V 风分量 → 风向、风速 | `u`、`v`（m/s） | `dir`（度）、`speed`（m/s） |
| `cal-prs` | 从海拔计算气压 | `altitude`（m） | `pressure`（hPa） |
| `cal-RH` | 计算相对湿度 | `T`、`Td`（°C） | `RH`（%） |
| `cal-th` | 计算位温 | `P`（hPa）、`T`（K） | `th`（K） |
| `help` | 显示可用命令 | — | — |
| `exit` | 退出程序 | — | — |

数值型返回值统一保留两位小数输出。

### 示例

#### 风向、风速 → U/V

```text
~ > cal-uv_wind
~/uv_wind.dir(deg) > 45
~/uv_wind.speed(m/s) > 1
~return.u(m/s) > -0.71
~return.v(m/s) > -0.71
```

这里采用气象学中的风向定义：

> 风向表示“风从哪里来”。

因此，45° 表示东北风，1 m/s 的东北风对应负的 U、V 分量。

#### U/V → 风向、风速

```text
~ > cal-dir-speed
~/uv_dir.u(m/s) > -0.7071
~/uv_dir.v(m/s) > -0.7071
~return.dir(deg) > 45.00
~return.speed(m/s) > 1.00
```

#### 海拔 → 气压

```text
~ > cal-prs
~/press.altitude > 1000
~return.pressure(hPa) > 898.75
```

#### 温度、露点 → 相对湿度

```text
~ > cal-RH
~/RH.T(°C) > 20
~/RH.Td(°C) > 10
~return.RH(%) > 52.51
```

#### 气压、温度 → 位温

```text
~ > cal-th
~/th.P(hPa) > 1000
~/th.T(K) > 290
~return.th(K) > 291.09
```

### 输入提示

- 参数为空：提示「参数 xxx 不能为空。」，并重新询问该参数；
- 参数格式错误：提示「参数 xxx 的格式错误，请输入 float 类型的数据。」，并重新询问该参数；
- 在参数输入时按 `Ctrl+C` 可取消当前命令；
- 输入未注册的命令：提示「未知的命令：xxx」。

## 项目结构

```text
weathercalculator_cli/
├── main.py              # 程序入口
├── cli.py               # 交互式 CLI（命令注册表与输入/输出处理）
├── modules/
│   ├── uv_wind.py       # U/V 风计算
│   ├── press.py         # 气压相关计算
│   ├── th.py            # 位温计算
│   └── RH.py            # 相对湿度计算
├── LICENSE
├── .gitignore
└── README.md
```

> `build/`、`dist/`、`*.spec` 以及本地构建脚本已在 `.gitignore` 中忽略，不会提交到仓库。

项目采用计算逻辑与用户交互分离的设计。

例如，`modules/uv_wind.py` 只负责计算：

```python
import modules.uv_wind as uv_wind

u, v = uv_wind.calculate_uv_windspeed(dir_deg, speed)
```

而 `cli.py` 负责：

- 接收用户输入
- 转换参数类型
- 调用计算函数
- 输出计算结果
- 处理输入错误

这样可以在不修改核心计算函数的情况下继续扩展 CLI。

## 添加新的计算功能

WeatherCalculator CLI 使用 `cli.py` 中的命令注册表 `COMMANDS` 管理 CLI 命令。

例如：

```python
import modules.example as example

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

其中：

- `parameters` 的每一项为 `(参数名, 提示符, 类型转换函数)`，CLI 会按顺序逐个询问，并自动完成空值与类型校验；
- `returns` 为返回值名称列表，输出格式为 `~return.<名称>`，数值统一保留两位小数；
- 计算函数返回元组时按顺序对应 `returns`，返回单个值时会被自动包装成元组；
- 返回值数量与 `returns` 长度不一致时会提示错误。

因此，添加新的计算功能时，可以主要关注三个部分：

1. 在 `modules/` 下实现计算函数（只负责计算，不处理输入输出）
2. 在 `cli.py` 顶部导入该模块
3. 在 `COMMANDS` 中注册命令

无需为每一个新功能重新编写一套 CLI 流程。

## 构建

项目使用 PyInstaller 构建 Windows 独立可执行文件。

```powershell
pyinstaller -F --clean --name weathercalculator main.py
```

- `-F` 表示生成单文件可执行文件，产物为 `dist/weathercalculator.exe`；
- `--clean` 在构建前清理 PyInstaller 缓存；
- 由于项目入口为 `main.py`，PyInstaller 会自动分析 Python 模块之间的 `import` 关系，并将项目所需的 Python 代码打包到可执行文件中。

首次构建后会在项目根目录生成 `weathercalculator.spec`，之后可以复用该配置：

```powershell
pyinstaller --clean weathercalculator.spec
```

工作目录中的 `build.ps1` 会先清理旧的 `build/`、`dist/` 目录再调用上述 PyInstaller 命令，方便一键构建（该脚本未纳入版本控制）。

## 开发环境

当前主要面向：

- Windows 10 / 11
- Python 3.x（开发环境使用 Python 3.13）
- PyInstaller（仅构建时需要）

项目运行时只依赖 Python 标准库（`sys`、`math`），因此不需要复杂的第三方运行环境。

## 开发计划

后续可能加入：

- 更多气象计算公式
- 位势高度与气压层相关计算
- 风场及热力参数计算
- 更完善的参数验证（取值范围与物理合理性检查）
- 更丰富的 CLI 输出（如对齐表格、单位切换）
- 命令别名与输入历史
- 配置文件支持
- 更完善的帮助系统
- 更多独立计算模块

具体功能将根据实际使用需求逐步增加。

## 版本

- 最新发布版本：**v0.2.0**
- 当前 `master` 分支包含尚未发布的变更：计算模块统一移入 `modules/` 包，CLI 增加彩色输出、单位提示与参数校验。

项目目前处于早期开发阶段，因此未来版本可能会调整命令名称、交互方式以及内部接口。

## License

MIT License
