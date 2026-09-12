import sys

import press
import uv_wind
import th
import RH


# =========================
# 颜色
# =========================

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


# =========================
# 命令定义
# =========================

COMMANDS = {

    "cal-uv_wind": {
        "description": "计算风向、风速 → U/V",
        "function": uv_wind.calculate_uv_windspeed,
        "parameters": [
            ("dir_deg", "~/uv_wind.dir(deg) > ", float),
            ("speed", "~/uv_wind.speed(m/s) > ", float),
        ],
        "returns": [
            "u(m/s)",
            "v(m/s)",
        ],
    },

    "cal-dir-speed": {
        "description": "计算 U/V → 风向、风速",
        "function": uv_wind.calculate_uv_windspeed_from_components,
        "parameters": [
            ("u", "~/uv_dir.u(m/s) > ", float),
            ("v", "~/uv_dir.v(m/s) > ", float),
        ],
        "returns": [
            "dir(deg)",
            "speed(m/s)",
        ],
    },

    "cal-prs": {
        "description": "从海拔计算气压",
        "function": press.calculate_pressure_from_altitude,
        "parameters": [
            ("altitude", "~/press.altitude > ", float),
        ],
        "returns": [
            "pressure(hPa)",
        ],
    },
    "cal-RH": {
        "description": "计算相对湿度",
        "function": RH.calculate_RH,
        "parameters": [
            ("T", "~/RH.T(°C) > ", float),
            ("Td", "~/RH.Td(°C) > ", float),
        ],
        "returns": [
            "RH(%)",
        ],
    },
    "cal-th": {
        "description": "计算位温",
        "function": th.calculate_th,
        "parameters": [
            ("P", "~/th.P(hPa) > ", float),
            ("T", "~/th.T(K) > ", float),
        ],
        "returns": [
            "th(K)",
        ],
    }
}


# =========================
# 基础功能
# =========================

def print_help():
    print("可用命令:")

    for name, command in COMMANDS.items():
        print(f"    {name:<20} {command['description']}")

    print("    help                 显示此帮助信息")
    print("    exit                 退出程序")


def get_parameter(name, prompt, converter):
    while True:
        try:
            value = input(prompt)

        except EOFError:
            print()
            return None

        except KeyboardInterrupt:
            print("\n操作已取消。")
            return None

        if value.strip() == "":
            print(f"{YELLOW}参数 {name} 不能为空。{RESET}")
            continue

        try:
            return converter(value)

        except ValueError:
            print(
                f"{RED}参数 {name} 的格式错误，"
                f"请输入 {converter.__name__} 类型的数据。{RESET}"
            )


def execute_command(command):
    function = command["function"]

    arguments = []

    for name, prompt, converter in command["parameters"]:
        value = get_parameter(name, prompt, converter)

        if value is None:
            return

        arguments.append(value)

    try:
        result = function(*arguments)

    except Exception as e:
        print(f"{RED}计算失败：{e}{RESET}")
        return

    if not isinstance(result, tuple):
        result = (result,)

    returns = command["returns"]

    if len(result) != len(returns):
        print(
            f"{RED}错误：算法返回值数量与命令定义不一致。{RESET}"
        )
        return

    for name, value in zip(returns, result):
        if value is None:
            print(f"{CYAN}~return.{name} > 无数据{RESET}")
        elif isinstance(value, float):
            print(f"{CYAN}~return.{name} > {value:.2f}{RESET}")
        else:
            print(f"{CYAN}~return.{name} > {value}{RESET}")


# =========================
# CLI
# =========================

def run_cli():

    print("""欢迎使用天气计算器 CLI。
输入 help 查看可用命令。""")

    while True:

        try:
            command_name = input("~ > ").strip()

        except EOFError:
            print("\n退出程序。")
            break

        except KeyboardInterrupt:
            print("\n输入 exit 退出程序。")
            continue

        if command_name == "":
            continue

        if command_name == "exit":
            print("退出程序。")
            sys.exit(0)

        if command_name == "help":
            print_help()
            continue

        command = COMMANDS.get(command_name)

        if command is None:
            print(
                f"{RED}未知的命令：{command_name}"
                f"{RESET}"
            )
            continue

        execute_command(command)