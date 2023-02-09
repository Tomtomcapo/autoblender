import inspect
from pprint import pprint
import bpy
import json

import mathutils
import yaml
import itertools

def create_available_parameters_file(obj, path="", processed_ids=None, exclude=[]):
    if processed_ids is None:
        processed_ids = set()

    members_tree = {}
    obj_id = id(obj)
    if obj_id in processed_ids:
        return members_tree
    processed_ids.add(obj_id)

    for name in dir(obj):
        if name.startswith("__") or name.startswith("_") or name in exclude:
            continue
        try:
            value = getattr(obj, name)

            if not callable(value) and not inspect.isroutine(value) and not isinstance(value, (mathutils.Vector, mathutils.Matrix, mathutils.Quaternion, mathutils.Euler)):
                if isinstance(value, (int, float, str)):
                    members_tree[name] = "disabled"
                else:
                    sub_tree = create_available_parameters_file(value, path + "." + name if path else name, processed_ids, exclude=exclude)
                    if sub_tree:
                        members_tree[name] = sub_tree
        except Exception:
            continue
    return members_tree

exclusion = [
    "identifier",
    "description",
    "rna_type",
    "active_object",
    "asset_library_ref",
    "bl_rna",
    "blend_data",
    "collection",
    "layer_collection",
    "object",
    "data",
]

scene_params = {"scene": create_available_parameters_file(bpy.context.scene, exclude=exclusion)}

yaml_string = yaml.dump(scene_params, default_flow_style=False)
with open('../../config/available_settings.yml', 'w') as file:
    file.write(yaml_string)

