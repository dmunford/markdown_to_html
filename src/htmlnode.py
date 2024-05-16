class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented()

    def props_to_html(self):
        html = []
        for key, prop in self.props.items():
            html.append(f"{key}=\"{prop}\"")
        return " ".join(html)

    def __repr__(self):
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Missing Value")
        if self.tag is None:
            return str(self.value)
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            # Not sure if this is how it should be done or not?
            return_text = []
            for key, prop in self.props.items():
                return_text.append(f"<{self.tag} {key}=\"{prop}\">{self.value}</{self.tag}>")
            return "".join(return_text)

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing Tag")
        if self.children is None:
            raise ValueError("Missing Children")
        return_text = ""
        return_text += f"<{self.tag}>"
        for child in self.children:
            return_text += child.to_html()
        return_text += f"</{self.tag}>"
        return return_text
