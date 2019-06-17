from ..utils import run
import logging

logger = logging.getLogger(__name__)

def process_node_packages(package_folders):
    package_list = []
    for folder in package_folders:
        result = get_ipython().getoutput(
            f'(cd {folder}; /home/tristan/code/cli/bin/npm-cli.js ls)')
        for line in result:
            try:
                name, version, path = line.split(' ').pop().split('@')
                size = get_ipython().getoutput(
                    f'du --max-depth=0 --exclude=./node_modules {path}').pop().split('\t').pop(0)
                package_list.append([name, version, int(size)])
            except Exception as e:
                logger.error(e)
                pass
    return package_list

def get_node_packages_info(path):
    node_modules = get_ipython().getoutput(
            f'find {path} -name node_modules -type d -not -path "*/node_modules/*"')
    return process_node_packages(node_modules)
    
