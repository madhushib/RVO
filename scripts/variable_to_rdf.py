import pandas as pd

prefix = """
@prefix dbr: <http://dbpedia.org/resource/>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix xml: <http://www.w3.org/XML/1998/namespace>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix analytics: <http://w3id.org/rv-ontology#>.
@prefix adage: <http://adage.cse.unsw.edu.au/resource/analytics#>.\n
"""

item ="""adage:{} rdf:type owl:NamedIndividual,analytics:Variable;
{}                                analytics:operationalize {};
                                analytics:origin {};
                                rdfs:label "{}"^^rdfs:Literal.\n"""

preformat_measure = """                                analytics:measuredBy {};
"""
ADAGE = 0
OPERATIONALIZE = 1

def getElements(larray, mode) :
    elementsArray = []
    for m in larray :
        if m != "" :
            if mode == ADAGE :
                elementsArray.append("adage:" + m.strip())
            else :
                elementsArray.append("dbr:" + m.replace(" ","_").capitalize())
    elements = ",".join(elementsArray)
    return elements

df = pd.read_excel("MacroDataList ver 4 Ali.xlsx", sheet_name="variable",  dtype = str)
df = df.replace('nan', '')
with open("phase0.ttl","w") as file :
    file.write(prefix)
    for _, row in df.iterrows():
        larray = row.tolist()
        if larray[4] == '' :
            measure = '';
        else :
            measure = preformat_measure.format(getElements(larray[4].split(","), ADAGE))
        operationalize = getElements(larray[5:], OPERATIONALIZE)
        reference = getElements(larray[2].split(",") + larray[3].split(","), ADAGE)
        file.write(item.format(larray[0], measure, operationalize, reference, larray[1]))
