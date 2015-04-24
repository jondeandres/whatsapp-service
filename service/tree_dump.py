import json
import base64

def dump(node):
    return json.dumps(to_hash(node))

def to_hash(node):
    hash = {}

    hash['tag'] = node.tag
    hash['data'] = base64.b64encode(node.data) if node.data is not None else None

    for key, value in node.attributes.items():
        hash[key] = value

    hash['nodes'] = {}

    for child in (node.children or []):
        hash['nodes'][child.tag] = to_hash(child)

    return hash

