
#%%
#!/bin/bash
# usage ./docker.sh image-name
# retrieves node libs, python libs and disk usage information for a dockerhub image
import sys
import json

from utils import mount_docker_image

from analyzers.base import get_base_info
from analyzers.native_packages import get_native_packages_info
from analyzers.python_packages import get_python_packages_info
from analyzers.node_packages import get_node_packages_info


def get_image_info(image):

    with mount_docker_image(image) as image_path:

        distro, version, image_size = get_base_info(image_path)
        
        natives_packages_info = get_native_packages_info(image_path, distro)

        python_packages_info = get_python_packages_info(image_path)
        
        node_packages_info = get_node_packages_info(image_path)
    

    return json.dumps({
            'image': image,
            'size': image_size,
            'distribution': distro,
            'version': version,
            'packages': {
                'native': natives_packages_info,
                'python3': python_packages_info,
                'node': node_packages_info
            }
        }, indent=4)

if __name__ == "__main__":
    print(get_image_info('amancevice/superset'))
