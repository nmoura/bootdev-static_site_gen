import unittest
from inline_markdown import (
        split_nodes_delimiter,
        extract_markdown_images,
        extract_markdown_links,
        split_nodes_link,
        split_nodes_image,
        text_to_textnodes
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    def test_split_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        splitted = split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertListEqual(
                [
                    TextNode("This is text with a ", TextType.TEXT, None),
                    TextNode("code block", TextType.CODE, None),
                    TextNode(" word", TextType.TEXT, None)
                ],
                splitted,
        )

    def test_split_delim_bold_double(self):
        node = TextNode("This is text with two **bold** sentences, **ok?**", TextType.TEXT)
        splitted = split_nodes_delimiter([node], '**', TextType.BOLD)
        self.assertListEqual(
                [
                    TextNode("This is text with two ", TextType.TEXT, None),
                    TextNode("bold", TextType.BOLD, None),
                    TextNode(" sentences, ", TextType.TEXT, None),
                    TextNode("ok?", TextType.BOLD, None),
                ],
                splitted,
        )

    def test_split_delim_italic(self):
        node = TextNode("This is an *italic sentence*, brother.", TextType.TEXT)
        splitted = split_nodes_delimiter([node], '*', TextType.ITALIC)
        self.assertListEqual(
                [
                    TextNode("This is an ", TextType.TEXT, None),
                    TextNode("italic sentence", TextType.ITALIC, None),
                    TextNode(", brother.", TextType.TEXT, None),
                ],
                splitted
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("Text with **bold** and *italic*.", TextType.TEXT)
        splitted = split_nodes_delimiter([node], "**", TextType.BOLD)
        splitted = split_nodes_delimiter(splitted, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(".", TextType.TEXT)
            ],
            splitted,
        )

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            extracted,
        )

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ],
            extracted,
        )

    def test_split_nodes_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
            ],
            new_nodes
        )

    def test_split_nodes_link_just_link(self):
        text = "[boot dev](https://www.boot.dev)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev")
            ],
            new_nodes
        )

    def test_split_nodes_link_text_appended(self):
        text = "[boot dev](https://www.boot.dev) appended text after link"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" appended text after link", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_nodes_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) images"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" images", TextType.TEXT, None)
            ],
            new_nodes
        )

    def test_split_nodes_image_just_image(self):
        text = "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")
            ],
            new_nodes
        )

    def test_split_nodes_image_text_appended(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) appended text after image"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" appended text after image", TextType.TEXT)
            ],
            new_nodes
        )
 
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            nodes
        )

