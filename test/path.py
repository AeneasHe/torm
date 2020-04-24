import sys
import os


def addRootPath(depth=1):
    folder = os.path.split(os.path.realpath(__file__))[0]
    workspace = folder
    for i in range(depth):
        workspace = os.path.dirname(workspace)
    sys.path.append(workspace)
    return workspace


workspace = addRootPath()
