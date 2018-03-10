"""
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/20
    Brief: Perlin Nosie Genrator
"""

import math
import random

__all__ = ["PerlinNoise2D", "PerlinNoise3D",]

class _Vec2:
  """2D Vector"""
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

class _Vec3:
  """3D Vector"""
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def length(self):
    return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
  
  def normalize(self):
    l = self.length()
    if l == 0.0:
      l = 1.0
    self.x = self.x / l
    self.y = self.y / l
    self.z = self.z / l

  def dot(self, v):
    return self.x * v.x + self.y * v.y + self.z * v.z

class PerlinNoise2D:
  """Generate 2D Perlin classic noise

  This class use the classic Perlin noise algorithm to generate 2D perlin noise
  """
  _ARRAY_SIZE = 256
  
  def __init__(self, seed):
    random.seed(seed)
    
    self._rand_gradient = []
    self._permutation_tbl = []
    
    for i in range(PerlinNoise2D._ARRAY_SIZE):
      v = _Vec2(random.uniform(-1,1), random.uniform(-1,1))
      v.normalize()
      self._rand_gradient.append(v)
      self._permutation_tbl.append(i)

    for i in range(PerlinNoise2D._ARRAY_SIZE):
      self._permutation_tbl.append(0)

    for i in range(PerlinNoise2D._ARRAY_SIZE):
      idx = random.randint(0, 256)
      temp = self._permutation_tbl[idx]
      self._permutation_tbl[idx] = self._permutation_tbl[i]
      self._permutation_tbl[i] = temp
      self._permutation_tbl[i + PerlinNoise2D._ARRAY_SIZE] = self._permutation_tbl[i]

  def noise(self, x, y):
    """ Generate one perlin noise value

    Input a 2d coordinate (x,y), this method will calculate a matching perlin noise value

    Args:
      x: 2d coordinate's x value
      y: 2d coordinate's y value

    Notes:
      Avoiding use full interger number 2d coordinates for generating noise,
      i.e 1,2,3,4,5..... for x and y.
      Because perlin noise 2d will generate 0 noise value at interger number 2d coordinates.

    Return:
      A 2d perlin noise value which in range [-1, 1]
    """
    def _quintic(x):
      return 6.0 * x * x * x * x * x - 15.0 * x * x * x * x + 10.0 * x * x * x
    
    # Calculate grid point coordinate
    xi = math.floor(x)
    yi = math.floor(y)

    # Calculate the interpolating weight
    tx = x - xi
    ty = y - yi

    # Calculate coordinate in one cycle
    x0 = int(int(xi) % PerlinNoise2D._ARRAY_SIZE)
    y0 = int(int(yi) % PerlinNoise2D._ARRAY_SIZE)
    x1 = int(int(x0 + 1) % PerlinNoise2D._ARRAY_SIZE)
    y1 = y0
    x2 = x0
    y2 = int(int(y0 + 1) % PerlinNoise2D._ARRAY_SIZE)
    x3 = x1
    y3 = y2

    # Get random gradient
    v0 = self._rand_gradient[self._permutation_tbl[self._permutation_tbl[x0] + y0]]
    v1 = self._rand_gradient[self._permutation_tbl[self._permutation_tbl[x1] + y1]]
    v2 = self._rand_gradient[self._permutation_tbl[self._permutation_tbl[x2] + y2]]
    v3 = self._rand_gradient[self._permutation_tbl[self._permutation_tbl[x3] + y3]]

    # Calculate bound point to current point's vec
    tv0 = _Vec2(tx, ty)
    tv1 = _Vec2(tx - 1.0, ty)
    tv2 = _Vec2(tx, ty - 1.0)
    tv3 = _Vec2(tx - 1.0, ty - 1.0)

    # Calculate the random values
    r0 = v0.dot(tv0)
    r1 = v1.dot(tv1)
    r2 = v2.dot(tv2)
    r3 = v3.dot(tv3)

    # Bilinear interpolating with quintic curve
    ru = r0 + (r1 - r0) * _quintic(tx)
    rd = r2 + (r3 - r2) * _quintic(tx)
    return ru + (rd - ru) * _quintic(ty)

