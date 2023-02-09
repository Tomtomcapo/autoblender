__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse

from autoblender.autoblender import main

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
