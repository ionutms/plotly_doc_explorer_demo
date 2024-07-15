"""Home"""
import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pages.utils.style_utils as styles

link_name = __name__.rsplit('.', maxsplit=1)[-1].replace('_page', '').title()

dash.register_page(__name__, name=link_name, path='/')

layout = dbc.Container([
    html.Div([
        html.H1(
            f"This is the '{__name__.rsplit('.', 1)[-1]}' page",
            style=styles.heading_style),
        html.Div(id='links_display'),
    ])
], fluid=True)


@callback(
    Output('links_display', 'children'),
    Input('links_store', 'data')
)
def display_links(links):
    """Display links."""
    if not links:
        return "Loading links..."

    return html.Div([
        html.Div(dcc.Link(link['name'], href=link['path']))
        for link in links][:-1])
