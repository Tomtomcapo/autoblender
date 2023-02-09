#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import os
from pathlib import Path
from src.autoblender.renderer_processor import RendererProcessor
from src.autoblender.settings_parser import SettingsParser
from src.autoblender.logger import *


def main(args):
    """ Main entry point of the app """
    blender_file = args.file
    settings_file = args.settings
    if settings_file is None:
        path = Path(blender_file)
        settings_file = f"{path.parent.absolute()}{os.sep}render_settings.yml"

    settings = {}
    if not os.path.isfile(settings_file):
        log_warning("settings_file_missing_or_not_a_file", "Settings file not found. Using parameters from the Blender file.")
    else:
        settings_parser = SettingsParser()
        settings = settings_parser.parse(settings_file)

    processor = RendererProcessor(blender_file, settings)
    log_action("open_and_read_file")
    processor.init()

    log_action("apply_settings")
    processor.apply_parameters_from_settings()
    log_info("settings_applied", "Settings are applied.")

    log_action("display_summary")
    processor.print_summary()

    log_action("computing_analytics")
    processor.print_analytics()

    if not args.dry_run:
        log_action("starting_render")
        processor.render()
        log_info("render_done", "Render is done.")
    else:
        log_info("dry_run_done", "Dry run is done.")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("file", help="Required blender (.blend) file")

    # Optional argument flag which defaults to False
    parser.add_argument("-s", "--settings", action="store", default=None)

    # Optional argument flag which defaults to False
    parser.add_argument("-d", "--dry-run", action="store_true", default=False)

    # Specify output of "--version"
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="Blender Renderer (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
