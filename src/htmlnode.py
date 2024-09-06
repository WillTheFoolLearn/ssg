class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return " " + " ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))
    
    def __repr__(self):
        return f"HTMLNode: {self.tag}, {self.value}, {self.children}, {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, value, tag = None, props = None):
        super().__init__(tag, value, None, props)

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

    def to_html(self):
        # if not self.value:
        #     raise ValueError
        
        if not self.tag:
            return self.value
        
        if self.props:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, children, tag = None, props = None):
        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        if isinstance(other,  ParentNode):
            return self.tag == other.tag and self.children == other.children and self.props == other.props
        
        return False
    
    def to_html(self):
        if not self.tag:
            raise ValueError
        if not self.children:
            raise ValueError("You will die alone")
        if not self.children:
            return ""
        HTMLstring = ''

        if self.props:
            HTMLstring += f'<{self.tag}{self.props_to_html()}>'
        else: 
            HTMLstring += f'<{self.tag}>'

        for node in self.children:
            HTMLstring += f'{node.to_html()}'
        HTMLstring += f'</{self.tag}>'
        return HTMLstring
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(text_node.text)
        case "bold":
            return LeafNode(text_node.text, "b")
        case "italic":
            return LeafNode(text_node.text, "i")
        case "code":
            return LeafNode(text_node.text, "code")
        case "link":
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case "image":
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Where are the kitty cats?!")
            

def main():
    test_node = HTMLNode("p", "I am hungry", [], {"align": "center"})
    print(test_node)

main()