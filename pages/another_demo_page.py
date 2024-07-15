"""Data Generator"""
import dash_bootstrap_components as dbc
from dash import html, dcc, register_page
import pages.utils.style_utils as styles

link_name = __name__.rsplit('.', maxsplit=1)[-1].replace('_page', '').title()

register_page(__name__, name=link_name, order=1)

layout = dbc.Container([
    html.Div([
        dcc.Link('Go back Home', href='/'),
        html.H1(f"This is the '{link_name}' page", style=styles.heading_style),
    ])
], fluid=True)
