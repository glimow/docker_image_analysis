class mount_docker_image:
    def __init__(self, image):
        # Running the container
        container = get_ipython().getoutput(f'sudo docker create {image}').pop()

        # Copying its content in a temporary directory
        tmp_dir = get_ipython().getoutput(f'mktemp -d -t dc-XXXXXXXXXX').pop()
        tmp_file = get_ipython().getoutput(f'mktemp -t fc-XXXXXXXXXX').pop()
        get_ipython().system(f'docker export  {container} > {tmp_file}')
        get_ipython().system(f'docker rm -f {container} > /dev/null')
        get_ipython().system(f'tar fx {tmp_file} -C {tmp_dir}')
        get_ipython().system(f'sudo rm -rf {tmp_file}')
        
        self.dir = tmp_dir


    def __enter__(self):
        return self.dir

    def __exit__(self, type, value, traceback):
        get_ipython().system(f'sudo rm -rf {self.dir}')
