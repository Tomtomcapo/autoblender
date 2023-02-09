# AutoBlender

AutoBlender is a powerful tool that simplifies and automates your Blender rendering tasks. With this tool, you can run a highly configurable Blender render pipeline through the terminal or a script, while also maintaining full control over the rendering parameters, Cycles engine, scene, and more. The parameters are contained within a YAML file, making it easy to version and maintain.

AutoBlender is highly suitable for automation and automated rendering, making it perfect for use in Blender farms or pipelines. Additionally, the tool's logs are easy to parse and interpret, allowing for easy monitoring of your rendering processes. With more than 500 available parameters, you have full control over which parameters are included in the rendering configuration file.

In short:
- AutoBlender offers a streamlined and efficient solution for Blender rendering workflows.
- The customizable render pipeline, which can be run through a terminal or script, provides comprehensive control over Blender rendering parameters.
- The use of a YAML-based configuration system helps to maintain the organization and versioning of rendering parameters.
- AutoBlender is well-suited for automation and large-scale rendering tasks, making it an ideal tool for use in Blender farms or pipelines.
- Detailed logs provide insight into the progress of render processes and support efficient monitoring.
- The wide range of available parameters allows for precise control over every aspect of the render process.

AutoBlender uses bpy from pip to run the render. Blender binaries are not needed inside the host system.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contribute](#contribute)
- [License](#license)

## Installation

To install AutoBlender, simply clone this repository and run:

```
pip install -r requirements.txt
```

## Getting started

To run AutoBlender, simply navigate to the src/renderer-cli/ directory and execute the following command:

```
python autoblender.py [file] [-s --settings file] [-d --dry-run]
```

- `file`: .blend file, mandatory
- `-s --settings`: (optional) generally render_settings.yml, contains all the settings for the render, if not set, it will find this file in the same folder as the blender file, and if not found, parameters from the blender file will be used
- `-d --dry-run`: (optional) if set, do not launch the render but only logs some summary and analytics computed from the scene

This will print a summary of the specified parameters, analytics, and launch the render.

## Examples

Consider the following example:

```
python autoblender.py myfile.blend -s render_settings.yml
```
This will run AutoBlender using the myfile.blend file and the settings specified in render_settings.yml.

For more information on how to configure AutoBlender, please refer to the config/ directory, specifically the render_settings.template.yml file, which contains an example of the settings that can be specified. Additionally, the config/available_settings.yml file contains all the available parameters for AutoBlender and is directly derived from the parameters in a Blender file.

## Contribute

Instructions on how to contribute to your project.

## License

The name of the license under which your project is published.