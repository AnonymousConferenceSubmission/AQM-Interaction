import rdflib
import os
from rdflib.namespace import RDFS, OWL
from application.owl2vowl import convert

#IRI constants
a = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Assess")
c = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Control")
es = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Estimate")
im = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Improve")
ma = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Manage")
me = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Measure")
mo = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Monitor")
pr = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Predict")
sp = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Specify")
so = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Source")
co = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#Construct")

def getAQM():
    
    #Load current backup of the AQM
    aqm = rdflib.Graph(base="http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#")
    
    aqm.parse(os.path.join(str(os.getcwd()) + "\\application\\static\\data\\AQM.owl"))
    
    #Save a subgraph and convert to JSON for WebVOWL
    aqm.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    convert()


def createAQMSubgraphForConsensus(source):
    
    #Load current backup of the AQM
    aqm = rdflib.Graph(base="http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#")
    
    aqm.parse(os.path.join(str(os.getcwd()) + "\\application\\static\\data\\AQM.owl"))

    subgraph = rdflib.Graph()
    
    for s, p, o in aqm.triples((None, so, rdflib.Literal(source, lang="en"))):
        
        subgraph.add((s,p,o))
        
        #For given subject, add annotation properties
        for s1, p1, o1 in aqm.triples((s, None, None)):
            subgraph.add((s1,p1,o1))
        
        #For a given subject, add related subjects
        for s2, p2, o2 in aqm.triples((None, None, s)):
            subgraph.add((s1,p1,o1))
        
        #For a given object, add object properties
        for s3, p3, o3 in aqm.triples((None, RDFS.range, s)):
            subgraph.add((s3,p3,o3))
            
            #For a given object property, add the respective domain
            for s33, p33, o33 in aqm.triples((s3, RDFS.domain, None)):
                subgraph.add((s33,p33,o33))            
                
                #For a given subject, add annotation properties
                for s333, p333, o333 in aqm.triples((o33, None, None)):
                    subgraph.add((s333,p333,o333))
                
                #For a given object property, add annotations
                for s334, p334, o334 in aqm.triples((s33, None, None)):
                    subgraph.add((s334,p334,o334))
                    
        #For a given subject, add object properties
        for s4, p4, o4 in aqm.triples((None, RDFS.domain, s)):
            subgraph.add((s4,p4,o4))
            
            #For a given object property, add the respective domain
            for s44, p44, o44 in aqm.triples((s4, RDFS.domain, None)):
                subgraph.add((s44,p44,o44))
    
    #Save a subgraph and convert to JSON for WebVOWL
    subgraph.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    convert()

def createAQMSubgraphForMeasurement(source):
    
    #Load current backup of the AQM
    aqm = rdflib.Graph(base="http://www.semanticweb.org/beyersdo/ontologies/2022/10/SRS_QualityCharacteristics#")
    
    aqm.parse(os.path.join(str(os.getcwd()) + "\\application\\static\\data\\AQM.owl"))

    subgraph = rdflib.Graph()
    
    for s, p, o in aqm.triples((None, so, rdflib.Literal(source, lang="en"))):
        
        subgraph.add((s,p,o))
        
        #For given subject, add annotation properties
        for s1, p1, o1 in aqm.triples((s, None, None)):
            subgraph.add((s1,p1,o1))
        
        #For a given subject, add related subjects
        for s2, p2, o2 in aqm.triples((None, None, s)):
            subgraph.add((s1,p1,o1))
        
        #For a given object, add object properties
        for s3, p3, o3 in aqm.triples((None, RDFS.range, s)):
            subgraph.add((s3,p3,o3))
            
            #For a given object property, add the respective domain
            for s33, p33, o33 in aqm.triples((s3, RDFS.domain, None)):
                subgraph.add((s33,p33,o33))            
                
                #For a given subject, add annotation properties
                for s333, p333, o333 in aqm.triples((o33, None, None)):
                    subgraph.add((s333,p333,o333))
                
                #For a given object property, add annotations
                for s334, p334, o334 in aqm.triples((s33, None, None)):
                    subgraph.add((s334,p334,o334))
                    
        #For a given subject, add object properties
        for s4, p4, o4 in aqm.triples((None, RDFS.domain, s)):
            subgraph.add((s4,p4,o4))
            
            #For a given object property, add the respective domain
            for s44, p44, o44 in aqm.triples((s4, RDFS.domain, None)):
                subgraph.add((s44,p44,o44))
    
    subgraphMeasurement = rdflib.Graph()
    subgraphMeasurement = subgraphMeasurement + subgraph
    purposes = [a, c, es, im, ma, me, mo, pr]


    for s, p, o in subgraph.triples((None, RDFS.subClassOf, co)):
        for sA, pA, oA in aqm.triples((None, RDFS.domain, s)):
            for sB, pB, oB in aqm.triples((sA, RDFS.range, None)):
                
                if oB in purposes:
                    subgraphMeasurement.add((sA, pA, oA))
                    for sC, pC, oC in aqm.triples((sA, RDFS.label, None)):
                        subgraphMeasurement.add((sC, pC, oC))
                    subgraphMeasurement.add((sB, pB, oB))
                    for sD, pD, oD in aqm.triples((sB, RDFS.label, None)):
                        subgraphMeasurement.add((sD, pD, oD))
                    
                if oB == sp:
                    print(str(s) + " - " + str(oB))
                    subgraphMeasurement.remove((s, None, None))
                    subgraphMeasurement.remove((None, None, s))
    
    #Save a subgraph and convert to JSON for WebVOWL
    subgraphMeasurement.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    convert()
    
    
