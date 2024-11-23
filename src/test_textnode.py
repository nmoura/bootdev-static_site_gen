import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_text_differ(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_differ(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_differ(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, TextType.TEXT, https://www.boot.dev)", repr(node)
        )


class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_link(self):
        node = TextNode("Link to Boot.dev", TextType.LINK, 'https://www.boot.dev')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "Link to Boot.dev")
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">Link to Boot.dev</a>')

    def test_image(self):
        node = TextNode("This is a beautiful image alt text", TextType.IMAGE, 'https://images.google.com/beauty.png')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(
                html_node.props,
                { 'src': 'https://images.google.com/beauty.png',
                  'alt': 'This is a beautiful image alt text'}
                )

    def test_code(self):
        node = TextNode('print("hello, world!")', TextType.CODE, None)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, 'print("hello, world!")')
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.to_html(), '<code>print("hello, world!")</code>')


class TestSplitNodeDelimiter(unittest.TestCase):

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        splitted = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertEqual(
                splitted,
                [
                    TextNode("This is text with a ", TextType.TEXT, None),
                    TextNode("code block", TextType.CODE, None),
                    TextNode(" word", TextType.TEXT, None)
                    ]
                )

    def test_bold(self):
        node = TextNode("This is text with two **bold** sentences, **ok?**", TextType.TEXT)
        splitted = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertEqual(
                splitted,
                [
                    TextNode("This is text with two ", TextType.TEXT, None),
                    TextNode("bold", TextType.BOLD, None),
                    TextNode(" sentences, ", TextType.TEXT, None),
                    TextNode("ok?", TextType.BOLD, None),
                    ]
                )

    def test_italic(self):
        node = TextNode("This is an *italic sentence*, brother.", TextType.TEXT)
        splitted = split_nodes_delimiter([node], '*', TextType.ITALIC)
        self.assertEqual(
                splitted,
                [
                    TextNode("This is an ", TextType.TEXT, None),
                    TextNode("italic sentence", TextType.ITALIC, None),
                    TextNode(", brother.", TextType.TEXT, None),
                    ]
                )


if __name__ == "__main__":
    unittest.main()
