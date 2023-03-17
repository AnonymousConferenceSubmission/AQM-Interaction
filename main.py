from flask import Flask, render_template, request, make_response
from application.AccessAQM import getAQM, createAQMSubgraphForConsensus, createAQMScopeComparision, createAQMSubgraphForMeasurement
import os
import shutil
import time

sourceInformation = [["People, Organizational and Technological Dimensions of Software Requirements Specification", "F. Belfo", "2012", "https://doi.org/10.1016/j.protcy.2012.09.034", "[Bel12]"], 
["Identifying and measuring quality in a software requirements specification", "A. Davis et al.", "1993", "https://doi.org/10.1109/METRIC.1993.263792", "[DOJ+93]"],
["ECSS-Q-HB-80-04A Space product assurance - Software metrication programme definition and implementation", "European Cooperation for Space Standardization (ECSS)", "2011", "https://ecss.nl/hbstms/ecss-q-hb-80-04a-software-metrication-handbook/", "[ECSS-Q-HB-80-04C]"],
["ISO 29148 Systems and software engineering – Life cycle processes – Requirements engineering", "International Standard ISO/IEC/IEEE", "2018", "https://doi.org/10.1109/IEEESTD.2018.8559686", "[ISO/IEC/IEEE29148:2018]"],
["Quality of software requirements specification in agile projects: A cross-case analysis of six companies", "J. Medeiros, A. Vasconcelos, C. Silva, and M. Goulão", "2018", "https://doi.org/10.1016/j.jss.2018.04.064", "[MVSG18]"],
["Requirements clinic: Third party inspection methodology and practice for improving the quality of software requirements specifications", "S. Saito, M. Takeuchi, M. Hiraoka, T. Kitani, and M. Aoyama", "2013", "htpps://doi.org/10.1109/RE.2013.6636732", "[STH+13]"],
["Assessing the Quality of Software Requirements Specifications for Automotive Software Systems", "A. Takoshima and M. Aoyama", "2015", "https://doi.org/10.1109/APSEC.2015.57", "[TA15]"],
["Requirements metrics: the basis of informed requirements engineering management", "R. J. Halligan", "1993", "-", "[Hal93]"],
["A new quality model for natural language requirements specifications", "D. M. Berry, A. Bucchiarone, S. Gnesi, G. Lami, and G. Trentanni", "2006", "-", "[BBG+06]"],
["A systematic literature review on quality criteria for agile requirements specifications", "P. Heck and A. Zaidman", "2018", "https://doi.org/10.1007/s11219-016-9336-4", "[HZ18]"],
["Handbook for the CPRE Foundation Level according to the IREB Standard", "M. Glinz, H. van Loenhoud, S. Staal, and S. Bühne", "2020", "-", "[GLSB20]"]]


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
    
    return render_template('consensus.html', sourceInformation=sourceInformation)

@app.route("/scope")
def scope_page():

    sources = ["[Bel12]", "[DOJ+93]", "[ECSS-Q-HB-80-04C]", "[ISO/IEC/IEEE29148:2018]", "[MVSG18]", "[STH+13]", "[TA15]", "[Hal93]", "[BBG+06]", "[HZ18]", "[GLSB20]"]
    
    return render_template('scope.html', sourceInformation=sourceInformation)

@app.route("/measurement")
def measurement_page():

    sources = ["[Bel12]", "[DOJ+93]", "[ECSS-Q-HB-80-04C]", "[ISO/IEC/IEEE29148:2018]", "[MVSG18]", "[STH+13]", "[TA15]", "[Hal93]", "[BBG+06]", "[HZ18]", "[GLSB20]"]
    
    return render_template('measurement.html', sourceInformation=sourceInformation)

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
    createAQMScopeComparision(list(msgdata)[0])
    
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