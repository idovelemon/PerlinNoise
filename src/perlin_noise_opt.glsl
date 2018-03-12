// Author: i_dovelemon[1322600812@qq.com]
// Date: 2018-03-12
// Brief: 3D Perlin noise for 2D Perlin noise animation

// Gradients
vec3 Gradients[12] = vec3[12](
    vec3(1,1,0),vec3(-1,1,0),vec3(1,-1,0),vec3(-1,-1,0),
    vec3(1,0,1),vec3(-1,0,1),vec3(1,0,-1),vec3(-1,0,-1),
    vec3(0,1,1),vec3(0,-1,1),vec3(0,1,-1),vec3(0,-1,-1)
);

// Trilinear interpolating method
vec3 quintic(vec3 x) {
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0);
}

// Hash Function from https://www.shadertoy.com/view/4djSRW
float hash(vec3 v) {
    float HASHSCALE = 0.1031;
    v  = fract(v * HASHSCALE);
    v += dot(v, v.yzx + 19.19);
    return fract((v.x + v.y) * v.z);
}

// 3D Perlin noise <optimization way>
float noise01(float x, float y, float z) {
    vec3 p = floor(vec3(x, y, z));
    vec3 t = vec3(x, y, z) - p;
    vec3 f = quintic(t);

    vec3 v0 = p + vec3(0.0, 0.0, 0.0);
    vec3 v1 = p + vec3(1.0, 0.0, 0.0);
    vec3 v2 = p + vec3(0.0, 1.0, 0.0);
    vec3 v3 = p + vec3(1.0, 1.0, 0.0);
    vec3 v4 = v0 + vec3(0.0, 0.0, 1.0);
    vec3 v5 = v1 + vec3(0.0, 0.0, 1.0);
    vec3 v6 = v2 + vec3(0.0, 0.0, 1.0);
    vec3 v7 = v3 + vec3(0.0, 0.0, 1.0);

    vec3 g0 = Gradients[int(hash(v0) * 12.0)];
    vec3 g1 = Gradients[int(hash(v1) * 12.0)];
    vec3 g2 = Gradients[int(hash(v2) * 12.0)];
    vec3 g3 = Gradients[int(hash(v3) * 12.0)];
    vec3 g4 = Gradients[int(hash(v4) * 12.0)];
    vec3 g5 = Gradients[int(hash(v5) * 12.0)];
    vec3 g6 = Gradients[int(hash(v6) * 12.0)];
    vec3 g7 = Gradients[int(hash(v7) * 12.0)];

    return mix(
        mix(
            mix(dot(g0, t - vec3(0.0, 0.0, 0.0)), dot(g1, t - vec3(1.0, 0.0, 0.0)), f.x),
            mix(dot(g2, t - vec3(0.0, 1.0, 0.0)), dot(g3, t - vec3(1.0, 1.0, 0.0)), f.x),
            f.y
        ),
        mix(
            mix(dot(g4, t - vec3(0.0, 0.0, 1.0)), dot(g5, t - vec3(1.0, 0.0, 1.0)), f.x),
            mix(dot(g6, t - vec3(0.0, 1.0, 1.0)), dot(g7, t - vec3(1.0, 1.0, 1.0)), f.x),
            f.y
        ),
        f.z
    );
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Output to screen
    float noise_scale = 0.05;
    float noise_animation_speed = 1.0;
    float v = noise01(fragCoord.x * noise_scale, fragCoord.y * noise_scale, iTime * noise_animation_speed);
    v = (v + 1.0) / 2.0;
    fragColor = vec4(v, v, v, 1.0);
}