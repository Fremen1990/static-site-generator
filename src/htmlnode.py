class HTMLNode:
    def __init__(self, tag = None, value= None, children = None, props = None):
        self.tag = tag
        self.value = value
        if children is  None:
            self.children = []
        else:
            self.children = children
        if props is None:
            self.props = {}
        else:
            self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props:
            for key, value in self.props.items():
                result += f' {key}="{value}"'

        return result

    def __repr__(self):
        return f"HTMLNode(tag={repr(self.tag)}, value={repr(self.value)}, children={repr(self.children)}, props={repr(self.props)})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
