from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD
from pandas import read_csv

# Carregar o grafo RDF existente
g = Graph()
g.parse("medical.ttl")

# Definir o namespace do seu grafo RDF
disease = Namespace("http://www.example.org/disease-ontology#")

# Função para formatar URIs
def format_uri(id):
    return URIRef(id)

# Abrir o arquivo csv e ler os dados
with open("Disease_Syntoms.csv", "r") as csv_file:
    data = read_csv(csv_file, delimiter=",")


# Iterar sobre cada entrada no arquivo csv e adicionar as informações ao grafo RDF
for i in range(1, len(data)):
    # remove spaces from disease name
    temp = data["Disease"][i].replace(" ", "_")
    disease_uri = format_uri(temp)
    g.add((disease_uri, RDF.type, disease.Disease))
    #for every field in the row except the first one, add a triple
    for j in range(1, len(data.columns)):
        text = "Symptom_" + str(j)
        tmp = str(data[text][i])[1:]
        if tmp != "nan":
            g.add((disease_uri, disease.hasSymptom, Literal(tmp)))
            # create a new URI for each symptom
            symptom_uri = format_uri(tmp)
            g.add((symptom_uri, RDF.type, disease.Symptom))
        
# Salvar o grafo RDF atualizado
#g.serialize(destination="disease-populated.ttl", format="turtle")

# Open the file with the content to prepend
#with open('disease-base.ttl', 'r') as prepend_file:
#    prepend_content = prepend_file.read()

# Open the target file in read mode to get its original content  
#with open('disease-populated.ttl', 'r') as target_file:
#    target_content = target_file.read()

# Open the target file in write mode and prepend the content
#with open('disease-populated.ttl', 'w') as target_file:
#    target_file.write(prepend_content + target_content)

print(g.serialize())
