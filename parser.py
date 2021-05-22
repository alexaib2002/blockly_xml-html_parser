# python packages
from typing import Dict
import xml.etree.ElementTree as Tree

# switchcase package
from switchcase import switch

# dominate package
import dominate
from dominate import *
from dominate.tags import *


def namespace(element):
    """
    Gets the namespace of the XML tag.
    :param element:
    """
    import re
    m = re.match(r'\{.*\}', element.tag)
    return m.group(0) if m else ''


def get_next_xml_tag(tag: Tree.Element) -> Tree.Element:
    """
    Gets the child of <next> tag on XML source.
    :param tag:
    :return: Tree.Element
    """
    return tag.find("%snext" % xml_namespace)[0]


def get_statement_xml_tag(tag: Tree.Element) -> Tree.Element:
    """
    Gets the child of <statement> tag on XML source.
    :param tag:
    :return: Tree.Element
    """
    return tag.find("%sstatement" % xml_namespace)[0]


def parse_statement(block: Tree.Element, tag: html_tag, add_element: html_tag = None) -> None:
    """
    Parses every block inside of the 'statement' block.
    :param block:
    :param tag:
    :param add_element:
    :return:
    """
    try:
        next_tag = get_statement_xml_tag(block)
        while next_tag is not None:  # Ugly trick
            if add_element is not None:
                add_element += make_html_tag(next_tag)
                tag += add_element
                breakpoint()
            else:
                tag += make_html_tag(next_tag)
            next_tag = get_next_xml_tag(next_tag)
    except Exception:
        pass

# while next_tag is not None:
#     if add_element is not None:
#         add_element += make_html_tag(next_tag)
#         tag += add_element
#     else:
#         tag += make_html_tag(next_tag)


def make_html_tag(block) -> html_tag:
    """
    Creates an HTML tag based on the passed block.
    """
    for case in switch(block.attrib.get('type')):
        if case("form_block"):
            tag = form()
            tag['name'] = block[0].text
            tag['action'] = block[1].text
            tag['method'] = block[2].text
            parse_statement(block, tag)
        if case("button_block"):
            tag = button(block[1].text)  # User-given text
            tag['type'] = block[0].text
        if case("input_block"):
            tag = input_()
            tag['name'] = block[0].text
            tag['value'] = block[1].text
            tag['type'] = block[2].text
        if case("list_block"):
            ty = block[0]
            if ty == 'ol':
                tag = ol()
            else:
                tag = ul()
            parse_statement(block, tag, li())
        if case("text_area"):
            tag = textarea()
            tag['name'] = block[0].text
            tag['form'] = block[1].text
        return tag
    else:
        print("No matching type %s" % (block.attrib.get('type')))


try:
    # input and basic settings
    file: str = 'map.xml'
    css: str = 'styles.css'
    OUT_NAME = 'index'
    # xml parser
    try:
        tree = Tree.parse(file)
        root = tree.getroot()
        xml_namespace = namespace(root)
        doc: document = dominate.document(title="Blockly Parsed")
    except Exception:
        print("Cannot open map.xml file")

    if __name__ == "__main__":  # main statement
        try:
            css = open(css)
            with doc.head:
                style(css.read())
            css.close()
        except Exception:
            print("Cannot open CSS File")
        with doc:
            make_html_tag(root[0])
        print(doc)
        output_file = open('%s.html' % OUT_NAME, 'w')
        output_file.write(str(doc))
        output_file.close()
except Exception:
    print("Something went wrong")
