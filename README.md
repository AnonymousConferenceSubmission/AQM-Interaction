# AQM-Interaction
Introduce the AQM

**Note:** This work is based on the flask extension for direcly using WebVOWL from: https://github.com/ahmedkhemiri95/flask-WebVOWL. Therefore, Python (here in version 3.11.2) and Java (here in version 1.8.0) are prerequisites.

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
The individually created AQM needs to be located in the [data](application/static/data) and must follow the conceptualization procedure from the paper. For demonstration purposes, the AQM from the case study of the paper was included in this repository.

In some browsers, the loaded subgraphs can be cached and different visualizations will not be shown. As a solution, disable caching for the "WebVOWL for AQM" page.

## Run the application
Start the flask server
```cmd
python main.py
```
Open your browser at http://localhost:5000
