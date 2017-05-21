#usr/env/bin python3.2


"""
    Declaration: Copyright (c), by i_dovelemon, 2017. All right reserved
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/20
    Brief: Perlin Nosie Genrator
"""


import math
import random

from window import *


__all__ = ["PerlinNoise2D", "BrownianNoise2D"]


#--------------------------------------------------------------
# 2D Perlin Noise Generator

class Vec2:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def length(self):
    return math.sqrt(self.x * self.x + self.y * self.y)
  
  def normalize(self):
    l = self.length()
    if l == 0.0:
      l = 1.0
    self.x = self.x / l
    self.y = self.y / l

  def dot(self, v):
    return self.x * v.x + self.y * v.y

class PerlinNoise2D:
  ARRAY_SIZE = 256
  
  def __init__(self, seed):
    random.seed(seed)
    
    self.randGradient = []
    self.permutationTbl = []
    
    for i in range(PerlinNoise2D.ARRAY_SIZE):
      v = Vec2(random.uniform(-1,1), random.uniform(-1,1))
      v.normalize()
      self.randGradient.append(v)
      self.permutationTbl.append(i)

    for i in range(PerlinNoise2D.ARRAY_SIZE):
      self.permutationTbl.append(0)

    for i in range(PerlinNoise2D.ARRAY_SIZE):
      idx = random.randint(0, 256)
      temp = self.permutationTbl[idx]
      self.permutationTbl[idx] = self.permutationTbl[i]
      self.permutationTbl[i] = temp
      self.permutationTbl[i + PerlinNoise2D.ARRAY_SIZE] = self.permutationTbl[i]

  def noise(self, x, y):
    def quintic(x):
      return 6.0 * x * x * x * x * x - 15.0 * x * x * x * x + 10.0 * x * x * x
    
    # Calculate grid point coordinate
    xi = math.floor(x)
    yi = math.floor(y)

    # Calculate the interpolating weight
    tx = x - xi
    ty = y - yi

    # Calculate coordinate in one cycle
    x0 = int(int(xi) % PerlinNoise2D.ARRAY_SIZE)
    y0 = int(int(yi) % PerlinNoise2D.ARRAY_SIZE)
    x1 = int(int(x0 + 1) % PerlinNoise2D.ARRAY_SIZE)
    y1 = y0
    x2 = x0
    y2 = int(int(y0 + 1) % PerlinNoise2D.ARRAY_SIZE)
    x3 = x1
    y3 = y2

    # Get random gradient
    v0 = self.randGradient[self.permutationTbl[self.permutationTbl[x0] + y0]]
    v1 = self.randGradient[self.permutationTbl[self.permutationTbl[x1] + y1]]
    v2 = self.randGradient[self.permutationTbl[self.permutationTbl[x2] + y2]]
    v3 = self.randGradient[self.permutationTbl[self.permutationTbl[x3] + y3]]

    # Calculate bound point to current point's vec
    tv0 = Vec2(tx, ty)
    tv1 = Vec2(tx - 1.0, ty)
    tv2 = Vec2(tx, ty - 1.0)
    tv3 = Vec2(tx - 1.0, ty - 1.0)

    # Calculate the random values
    r0 = v0.dot(tv0)
    r1 = v1.dot(tv1)
    r2 = v2.dot(tv2)
    r3 = v3.dot(tv3)

    # Bilinear interpolating with quintic curve
    ru = r0 + (r1 - r0) * quintic(tx)
    rd = r2 + (r3 - r2) * quintic(tx)
    return ru + (rd - ru) * quintic(ty)

class BrownianNoise2D:
  def __init__(self, num_layers, seed, begin_frequency, begin_amplitude):
    self.perlin = PerlinNoise2D(seed)
    self.layers = num_layers
    self.begin_frequency = begin_frequency
    self.begin_amplitude = begin_amplitude
    self.total_amplitude = 0.0
    for i in range(num_layers):
      self.total_amplitude = self.total_amplitude + 1.0 * self.begin_amplitude / pow(2, i)

  def noise(self, x, y):
    v = 0.0
    for i in range(self.layers):
      tx = x * self.begin_frequency * pow(2, i)
      ty = y * self.begin_frequency * pow(2, i)
      ta = 1.0 * self.begin_amplitude / pow(2, i)
      v = v + self.perlin.noise(tx, ty)* ta
    return v

  def normalize(self, v):
    v = v + self.total_amplitude
    v = v / 2.0 / self.total_amplitude
    return v
    
if __name__ == "__main__":
  #-------------------------------------------------------------------
  # Test code

  def drawPerlinNoise2D():
    WIDTH = 512
    HEIGHT = 512
    frequency = 16
    cycle = 256.0
    amplitude = 1.0
    stepx = frequency * 1.0 / WIDTH
    stepy = frequency * 1.0 / HEIGHT
    w = Window(WIDTH, HEIGHT)
    noise = PerlinNoise2D(2)
    
    color=[]
    for i in range(WIDTH):
      for j in range(HEIGHT):
        color.append(0)  # R
        color.append(0)  # G
        color.append(0)  # B
        
    for i in range(HEIGHT):
      for j in range(WIDTH):
        v = noise.noise(j * stepy, i * stepx) * amplitude
        v = (v + 1.0) / 2.0
        color[i * WIDTH * 3 + j * 3 + 0] = v
        color[i * WIDTH * 3 + j * 3 + 1] = v
        color[i * WIDTH * 3 + j * 3 + 2] = v

    w.save("GradientNoise2D.png", color, WIDTH, HEIGHT)

  def drawBrownianNoise2D():
    WIDTH = 512
    HEIGHT = 512
    stepx = 1.0 / WIDTH
    stepy = 1.0 / HEIGHT
    w = Window(WIDTH, HEIGHT)
    brownianNoise = BrownianNoise2D(5, 2, 1.0, 1.0)
    
    color=[]
    for i in range(WIDTH):
      for j in range(HEIGHT):
        color.append(0)  # R
        color.append(0)  # G
        color.append(0)  # B
        
    for i in range(HEIGHT):
      for j in range(WIDTH):
        v = brownianNoise.noise(j * stepy, i * stepx)
        v = brownianNoise.normalize(v)
        color[i * WIDTH * 3 + j * 3 + 0] = v
        color[i * WIDTH * 3 + j * 3 + 1] = v
        color[i * WIDTH * 3 + j * 3 + 2] = v

    w.save("BrownianNoise2D.png", color, WIDTH, HEIGHT)

  #drawPerlinNoise2D()
  drawBrownianNoise2D()
