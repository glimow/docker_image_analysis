import subprocess

def run(command):
    result = subprocess.run([command], stdout=subprocess.PIPE, shell=True)
    return result.stdout.decode("utf-8").split("\n")[:-1]

def docker_cleanup():
    get_ipython().getoutput("docker system prune -af && docker volume prune -f")

class mount_docker_image:
    def __init__(self, image):
        # Running the container
        container = get_ipython().getoutput(f'sudo docker create {image}').pop()

        # Copying its content in a temporary directory
        tmp_dir = get_ipython().getoutput(f'mktemp -d -t dc-XXXXXXXXXX').pop()
        tmp_file = get_ipython().getoutput(f'mktemp -t fc-XXXXXXXXXX').pop()
        get_ipython().getoutput(f'docker export  {container} > {tmp_file}')
        get_ipython().getoutput(f'docker rm -f {container} > /dev/null')
        get_ipython().getoutput(f'tar fx {tmp_file} -C {tmp_dir}')
        get_ipython().getoutput(f'sudo rm -rf {tmp_file}')
        
        self.dir = tmp_dir


    def __enter__(self):
        return self.dir

    def __exit__(self, type, value, traceback):
        get_ipython().getoutput(f'sudo rm -rf {self.dir}')

