import csv
import json
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

with open("pg53651.json", "r") as json_file:
    patients = json.load(json_file)

# Iterar sobre cada paciente no arquivo JSON e adicionar as informações ao grafo RDF
for idx, patient in enumerate(patients):
    patient_id = "p" + str(idx + 1)  # Gerar um ID para o paciente
    patient_uri = uri_format(patient_id)
    g.add((patient_uri, RDF.type, OWL.NamedIndividual))
    g.add((patient_uri, RDF.type, medical.Patient))
    g.add((patient_uri, medical.name, Literal(patient['nome'])))  # Adicionar o nome do paciente

    # Adicionar os sintomas associados ao paciente
    for symptom in patient['sintomas']:
        symptom_uri = uri_format(symptom)
        g.add((patient_uri, medical.exhibitsSymptom, symptom_uri))

g.serialize(destination="med_doencas.ttl", format="turtle")