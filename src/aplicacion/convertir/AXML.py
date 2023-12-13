import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

# Crear un DataFrame de ejemplo
data = {'Nombre': ['Juan', 'María', 'Carlos'],
        'Edad': [25, 30, 22],
        'Ciudad': ['México', 'Madrid', 'Buenos Aires']}

df = pd.DataFrame(data)

# Convertir el DataFrame a XML
root = Element('Personas')
for index, row in df.iterrows():
    persona = SubElement(root, 'Persona')
    for col, value in row.items():
        SubElement(persona, col).text = str(value)

# Convertir el árbol XML a una cadena con formato
xml_str = tostring(root, 'utf-8')
xml_pretty_str = minidom.parseString(xml_str).toprettyxml(indent="  ")

# Guardar el resultado en un archivo
with open('personas.xml', 'w') as xml_file:
    xml_file.write(xml_pretty_str)
