# KotorBlender

This add-on is a fork of KotORBlender 1.01 by Purifier and Ndix UR, upgraded to support Blender versions 2.80 and above, which are notable by a redesigned user interface and a new real-time render engine. KotORBlender is in turn based on NeverBlender by Symmetric, forked from version 1.23a.

Significant changes have been introduced since KotORBlender 1.01, including, but not limited to, replacing ASCII model import/export with binary format, and ability to import/export layouts and path files.

## Features

- Import & export MDL models, including animations and walkmeshes
- Import & export LYT files
- Import & export PTH files
- Lightmap texture baking
- Area minimap rendering

## Compatibility

Current version of KotorBlender is tested against the following Blender LTS releases. Blender 4.2 introduced extensions, and earlier releases install KotorBlender as an add-on instead.

| Blender LTS | Installs as |
|---|---|
| 5.2 | Extension |
| 4.5 | Extension |
| 4.2 | Extension |
| 3.6 | Add-on |
| 3.3 | Add-on |
| 2.93 | Add-on |
| 2.83 | Add-on |

Blender development moves fast and is known to introduce breaking changes, therefore compatibility with any other version of Blender, including non-LTS releases, is not guaranteed.

## Installation

### From GitHub Releases

1. Open the [latest release](https://github.com/OpenKotOR/kotorblender/releases/latest)
1. Download the archive for your Blender version and install it:

| Blender | Archive | Install via |
|---|---|---|
| 4.2 and later | **io_scene_kotor-*version*.zip** | Edit → Preferences → Get Extensions → Install from Disk, as described in the [Blender documentation](https://docs.blender.org/manual/en/4.2/editors/preferences/extensions.html#bpy-ops-extensions-package-install-files) |
| 3.6 and earlier | **io_scene_kotor-*version*-addon.zip** | Edit → Preferences → Add-ons → Install |

### From Source

1. Clone [GitHub repository](https://github.com/OpenKotOR/kotorblender)
1. Set cloned repository as current directory
1. Create a symlink to the **io_scene_kotor** directory in the directory your Blender version reads, adjusting the Blender version number in the path:

| Blender | Symlink on Windows | Symlink on Linux |
|---|---|---|
| 4.2 and later | `mklink /D "%APPDATA%\Blender Foundation\Blender\5.2\extensions\user_default\io_scene_kotor" "%CD%/io_scene_kotor"` | `ln -s $(pwd)/io_scene_kotor ~/.config/blender/5.2/extensions/user_default/io_scene_kotor` |
| 3.6 and earlier | `mklink /D "%APPDATA%\Blender Foundation\Blender\3.6\scripts\addons\io_scene_kotor" "%CD%/io_scene_kotor"` | `ln -s $(pwd)/io_scene_kotor ~/.config/blender/3.6/scripts/addons/io_scene_kotor` |

### Original Releases

The original KotorBlender releases by seedhartha remain available on [Deadly Stream](https://deadlystream.com/files/file/1853-kotorblender-for-blender-293/). They are published separately from the releases in this repository.

## Usage

### Data Preparation

Extract models, textures, walkmeshes, LYT and PTH files into a working directory, using a tool of your choice, e.g. [reone toolkit](https://deadlystream.com/files/file/1862-reone-toolkit/). Recommended directory structure:

- *data* — extract all BIF archives here without subdirectories
- *texturepacks*
  - *swpc_tex_tpa* — extract swpc_tex_tpa ERF archive here

If you plan to edit textures, batch-convert TPC to TGA / TXI files using **reone toolkit**, although TPC textures are also supported by KotorBlender.

### Model Import and Export

1. Import via File → Import → KotOR Model (.mdl)
1. Select top-level MDL root object to be exported
1. Export via File → Export → KotOR Model (.mdl)

### Editing Animations

To edit list of model animations and corresponding events, select MDL root object and navigate to Object → KotOR Animations. KotorBlender supports both object and armature-based edits. To create an armature from objects, navigate to KotOR Animations → Armature and press Rebuild Armature and Apply Object Keyframes. Before exporting a model, make sure to copy armature keyframes back to objects by pressing Unapply Object Keyframes.

### Lightmapping

1. Select objects for which you want lightmaps to be recreated, or unselect all objects to recreate all lightmaps
1. Press KotOR → Lightmaps → Bake (auto)
1. Open and save each individual lightmap image from UV Editing tab

UV mapping:

1. Select objects having the same lightmap texture and enter Edit mode
1. For every object, ensure that `UVMap_lm` UV layer is active
1. Select all faces and unwrap UVs via UV → Lightmap Pack, increase Margin to avoid face overlapping

Fine-tuning:

1. Increase lightmap image size via UV Editing → Image → Resize
1. Tweak ambient color via Scene → World → Surface → Color
1. Manually toggle rendering of objects in Outliner and press KotOR → Lightmaps → Bake (manual)
1. In Scene → Render, set Device to GPU Compute to improve performance, set Render Engine to Cycles if not already
1. In Scene → Render → Sampling → Render increase Max Samples to improve quality

### Minimap Rendering

1. Press KotOR → Minimap → Render (auto)
1. Open "Render Result" image in UV Editing tab and save it as "lbl_map{modulename}.tga"
1. Open "MinimapCoords" text in Scripting tab and copy-paste generated properties into module .ARE file using any GFF editor

Fine-tuning:

1. Tweak background color via Scene → World → Surface → Color
1. Manually toggle rendering of objects in Outliner and press KotOR → Minimap → Render (manual)

### Connecting Rooms

1. Select a room walkmesh
1. Enter Edit mode and select two vertices adjacent to another room
1. Determine 0-based index of the other room into the LYT file
1. Enter Vertex Paint mode and set brush color to (0.0, G, 0.0), where G = (200 + room index) / 255
1. Ensure that brush blending mode is set to Mix, and brush strength is set to 1.0
1. Paint over the selected vertices

### Editing Paths

1. Extract PTH file from the module's RIM file, e.g. "modules/danm13_s.rim" (Kotor Tool, reone toolkit, etc.)
1. Import PTH into Blender via File → Import → KotOR Path (.pth)
1. Create/move path points, or modify path connections via Object Properties
1. Export PTH via File → Export → KotOR Path (.pth)

## Credits

KotorBlender builds on the work of several authors:

- **NeverBlender** by Symmetric. KotORBlender was forked from version 1.23a.
- **KotORBlender 1.01** by Purifier and Ndix UR.
- **KotorBlender** by seedhartha, who upgraded it to Blender 2.80 and later and developed it up to version 4.0.3.
- **OpenKotOR**, who maintain this version of KotorBlender today.

Other contributors are listed in the [commit history](https://github.com/OpenKotOR/kotorblender/commits/master).

## License

[GPL 3.0 or later](LICENSE)
