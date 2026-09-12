import math

def calculate_pressure_from_altitude(altitude):
    # Constants
    P0 = 1013.25  # 标准大气压强(hPa)
    T0 = 288.15   # 标准温度(K)
    L = 0.0065    # 温度递减率(K/m)
    R = 8.31447   # 气体常数(J/(mol·K))
    M = 0.0289644 # 摩尔质量(kg/mol)
    g = 9.80665   # 重力加速度(m/s^2)
    
    pressure = P0 * (1 - (L * altitude) / T0) ** (g * M / (R * L))
    return pressure