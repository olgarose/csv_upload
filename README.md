# CSV Upload
Flask web application that uploads csv into mysql database.
Validates csv file has columns 'parent', 'child', and 'quanity' to represent edges on a graph.

## Getting started
For security, the config module was removed. 

To run the application create a config directory with an ```__init__.py``` file.

In the ```__init__.py``` save the variable 
DATABASE_URI = 'mysql://<user_name>:<password>@<end_point>/<database_name>'

Replace the variable with your database info.

## Running application
Clone or download repo and go to source directory.

Install virtualenv for Python 2.7:
```
pip install virtualenv
```

Create your virtual environment:
```
virtualenv venv
```

Activate your virtual environment:
```
source venv/bin/activate
```

Install requirements:
```
pip install -r requirements.txt
```

Run application:
``` 
python application.py
```

Head to http://127.0.0.1:5000/

## Built With

* [Flask](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
