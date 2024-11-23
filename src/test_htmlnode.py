import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("p", "This is a paragraph.")
        self.assertEqual("HTMLNode(tag=p, value=This is a paragraph., children=None, props=None)", repr(node))
        node2 = LeafNode("p", "This is a paragraph.", {'class': 'emptyclass'})
        self.assertEqual("LeafNode(tag=p, value=This is a paragraph., props={'class': 'emptyclass'})", repr(node2))
    
    def test_to_html_props(self):
        node = HTMLNode(
                "a",
                None, None,
                {'href': 'https://www.boot.dev', 'target': '_blank'},
        )
        self.assertEqual(
                ' href="https://www.boot.dev" target="_blank"',
                node.props_to_html()
        )

    def test_to_html(self):
        node = HTMLNode(
                "p",
                "This is a paragraph."
        )
        self.assertRaises(NotImplementedError, node.to_html)

    def test_values(self):
        node = HTMLNode(
                "div",
                "This is a div"
        )
        self.assertEqual(
                node.tag,
                "div"
        )
        self.assertEqual(
                node.value,
                "This is a div"
        )
        self.assertEqual(
                node.children,
                None
        )
        self.assertEqual(
                node.props,
                None
        )

    def test_to_html_no_children(self):
        node = LeafNode(
                "p",
                "A beautiful paragraph that says nothing.",
                {'class': 'emptyclass'}
        )
        self.assertEqual(
                node.to_html(),
                '<p class="emptyclass">A beautiful paragraph that says nothing.</p>'
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a sentence")
        self.assertEqual(node.to_html(), 'This is a sentence')

    def test_to_html_with_many_children(self):
        child_nodes = [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                        ]
        parent_node = ParentNode("p", child_nodes)
        self.assertEqual(parent_node.to_html(),
                         '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_to_html_parent_with_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_parent_with_no_tag(self):
        child_node = [LeafNode("b", "bold text")]
        parent_node = ParentNode(None, child_node)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_grandchildren(self):
        grandchildren_node = [LeafNode("b", "Bold text"),
                              LeafNode(None, "Normal text")]
        child_node = ParentNode("div", grandchildren_node, {'class': 'test'})
        parent_node = ParentNode("p", [child_node])
        self.assertEqual(parent_node.to_html(),
                         '<p><div class="test"><b>Bold text</b>Normal text</div></p>')


if __name__ == "__main__":
    unittest.main()
