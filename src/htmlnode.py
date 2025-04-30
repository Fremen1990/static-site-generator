from typing import Optional, List, Dict


class HTMLNode:
    def __init__(self, tag:Optional[str] = None, value: Optional[str]= None, children:Optional[List['HTMLNode']]= None, props: Optional[Dict[str, str]] = None):
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


class ParentNode(HTMLNode):
    def __init__(self, tag: Optional[str], children: Optional[List['HTMLNode']], props: Optional[Dict[str,str]] = None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        props_html = self.props_to_html()

        result = f"<{self.tag}{props_html}>"

        for child in self.children:
            result += child.to_html()

        result += f"</{self.tag}>"

        return result


class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: Optional[str], props: Optional[Dict[str,str]]=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self)-> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
