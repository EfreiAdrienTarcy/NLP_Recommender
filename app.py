import pandas as pd
import flask
import dash
import dash_bootstrap_components as dbc
from dash import html, Input, Output, dcc, State
import webbrowser
import plotly.graph_objs as gobs
import webbrowser
from flask import url_for

# from components.infer import *
import gensim
import nltk
import ast
from typing import List
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

# nltk.download('averaged_perceptron_tagger')

external_stylesheets = [dbc.themes.UNITED]


external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)


# HEADER
# ======

header = dbc.NavbarSimple(
    children=[
    ],
    brand="Recipe-Chatbot",
    brand_href="#",
    color="primary",
    dark=True
)


# COMPONENTS
# ==========

# *Starting on load

link = None

modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Recipe Chatbot")),
                dbc.ModalBody(
                    "Hello there! Welcome to Recipe Chatbot. Are you tired of staring at a fridge full of ingredients, wondering what to cook for dinner? Look no further! Our chatbot is here to help.\
                "),
                dbc.ModalBody(
                    "Simply tell us what ingredients you have available, and we'll recommend a delicious recipe that you can make with what you have. Whether you're a seasoned chef or a beginner in the kitchen, Recipe Chatbot is here to make your life easier.\
                "),
                dbc.ModalBody(
                    "So why wait? Start chatting with Recipe Chatbot now and see what culinary creations you can whip up tonight!\
                "),
            ],
            id="modal",
            size="lg",
            centered=True,
            is_open=True,
        ),
    ]
)


# *Left Part

link_button = dbc.Button("Open Recipe in another window",
                         style={
                             "margin-bottom": "5%", "width": "38%", "position": "absolute", "bottom": 0},
                         id="launch-button",
                         )

# * Right Part
text_input = dbc.Col(dbc.Input(id='input-field', type='text',
                     placeholder='Enter your ingredients here', n_submit=0))

card = dbc.Card(
    [
        dbc.CardHeader("Conversation"),
        dbc.CardBody(id='card-body'),
        dbc.CardFooter(text_input),
    ],
    color="secondary", outline=True,
    style={"width": "auto", "height": 700},
)


# INTERACTION
# ===========

df = pd.read_csv('data/dataset_nlp.csv', converters={
                 'NER': ast.literal_eval, 'ingredients': ast.literal_eval, 'directions': ast.literal_eval})
model = Doc2Vec.load("models/d2v.model")


def inference(user_sentence: str) -> pd.DataFrame:
    # Simple preprocessing user sentence
    preprocessed_sentence = gensim.utils.simple_preprocess(
        user_sentence, deacc=True)

    # Lambda function to get only nouns
    def is_noun(pos): return pos[:2] == 'NN'

    # Applying Lambda function and removing duplicates
    nouns = [word for (word, pos) in nltk.pos_tag(
        preprocessed_sentence) if is_noun(pos)]
    nouns = set(nouns)

    # Infering
    v1 = model.infer_vector(list(nouns))
    similar_docs = model.dv.most_similar(positive=[v1])

    # Getting indexes of most similar lines
    indexes = [int(i[0]) for i in similar_docs]

    # returning recommendations
    new_df = df.iloc[indexes]
    new_df['missing_ingredients'] = new_df['NER'].apply(
        lambda lst: [ingredient for ingredient in lst if ingredient not in nouns])

    return new_df


# Get user input
@app.callback(Output('card-body', 'children'),
              [Input('input-field', 'n_submit')],
              [State('input-field', 'value')])
def update_card_body(n_submit, input_value):
    if n_submit > 0 and input_value is not None:
        global result
        result = inference(input_value)  # Get recommandation dataset
        titles = result['title'].tolist()  # Extract list of recipe title

        recipe_list = ["Here are my recommendation :"]
        for i in range(len(titles)):
            recipe_list.append(dbc.Row([dbc.Button(str(titles[i]),
                                                   color="light",
                                                   id="option-" +
                                                   str(i) + "-button",
                                                   style={"width": "100%"})
                                        ],
                                       style={
                                           'margin-left': '10%', 'margin-right': '10%', 'margin-top': '2%'}
                                       )
                               )
        recipe_result = html.Div(recipe_list)
        return html.Div(recipe_result)
    else:
        return html.H4('Recipe Chatbot')


options = [{'id': 'option-0-button'},
           {'id': 'option-1-button'},
           {'id': 'option-2-button'},
           {'id': 'option-3-button'},
           {'id': 'option-4-button'},
           {'id': 'option-5-button'},
           {'id': 'option-6-button'},
           {'id': 'option-7-button'},
           {'id': 'option-8-button'},
           {'id': 'option-9-button'},
           ]


@app.callback(
    Output("div-ingredients", "children"),
    [Input(opt['id'], "n_clicks") for opt in options])
def update_output(*args):
    button_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    global button_number
    button_number = int(button_id[7])

    recipe_directions = []

    global title
    title = result.iloc[button_number]['title']
    recipe_directions.append(html.H4(str(title)))

    global link
    link = result.iloc[button_number]['link']

    global ingredients
    ingredients = result.iloc[button_number]['ingredients']
    for ingr in ingredients:
        recipe_directions.append(dbc.Row([
            html.P("□   " + str(ingr),
                   )
        ],
            style={
            'margin-left': '10%', 'margin-right': '5%'}
        )
        )

    recipe_directions.append(html.Br())

    step = 0

    global directions
    directions = result.iloc[button_number]['directions']
    for ingr in directions:
        step += 1

        recipe_directions.append(dbc.Row([
            html.H5("Step " + str(step))
        ],
            style={
            'margin-left': '10%', 'margin-right': '10%'}
        )
        )

        recipe_directions.append(dbc.Row([
            html.P(str(ingr),)
        ],
            style={
            'margin-right': '10%'}
        )
        )

    return recipe_directions


@app.callback(
    Output("launch-button", "href"),
    Input("launch-button", "n_clicks"))
def open_link(n_clicks):
    if n_clicks and link is not None:
        return link
    else:
        return ""


# APP LAYOUT
# ==========
app.layout = html.Div([
    header,
    modal,
    html.Div([
        dbc.Row([
            dbc.Col([

                html.Div(id='div-ingredients', style={'overflow': 'auto',
                                                      "height": "90%",
                                                      "max-height": 700}),
                link_button
            ],
                style={'overflow': 'hidden'}),
            dbc.Col(html.Div(card)),
        ],
        ), ], style={'margin-left': '10%', 'margin-right': '10%', 'margin-top': '5%', 'margin-bottom': '2%', 'overflow': 'hidden'}
    ),
],
    style={'overflow': 'hidden'}
)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8080)
