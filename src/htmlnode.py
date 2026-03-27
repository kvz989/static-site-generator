class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ""
        output = ""
        for key in list(self.props.keys()):
            output += f'{key}="{self.props[key]}" '
        return output

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, props: {self.props_to_html()})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        prop = ""
        if self.value is None:
            raise ValueError()
        if not self.tag:
            return self.value
        if self.props:
            key = list(self.props.keys())[0]
            prop = f' {key}="{self.props[key]}"'
        return f"<{self.tag}{prop}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, props: {self.props_to_html()})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        children_output = ""
        if not self.tag:
            raise ValueError("tag not found")
        for child in self.children:  # pyright: ignore[reportOptionalIterable]
            if child.value is None and not isinstance(child, ParentNode):
                raise ValueError("child missing value")
            child_output = child.to_html()
            children_output += child_output
        return f"<{self.tag}>{children_output}</{self.tag}>"
