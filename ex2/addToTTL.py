import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, OWL, XSD

from icecream import ic

g = Graph()
g.parse("medical.ttl")

medical = Namespace('http://www.example.org/disease-ontology#')

def uri_format(individuo):
    return URIRef(f"""{medical}{individuo.replace(' ', "_").replace('"', '').replace('%', '')}""")

doencas = {}

with open("Disease_Syntoms.csv", "r") as file:
    content = csv.reader(file)
    keys = []
    for c in content:
        if len(keys) == 0:
            keys = c
        else:
            if c[0] not in doencas.keys():
                doenca = {"doenca": c[0].strip(), "sintomas": set()}
            else:
                doenca = doencas[c[0].strip()]
            for k in range(1, len(keys)):
                if len(c[k].strip()) > 0:
                    doenca["sintomas"].add(c[k].strip())
            doencas[c[0].strip()] = doenca

        
for k in doencas.keys():
    doenca_uri = uri_format(k)
    g.add((doenca_uri, RDF.type, OWL.NamedIndividual))
    g.add((doenca_uri, RDF.type, medical.Disease))
    for sintoma in doencas[k]["sintomas"]:
        sintoma_uri = uri_format(sintoma)
        g.add((sintoma_uri, RDF.type, OWL.NamedIndividual))
        g.add((sintoma_uri, RDF.type, medical.Symptom))
        g.add((doenca_uri, medical.hasSymptom, sintoma_uri))

g.serialize(destination="med_doencas.ttl", format="turtle")