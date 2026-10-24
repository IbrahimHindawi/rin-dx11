# rin-dx11

[LearnOpenGL](https://learnopengl.com/)'s lessons, from the first window to
image based PBR, rewritten for Windows and Direct3D 11 in
[rin](https://github.com/IbrahimHindawi/rin).

Every lesson is a standalone program in its own folder, laid out like the
[LearnOpenGL repository](https://github.com/JoeyDeVries/LearnOpenGL): one
source file that creates its window, its device and swap chain, its buffers
and textures, and runs its own render loop, with its shaders beside it.

## Layout

    src/
      1.getting_started/
        2.1.hello_triangle/
          hello_triangle.rin      the program
          hello_triangle.hlsl     its shaders (vs_main, ps_main)
      ...
    includes/
      win32.rin                   Win32, D3D11, DXGI, D3DCompile, WIC declarations
      math.rin                    vectors and matrices
      image.rin                   .png/.jpg through WIC, Radiance .hdr
      learn/
        filesystem.rin            paths under the repository root
        shader.rin                compile a .hlsl file, create its input layout
        camera.rin                the fly camera
        model.rin                 Wavefront .obj models and their textures
    resources/                    textures, models, the HDR environment

`includes/` plays the part LearnOpenGL's `includes/` does. `win32.rin`,
`math.rin` and `image.rin` stand in for glad and GLFW, glm and stb_image;
`learn/` holds the small helpers its `learnopengl/` folder holds (`shader.h`,
`camera.h`, `model.h`, `filesystem.h`). Nothing third-party is involved: the
window is Win32, images are decoded by Windows' own WIC, shaders are compiled
by `D3DCompile`, and the rest is rin.

## Build and run

Needs the rin compiler (`rin-windows-x64`, or `rin.exe` on `PATH`), CMake,
Ninja, clang-cl and the Windows SDK.

    rin build
    build\cmake\hello_triangle.exe

Each lesson builds to an executable named after its file. Lessons find
`resources/` and their shaders by walking up from the executable, so they run
from anywhere.

`python tools/screenshot.py` runs every built lesson, captures its window and
writes the pictures to `shots/`; that is how each lesson here was checked.

| key | does |
|---|---|
| W A S D, Space, Shift | fly (from 1.7 camera on) |
| right mouse + drag | look around |
| wheel | zoom |
| Tab, 1..6 | each lesson's modes, named in its window title |
| Esc | quit |

## How to read it

Read each lesson's `.rin` file top to bottom: it opens with what the lesson is
about, and the code follows the order LearnOpenGL's does (settings, window,
device, shaders, data, render loop). Early lessons write out every D3D11
call; 2.1 hello triangle compiles its shaders by hand, and from 3.1 shaders on
`learn/shader.rin` does that part. The guides in `docs/` give the background a
single file has no room for, starting with how D3D11's conventions differ
from GL's.

## The lessons

| | lesson | about |
|---|---|---|
| **1** | [getting started](docs/1_getting_started.md) | |
| 1.1 | hello window | a window, a device, a clear colour |
| 2.1 | hello triangle | buffers, shaders, input layouts, indexed drawing |
| 3.1 | shaders | per-vertex data and constant buffers |
| 4.1 | textures | WIC images, mipmaps, samplers |
| 5.1 | transformations | matrices and their order |
| 6.1 | coordinate systems | model, view, projection; the depth buffer |
| 7.1 | camera | a fly camera from yaw and pitch |
| **2** | [lighting](docs/2_lighting.md) | |
| 1 | colors | light colour times surface colour |
| 2.1 | basic lighting | Phong: ambient, diffuse, specular |
| 3.1 | materials | per-term material and light colours |
| 4.1 | lighting maps | diffuse and specular textures |
| 5.1 | light casters | directional, point and spot lights |
| 6 | multiple lights | summing them |
| **3** | [model loading](docs/3_model_loading.md) | |
| 1 | model loading | an `.obj` backpack and its materials |
| **4** | [advanced D3D11](docs/4_advanced.md) | |
| 1.1 | depth testing | the depth buffer, and linear depth |
| 2 | stencil testing | outlines through the stencil buffer |
| 3.1 | blending | clipped grass, sorted transparent windows |
| 4 | face culling | winding and back faces |
| 5.1 | framebuffers | render to texture, post-processing |
| 6.1 | cubemaps | skybox, reflection, refraction |
| 7 | advanced data | dynamic and split vertex buffers |
| 8 | advanced HLSL | shared constant buffers, system values |
| 9.1 | geometry shader | exploding a model, drawing its normals |
| 10.1 | instancing | twenty thousand asteroids in one draw |
| 11.1 | anti-aliasing | MSAA and resolving it |
| **5** | [advanced lighting](docs/5_advanced_lighting.md) | |
| 1 | advanced lighting | Blinn-Phong, the halfway vector |
| 2 | gamma correction | sRGB textures and back buffer, linear lighting |
| 3.1 | shadow mapping | directional shadows, hardware PCF |
| 3.2 | point shadows | a depth cubemap in one pass |
| 4 | normal mapping | tangent space |
| 5.1 | parallax mapping | parallax occlusion mapping |
| 6 | hdr | float targets and tone mapping |
| 7 | bloom | bright pass, ping-pong blur |
| 8.1 | deferred shading | the G-buffer, 32 lights |
| 9 | ssao | screen-space ambient occlusion |
| **6** | [pbr](docs/6_pbr.md) | |
| 1.1 | lighting | Cook-Torrance, metallic and roughness |
| 2.1 | ibl irradiance | lighting by an HDR environment |
| 2.2 | ibl specular | prefiltered reflections, the BRDF table |

LearnOpenGL splits some lessons into variants (2.2 hello_triangle_indexed,
3.2 shaders_interpolation, 1.2 lighting_textured, ...). Here each lesson keeps
its variants together as modes, switched with Tab or the number keys.

## Credits

The lessons follow LearnOpenGL by Joey de Vries, rewritten rather than
translated; its code is CC BY-NC 4.0, and so is this. The textures, models and
HDR environment come from the LearnOpenGL repository. See
[NOTICE.md](NOTICE.md).
