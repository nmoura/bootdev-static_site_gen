class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        props = ""
        for k, v in self.props.items():
            props += f' {k}="{v}"'
        return props

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("A LeafNode should have a value")
        if self.tag is None or self.tag == "":
            return f"{self.value}"
        if self.tag == "blockquote" or self.tag == "code":
            return f"<{self.tag}{self.props_to_html()}>{self.value.replace("\n", "<br/>")}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A ParentNode should have a tag")
        if self.children is None:
            raise ValueError("A ParentNode should have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        if self.tag == "blockquote" or self.tag == "code":
            children_html = children_html.replace("\n", "<br/>")
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"
