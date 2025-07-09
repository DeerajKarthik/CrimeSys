
from pyvis.network import Network
import networkx as nx
import tempfile
import os

def get_node_color(label):
    color_map = {
        'Person': '#FFD700',
        'Crime': '#FF6347',
        'Location': '#87CEEB',
        'Officer': '#90EE90',
        'Object': '#DDA0DD',
        'Vehicle': '#00CED1',
        'Phone': '#B0C4DE',
        'PhoneCall': '#FFA07A',
        'Email': '#F08080',
        'PostCode': '#20B2AA',
        'AREA': '#BDB76B',
    }
    return color_map.get(label, '#CCCCCC')

def render_graph(results):
    
    if not results or not isinstance(results, list):
        return None

    G = nx.MultiDiGraph()
    node_labels = {}
    edge_labels = {}
    node_colors = {}

    def add_node(n):
        if hasattr(n, 'labels'):
            label = list(n.labels)[0] if n.labels else 'Node'
            node_id = n.id
            props = dict(n)
            title = '<br>'.join(f"{k}: {v}" for k, v in props.items())
            G.add_node(node_id, label=label, title=title)
            node_labels[node_id] = f"{label}: {props.get('name', props.get('id', node_id))}"
            node_colors[node_id] = get_node_color(label)
        elif isinstance(n, dict) and 'labels' in n:
            label = n.get('labels', ['Node'])[0]
            node_id = n.get('id')
            title = '<br>'.join(f"{k}: {v}" for k, v in n.items())
            G.add_node(node_id, label=label, title=title)
            node_labels[node_id] = f"{label}: {n.get('name', node_id)}"
            node_colors[node_id] = get_node_color(label)

    def add_edge(start, end, rel_type):
        G.add_edge(start, end, label=rel_type, title=rel_type)

    for rec in results:
        for v in rec.values():
            if hasattr(v, 'nodes') and hasattr(v, 'relationships'):
                nodes = v.nodes
                rels = v.relationships
                for n in nodes:
                    add_node(n)
                for r in rels:
                    add_edge(r.start_node.id, r.end_node.id, r.type)
            elif hasattr(v, 'labels') and hasattr(v, 'id'):
                add_node(v)
            elif hasattr(v, 'type') and hasattr(v, 'start_node') and hasattr(v, 'end_node'):
                add_edge(v.start_node.id, v.end_node.id, v.type)
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, dict) and 'labels' in v2:
                        add_node(v2)

    if len(G.nodes) == 0:
        return None

    net = Network(height="500px", width="100%", directed=True, notebook=False)
    for n, data in G.nodes(data=True):
        net.add_node(n, label=node_labels.get(n, str(n)), title=data.get('title', ''), color=node_colors.get(n, '#CCCCCC'))
    for u, v, data in G.edges(data=True):
        net.add_edge(u, v, label=data.get('label', ''), title=data.get('label', ''))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.show(tmp_file.name)
        tmp_file.flush()
        with open(tmp_file.name, "r", encoding="utf-8") as f:
            html = f.read()
        os.unlink(tmp_file.name)
    return html 