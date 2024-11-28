import re
import tarfile
from io import BytesIO

import requests
from pycparser.ply.yacc import resultlimit


class Package:
    def __init__(self, name, version, provides, depends_on):
        self.name = name
        self.version = version
        self.provides = provides
        self.depends_on = depends_on


class PackageBuilder:
    def __init__(self):
        self.name = None
        self.version = None
        self.provides = []
        self.depends_on = []

    def clean(self):
        self.name = None
        self.version = None
        self.provides = []
        self.depends_on = []

    def is_valid(self) -> bool:
        return self.name is not None and self.version is not None

    def build(self) -> Package:
        package = Package(self.name, self.version, self.provides, self.depends_on)
        
        self.clean()

        return package


class Index:
    def __init__(self):
        self.provisions = {}

    def add_package(self, package: Package):
        self.provisions[package.name] = package

        for provision in package.provides:
            if provision in self.provisions:
                existing = self.provisions[provision]
                if isinstance(existing, list):
                    existing.append(package)
                else:
                    self.provisions[provision] = [existing, package]
            else:
                self.provisions[provision] = package

    def get_package(self, name: str) -> Package:
        return self.provisions[name]


def apk_index_from_string(content: str) -> Index:
    index = Index()
    package_builder = PackageBuilder()

    for line in content.splitlines():
        if len(line) == 0:
            if package_builder.is_valid():
                index.add_package(package_builder.build())

        if line.startswith('#'):
            continue

        if line.startswith('P:'):
            package_builder.name = line[2:].strip()
        elif line.startswith('V:'):
            package_builder.version = line[2:].strip()
        elif line.startswith('D:'):
            package_builder.depends_on = [re.split('=|>|<|>=|<=', item)[0] for item in line[2:].strip().split(' ')] # "  a b=1 c>=2   " -> ["a", "b", "c"]
        elif line.startswith('p:'):
            package_builder.provides = [re.split('=|>|<|>=|<=', item)[0] for item in line[2:].strip().split(' ')]

    if package_builder.is_valid():
        index.add_package(package_builder.build())

    return index

        
def apk_index_from_repository(repository_url: str) -> Index:
    response = requests.get(repository_url + "/APKINDEX.tar.gz")

    tf = tarfile.open(fileobj=BytesIO(response.content))

    return apk_index_from_string(tf.extractfile('APKINDEX').read().decode('utf-8'))
