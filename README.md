# DISARM Flask webaite
Code for an online viewer of the DISARM frameworks and datasets. 

Written in Python, Flask, D3. 

## How to make this run

Running locally - getting set up

* install postgresql locally https://www.postgresql.org/
* Use the DISARM repo to generate a database for you https://github.com/DISARMFoundation/DISARM file CODE/generate_DISARM_sql.ipynb will do this for you (run it using jupyter - install that using anaconda https://www.anaconda.com/). NB You might need to go to the terminal window and type "created disarmsite" first. 
* Open a terminal window.  git clone this repo. cd into it   

Running locally

* . venv/bin/activate; 
* export FLASK_APP=disarmsite; export FLASK_ENV=development; export DATABASE_URL2="postgresql:///disarmsite"
* flask run
* go to http://127.0.0.1:5000/


Running on Heroku - getting set up

* Create a heroku account. Create an app. 
* Click on the app, then the resources tab. Add the Postgres add-on.  
* go to https://dashboard.heroku.com/apps/<your heroku app name>/settings
* click "reveal config vars"
* Edit DATABASE_URL: take a copy of it. It will start with "postgres://"
* Create DATABASE_URL2: copy DATABASE_URL into it, but start it with start with "postgresql://" instead

Running on Heroku - updating Heroku code and database

* pg_dump -Fc -h localhost -U <yourdatabaseusername> disarmsite > disarmsite.dump  
* heroku pg:reset -a <your heroku app name>   
* heroku pg:push disarmsite DATABASE_URL -a <your heroku app name> 
* git add .; git commit -m "heroku stuff"; git push heroku main


## Database notes

* Database objects are generated by the DISARM repo, Jupyter notebook file [generate_DISARM_sql.ipynb](https://github.com/DISARMFoundation/DISARM/blob/main/CODE/generate_DISARM_sql.ipynb).  Still normalising the DISARM repo tables - adding tables as they're needed. Also, the MISP galaxy for this is at [https://github.com/MISP/misp-galaxy/blob/main/clusters/misinfosec-amitt-misinformation-pattern.json](https://github.com/MISP/misp-galaxy/blob/main/clusters/misinfosec-amitt-misinformation-pattern.json) and will need updating also. 
* Next: adding in ability to create the new disinformation-specific MISP objects in https://github.com/MISP/misp-objects/tree/main/objects
