import rdflib
import os
from rdflib import Namespace
from rdflib.namespace import RDF, RDFS, OWL
from application.owl2vowl import convert

#IRI constants
a = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Assess")
c = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Control")
es = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Estimate")
im = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Improve")
ma = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Manage")
me = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Measure")
mo = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Monitor")
pr = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Predict")
sp = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Specify")
ci = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Citation")
pu = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Purpose")
hRS = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#hasRefinementStructureC")
eq = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#E01")
co = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#Construct")
qa = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#QualityAttribute")
vf = rdflib.URIRef("http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#VariationFactor")


purposes = [a, c, es, im, ma, me, mo, pr, sp]
measurement_purposes = [a, c, es, im, ma, me, mo, pr]



def getAQM(conversion=True):
    """
        Load and serialize the full AQM for displaying in WebVOWL
    """
    
    #Load current backup of the AQM
    aqm = rdflib.Graph(base="http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#")
    aqm.parse(os.path.join(str(os.getcwd()) + "\\application\\static\\data\\AQM.owl"))
    
    #Save the graph and convert to JSON for WebVOWL
    aqm.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    if conversion:
        convert()
    else:
        return aqm


def createAQMSubgraphForConsensus(source, conversion=True):
    """
        This function shall enable the analysis of semantic equivalence of one quality model (source) with the others in the AQM.
        A subgraph of the AQM is needed, containing the requested quality model (source) and quality attributes of other quality models,
        that are aligned via the isEquivalent object property. 
        
        Note: The source needs to be a string representation of the annotation property "Citation" in the AQM (currently in AlphaBixTex format)
    """
    
    #Load the current backup of the AQM and create an empty subgraph
    aqm = rdflib.Graph(base="http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#")
    aqm.parse(os.path.join(str(os.getcwd()) + "\\application\\static\\data\\AQM.owl"))

    subgraph = rdflib.Graph()
    
    #Iterate through all triples with the annotation property "Citation" and having the value of the requested source.
    for s, p, o in aqm.triples((None, ci, rdflib.Literal(source, lang="en"))):
        
        subgraph.add((s,p,o)) #subgraph now contains all quality attributes / variation factors of the requested quality model
        
        #For given quality attribute / variation factor, add properties (e.g. subClassOf or annotations)
        for s1, p1, o1 in aqm.triples((s, None, None)):
            subgraph.add((s1,p1,o1))        
        
        #For a given quality attributes / variation factors, add related attributes / factors (e.g. RefinementStructures or isEquivalent)
        for s2, p2, o2 in aqm.triples((None, None, s)):
            subgraph.add((s2,p2,o2))
        
            #For a related quality attribute / factor, add properties (e.g. subClassOf, annotations, hasPurpose)
            for s3, p3, o3 in aqm.triples((s2, None, None)):
                
                subgraph.add((s3,p3,o3))
            
                #For given quality attribute / variation factor, add properties (e.g. subClassOf or annotations)
                for s4, p4, o4 in aqm.triples((o3, None, None)):
                    subgraph.add((s4,p4,o4))    
    
    #Remove additional super-level elements as well as purpuses to focus on the quality attributes
    for s5, p5, o5 in subgraph.triples((None, RDFS.label, rdflib.Literal("hasPurpose", lang="en"))):
        subgraph.remove((s5, None, None))
    
    for s6, p6, o6 in subgraph.triples((None, None, None)):
        if s6 in purposes or s6 == co or s6 == pu:
            subgraph.remove((s6, None, None))
        if o6 in purposes or o6 == co or s6 == pu:
            subgraph.remove((s6, None, None))
        if s6 == hRS or s6 == eq or o6 == hRS or o6 == eq:
            subgraph.remove((s6, None, o6))
         
    #Save the subgraph and convert to JSON for WebVOWL
    subgraph.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    
    if conversion:
        convert()
    else:
        return subgraph



