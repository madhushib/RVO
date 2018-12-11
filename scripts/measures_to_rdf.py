import pandas as pd
import numpy as np

header = \
"""@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix analytics: <http://w3id.org/rv-ontology#> .
@prefix adage: <http://adage.cse.unsw.edu.au/resource/analytics#> .

"""

# DatasourceID, Link, Name (Dataset)
ds_template = """
adage:{id} rdf:type owl:NamedIndividual , analytics:DataSource ;
                   analytics:webLink "{link}"^^xsd:anyURI ;
                   rdfs:label "{name}"^^rdfs:Literal .

"""


def write_datasource(file_handle, datasource):
    for _, row in datasource.iterrows():
        if row['Datasource ID'] == '':
            continue
        lines = []
        lines.append('adage:{id} rdf:type owl:NamedIndividual , analytics:DataSource '.format(id=row['Datasource ID']))
        if row['Web link'] != '':
            lines.append('                   analytics:webLink "{link}"^^xsd:anyURI '.format(link=row['Web link']))
        if row['Name'] != '':
            lines.append('                   rdfs:label "{name}"^^rdfs:Literal '.format(name=row['Name']))
        buffer = ';\n'.join(lines) + '.\n\n'
        file_handle.write(buffer)


# Data structure ID, Name, Web Link, Description, Data source ID
dataset_template ="""
adage:{id} rdf:type owl:NamedIndividual , analytics:DatasetStructure ;
                   analytics:webLink "{link}"xsd:anyURI ;
                   rdfs:label "{name}"^^rdfs:Literal;
            	   rdfs:comment "{desc}"^^rdfs:Literal;
                   analytics:dataSource adage:{ref} .

"""

def write_dataset(file_handle, dataset):
    for _, row in dataset.iterrows():
        if row['Dataset structure ID'] == '':
            continue
        lines = []
        lines.append('adage:{id} rdf:type owl:NamedIndividual , analytics:DatasetStructure '.format(id=row['Dataset structure ID']))
        if row['Web link'] != '':
            # TODO: Double check this
            lines.append('                   analytics:webLink "{link}"^^xsd:anyURI '.format(link=row['Web link']))
        if row['Name'] != '':
            lines.append('                   rdfs:label "{name}"^^rdfs:Literal '.format(name=row['Name']))
        if row['Description'] != '':
            lines.append('            	   rdfs:comment "{desc}"^^rdfs:Literal '.format(desc=row['Description']))
        if row['Datasource ID'] != '':
            lines.append('                   analytics:dataSource adage:{ref} '.format(ref=row['Datasource ID']))
        buffer = ';\n'.join(lines) + '.\n\n'
        file_handle.write(buffer)

# MeasureID, DatasourceRef, MeasureRef, Comment?, MeasureName
ms_template = """
adage:{id} rdf:type owl:NamedIndividual , analytics:Measure ;
                   analytics:measureReferenceInDatasource "{mref}"^^rdfs:Literal ;
                   rdfs:comment "{desc}"^^rdfs:Literal ;
                   rdfs:label "{name}"^^rdfs:Literal .

adage:{sref}   analytics:containMeasure adage:{id} .

"""


def write_measures(file_handle, measure):
    for _, row in measure.iterrows():
        if row['Measure ID'] == '':
            continue

        lines = []
        lines.append('adage:{id} rdf:type owl:NamedIndividual , analytics:Measure '.format(id=row['Measure ID']))

        if row['Measure Ref @ Datasource'] != '':
            lines.append('                   analytics:measureReferenceInDatasource "{mref}"^^rdfs:Literal '.format(mref=row['Measure Ref @ Datasource']))

        if row['Description'] != '':
            lines.append('                   rdfs:comment "{desc}"^^rdfs:Literal '.format(desc=row['Description']))

        if row['Measure Name'] != '':
            lines.append('                   rdfs:label "{name}"^^rdfs:Literal '.format(name=row['Measure Name']))


        buffer = ';\n'.join(lines) + '.\n\n'
        file_handle.write(buffer)

        if row['Source Reference'] != '':
            file_handle.write('adage:{sref}   analytics:containMeasure adage:{id} .\n\n'.format(
                sref=row['Source Reference'],
                id=row['Measure ID'],
            ))


if __name__ == '__main__':
    dataset = pd.read_excel('MeasureData ver 4.xlsx', 'dataset_structure')
    datasource = pd.read_excel('MeasureData ver 4.xlsx', 'Datasource')
    measure = pd.read_excel('MeasureData ver 4.xlsx', 'Measures')


    dataset = dataset.fillna('')
    datasource = datasource.fillna('')
    measure = measure.fillna('')

    dataset = dataset.replace(r'\s+', ' ', regex=True)
    datasource = datasource.replace(r'\s+', ' ', regex=True)
    measure = measure.replace(r'\s+', ' ', regex=True)

    with open('measures.ttl', 'w') as file:
        file.write(header)
        write_datasource(file, datasource)
        write_dataset(file, dataset)
        write_measures(file, measure)
