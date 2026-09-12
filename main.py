import press
import uv_wind
import sys

def print_help():
    print("""可用命令:
        "cal-uv_wind": 计算UV风速
        "cal-dir-speed": 从分量计算UV风速
        "cal-prs": 从海拔计算气压
        "help": 显示此帮助信息
        "exit": 退出程序
    """)

def calculate_uv_windspeed():
    dir_deg = float(input("~/uv_wind.dir > "))
    speed = float(input("~/uv_wind.speed > "))
    u, v = uv_wind.calculate_uv_windspeed(dir_deg, speed)
    print(f"""~return.u > {u:.2f}
~return.v > {v:.2f}
""")

def calculate_uv_windspeed_from_components():
    u = float(input("~/uv_dir.u > "))
    v = float(input("~/uv_dir.v > "))
    dir_deg, speed = uv_wind.calculate_uv_windspeed_from_components(u, v)
    print(f"""~return.dir > {dir_deg:.2f}
~return.speed > {speed:.2f}
""")

def calculate_pressure_from_altitude():
    altitude = float(input("~/press.altitude > "))
    pressure = press.calculate_pressure_from_altitude(altitude)
    print(f"""~return.pressure > {pressure:.2f}
""")

commands = {
    "cal-uv_wind": calculate_uv_windspeed,
    "cal-dir-speed": calculate_uv_windspeed_from_components,
    "cal-prs": calculate_pressure_from_altitude,
    "help": print_help,
    "exit": sys.exit
}

def main():
    print("""欢迎使用天气计算器CLI。
    输入help查看可用命令。""")
    while True:
        command = input("~ > ").strip()

        if command in commands:
            commands[command]()
        else:
            print(f"\033[31m未知的命令 {command}\033[0m")

if __name__ == "__main__":
    main()