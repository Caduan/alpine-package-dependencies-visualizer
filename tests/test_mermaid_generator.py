import unittest
from io import StringIO

from apk import Index, Package
from mermaid_generator import write_package_to_mermaid_file, write_graph_to_mermaid_file


class MermaidGeneratorTestCase(unittest.TestCase):
    def test_write_package_to_mermaid_file_produces_valid_output(self):
        f = StringIO()
        index = Index()
        p1 = Package('p1', '1', ['p1'], ['p2'])
        p2 = Package('p2', '1', ['p2'], [])
        
        index.add_package(p1)
        index.add_package(p2)
        
        write_package_to_mermaid_file(f, index, p1, {})
        
        self.assertEqual(f.getvalue(), "  p1 --> p2\n")
        
    def test_write_package_to_mermaid_file_produces_different_arrow_for_commands(self):
        f = StringIO()
        index = Index()
        p1 = Package('p1', '1', ['p1'], ['/bin/sh'])
        p2 = Package('p2', '1', ['/bin/sh'], [])
        
        index.add_package(p1)
        index.add_package(p2)
        
        write_package_to_mermaid_file(f, index, p1, {})
        
        self.assertEqual(f.getvalue(), "  p1 -. /bin/sh .-> p2\n")
        
    def test_write_graph_to_mermaid_file_produces_valid_output(self):
        f = StringIO()
        index = Index()
        p1 = Package('p1', '1', ['p1'], ['p2'])
        p2 = Package('p2', '1', ['p2'], [])
        
        index.add_package(p1)
        index.add_package(p2)
        
        write_graph_to_mermaid_file(f, index, p1)
        
        self.assertEqual(f.getvalue(), "graph LR\n  p1 --> p2\n")
