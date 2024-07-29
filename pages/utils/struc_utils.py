"""
Structural Utilities for Dash Components

This module provides utility functions for creating and managing various
Dash Bootstrap Components (dbc) and Dash Core Components (dcc).

Functions:
    app_description: Create app description component.

These utilities simplify the creation of common UI elements in Dash
applications, providing consistent styling and behavior.
"""

from typing import List

from dash import html
import dash_bootstrap_components as dbc


def app_description() -> html.Div:
    """
    Create a description component for the Graph Objects Explorer app.

    This function generates a Dash component that provides an overview of
    the app, its key features, and instructions on how to use it. The
    description is formatted using Dash Bootstrap Components with the
    'Key Features' and 'How to Use' sections displayed side by side on
    larger screens.

    Returns:
        html.Div: A Div component containing the formatted app description.
    """
    unordered_list_content: List[str] = [
        "Dynamic treemap visualization of Plotly graph objects",
        "Interactive filtering of treemap levels using range sliders",
        "Option to sort treemap items",
        "Clickable treemap nodes with corresponding documentation display",
        "Theme switching between light and dark modes"
    ]

    ordered_list_content: List[str] = [
        "Select a graph object from the radio bottom list.",
        "Use the range sliders to filter items at each levels of the treemap.",
        "Toggle the switch to change the ordering of items in the treemap.",
        "Click on treemap nodes to view the corresponding documentation.",
        "Use the theme switch to toggle between light and dark modes."
    ]

    left_column_content: dbc.Col = dbc.Col([
        html.H4("Key Features:"),
        html.Ul([html.Li(content) for content in unordered_list_content])
    ], xs=12, md=6)

    right_column_content: dbc.Col = dbc.Col([
        html.H4("How to Use:"),
        html.Ol([html.Li(content) for content in ordered_list_content])
    ], xs=12, md=6)

    description: html.Div = html.Div([
        html.Hr(),
        html.H3("About the Graph Objects Explorer"),
        html.Div(
            "The Graph Objects Explorer is an interactive tool for visualizing"
            " and exploring the structure of Plotly graph objects."),
        html.Div(
            "It provides a dynamic treemap representation of graph object "
            "properties and allows users to filter and navigate through "
            "different levels of detail."),
        html.Hr(),
        dbc.Row([left_column_content, right_column_content])
    ])

    return description
