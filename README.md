# flask-project
Building apis using flask Web framework

# create a virtual environment for windows
python -m venv .venv
source .venv/Scripts/activate


## install the required packages
pip install -r requirements.txt

## run the flask server and test it away
python app_ex4.py &

## use http or curl or postman to test the apis
http GET localhost:5000/recipes

> This was inspired by Python API Development Fundamentals by Jack Huang and Ray Chung
