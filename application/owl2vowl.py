import subprocess 
import os 
import shutil

def convert():

    # Run owl2vowl.jar converter : convert ontology file TTL to JSON format supported by WebVOWL
    proc = subprocess.Popen("java -jar ./application/static/owl2vowl.jar -file ./application/static/data/YOUR_ONTOLOGY.TTL", shell=True, stdout=subprocess.PIPE) 
    
    
