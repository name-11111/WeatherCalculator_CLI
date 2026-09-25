def calculate_th(P, T):
    # 定义常数
    P0 = 1013.25 # 标准大气压强(hPa)
    Rd = 287.05  # 干空气气体常数(J/(kg·K))
    Cp = 1004.0  # 干空气定压比热容(J/(kg·K))

    th = T * (P0 / P) ** (Rd / Cp)
    return th