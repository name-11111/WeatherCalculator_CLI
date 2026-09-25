import math

def calculate_uv_windspeed(dir_deg, speed):
    speed_rad = math.radians(dir_deg)
    u = speed * -math.sin(speed_rad)
    v = speed * -math.cos(speed_rad)
    return u, v

def calculate_uv_windspeed_from_components(u, v):
    speed = math.sqrt(u**2 + v**2)
    dir_rad = math.atan2(-u, -v)
    dir_deg = math.degrees(dir_rad) % 360
    return dir_deg, speed