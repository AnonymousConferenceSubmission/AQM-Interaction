from flask import Flask, render_template, request, make_response
from application.AccessAQM import getAQM, createAQMSubgraphForConsensus, createAQMSubgraphForMeasurement
import os
import shutil
import time

app = Flask(__name__, template_folder="./application/templates", static_folder="./application/static")

@app.after_request
def add_header(r):
    """
    Prevent caching of documents. 
    Especially the ontologies should always be loaded in the latest version.
    """
    
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    
    return r

@app.route("/")
def start_page():
    return render_template('index.html')

@app.route("/consensus")
def consensus_page():
    
    sources = ["[Bel12]", "[DOJ+93]", "[ECSS-Q-HB-80-04C]", "[ISO/IEC/IEEE29148:2018]", "[MVSG18]", "[STH+13]", "[TA15]", "[Hal93]", "[BBG+06]", "[HZ18]", "[GLSB20]"]
    
    return render_template('consensus.html', sources=sources)

@app.route("/scope")
def scope_page():

    sources = ["[Bel12]", "[DOJ+93]", "[ECSS-Q-HB-80-04C]", "[ISO/IEC/IEEE29148:2018]", "[MVSG18]", "[STH+13]", "[TA15]", "[Hal93]", "[BBG+06]", "[HZ18]", "[GLSB20]"]
    
    return render_template('scope.html', sources=sources)

@app.route("/measurement")
def measurement_page():

    sources = ["[Bel12]", "[DOJ+93]", "[ECSS-Q-HB-80-04C]", "[ISO/IEC/IEEE29148:2018]", "[MVSG18]", "[STH+13]", "[TA15]", "[Hal93]", "[BBG+06]", "[HZ18]", "[GLSB20]"]
    
    return render_template('measurement.html', sources=sources)

@app.route("/explore")
def explore_page():
    
    getAQM()
    
    # Move generated JSON file containing the subgraph to the data directory 
    source = './YOUR_ONTOLOGY.json' 
    destination = './application/static/data/YOUR_ONTOLOGY.json'
    
    while(not os.path.exists(source)):
        # Wait until the JSON file was created by the called functions
        time.sleep(1) # = 1sec
    
    dest = shutil.move(source, destination)
   
    return render_template('webvowl.html')

@app.route("/getAQMSubgraphForConsensus", methods=['POST'])
def consensus_req():
    """
        A request for a consensus analysis is received from the consensus page.
        (1) Extract the quality model soruce requested for
        (2) Create a AQM subgraph with the quality model and equivalent attributes from other models in the AQM
        (3) Render the WebVOWL page and load the created subgraph
    """
    
    # Source extraction from POST request (note: Sources are in the AlphaBixTex short reference format)
    msgdata = request.form.to_dict().keys()
    createAQMSubgraphForConsensus(list(msgdata)[0])
    
    # Move generated JSON file containing the subgraph to the data directory 
    source = './YOUR_ONTOLOGY.json' 
    destination = './application/static/data/YOUR_ONTOLOGY.json'
    
    while(not os.path.exists(source)):
        # Wait until the JSON file was created by the called functions
        time.sleep(1) # = 1sec
    
    dest = shutil.move(source, destination)
   
    return render_template('webvowl.html')

@app.route("/getScopeComparision", methods=['POST'])
def scope_req():
    """
        A request for a consensus analysis is received from the consensus page.
        (1) Extract the quality model soruce requested for
        (2) Create a AQM subgraph with the quality model and equivalent attributes from other models in the AQM
        (3) Render the WebVOWL page and load the created subgraph
    """
    
    ###### TODO ######
    
    # Source extraction from POST request (note: Sources are in the AlphaBixTex short reference format)
    msgdata = request.form.to_dict().keys()
    createAQMSubgraphForConsensus(list(msgdata)[0])
    
    # Move generated JSON file containing the subgraph to the data directory 
    source = './YOUR_ONTOLOGY.json' 
    destination = './application/static/data/YOUR_ONTOLOGY.json'
    
    while(not os.path.exists(source)):
        # Wait until the JSON file was created by the called functions
        time.sleep(1) # = 1sec
    
    dest = shutil.move(source, destination)
   
    return render_template('webvowl.html')

@app.route("/getAQMSubgraphForMeasurement", methods=['POST'])
def measurement_req():
    """
        A request for a consensus analysis is received from the consensus page.
        (1) Extract the quality model soruce requested for
        (2) Create a AQM subgraph with the quality model and equivalent attributes from other models in the AQM
        (3) Render the WebVOWL page and load the created subgraph
    """
    
    ###### TODO ######
    
    # Source extraction from POST request (note: Sources are in the AlphaBixTex short reference format)
    msgdata = request.form.to_dict().keys()
    createAQMSubgraphForMeasurement(list(msgdata)[0])
    
    # Move generated JSON file containing the subgraph to the data directory 
    source = './YOUR_ONTOLOGY.json' 
    destination = './application/static/data/YOUR_ONTOLOGY.json'
    
    while(not os.path.exists(source)):
        # Wait until the JSON file was created by the called functions
        time.sleep(1) # = 1sec
    
    dest = shutil.move(source, destination)
   
    return render_template('webvowl.html')

@app.route('/static/data/<var1>')
def static_file(var1):
    """
    
        By defining a own route for all data requests, the headers of the responses
        get the cache policy defined in .after_request
    """
    
    return app.send_static_file('./data/YOUR_ONTOLOGY.json')


if __name__== "__main__":
    app.run(debug=True)