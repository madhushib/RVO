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
        
rdf = """
adage:{} rdf:type owl:NamedIndividual,
analytics:LinkedVariables;
analytics:firstVariable adage:{};
analytics:linkType analytics:{};
analytics:secondVariable adage:{};
analytics:origin adage:{}origin.

adage:{}origin rdf:type owl:NamedIndividual ,
analytics:Origin;
{}
{}.\n
"""

import pandas as pd
df = pd.read_excel("MacroDataList ver 4 Ali.xlsx", sheet_name="var link",  dtype = str)
df = df.replace('nan', '')

file = open("phase0.ttl","w")

file.write(prefix)
for index, row in df.iterrows():
    adages = []
    originType = []
    
    if row["Link Origin - Model"] is not '' :
        originType.append("analytics:ViaModel")
        adages.extend(row["Link Origin - Model"].replace(" ", "").split(","))

    if row["Link Origin - Ref"] is not '' :
        originType.append("analytics:ViaLiterature")
        adages.extend(row["Link Origin - Ref"].replace(" ", "").split(","))
        
    if row["Link Origin - People"] is not '' :
        originType.append("analytics:FromExpert")
        adages.extend(row["Link Origin - People"].replace(" ", "").split(","))
        
    originTypeStr = ''
    adagesStr = ''
    if len(originType) > 0 :
        originTypeStr = "analytics:originType " + ",".join(originType) + ";"
        adages = ["adage:" + s for s in adages]
        adagesStr = "analytics:referenceOfOrigin " + ",".join(adages)
        
    file.write(rdf.format(row["Var Link ID"], row["Var 1"], row["Link Type"], row["Var 2"], row["Var Link ID"], row["Var Link ID"], originTypeStr, adagesStr))

file.close()
