# AQM-Interaction
This repository contains (1) the [replication package](replication_package) of the paper _Alignment of Quality Models for Assessing Software Requirements in Large-scale Projects: A Case from Space_ (currently under review), and (2) the code for the implemented lightweighted tool to interact with the Aligned Quality-Model Map (AQM) during the applied case study. Both contributions are desired for usage in further projects to achieve reliable quality assessment during large-scale software development projects.

## Installation
Clone this repository on your machine:

```cmd
git clone https://github.com/AnonymousREConfSubmission/AQM-Interaction.git
```

Create a virtual Python environment for this project, e.g.

```cmd
python -m venv env
```

Activate the create environment, e.g. (Windows command)
```cmd
.\env\Scripts\activate
```

Install the needed libaries (e.g. flask and rdflib) using pip, e.g.
```cmd
pip install -r dependencies.txt
```

## Important Notes
This work is based on the flask extension for direcly using WebVOWL from: https://github.com/ahmedkhemiri95/flask-WebVOWL. Therefore, Python (here in version 3.11.2) and Java (here in version 1.8.0) are prerequisites.
The individually created AQM needs to be located in the [data](application/static/data) directory and must follow the conceptualization procedure described in the related paper. For demonstration purposes, the AQM from the case study of the paper was included in this repository.

## Run the application
Start the flask server
```cmd
python main.py
```
Open your browser at http://localhost:5000
