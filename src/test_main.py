import unittest
from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        markdown = '# this is the title of this useless markdown\n\nblablabla'
        title = 'this is the title of this useless markdown'
        self.assertEqual(
            extract_title(markdown),
            title
        )

        markdown = 'blablabla\n\n# useless markdown '
        title = 'useless markdown'
        self.assertEqual(
            extract_title(markdown),
            title
        )

        markdown = 'blablabla\n\nno title here'
        with self.assertRaises(Exception):
            extract_title(markdown)