def createAQMScopeComparision(source):
    """
        Visual comparison of a quality model with the full AQM shall be applied by creating an ontology file, that contains two disjunct graphs.
        First the quality model (source) needs to be extracted from the AQM and new URIs need to be assigned. Second, the full AQM can be added to the new graph.
    """

    #Create AQM subgraph for requested source
    subgraph = createAQMSubgraphForConsensus(source, conversion=False)
    
    
    #Remove isEquivalent properties
    for s, p, o in subgraph.triples((None, RDFS.label, rdflib.Literal("isEquivalent"))):
        subgraph.remove((s, p, o))
    
    #Remove all quality attributes from other quality models
    for s1, p1, o1 in subgraph.triples((None, ci, None)):
        
        if not o1 == rdflib.Literal(source, lang="en"):
            for s2, p2, o2 in subgraph.triples((None, None, s1)):
                subgraph.remove((s2, None, None))
                subgraph.remove((o2, None, None))
    
    #Define a temp namespace for the requested subgraph. 
    #Note: if the subgraph and the AQM are based on the same namespaces, the graphs will be merged.
    AQMnamespace = "http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#"
    TempNamespace = "http://www.semanticweb.org/beyersdo/ontologies/2023/03/TempSubgraph#"
    comparisonGraph = rdflib.Graph()
    
    #Iterate the full subgraph and replace every AQM namespace with the temp namespace
    for s3, p3, o3 in subgraph.triples((None, None, None)):
        if(AQMnamespace in str(s3)):
            sNew = rdflib.URIRef(s3.replace(AQMnamespace, TempNamespace))
        else:
            sNew = s3
        
        if(AQMnamespace in str(p3)):
            pNew = rdflib.URIRef(p3.replace(AQMnamespace, TempNamespace))
        else:
            pNew = p3
        
        if(AQMnamespace in str(o3)):
            oNew = rdflib.URIRef(o3.replace(AQMnamespace, TempNamespace))
        else:
            oNew = o3

        subgraph.remove((s3, p3, o3))
       
        comparisonGraph.add((sNew, pNew, oNew))
    
    #Combine the disjunct graphs (because of different namespaces) in one ontology file for viusal comparision
    comparisonGraph = comparisonGraph + getAQM(conversion=False)
    
    #Save the subgraph and convert to JSON for WebVOWL
    comparisonGraph.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    convert()



def createAQMSubgraphForMeasurement(source):
    """
        Add to a subgraph for a requested quality model (source) all purposes that enable measurement.
    """
    
    #Create AQM subgraph for requested source
    subgraph = createAQMSubgraphForConsensus(source, conversion=False)
    
    #Load current backup of the AQM and create empty subgraph
    aqm = rdflib.Graph(base="http://www.semanticweb.org/beyersdo/ontologies/2022/10/AQM#")
    aqm.parse(os.path.join(str(os.getcwd()) + "\\application\\static\\data\\AQM.owl"))
    
    #Iterate all quality attributes in subgraph
    for s, p, o in subgraph.triples((None, RDFS.subClassOf, qa)):
        
        #Iterate all object properties that have the quality attribute in its domain
        for s1, p1, o1 in aqm.triples((None, RDFS.domain, s)):
            
            #Iterate a object property and check the range
            for s2, p2, o2 in aqm.triples((s1, RDFS.range, None)):
                
                #Check if object property has range in measurement_purposes
                if o2 in measurement_purposes:
                    print(str(s2))
                    subgraph.add((s2, p2, o2))
                    subgraph.add((s1, p1, o1))
                    
                    #Add object property label
                    for s3, p3, o3 in aqm.triples((s2, RDFS.label, None)):
                        subgraph.add((s3, p3, o3))
                
    #Save the subgraph and convert to JSON for WebVOWL
    subgraph.serialize(destination=os.path.join(str(os.getcwd()) + "\\application\\static\\data\\YOUR_ONTOLOGY.TTL"), format="turtle")
    convert()
    
    
