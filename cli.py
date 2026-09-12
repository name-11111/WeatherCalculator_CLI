import sys

import press
import uv_wind


def print_help():
    print("""可用命令:
    cal-uv_wind   计算风向、风速 → U/V
    cal-dir-speed 计算 U/V → 风向、风速
    cal-prs       从海拔计算气压
    help          显示此帮助信息
    exit           退出程序
    """)


def calculate_uv_wind():
    dir_deg = float(input("~/uv_wind.dir > "))
    speed = float(input("~/uv_wind.speed > "))

    u, v = uv_wind.calculate_uv_windspeed(dir_deg, speed)

    print(f"~return.u > {u:.2f}")
    print(f"~return.v > {v:.2f}")


def calculate_dir_speed():
    u = float(input("~/uv_dir.u > "))
    v = float(input("~/uv_dir.v > "))

    dir_deg, speed = uv_wind.calculate_uv_windspeed_from_components(u, v)

    print(f"~return.dir > {dir_deg:.2f}")
    print(f"~return.speed > {speed:.2f}")


def calculate_pressure():
    altitude = float(input("~/press.altitude > "))

    pressure = press.calculate_pressure_from_altitude(altitude)

    print(f"~return.pressure > {pressure:.2f}")


COMMANDS = {
    "cal-uv_wind": calculate_uv_wind,
    "cal-dir-speed": calculate_dir_speed,
    "cal-prs": calculate_pressure,
    "help": print_help,
    "exit": sys.exit,
}


def run_cli():
    print("""欢迎使用天气计算器CLI。
输入 help 查看可用命令。""")

    while True:
        command = input("~ > ").strip()

        if command in COMMANDS:
            COMMANDS[command]()
        else:
            print(f"\033[31m未知的命令 {command}\033[0m")