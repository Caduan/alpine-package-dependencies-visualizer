import yaml


class Config:
    def __init__(self, package, repository, visualizer, png_file):
        self.package = package
        self.repository = repository
        self.visualizer = visualizer
        self.png_file = png_file


def load_config(file_path='config.yaml'):
    with open(file_path, 'r') as file:
        content = yaml.safe_load(file)

        return Config(
            content['package'],
            content['repository'],
            content['visualizer'],
            content['png_file'])
