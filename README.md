# coingeckoapiwrapper
A python wrapper for the coingecko API written with [Django Rest Framework](https://www.django-rest-framework.org/)

## Setup Not Working for you ?
Please visit [here](https://radiant-island-10503.herokuapp.com) to view a deployed heroku app of this project.

## Setup
Clone repo and install dependencies from requirements.txt file. You also can use a virtual environment which is recommended but optional:
```bash
git clone git@github.com:drinkingjava/coingeckoapiwrapper.git && cd coingeckoapiwrapper
python3 -m virtual -p python3.8 .env
source .env/bin/activate
pip install -r requirements.txt
```

The command should navigate in to the root of the cloned folder and create a virtual environment there as well. Next run migrations:
```bash
./manage.py migrate
```
No models have been defined for this exercise so no need to run `./manage.py makemigrations`

After that you can run the Django dev server and browse the api at localhost:8000/api or 127.0.0.1:8000
```bash
./manage.py runserver
```
## Scaling the /marketCap endpoint.
The Coingecko /coins/{id}/history endpoint my support extra or deprecate some query parameters.
Although it is bad practice to change endpoints without upgrading the version number i.e v3 -> v4, since
this is a 3rd party API, you have no control over their practices. Nevertheless, if in luck the endpoint
may stay unchanged after an API upgrade.

Iterating through the list of parameters without hardcoding anything will avoid the 
need to update the endpoint every single time, given that the structure of the endpoint 
does not change i.e when the API is upgraded to v4.

## Improvements that can be made with more time
1. Inside API overview, it may be easier for the user to be able to click on generated urls instead of typing them out manually
2. Invest some time to look at unit testing and adding code coverage
3. Better HTTP error handling. There could be edge cases where the reported errors may not be a 404 for example
4. There are also edge cases where the user can query a coin date where the requested coin does exist at that time.