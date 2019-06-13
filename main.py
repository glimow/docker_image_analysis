
#%%
#!/bin/bash
# usage ./docker.sh image-name
# retrieves node libs, python libs and disk usage information for a dockerhub image

import sys
import json

from analyzers.base import get_base_info
from analyzers.native_packages import get_native_packages_info
from analyzers.python_packages import get_python_packages_info
from analyzers.node_packages import get_node_packages_info

def get_image_info(image):
    # Running the container
    container = get_ipython().getoutput(f'sudo docker create {image}').pop()

    # Copying its content in a temporary directory
    tmp_dir = get_ipython().getoutput(f'mktemp -d -t dc-XXXXXXXXXX').pop()

    get_ipython().system(f'docker export  {container} > temp.tar')
    get_ipython().system(f'docker rm -f {container} > /dev/null')
    get_ipython().system(f'tar fx temp.tar -C {tmp_dir}')

    distro, version, image_size = get_base_info(tmp_dir)
    
    natives_packages_info = get_native_packages_info(tmp_dir, distro)

    python_packages_info = get_python_packages_info(tmp_dir)
    
    node_packages_info = get_node_packages_info(tmp_dir)

    # cleaning up
    get_ipython().system('sudo rm -rf temp.tar')
    get_ipython().system(f'sudo rm -rf {tmp_dir}')

    return json.dumps({
            'slug': image,
            'size': image_size,
            'distribution': distro,
            'version': version,
            'packages': {
                'native': natives_packages_info,
                'python3': python_packages_info,
                'node': node_packages_info
            }
        }, indent=4)


print(get_image_info('faizanbashir/python-datascience'))
