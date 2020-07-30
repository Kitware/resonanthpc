"""A few conveinance methods for reading these templates and gemerating XML elements"""

from xml.dom.minidom import parseString
import os

TEMPLATES_DIR = os.path.dirname(__file__)


def append_template(parent, fname, mapping=None):
    """All key/value pairs in ``mapping`` dict will be swapped.

    For example, the key `${NAME}` in the template will be replaced with whatever
    value is passed in the mapping dict.

    This will return a `xml.dom.minidom.Document` object
    """
    if mapping is None:
        mapping = {}
    path = os.path.join(TEMPLATES_DIR, fname)
    with open(path, "r") as f:
        content = f.read()
    for key, value in mapping.items():
        # TODO: optimize
        content = content.replace(key, value)
    # Create XML objects of it.
    nodes = parseString(content).childNodes
    if len(nodes) != 1:
        raise AssertionError("This has too many nodes, can't do that.")
    node = nodes[0]
    parent.appendChild(node)
    return node  # Return the node so that we can add the time integrator to PK
