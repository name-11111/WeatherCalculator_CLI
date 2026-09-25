import math

def calculate_RH(T, Td):
    es = 6.112 * math.exp((17.67 * T) / (T + 243.5))
    e = 6.112 * math.exp((17.67 * Td) / (Td + 243.5))
    RH = (e / es) * 100
    return RH