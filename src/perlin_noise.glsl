// Author: i_dovelemon[1322600812@qq.com]
// Date: 2018-03-09
// Brief: 3D Perlin noise for 2D Perlin noise animation

// Size
float ARRAY_SIZE = 256.0;

// Gradients
vec3 Gradients[12] = vec3[12](
    vec3(1,1,0),vec3(-1,1,0),vec3(1,-1,0),vec3(-1,-1,0),
    vec3(1,0,1),vec3(-1,0,1),vec3(1,0,-1),vec3(-1,0,-1),
    vec3(0,1,1),vec3(0,-1,1),vec3(0,1,-1),vec3(0,-1,-1)
);

// Permutation Table
int Permutations[512] = int[512](
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
      138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180,
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
      138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180          
);

// Trilinear interpolating method
vec3 quintic(vec3 x) {
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0);
}

// 3D Perlin noise <brute force way>
float noise01(float x, float y, float z) {
    // Calculate grid point coordinate
    vec3 p = floor(vec3(x, y, z));

    // Calculate the interpolating weight
    vec3 t = vec3(x, y, z) - p;

    // Calculate coordinate in one cycle
    float x0 = mod(p.x, ARRAY_SIZE);
    float y0 = mod(p.y, ARRAY_SIZE);
    float z0 = mod(p.z, ARRAY_SIZE);

    //float x1 = mod(x0 + 1.0, ARRAY_SIZE);
    float x1 = x0 + 1.0;
    float y1 = y0;
    float z1 = z0;

    float x2 = x0;
    //float y2 = mod(y0 + 1.0, ARRAY_SIZE);
    float y2 = y0 + 1.0;
    float z2 = z0;

    float x3 = x1;
    float y3 = y2;
    float z3 = z0;

    float x4 = x0;
    float y4 = y0;
    //float z4 = mod(z0 + 1.0, ARRAY_SIZE);
    float z4 = z0 + 1.0;

    float x5 = x1;
    float y5 = y0;
    float z5 = z4;

    float x6 = x0;
    float y6 = y2;
    float z6 = z4;

    float x7 = x1;
    float y7 = y2;
    float z7 = z4;

    // Get random gradients
    vec3 v0 = Gradients[Permutations[int(z0) + Permutations[int(y0) + Permutations[int(x0)]]] % 12];
    vec3 v1 = Gradients[Permutations[int(z1) + Permutations[int(y1) + Permutations[int(x1)]]] % 12];
    vec3 v2 = Gradients[Permutations[int(z2) + Permutations[int(y2) + Permutations[int(x2)]]] % 12];
    vec3 v3 = Gradients[Permutations[int(z3) + Permutations[int(y3) + Permutations[int(x3)]]] % 12];
    vec3 v4 = Gradients[Permutations[int(z4) + Permutations[int(y4) + Permutations[int(x4)]]] % 12];
    vec3 v5 = Gradients[Permutations[int(z5) + Permutations[int(y5) + Permutations[int(x5)]]] % 12];
    vec3 v6 = Gradients[Permutations[int(z6) + Permutations[int(y6) + Permutations[int(x6)]]] % 12];
    vec3 v7 = Gradients[Permutations[int(z7) + Permutations[int(y7) + Permutations[int(x7)]]] % 12];

    // Calculate bound point to current point's vec
    vec3 tv0 = vec3(t.x, t.y, t.z);
    vec3 tv1 = vec3(t.x - 1.0, t.y, t.z);
    vec3 tv2 = vec3(t.x, t.y - 1.0, t.z);
    vec3 tv3 = vec3(t.x - 1.0, t.y - 1.0, t.z);
    vec3 tv4 = vec3(t.x, t.y, t.z - 1.0);
    vec3 tv5 = vec3(t.x - 1.0, t.y, t.z - 1.0);
    vec3 tv6 = vec3(t.x, t.y - 1.0, t.z - 1.0);
    vec3 tv7 = vec3(t.x - 1.0, t.y - 1.0, t.z - 1.0);

    // Calculate the random values
    float r0 = dot(v0, tv0);
    float r1 = dot(v1, tv1);
    float r2 = dot(v2, tv2);
    float r3 = dot(v3, tv3);
    float r4 = dot(v4, tv4);
    float r5 = dot(v5, tv5);
    float r6 = dot(v6, tv6);
    float r7 = dot(v7, tv7);

    // Trilinear interpolating with quintic curve
    vec3 f = quintic(t);
    return mix(
        mix(
            mix(r0, r1, f.x),
            mix(r2, r3, f.x),
            f.y
        ),
        mix(
            mix(r4, r5, f.x),
            mix(r6, r7, f.x),
            f.y
        ),
        f.z
        );
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    // Output to screen
    float noise_scale = 0.05;
    float noise_animation_speed = 0.1;
    float v = noise01(fragCoord.x * noise_scale, fragCoord.y * noise_scale, iTime * noise_animation_speed);
    v = (v + 1.0) / 2.0;
    fragColor = vec4(v, v, v, 1.0);
}