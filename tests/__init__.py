# add workspace dir to system path, otherwise cannot import project modules
import os
import sys
proj_root_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir
)
sys.path.append(proj_root_path)
