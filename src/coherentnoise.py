#usr/env/bin python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/20
    Brief: Coherent Nosie Genrator
"""


import math

from window import *


__all__ = ["coherent_noise_linear_1D",
           "coherent_noise_cubic_1D",
           "coherent_noise_quintic_1D",
           "coherent_noise_linear_2D",
           "coherent_noise_cubic_2D",
           "coherent_noise_quintic_2D"]

#---------------------------------------------------------------------------
# Random number genrator

def rand(seed):
  seed = (seed >> 13) ^ seed
  nn = (seed * (seed * seed * 60493 + 19990303) + 1376312589) & 0x7fffffff
  return 1.0 - (1.0 * nn / 1073741824.0)

def rand2(seedx, seedy):
    seed = seedx * 12.9898 + seedy * 78.233
    seed = math.sin(seed)
    seed = seed * 43758.5453
    seed = seed - math.floor(seed)
    seed = seed * 2.0 - 1.0
    return seed

#---------------------------------------------------------------------------
# 1D Coherent Noise Generator

def coherent_noise_linear_1D(v):
    vd = math.floor(v)
    vu = vd + 1
    t = v - vd
    vd = rand(vd)
    vu = rand(vu)
    return vd + t * (vu - vd)

def coherent_noise_cubic_1D(v):
    def cubic(x):
        return -2.0 * x * x * x + 3 * x * x
    vd = math.floor(v)
    vu = vd + 1
    t = v - vd
    vd = rand(vd)
    vu = rand(vu)
    return vd + cubic(t) * (vu - vd)

def coherent_noise_quintic_1D(v):
    def quintic(x):
        return 6 * x * x * x * x * x - 15 * x * x * x * x + 10 * x * x * x
    vd = math.floor(v)
    vu = vd + 1
    t = v - vd
    vd = rand(vd)
    vu = rand(vu)
    return vd + quintic(t) * (vu - vd)

#---------------------------------------------------------------------------
# 2D Coherent Noise Generator

def coherent_noise_linear_2D(vx, vy):
    vlux = math.floor(vx)
    vluy = math.floor(vy)
    vrux = vlux + 1
    vruy = vluy
    vldx = vlux
    vldy = vluy + 1
    vrdx = vrux
    vrdy = vldy
    vlu = rand2(vlux, vluy)
    vru = rand2(vrux, vruy)
    vld = rand2(vldx, vldy)
    vrd = rand2(vrdx, vrdy)
    tx = vx - vlux
    ty = vy - vluy
    ux = vlu + tx * (vru - vlu)
    dx = vld + tx * (vrd - vld)
    return ux + ty * (dx - ux)

def coherent_noise_cubic_2D(vx, vy):
    def cubic(x):
        return -2.0 * x * x * x + 3 * x * x
    vlux = math.floor(vx)
    vluy = math.floor(vy)
    vrux = vlux + 1
    vruy = vluy
    vldx = vlux
    vldy = vluy + 1
    vrdx = vrux
    vrdy = vldy
    vlu = rand2(vlux, vluy)
    vru = rand2(vrux, vruy)
    vld = rand2(vldx, vldy)
    vrd = rand2(vrdx, vrdy)
    tx = vx - vlux
    ty = vy - vluy
    ux = vlu + cubic(tx) * (vru - vlu)
    dx = vld + cubic(tx) * (vrd - vld)
    return ux + cubic(ty) * (dx - ux)

def coherent_noise_quintic_2D(vx, vy):
    def quintic(x):
        return 6 * x * x * x * x * x - 15 * x * x * x * x + 10 * x * x * x
    vlux = math.floor(vx)
    vluy = math.floor(vy)
    vrux = vlux + 1
    vruy = vluy
    vldx = vlux
    vldy = vluy + 1
    vrdx = vrux
    vrdy = vldy
    vlu = rand2(vlux, vluy)
    vru = rand2(vrux, vruy)
    vld = rand2(vldx, vldy)
    vrd = rand2(vrdx, vrdy)
    tx = vx - vlux
    ty = vy - vluy
    ux = vlu + quintic(tx) * (vru - vlu)
    dx = vld + quintic(tx) * (vrd - vld)
    return ux + quintic(ty) * (dx - ux)

#---------------------------------------------------------------------------
# Test code

def drawLinearCoherentNoise2D():
    WIDTH = 400
    HEIGHT = 400
    w = Window(WIDTH, HEIGHT)
    color_buf = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            color_buf.append(0.0)  # R
            color_buf.append(0.0)  # G
            color_buf.append(0.0)  # B
            
    for i in range(HEIGHT):
        for j in range(WIDTH):
            x = i / 10.0
            y = j / 10.0
            v = coherent_noise_linear_2D(x,y)
            v = (v + 1.0) / 2.0
            color_buf[i * WIDTH * 3 + j * 3 + 0] = v
            color_buf[i * WIDTH * 3 + j * 3 + 1] = v
            color_buf[i * WIDTH * 3 + j * 3 + 2] = v
    w.save("2dlinear.png", color_buf, WIDTH, HEIGHT)

def drawCubicCoherentNoise2D():
    WIDTH = 400
    HEIGHT = 400
    w = Window(WIDTH, HEIGHT)
    color_buf = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            color_buf.append(0.0)  # R
            color_buf.append(0.0)  # G
            color_buf.append(0.0)  # B
            
    for i in range(HEIGHT):
        for j in range(WIDTH):
            x = i / 10.0
            y = j / 10.0
            v = coherent_noise_cubic_2D(x,y)
            v = (v + 1.0) / 2.0
            color_buf[i * WIDTH * 3 + j * 3 + 0] = v
            color_buf[i * WIDTH * 3 + j * 3 + 1] = v
            color_buf[i * WIDTH * 3 + j * 3 + 2] = v
    w.save("2dcubic.png", color_buf, WIDTH, HEIGHT)

def drawQuinticCoherentNoise2D():
    WIDTH = 400
    HEIGHT = 400
    w = Window(WIDTH, HEIGHT)
    color_buf = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            color_buf.append(0.0)  # R
            color_buf.append(0.0)  # G
            color_buf.append(0.0)  # B
            
    for i in range(HEIGHT):
        for j in range(WIDTH):
            x = i / 10.0
            y = j / 10.0
            v = coherent_noise_quintic_2D(x,y)
            v = (v + 1.0) / 2.0
            color_buf[i * WIDTH * 3 + j * 3 + 0] = v
            color_buf[i * WIDTH * 3 + j * 3 + 1] = v
            color_buf[i * WIDTH * 3 + j * 3 + 2] = v
    w.save("2dquintic.png", color_buf, WIDTH, HEIGHT)
    
if __name__ == "__main__":
    drawLinearCoherentNoise2D()
    drawCubicCoherentNoise2D()
    drawQuinticCoherentNoise2D()

