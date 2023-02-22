# Recipe-Chatbot
#### Team 4
#### Members : W.PONNOU, A.LEBLANC, A.TARCY, M.GONCALVES, Y. TOUHAMI-KADIRI

[! https://img.shields.io/github/license/mathys.goncalves@efrei.net/Recipe-Chatbot] [! https://img.shields.io/badge/Made%20at-Starschema-red]
A short description of the project.


## Running locally

To run a development instance locally, create a virtualenv, install the 
requirements from `requirements.txt` and launch `app.py` using the 
Python executable from the virtualenv.

## Deploying on ECS

Use `make image` to create a Docker image. Then, follow [these 
instructions](https://www.chrisvoncsefalvay.com/2019/08/28/deploying-dash-on-amazon-ecs/) 
to deploy the image on ECS.

## Possible improvments for the future

- Allow mandatory ingredients or the removal of ingredients among the recommendations of recipes
- Implement a cache system for the web interface to avoid reloading elements when it is unecessary
- Create several recipes from a single long list of ingredients
