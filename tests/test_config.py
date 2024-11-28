import tempfile
import textwrap
import unittest

from config import load_config


class TestConfig(unittest.TestCase):
    def test_load_config(self):
        with tempfile.NamedTemporaryFile("wt", encoding="utf-8") as f:
            f.write(textwrap.dedent("""
                package: graphviz
                repository: http://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64
                visualizer: /opt/homebrew/bin/mmdc
                png_file: graph.png
                """))

            f.flush()

            cfg = load_config(f.name)

        self.assertEqual(cfg.package, 'graphviz')
        self.assertEqual(cfg.repository, 'http://dl-cdn.alpinelinux.org/alpine/edge/main/x86_64')
        self.assertEqual(cfg.visualizer, '/opt/homebrew/bin/mmdc')
        self.assertEqual(cfg.png_file, 'graph.png')
