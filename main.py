

# retrieves node libs, python libs and disk usage information for a dockerhub image
import sys
import json
import os

from analyzer.utils import mount_docker_image, docker_cleanup

from analyzer.analyzers.base import get_base_info
from analyzer.analyzers.native_packages import get_native_packages_info
from analyzer.analyzers.python_packages import get_python_packages_info
from analyzer.analyzers.node_packages import get_node_packages_info


def get_image_info(image):

    with mount_docker_image(image) as image_path:

        distro, version, image_size = get_base_info(image_path)

        natives_packages_info = get_native_packages_info(image_path, distro)

        python_packages_info = get_python_packages_info(image_path)
        
        node_packages_info = get_node_packages_info(image_path)
    
    return {
        'image': image,
        'size': image_size,
        'distribution': distro,
        'version': version,
        'packages': {
            'native': natives_packages_info,
            'python3': python_packages_info,
            'node': node_packages_info
        }
    }

if __name__ == "__main__":
    
    images_file = sys.argv[1]
    output_folder = sys.argv[2]
    pid = int(sys.argv[3])
    njob = int(sys.argv[4])
    
    with open(images_file, 'r') as images:

        for i in range(pid):
            images.readline().replace('\n', '')
        
        image = images.readline().replace('\n', '')
        count = 0

        while image:
            try:

                image_data = get_image_info(image)

                if image.endswith(":latest"):
                    filename = output_folder + '/' + \
                        image[:2] + '/' + image.split(":").pop() + '.json'
                else:
                    filename = output_folder + '/' + \
                        image[:2] + '/' + image + '.json'
                
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                
                with open(filename, "w") as output_file:
                    json.dump(image_data, output_file, indent=4)
                print("processed %s", image)
            
            except:
                print("failed %s", image)

            for i in range(njob - 1):
                images.readline().replace('\n', '')
            
            image = images.readline().replace('\n', '')
            
            count += 1

            # Remove all unused images and volumes
            # So the script do not end up filling all available disk space
            if count % 100:
                docker_cleanup()
