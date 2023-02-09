import sys
import bpy
import os
import platform

from pathlib import Path
from src.autoblender.logger import *
from yaml import safe_load

from src.autoblender.singleton import Singleton


class RendererProcessor(object):
    __metaclass__ = Singleton

    AVAILABLE_SETTINGS_CONFIGURATION_FILE = f"..{os.sep}..{os.sep}config{os.sep}available_settings.yml"

    def __init__(self, blender_file: str, settings: dict, available_settings_file: str = AVAILABLE_SETTINGS_CONFIGURATION_FILE):
        self.blender_file = blender_file
        self.settings = settings
        self.available_settings_file = available_settings_file

    def apply_parameters_from_settings(self):
        """
        Apply all the parameters from the settings dictionary to the loaded blender file.
        :return:
        """
        # reset the filepath
        bpy.context.scene.render.filepath = f"//output{os.sep}frame_######"

        with open(self.available_settings_file, 'r') as stream:
            available_settings = safe_load(stream)

        def dict_to_path_dict(d, path=None):
            if path is None:
                path = []
            if not isinstance(d, dict):
                return {".".join(path): d}
            leaves = {}
            for k, v in d.items():
                leaves.update(dict_to_path_dict(v, path + [k]))
            return leaves

        def get_parameter_state(d, path):
            path_parts = path.split(".")
            for part in path_parts:
                d = d[part]
            return d

        flat_settings = dict_to_path_dict(self.settings)
        for key, val in flat_settings.items():
            state = get_parameter_state(available_settings, key)

            if state == "enabled":
                self.__set_parameter(bpy.context, key, val)
                log_info("parameter_set", f"Parameter '{key}' set to {val}.")

            elif state == "custom":
                # process custom
                if key == "scene.frame_current":
                    bpy.context.scene.frame_set(val)
                log_info("parameter_set", f"Custom action parameter '{key}' set to {val}.")
            elif state == "disabled":
                log_warning("parameter_not_set", f"Parameter '{key}' set to 'disabled', skipping.")
            else:
                raise Exception(f"Unrecognized state for parameter '{key}'")

    def __set_parameter(self, context, prop_path: str, value):
        props = prop_path.split('.')
        for prop in props[:-1]:
            context = getattr(context, prop)
        setattr(context, props[-1], value)

    def __get_leaf_nodes_and_paths(self, data, parent_key="root"):
        leaf_nodes_and_paths = []
        for key, value in data.items():
            if isinstance(value, dict):
                leaf_nodes_and_paths.extend(
                    self.__get_leaf_nodes_and_paths(value, parent_key + "." + key)
                )
            else:
                leaf_nodes_and_paths.append(
                    (parent_key + "." + key, value)
                )
        return leaf_nodes_and_paths

    def print_summary(self):
        """
        Print all the settings from the blender file to the console.
        :return:
        """

        def print_summary_element(key: str, val):
            log_info("summary", f"{key}:{val}")

        summary = {
            "file_name": self.blender_file,
            "output_folder": f"{Path(self.blender_file).parent.absolute()}{os.sep}output",
            "file_size": os.stat(self.blender_file).st_size,
            "platform": platform.platform(),
            "blender_version": bpy.app.version_string,
            "resolution_x": bpy.context.scene.render.resolution_x,
            "resolution_y": bpy.context.scene.render.resolution_y,
            "resolution_percentage": bpy.context.scene.render.resolution_percentage,
            "engine": bpy.context.scene.render.engine,
            "samples": bpy.context.scene.cycles.samples,
            "use_denoising": bpy.context.scene.cycles.use_denoising,
            "use_compositing": bpy.context.scene.render.use_compositing,
            "use_motion_blur": bpy.context.scene.render.use_motion_blur,
            "frame_start": bpy.context.scene.frame_start,
            "frame_end": bpy.context.scene.frame_end,
            "frame_current": bpy.context.scene.frame_current,
            "fps": bpy.context.scene.render.fps,
            "fps_base": bpy.context.scene.render.fps_base,
            "file_extension": bpy.context.scene.render.file_extension,
            "color_management.view_transform": bpy.context.scene.view_settings.view_transform,
            "color_management.look": bpy.context.scene.view_settings.look,
            "color_management.exposure": bpy.context.scene.view_settings.exposure,
            "color_management.gamma": bpy.context.scene.view_settings.gamma,
            "filepath": bpy.context.scene.render.filepath
        }

        for key, val in summary.items():
            print_summary_element(key, val)

    def print_analytics(self):
        """
        Print analytics generated from the scene data.
        :return:
        """
        # Initialize the polygon count
        polygon_count = 0
        vertex_count = 0
        edge_count = 0

        # Iterate through all the objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is a mesh
            if obj.type == 'MESH':
                # Add the number of polygons in the object's mesh data to the polygon count
                polygon_count += len(obj.data.polygons)
                vertex_count += len(obj.data.vertices)
                edge_count += len(obj.data.edges)

        def print_analytics_element(key: str, val):
            log_info("analytics", f"{key}:{val}")

        analytics = {
            "analytics.objects": len(bpy.data.objects),
            "analytics.polygons": polygon_count,
            "analytics.vertices": vertex_count,
            "analytics.edges": edge_count,
            "analytics.materials": len(bpy.data.materials),
            "analytics.active_camera": bpy.context.scene.camera.name,
            "analytics.animation_duration": (bpy.context.scene.frame_end - bpy.context.scene.frame_start + 1) / bpy.context.scene.render.fps,
            "analytics.bounding_box": self.get_scene_bounding_box(),
            "analytics.scene_size": self.get_scene_bounding_box_size()
        }

        for key, val in analytics.items():
            print_analytics_element(key, val)

    def get_scene_bounding_box(self):
        """
        Calculate scene bounding box.
        :return:
        """
        # Get a reference to the scene
        scene = bpy.context.scene

        # Initialize variables to store the minimum and maximum x, y, and z values
        min_x, min_y, min_z = float("inf"), float("inf"), float("inf")
        max_x, max_y, max_z = float("-inf"), float("-inf"), float("-inf")

        # Loop over all objects in the scene
        for obj in scene.objects:
            # Skip the object if it's not a mesh
            if obj.type != "MESH":
                continue

            # Get the object's bounding box
            bbox = obj.bound_box

            # Update the minimum and maximum x, y, and z values
            for point in bbox:
                x, y, z = point
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                min_z = min(min_z, z)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                max_z = max(max_z, z)

        # Return the scene's bounding box as a tuple of minimum and maximum values
        return (min_x, min_y, min_z), (max_x, max_y, max_z)

    def get_scene_bounding_box_size(self):
        """
        Calculate scene bounding box size.
        :return:
        """
        min_point, max_point = self.get_scene_bounding_box()

        # Calculate the size of the x, y, and z axes
        size_x = max_point[0] - min_point[0]
        size_y = max_point[1] - min_point[1]
        size_z = max_point[2] - min_point[2]

        # Return the sizes of the x, y, and z axes
        return size_x, size_y, size_z

    def render(self):
        """
        Render the scene.
        :return:
        """
        bpy.ops.render.render('INVOKE_DEFAULT', write_still=True, animation=True)

    def init(self):
        """
        Intialize by opening the Blender file
        :return:
        """
        # redirect output to null
        old = os.dup(sys.stdout.fileno())
        sys.stdout.flush()
        os.close(sys.stdout.fileno())
        fd = os.open(os.devnull, os.O_WRONLY)

        # do the rendering
        bpy.ops.wm.open_mainfile(filepath=self.blender_file)

        # disable output redirection
        os.close(fd)
        os.dup(old)
        os.close(old)
