# DISARM Explorer code
Code for an online viewer of the DISARM frameworks and datasets.

Written in Python, Flask, D3.

# How to make this run

## Running locally

Getting set up to run the code:

* **Install postgresql locally** You can get postgresql from https://www.postgresql.org/
* **Create a DISARM database**.  Use postgresql to create a database called "disarmsite".
* **Populate the DISARM database**.  The Jupyter file [generate_disarm_pages.ipynb](https://github.com/DISARMFoundation/DISARMframeworks/blob/main/CODE/generate_DISARM_pages.ipynb) in the [DISARM Frameworks repository](https://github.com/DISARMFoundation/DISARMframeworks) will do this for you - you'll need to install [Anaconda](https://www.anaconda.com/) or another Jupyter package first.  NB if you don't want to run Jupyter, you can run the python file generate_disarm_sql.py to do the same thing.  
* **Get a local copy of this repository**. Open a terminal window.  git clone this repository. cd into it
* **Create a virtual environment**. From the top folder of this repo, type "virtualenv venv" in the terminal window.  See [this](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/) for more details.

Updating the code:
* Edit the code. The html updates will show immediately.  You might have to clear your browser caches to show any javascript changes though.

Running the code:

* . venv/bin/activate;
* export FLASK_APP=disarmsite; export FLASK_ENV=development; export DATABASE_URL2="postgresql:///disarmsite"
* flask run

These instructions: start your virtual environment, points the app at the database you just created, and start the app.  You can now go to http://127.0.0.1:5000/ in your browser, and interact with it.


## Running on Heroku

Getting set up to run on Heroku:

* **Create a Heroku account**. Go to [https://www.heroku.com/](https://www.heroku.com/)
* **Create a Heroku app**.  Click "new" in [https://dashboard.heroku.com/apps](https://dashboard.heroku.com/apps)
* **Add postgres to your Heroku app**. Click on the app, then the resources tab. Add the Postgres add-on.  
* **Update your Heroku app settings**
* go to https://dashboard.heroku.com/apps/<your heroku app name>/settings
* click "reveal config vars"
* Edit DATABASE_URL: take a copy of it. It will start with "postgres://"
* Create DATABASE_URL2: copy DATABASE_URL into it, but start it with start with "postgresql://" instead
* **Go back to your terminal window and connect the Heroku app**
* heroku git:remote -a your-app-name (see https://devcenter.heroku.com/articles/git)

Updating Heroku code and database:

* pg_dump -Fc -h localhost -U \<yourdatabaseusername\> disarmsite > disarmsite.dump  
* heroku pg:reset -a \<your heroku app name\>   
* heroku pg:push disarmsite DATABASE_URL -a \<your heroku app name\>
* git add .; git commit -m "heroku stuff"; git push heroku main

These instructions: take a copy of your local postgresql database and put it into file disarmsite.dump.  Hard-resets the Heroku app.  Pushes the data from disarmsite.dump to the Heroku app. Pushes the code from the current repository into the Heroku app.  It's brutal, but whilst the database and app are changing a lot, it's what we do.

Running on Heroku:

* Go to the webpage associated with your Heroku app. It's going to look something like https://disarmframework.herokuapp.com/

# Code notes

Database notes:

* Database objects are generated by file generate_disarm_sql.py in the DISARM Frameworks repository
* The MISP galaxy for DISARM is at [https://github.com/MISP/misp-galaxy/blob/main/clusters/misinfosec-amitt-misinformation-pattern.json](https://github.com/MISP/misp-galaxy/blob/main/clusters/misinfosec-amitt-misinformation-pattern.json). This will also need updating.

Planned capabilities:

* Continue normalising the DISARM database tables.
* Create disinformation-specific MISP objects in https://github.com/MISP/misp-objects/tree/main/objects
