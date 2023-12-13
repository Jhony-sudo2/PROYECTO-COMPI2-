import pandas as pd
from xml.etree.ElementTree import parse

# Cargar el archivo XML
tree = parse('personas.xml')
root = tree.getroot()

# Crear un DataFrame a partir del XML
data = []
for persona in root.findall('Persona'):
    row = {}
    for child in persona:
        row[child.tag] = child.text
    data.append(row)

df_from_xml = pd.DataFrame(data)

# Imprimir el DataFrame resultante
print(df_from_xml)
