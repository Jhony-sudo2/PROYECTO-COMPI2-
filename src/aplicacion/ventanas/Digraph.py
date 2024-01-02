import subprocess
import os
import tempfile


class Digraph(object):
    def __init__(self, comment='Abstract Syntax Tree'):
        self.nodes = {}
        self.comment = comment

    def node(self, name, label):
        self.nodes[name] = label

    def edge(self, from_node, to_node):
        self.nodes[from_node] = f'{self.nodes[from_node]} -> {to_node}'

    def render(self, filename, view=False):
        with open(filename, 'w') as f:
            f.write(f'digraph {self.comment} {{')
            for node, label in self.nodes.items():
                f.write(f'  {node} [label="{label}"];')
            for from_node, to_node in self.nodes.items():
                if to_node not in self.nodes:
                    continue
                f.write(f'  {from_node} -> {to_node};')
            f.write('}')
        if view:
            temp_dir = tempfile.gettempdir()
            filename = os.path.join(temp_dir, "ast.dot.png")
            subprocess.run(["dot", "-Tpng", filename, "-o", filename])  # Sin `dot_path`

            #dot_path = os.getcwd()# Reemplaza con la ruta real a `dot`
            #subprocess.run([dot_path, "-Tpng", filename, "-o", filename + ".png"])
            #subprocess.run(f'{dot_path}, -Tpng {filename} -o {filename}.png')

