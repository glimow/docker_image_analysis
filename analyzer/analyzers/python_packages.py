from ..utils import run
import logging

logger = logging.getLogger(__name__)


def process_one_package(path, package, python_version="3"):
    command = f"sudo chroot {path} pip{python_version} show {package}"
    info = get_ipython().getoutput(command)
    for line in info:
        if "Name" in line:
            name = line.split(" ").pop()
        if "Version" in line:
            version = line.split(" ").pop()
        if "Location" in line:
            location = line.split(" ").pop()
    result = get_ipython().getoutput(
        f"du --max-depth=0 {path}{location}/{name}").pop()
    # If the folder does not exist, try lowercase
    if "cannot access" in result:
        result = get_ipython().getoutput(
            f"du --max-depth=0 {path}{location}/{name.lower()}").pop()
    # If the lowercase folder do not exist either
    if "cannot access" not in result:
        size = int(result.split('\t').pop(0))
    # List the files by hand
    else:
        command = f"sudo chroot {path} pip{python_version} show {package} -f"
        info = get_ipython().getoutput(command)
        flag = False
        size = 0
        for line in info:
            if flag:
                command = f"du {path}{location}/{line.strip()}"
                size += int(get_ipython().getoutput(command).pop().split('\t').pop(0))
            if 'Files' in line:
                flag = True
    return [name, version, size]

def get_python_packages_info(path, python_version="3"):

    command = f"sudo chroot {path} pip{python_version} list --format freeze --no-cache-dir 2>/dev/null"

    packages = [package.split('==')
                for package in get_ipython().getoutput(command)]

    package_list = []
    for package in packages:
        try:
            package_list.append(process_one_package(path, package[0]))
        except Exception as e:
            logger.error("Error processing python packages", package[0], e)
            pass
    return package_list
