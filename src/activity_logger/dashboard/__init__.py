"""Instantiate a Dash app."""
import dash
from dash import dcc, html
from flask import Flask

# from .layout import html_layout


def init_dashboard(app: Flask):
    """
    Create a Plotly Dash dashboard within a running Flask app.

    :param Flask app: Top-level Flask application.
    """
    dash_module = dash.Dash(
        server=app,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/master.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Custom HTML layout
    # dash_module.index_string = html_layout

    # Create Layout
    dash_module.layout = html.H1("Hello world!")

    return dash_module.server
