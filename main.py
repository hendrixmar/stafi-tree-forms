import csv
import math
import random
import json
from typing import Optional

from streamlit.runtime.uploaded_file_manager import UploadedFile


def search_button_node(nodes: dict[str, dict], node_id: str) -> dict:
    for node_key, node in nodes.items():
        for _, button in node["buttons"].items():
            if button["button_link"] == node_id:
                yield node


def search_node(nodes: dict[str, dict], node_id: str) -> Optional[dict]:
    return nodes.get(node_id)


def next_node_to_connect__(next_node: str, tree: dict[str, dict], nodes_settings: dict) -> str:
    if (node_found := nodes_settings.get(next_node)) and node_found['include'] == '1':
        return next_node

    if next_node in tree['nodes']:
        temp_node = tree['nodes'][next_node]["buttons"]["0"]["button_link"]
        del tree['nodes'][next_node]

        next_node_to_connect__(temp_node, tree, nodes_settings)


def delete_node(nodes: dict[str, dict], node_id: str):
    if node_id not in nodes['nodes']:
        return

    del nodes['nodes'][node_id]


def next_node_to_connect(next_node: str, tree: dict[str, dict], nodes_settings: dict) -> str:
    if (node_found := nodes_settings.get(next_node)) and node_found['include']:
        return next_node
    elif next_node not in nodes_settings:
        return next_node

    if next_node in tree['nodes']:
        temp_node = tree['nodes'][next_node]["buttons"]["0"]["button_link"]
        return next_node_to_connect(temp_node, tree, nodes_settings)


# get the node that should no be included
# find the next node of that node that is included and delete all the childs that are not included
# find out the node that have that node


# test_2()


def load_settings(file_uploaded: UploadedFile):
    positions = [
        None, None, None, 39, 40, 41,
        42, 70, 44, 47, 48, 49, 50, 54,
        55, 56, 57, 58, 60, 62, 64, 65,
        66, 67, 51, 52, 61, 63, 68
    ]
    nodes = {i: str(e) for i, e in enumerate(positions) if e is not None}
    settings = {}

    import pandas as pd

    data = pd.read_csv(file_uploaded)
    for index, col in enumerate(data.iloc[0]):
        if isinstance(col, str):
            settings[nodes[index]] = {'include': bool(col == 'TRUE'), 'node': nodes[index]}

    return settings


def create_tree(zoho_report: UploadedFile, zingtree_json: Optional[UploadedFile] = None):

    if zingtree_json is None:
        with open('example.json', 'r') as fp:
            zingtree = json.load(fp)
    else:
        zingtree = json.loads(zingtree_json.read())

    #with open(file_name.name, 'r') as fp:
    #    settings = {row['node']: row for row in csv.DictReader(fp)}
    settings = load_settings(zoho_report)
    node_deletes = []
    for node_ide, setting in settings.items():
        if not setting['include']:
            result = next_node_to_connect(setting['node'], zingtree, settings)
            node_deletes.append(node_ide)
            for node_button in search_button_node(zingtree["nodes"], setting['node']):
                # delete_node(zingtree, setting['node'])
                if node_button:
                    project = node_button['project_node_id']
                    for key in zingtree["nodes"][project]["buttons"]:
                        button = zingtree["nodes"][project]["buttons"][key]
                        button['button_link'] = result

    for node in node_deletes:
        delete_node(zingtree, node)

    return zingtree