class PerlinNoise3D:
  """Generate 3D Perlin classic noise

  This class use the classic Perlin noise algorithm to generate 3D perlin noise
  """
  _ARRAY_SIZE = 256
  
  def __init__(self, seed):    
    self._gradient = [
      _Vec3(1,1,0),_Vec3(-1,1,0),_Vec3(1,-1,0),_Vec3(-1,-1,0),
      _Vec3(1,0,1),_Vec3(-1,0,1),_Vec3(1,0,-1),_Vec3(-1,0,-1),
      _Vec3(0,1,1),_Vec3(0,-1,1),_Vec3(0,1,-1),_Vec3(0,-1,-1),
    ]
    self._permutation_tbl = [
      151,160,137,91,90,15,
      131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
      190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,
      88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
      77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,
      102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
      135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,
      5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
      223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,
      129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
      251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,
      49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
      138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]

    for i in range(PerlinNoise2D._ARRAY_SIZE):
      self._permutation_tbl.append(0)

    for i in range(PerlinNoise2D._ARRAY_SIZE):
      self._permutation_tbl[i + PerlinNoise2D._ARRAY_SIZE] = self._permutation_tbl[i]

  def noise(self, x, y, z):
    """ Generate one perlin noise value

    Input a 3d coordinate (x,y,z), this method will calculate a matching perlin noise value

    Args:
      x: 3d coordinate's x value
      y: 3d coordinate's y value
      z: 3d coordinate's z value

    Notes:
      Avoiding use full interger number 3d coordinates for generating noise,
      i.e 1,2,3,4,5..... for x and y.
      Because perlin noise 3d will generate 0 noise value at interger number 3d coordinates.

    Return:
      A 3d perlin noise value which in range [-1, 1]
    """
    def _quintic(x):
      return 6.0 * x * x * x * x * x - 15.0 * x * x * x * x + 10.0 * x * x * x
    
    # Calculate grid point coordinate
    xi = math.floor(x)
    yi = math.floor(y)
    zi = math.floor(z)

    # Calculate the interpolating weight
    tx = x - xi
    ty = y - yi
    tz = z - zi

    # Calculate coordinate in one cycle
    x0 = int(int(xi) % PerlinNoise2D._ARRAY_SIZE)
    y0 = int(int(yi) % PerlinNoise2D._ARRAY_SIZE)
    z0 = int(int(zi) % PerlinNoise2D._ARRAY_SIZE)

    x1 = int(int(x0 + 1) % PerlinNoise2D._ARRAY_SIZE)
    y1 = y0
    z1 = z0

    x2 = x0
    y2 = int(int(y0 + 1) % PerlinNoise2D._ARRAY_SIZE)
    z2 = z0

    x3 = x1
    y3 = y2
    z3 = z0

    x4 = x0
    y4 = y0
    z4 = int(int(z0 + 1) % PerlinNoise2D._ARRAY_SIZE)

    x5 = x1
    y5 = y0
    z5 = z4

    x6 = x0
    y6 = y2
    z6 = z4

    x7 = x1
    y7 = y2
    z7 = z4

    # Get random gradient
    v0 = self._gradient[self._permutation_tbl[z0 + self._permutation_tbl[y0 + self._permutation_tbl[x0]]] % 12]
    v1 = self._gradient[self._permutation_tbl[z1 + self._permutation_tbl[y1 + self._permutation_tbl[x1]]] % 12]
    v2 = self._gradient[self._permutation_tbl[z2 + self._permutation_tbl[y2 + self._permutation_tbl[x2]]] % 12]
    v3 = self._gradient[self._permutation_tbl[z3 + self._permutation_tbl[y3 + self._permutation_tbl[x3]]] % 12]
    v4 = self._gradient[self._permutation_tbl[z4 + self._permutation_tbl[y4 + self._permutation_tbl[x4]]] % 12]
    v5 = self._gradient[self._permutation_tbl[z5 + self._permutation_tbl[y5 + self._permutation_tbl[x5]]] % 12]
    v6 = self._gradient[self._permutation_tbl[z6 + self._permutation_tbl[y6 + self._permutation_tbl[x6]]] % 12]
    v7 = self._gradient[self._permutation_tbl[z7 + self._permutation_tbl[y7 + self._permutation_tbl[x7]]] % 12]
    # v0.normalize()
    # v1.normalize()
    # v2.normalize()
    # v3.normalize()
    # v4.normalize()
    # v5.normalize()
    # v6.normalize()
    # v7.normalize()

    # Calculate bound point to current point's vec
    tv0 = _Vec3(tx, ty, tz)
    tv1 = _Vec3(tx - 1.0, ty, tz)
    tv2 = _Vec3(tx, ty - 1.0, tz)
    tv3 = _Vec3(tx - 1.0, ty - 1.0, tz)
    tv4 = _Vec3(tx, ty, tz - 1.0)
    tv5 = _Vec3(tx - 1.0, ty, tz - 1.0)
    tv6 = _Vec3(tx, ty - 1.0, tz - 1.0)
    tv7 = _Vec3(tx - 1.0, ty - 1.0, tz - 1.0)

    # Calculate the random values
    r0 = v0.dot(tv0)
    r1 = v1.dot(tv1)
    r2 = v2.dot(tv2)
    r3 = v3.dot(tv3)
    r4 = v4.dot(tv4)
    r5 = v5.dot(tv5)
    r6 = v6.dot(tv6)
    r7 = v7.dot(tv7)    

    # Trilinear interpolating with quintic curve
    ru0 = r0 + (r1 - r0) * _quintic(tx)
    ru1 = r2 + (r3 - r2) * _quintic(tx)
    ru = ru0 + (ru1 - ru0) * _quintic(ty)

    rd0 = r4 + (r5 - r4) * _quintic(tx)
    rd1 = r6 + (r7 - r6) * _quintic(tx)
    rd = rd0 + (rd1 - rd0) * _quintic(ty)
    return ru + (rd - ru) * _quintic(tz)

if __name__ == "__main__":
  print("Use test.py to check examples")