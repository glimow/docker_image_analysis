import sys
import json


def get_dir_size(directory):
    size = get_ipython().getoutput(f'sudo du -s {directory}/ | cut -f1').pop()
    return int(size)

def get_base_info(path):
   distro, version = get_ipython().getoutput(
       f'bash extract_packages.sh {path}').pop(0).split(':')
   
   size = get_dir_size(path)
   
   return distro, version, size
