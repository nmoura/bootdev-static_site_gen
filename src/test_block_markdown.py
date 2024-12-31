import unittest
from block_markdown import (
        markdown_to_blocks,
        block_to_block_type,
        markdown_to_html_node
)
from htmlnode import ParentNode, LeafNode


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_simple(self):
        markdown_str = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item


 This is another paragraph of text after several new lines with leading and trailing whitespaces. """
        blocks = markdown_to_blocks(markdown_str)
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item',
                'This is another paragraph of text after several new lines with leading and trailing whitespaces.'
            ],
            blocks
        )

    def test_markdown_to_blocks_complex(self):
        markdown_str = """
# heading level 1

Some text paragraph

```
import pprint

print('hello world')


def dosomething(args):
    print('nah')


def donothing(args):
    print('cmon')
```

1. item 1
2. item 2
3. **bolded item 3**

an unordered list of nothing:

- bla
- ble
- bleia
"""
        blocks = markdown_to_blocks(markdown_str)
        self.assertListEqual(
            [
                '# heading level 1',
                'Some text paragraph',
                "```\nimport pprint\n\nprint('hello world')\n\n\ndef dosomething(args):\n    print('nah')\n\n\ndef donothing(args):\n    print('cmon')\n```",
                '1. item 1\n2. item 2\n3. **bolded item 3**',
                'an unordered list of nothing:',
                '- bla\n- ble\n- bleia',
            ],
            blocks
        )

    def test_block_to_block_type_code(self):
        block = """```import pprint```"""
        block_type = block_to_block_type(block)
        self.assertEqual("code", block_type)

    def test_block_to_block_type_not_code(self):
        block = """``import pprint``"""
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)

    def test_block_to_block_type_heading(self):
        block = """###### heading level 6"""
        block_type = block_to_block_type(block)
        self.assertEqual("heading", block_type)

    def test_block_to_block_type_not_heading(self):
        block = """####### heading level 7 does not exist"""
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)

    def test_block_to_block_type_quote(self):
        block = "> I really can't stay\n> But baby it's cold outside"
        block_type = block_to_block_type(block)
        self.assertEqual("quote", block_type)

    def test_block_to_block_type_not_quote(self):
        block = "> I really can't stay\nBut baby it's cold outside"
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)

    def test_block_to_block_type_unordered_list(self):
        block = "* cold\n* snow\n* rudolph"
        block_type = block_to_block_type(block)
        self.assertEqual("unordered_list", block_type)
        block = "- cold\n- snow\n- rudolph"
        block_type = block_to_block_type(block)
        self.assertEqual("unordered_list", block_type)

    def test_block_to_block_type_not_unordered_list(self):
        block = "* cold\n* snow\n*rudolph"
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)
        block = "- cold\n- snow\n-rudolph"
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)

    def test_block_to_block_type_ordered_list(self):
        block = "1. cold\n2. snow\n3. rudolph"
        block_type = block_to_block_type(block)
        self.assertEqual("ordered_list", block_type)

    def test_block_to_block_type_not_ordered_list(self):
        block = "2. cold\n3. snow\n4. rudolph"
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)
 
    def test_block_to_block_type_paragraph(self):
        block = "This is just a common paragraph."
        block_type = block_to_block_type(block)
        self.assertEqual("paragraph", block_type)

    def test_markdown_to_html_str_simple(self):
        markdown_str = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item


 This is another paragraph of text after several new lines with leading and trailing whitespaces. """
        html_str = markdown_to_html_node(markdown_str).to_html()
        self.assertEqual(
            '<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul><p>This is another paragraph of text after several new lines with leading and trailing whitespaces.</p></div>',
            html_str
        )

    def test_markdown_to_html_str_complex(self):
        markdown_str = """
# heading level 1

Some text paragraph

```
import pprint

print('hello world')


def dosomething(args):
    print('nah')


def donothing(args):
    print('cmon')
```

1. item 1
2. item 2
3. **bolded item 3**

an unordered list of nothing:

- bla
- ble
- bleia
"""
        html_str = markdown_to_html_node(markdown_str).to_html()
        self.assertEqual(
            "<div><h1>heading level 1</h1><p>Some text paragraph</p><pre><code>import pprint<br/><br/>print('hello world')<br/><br/><br/>def dosomething(args):<br/>    print('nah')<br/><br/><br/>def donothing(args):<br/>    print('cmon')</code></pre><ol><li>item 1</li><li>item 2</li><li><b>bolded item 3</b></li></ol><p>an unordered list of nothing:</p><ul><li>bla</li><li>ble</li><li>bleia</li></ul></div>",
            html_str
        )

    def test_markdown_to_html_code_only(self):
        markdown_str = """```
import pprint

print('hello world')


def dosomething(args):
    print('nah')


def donothing(args):
    print('cmon')
```"""
        html_str = markdown_to_html_node(markdown_str).to_html()
        self.assertEqual(
            "<div><pre><code>import pprint<br/><br/>print('hello world')<br/><br/><br/>def dosomething(args):<br/>    print('nah')<br/><br/><br/>def donothing(args):<br/>    print('cmon')</code></pre></div>",
            html_str
        )

