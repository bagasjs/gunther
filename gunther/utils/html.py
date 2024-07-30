from __future__ import annotations
from typing import Dict, List, Any

class HTMLElement(object):
    def __init__(self, tag: str, attrs: Dict[str, str], children: List[HTMLElement|str]):
        self.tag = tag
        self.attrs = attrs
        self.children = children

    def setattr(self, key, value) -> HTMLElement:
        self.attrs[key] = value
        return self

    def addchildren(self, *children: HTMLElement|str) -> HTMLElement:
        for child in children:
            self.children.append(child)
        return self

def render_element_to_html_string(element) -> str:
     # Convert attributes dictionary to a string
    attrs_str = ' '.join(f'{key}="{value}"' for key, value in element.attrs.items())
    if attrs_str:
        attrs_str = ' ' + attrs_str

    # Convert children to their string representations
    children_str = ''.join(render_element_to_html_string(child) 
                           if isinstance(child, HTMLElement) else child for child in element.children)

    # Form the final HTML string
    if element.children:
        return f'<{element.tag}{attrs_str}>{children_str}</{element.tag}>'
    else:
        return f'<{element.tag}{attrs_str}/>'

 
class p(HTMLElement):
    def __init__(self, *stringifyable: Any, attrs: Dict[str,str]|None = None):
        super().__init__("p", attrs if attrs != None else {}, [" ".join(stringifyable)])

class h1(HTMLElement):
    def __init__(self, *stringifyable: Any, attrs: Dict[str,str]|None = None):
        super().__init__("h1", attrs if attrs != None else {}, [" ".join(stringifyable)])

class h2(HTMLElement):
    def __init__(self, *stringifyable: Any, attrs: Dict[str,str]|None = None):
        super().__init__("h2", attrs if attrs != None else {}, [" ".join(stringifyable)])

class h3(HTMLElement):
    def __init__(self, *stringifyable: Any, attrs: Dict[str,str]|None = None):
        super().__init__("h3", attrs if attrs != None else {}, [" ".join(stringifyable)])

class div(HTMLElement):
    def __init__(self, *children: HTMLElement, attrs: Dict[str,str]|None = None):
        super().__init__("div", attrs if attrs != None else {}, list(children))

class center(HTMLElement):
    def __init__(self, *children: HTMLElement, attrs: Dict[str,str]|None = None):
        super().__init__("center", attrs if attrs != None else {}, list(children))

class ol(HTMLElement):
    def __init__(self, *children: HTMLElement, attrs: Dict[str,str]|None = None):
        super().__init__("ol", attrs if attrs != None else {}, list(children))

class ul(HTMLElement):
    def __init__(self, *children: HTMLElement, attrs: Dict[str,str]|None = None):
        super().__init__("ul", attrs if attrs != None else {}, list(children))

class li(HTMLElement):
    def __init__(self, *children: HTMLElement, attrs: Dict[str,str]|None = None):
        super().__init__("li", attrs if attrs != None else {}, list(children))

