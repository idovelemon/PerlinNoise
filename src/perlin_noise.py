"""
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2017/05/20
    Brief: Perlin Nosie Genrator
"""

import math
import random

__all__ = ["PerlinNoise2D", "OctaveNoise2D"]

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

class OctaveNoise2D:
  """ Generate 2D Octave noise

  Use the 2D Perlin noise to generate octave noise
  """
  def __init__(self, num_layers, seed, begin_frequency, begin_amplitude):
    """ Init octave noise 2d

    Args:
      num_layers: Octave layers number
      seed: Perlin noise random seed
      begin_frequency: The first frequency, all other layers' frequency will be begin_frequency * pow(2, i)
      begin_amplitude: The first amplitude, all other layers' amplitude will be begin_amplitude / pow(2, i)
    """
    self._perlin = PerlinNoise2D(seed)
    self._layers = num_layers
    self._begin_frequency = begin_frequency
    self._begin_amplitude = begin_amplitude
    self._max_amplitude = 0.0

    for i in range(self._layers):
      self._max_amplitude = self._max_amplitude + self._begin_amplitude / pow(2, i)

  def noise(self, x, y):
    """ Generate one octave noise value

    Input a 2d coordinate (x,y), this method will calculate a matching octave noise value

    Args:
      x: 2d coordinate's x value
      y: 2d coordinate's y value

    Notes:
      Avoiding use full interger number 2d coordinates for generating noise,
      i.e 1,2,3,4,5..... for x and y.
      Because octave noise 2d will generate 0 noise value at interger number 2d coordinates.      

    Return:
      A 2d octave noise value which in range [-1, 1]
    """    
    v = 0.0

    for i in range(self._layers):
      tx = x * self._begin_frequency * pow(2, i)
      ty = y * self._begin_frequency * pow(2, i)
      ta = 1.0 * self._begin_amplitude / pow(2, i)
      v = v + self._perlin.noise(tx, ty) * ta

    # normliaze
    v = v / self._max_amplitude

    return v

if __name__ == "__main__":
  print("Use test.py to check examples")