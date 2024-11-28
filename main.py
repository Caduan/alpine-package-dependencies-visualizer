import os
import tempfile

from apk import apk_index_from_repository
from config import load_config
from mermaid_generator import write_graph_to_mermaid_file


def run():
    cfg = load_config()
    index = apk_index_from_repository(cfg.repository)

    package = index.get_package(cfg.package)
    if package is None:
        print(f"Package '{cfg.package}' not found")
        exit(1)

    with tempfile.NamedTemporaryFile("wt", encoding="utf-8") as f:
        write_graph_to_mermaid_file(f, index, package)
        f.flush()
        
        command = cfg.visualizer.format(input_file=f.name, output_file=cfg.png_file)
        
        exit_code = os.system(command)

    if exit_code != 0:
        print(f"Unable to generate graph image: (exit code {exit_code})")
    else:
        print(f"Successfully generated graph image {cfg.png_file}")


if __name__ == '__main__':
    run()
