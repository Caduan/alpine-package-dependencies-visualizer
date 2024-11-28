import unittest

from apk import PackageBuilder, Index, Package, apk_index_from_string

class PackageBuilderTestCase(unittest.TestCase):
    def test_is_valid_returns_false_if_name_is_not_set(self):
        builder = PackageBuilder()

        builder.version = '1'

        self.assertFalse(builder.is_valid())

    def test_is_valid_returns_false_if_version_is_not_set(self):
        builder = PackageBuilder()

        builder.name = '1'

        self.assertFalse(builder.is_valid())

    def test_is_valid_returns_true_if_name_and_version_are_set(self):
        builder = PackageBuilder()

        builder.name = '1'
        builder.version = '1'

        self.assertTrue(builder.is_valid())

    def test_build_creates_and_returns_package(self):
        builder = PackageBuilder()

        builder.name = '1'
        builder.version = '1'
        builder.provides = ['p']
        builder.depends_on = ['d']

        package = builder.build()

        self.assertEqual(package.name, '1')
        self.assertEqual(package.version, '1')
        self.assertEqual(package.provides, ['p'])
        self.assertEqual(package.depends_on, ['d'])

    def test_build_cleans_state(self):
        builder = PackageBuilder()

        builder.name = '1'
        builder.version = '1'
        builder.provides = ['p']
        builder.depends_on = ['d']

        builder.build()

        self.assertIsNone(builder.name)
        self.assertIsNone(builder.version)
        self.assertListEqual(builder.provides, [])
        self.assertListEqual(builder.depends_on, [])


class IndexTestCase(unittest.TestCase):
    def test_add_package_adds_package_to_provisions(self):
        index = Index()

        index.add_package(Package('1', '1', ['p'], ['d']))

        p = index.get_package('1')

        self.assertEqual(p.name, '1')
        self.assertEqual(p.version, '1')
        self.assertEqual(p.provides, ['p'])
        self.assertEqual(p.depends_on, ['d'])

    def test_add_package_convert_package_to_list_when_provision_with_the_same_name_already_exists(self):
        index = Index()

        p1 = Package('p1', '1', ['p', 'p1'], ['d'])
        p2 = Package('p2', '1', ['p', 'p2'], ['d'])

        index.add_package(p1)
        index.add_package(p2)

        p = index.get_package('p')

        self.assertIsInstance(p, list)
        self.assertIn(p1, p)
        self.assertIn(p2, p)


class IndexFromStringTestCase(unittest.TestCase):
    def test_apk_index_from_string_returns_apk_index(self):
        apk_index = apk_index_from_string('P: 1\nV: 1\np: p\nD: d')

        p = apk_index.get_package('1')

        self.assertEqual(p.name, '1')
        self.assertEqual(p.version, '1')
        self.assertEqual(p.provides, ['p'])
        self.assertEqual(p.depends_on, ['d'])

    def test_apk_index_from_string_does_not_crash_on_unknown_keys(self):
        apk_index = apk_index_from_string('P: 1\nV: 1\np: p\nD: d\nZ: z')

        p = apk_index.get_package('1')

        self.assertEqual(p.name, '1')
        self.assertEqual(p.version, '1')
        self.assertEqual(p.provides, ['p'])
        self.assertEqual(p.depends_on, ['d'])

    def test_apk_index_from_string_can_read_more_than_one_package(self):
        apk_index = apk_index_from_string('P: 1\nV: 1\np: p\nD: d\n\nP: 2\nV: 1\np: p\nD: d')

        p1 = apk_index.get_package('1')
        p2 = apk_index.get_package('2')

        self.assertEqual(p1.name, '1')
        self.assertEqual(p1.version, '1')
        self.assertEqual(p1.provides, ['p'])
        self.assertEqual(p1.depends_on, ['d'])

        self.assertEqual(p2.name, '2')
        self.assertEqual(p2.version, '1')
        self.assertEqual(p2.provides, ['p'])
        self.assertEqual(p2.depends_on, ['d'])

    def test_apk_from_index_strips_versions_from_provisions_and_dependencies(self):
        apk_index = apk_index_from_string('P: 1\nV: 1\np: p=1\nD: d>=1')

        p = apk_index.get_package('1')

        self.assertEqual(p.name, '1')
        self.assertEqual(p.version, '1')
        self.assertEqual(p.provides, ['p'])
        self.assertEqual(p.depends_on, ['d'])

    def test_apk_from_index_allows_multiple_provisions_and_dependencies(self):
        apk_index = apk_index_from_string('P: 1\nV: 1\np: p1=1 p2=2\nD: d1=1 d2=2')

        p = apk_index.get_package('1')
        
        self.assertEqual(p.name, '1')
        self.assertEqual(p.version, '1')
        self.assertEqual(p.provides, ['p1', 'p2'])
        self.assertEqual(p.depends_on, ['d1', 'd2'])
