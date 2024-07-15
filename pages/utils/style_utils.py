"""Styles for miscellaneous elements."""

from dash import html

heading_style = {
    "font-size": "30px", "font-weight": "bold", "font-family": "Roboto"}

accordionitem_style = {"border": "2px solid #abc", "border-radius": "5px"}

accordion_style = {"width": "100%", "margin": "5px auto"}

radioitems_style = {"max-height": "200px", "overflow-y": "auto"}

popover_style = {
    "max-width": "440px", "border-radius": "10px",
    "font-size": "16px", "font-family": "Roboto"}


def style_accordionitem_title(title: str, font_size: int = 24):
    """Style accordionitem title."""
    style_accordionitem_title_params = {
        "font-size": f"{font_size}px", "font-weight": "bold",
        "font-family": "Roboto", "text-align": "center",
        "width": "100%", "margin": "0px auto", "padding": "0px"}
    return html.H1(title, style=style_accordionitem_title_params)
