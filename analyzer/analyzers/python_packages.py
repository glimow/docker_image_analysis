from ..utils import run

def get_python_packages_info(path, python_version="3"):

    command = f"sudo chroot {path} pip{python_version} list --format freeze --no-cache-dir . 2>/dev/null"

    packages = [package.split('==')
                for package in (command)]
    command = """sudo chroot """ + path + \
        """ pip"""+ python_version + \
        """ list --format freeze --no-cache-dir .|awk -F = {'print $1'}| xargs pip2 show | grep -E 'Location:|Name:' | cut -d ' ' -f 2 | paste -d ' ' - - | awk '{print $2 "/" tolower($1)}' | xargs du -s 2> /dev/null"""

    sizes_raw = get_ipython().getoutput(command)

    package_list = []
    for raw_line in sizes_raw:
        try:
            line = raw_line.split("\t")
            size = line.pop(0)
            package = line.pop().split("/").pop()
            for package_version in packages:
                if package in package_version[0]:
                    version = package_version[1]
                    package_list.append([package, version, int(size)])
        except:
            pass
    return package_list
