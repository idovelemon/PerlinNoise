"""
    Author: i_dovelemon[1322600812@qq.com]
    Date: 2018/03/08
    Brief: Test Perlin Nosie Genrator
"""

import tkinter
import perlin_noise

if __name__ == "__main__":
    def _draw_perlin_noise_2d():
        perlin = perlin_noise.PerlinNoise2D(0)

        tk = tkinter.Tk()
        canvas = tkinter.Canvas(tk, width = 256, height = 256, bg = "black")
        canvas.pack()

        noise_scale = 0.01

        for i in range(256):
            for j in range(256):
                noise = perlin.noise(i * noise_scale, j * noise_scale)
                noise = (noise + 1.0) / 2.0
                noise = int(noise * 256)
                canvas.create_line(i, j, i + 1, j, fill = "#%02x%02x%02x" % (noise, noise, noise))
        
        tk.mainloop()

    def _draw_octave_noise_2d():
        octave = perlin_noise.OctaveNoise2D(4, 0, 1.0, 1.0)

        tk = tkinter.Tk()
        canvas = tkinter.Canvas(tk, width = 256, height = 256, bg = "black")
        canvas.pack()

        noise_scale = 0.1

        for i in range(256):
            for j in range(256):
                noise = octave.noise(i * noise_scale, j * noise_scale)
                noise = (noise + 1.0) / 2.0
                noise = int(noise * 256)
                canvas.create_line(i, j, i + 1, j, fill = "#%02x%02x%02x" % (noise, noise, noise))
        
        tk.mainloop()

    #_draw_perlin_noise_2d()
    _draw_octave_noise_2d()
