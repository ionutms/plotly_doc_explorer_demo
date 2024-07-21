"""Graph Objects Explorer"""
from typing import Any, Dict, List, Tuple
from dash import register_page
from dash import html, dcc, callback, MATCH
from dash import Output, Input, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pages.utils.fig_utils as fig_u
import pages.utils.web_utils as web_u
import pages.utils.style_utils as styles

link_name = __name__.rsplit('.', maxsplit=1)[-1].replace('_page', '').title()

register_page(__name__, name=link_name, order=0)


# ================= GRAPH OBJECTS EXPLORER PAGE ==== LAYOUT SECTION START ====

MAIN_DIV_CHILDREN = [
    dbc.Row([dbc.Col([dcc.Link('Go back Home', href='/'),])]),
    dbc.Row([dbc.Col([
        html.H1(f"This is the '{link_name}' page", style=styles.heading_style)
    ])]),
    html.Hr(),
    dbc.Row([dbc.Col([dbc.RadioItems(
        options=[
            {"label": key, "value": key}
            for _, key in enumerate(fig_u.GO_INFO)],
        id='checklist', inline=True, switch=False,
        style=styles.radioitems_style
    ),
    ])]),
    dcc.Store(id='store', data={'count': 0}),
    html.Hr(),
    html.Div(id='container'),
]

layout = dbc.Container([html.Div(MAIN_DIV_CHILDREN)], fluid=True)


def create_labeled_range_slider_column(
        slider_id: dict, label_text: str, min_val: int = 0,
        pushable_val: int = 0) -> dbc.Col:
    """
    Create a labeled range slider within a responsive Bootstrap column.

    This function generates a Dash Bootstrap column containing a labeled
    range slider. The slider is configured with specific properties and a
    tooltip.

    Args:
        slider_id (dict): A dictionary used as the ID for the range slider.
        label_text (str): The text to be displayed as the slider's label.
        min_val (int, optional):
            The minimum value for the slider. Defaults to 0.
        pushable_val (int, optional):
            The pushable value for the slider. Defaults to 0.

    Returns:
        dbc.Col: A Dash Bootstrap column containing a labeled range slider.
    """
    labeled_range_slider_column = dbc.Col([
        dbc.Label(
            label_text,
            className="d-flex justify-content-center align-items-center"),
        dcc.RangeSlider(
            id=slider_id, value=[min_val, 500], min=min_val, step=1,
            allowCross=False, pushable=pushable_val, marks=None, tooltip={
                "placement": "bottomLeft", "always_visible": True,
                "style": {"fontSize": "14px"}}),
    ], xs=12, md={"size": 4})
    return labeled_range_slider_column


def create_three_level_filter_row(instance_id: int = 0) -> dbc.Row:
    """
    Create a row with three-level filter controls for property documentation.

    This function generates a set of three range sliders for filtering
    items at different levels of detail.
    The sliders are arranged vertically in a column.

    Args:
        instance_id (int, optional): Unique identifier used to create distinct
            component IDs for each instance of these controls. Defaults to 0.

    Returns:
        dbc.Row:
            A Dash Bootstrap row containing the three-level filter controls.
            The row includes:
            - A column with three labeled range sliders for Level 1, 2, and 3
              items.
            - A horizontal line separator below the sliders.
    """
    level_sliders_column = dbc.Col([dbc.Row([
        create_labeled_range_slider_column(
            {'type': 'slider_1', 'index': instance_id}, 'Level 1 items', 1, 1),
        create_labeled_range_slider_column(
            {'type': 'slider_2', 'index': instance_id}, 'Level 2 items'),
        create_labeled_range_slider_column(
            {'type': 'slider_3', 'index': instance_id}, 'Level 3 items'),
    ])
    ], xs=12, md={"size": 12})

    three_level_filter_row = dbc.Row([dbc.Col([
        dbc.Row([level_sliders_column]), html.Hr()])])

    return three_level_filter_row


def create_color_theme_controls_row(instance_id: int = 0) -> dbc.Row:
    """
    Create a row with color theme controls for property documentation.

    This function generates a Dash Bootstrap row component that includes:
    - Two switches:
      1. Sort switch: Toggles sorting of graph items (e.g., by value or name)
      2. Color reverse switch: Flips the direction of the selected color scale
    - Radio buttons to select from predefined color scales

    Args:
        instance_id (int, optional): Unique identifier used to create distinct
            component IDs for each instance of these controls. Defaults to 0.

    Returns:
        dbc.Row: A Dash Bootstrap row containing the color theme controls.
            The row includes:
            - A column with two switches for sorting and color reversal
            - A column with radio buttons for color scale selection
    """
    switches_column = dbc.Col([html.Div([
        dbc.Label("Sort graph items", className="mb-2 text-center"),
        html.Div([dbc.Switch(
            {'type': 'sort_switch', 'index': instance_id}, value=True)
        ], className="d-flex justify-content-center"),
        html.Br(),
        dbc.Label("Reverse colors", className="mb-2 text-center"),
        html.Div([dbc.Switch(
            {'type': 'reverse_colors_switch', 'index': instance_id},
            value=False)
        ], className="d-flex justify-content-center")
    ], className=styles.CENTER_DIV_CONTENT)
    ], xs=4, md=2)

    radioitems_column = dbc.Col([
        html.Div([
            dbc.Label("Colorscales", className="mb-2 text-center")
        ], className="d-flex justify-content-center"),
        dbc.RadioItems([
            {"label": colorscale, "value": colorscale}
            for colorscale in fig_u.MARKER_COLORSCALE
        ], value="sunsetdark",
            id={'type': 'checklist_colorscale', 'index': instance_id},
            inline=True, switch=False, style=styles.radioitems_style)
    ], xs=8, md=10)

    color_theme_controls_row = dbc.Row([switches_column, radioitems_column])
    return color_theme_controls_row


def create_main_controls_accordion(index_id: int = 0):
    """
    Create the main controls accordion with associated stores.

    This function generates a Dash Bootstrap row containing:
    - Two dcc.Store components for storing state
    - An accordion with two main sections:
        1. Filter controls
            (created by create_filter_controls_accordion())
        2. Color theme controls
            (created by create_color_theme_controls_accordion())

    The accordion is initially collapsed and hidden.

    Args:
        index_id (int, optional): Index used for component IDs. Defaults to 0.

    Returns:
        dbc.Row:
            A Dash Bootstrap row containing the main controls accordion
            and associated store components.
    """
    main_controls_accordion = dbc.Row([dbc.Col([
        dcc.Store(
            id={'type': 'store_len_lev_1', 'index': index_id}, data=None),
        dcc.Store(
            id={'type': 'store_split', 'index': index_id}, data=None),
        dbc.Accordion([dbc.AccordionItem([
            create_three_level_filter_row(),
            create_color_theme_controls_row()],
            style={'display': 'none'},
            id={'type': 'accordion_item', 'index': index_id},
        )], start_collapsed=True, flush=False, style=styles.accordion_style),
    ])])
    return main_controls_accordion


def create_graph_and_iframe_section(index_id: int = 0):
    """
    Creates a DBC row containing a graph and an iframe section.

    Parameters:
    index_id (int): The index identifier for the components. Default is 0.

    Returns:
    dbc.Row: A row containing a graph and an iframe section.
    """
    graph_section_column = dbc.Col([dcc.Loading([dcc.Graph(
        id={'type': 'treemap', 'index': index_id}, config=fig_u.GRAPH_CONFIG,
        style={'display': 'none'})])], xs=12, md={"size": 12},
        className="text-center my-auto",
        id={'type': 'col_graph', 'index': index_id})

    iframe_section_column = dbc.Col([
        dbc.Row([dbc.Col([html.A(
            id={'type': 'click_data', 'index': index_id})])]),
        html.Iframe(
            id={'type': 'iframe', 'index': index_id},
            style={"width": "100%", "height": "480px"})],
        xs=12, md={"size": 6}, style={'display': 'none'},
        id={'type': 'col_iframe', 'index': index_id},
        className="text-center my-auto")

    graph_and_iframe_section = dbc.Row([
        graph_section_column, iframe_section_column
    ], justify="center", className="h-100")

    return graph_and_iframe_section

# =================== GRAPH OBJECTS EXPLORER PAGE ==== LAYOUT SECTION END ====


@callback(
    Output('store', 'data'),
    Input('checklist', 'value'),
    State('store', 'data')
)
def reset_store_count_on_checklist_change(
        checklist: List[str], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reset the count in the data store when the checklist value changes.

    This callback function is triggered whenever the value of the
    'checklist' component changes. It updates the 'count' key in the data
    store to 1 if a checklist item is selected.

    Args:
        checklist (List[str]):
            The currently selected values from the checklist.
            Empty list if no selection.
        data (Dict[str, Any]):
            The current data stored in the 'store' component.

    Returns:
        Dict[str, Any]:
            Updated data dictionary.
            If a checklist item is selected, the 'count' key is set to 1.
            Otherwise, the original data is returned unchanged.
    """
    if checklist:
        data['count'] = 1
    return data


@callback(
    Output('container', 'children'),
    Input('store', 'data')
)
def display_components(data: Dict[str, Any]) -> List[html.Div]:
    """
    Generate and display components based on the data in the store.

    This callback function is triggered when the 'store' data changes.
    It creates various UI components including range sliders, accordions,
    switches, and a treemap graph. The function organizes these components
    into a structured layout using Dash Bootstrap Components.

    Args:
        data (Dict[str, Any]):
            The current data stored in the 'store' component.
            Expected to contain a 'count' key.

    Returns:
        List[html.Div]:
            A list of Dash components to be rendered in the 'container'.

    Raises:
        PreventUpdate:
            If data['count'] is 0, preventing unnecessary updates.

    Components created:
    - Range sliders for level 1, 2, and 3 items
    - Sort switch
    - Color theme selection with reverse colors option
    - Treemap graph
    - iframe for displaying additional content
    """
    children: List[html.Div] = []
    if data['count'] == 0:
        raise PreventUpdate

    children.append(html.Div([
        create_main_controls_accordion(), html.Hr(),
        create_graph_and_iframe_section(), html.Hr()]))
    return children


@callback(
    Output({'type': 'checklist_colorscale', 'index': MATCH}, 'value'),
    Output({'type': 'checklist_colorscale', 'index': MATCH}, 'options'),
    Input({'type': 'reverse_colors_switch', 'index': MATCH}, 'value'),
    State({'type': 'checklist_colorscale', 'index': MATCH}, 'value'),
    State({'type': 'checklist_colorscale', 'index': MATCH}, 'options'),
)
def update_colorscale_checklist(
        switch_value: bool, checklist_value: str,
        checklist_options: List[Dict[str, str]]
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Update the colorscale checklist based on the reverse colors switch.

    This function modifies the checklist options and selected value to
    reverse the colorscale when the switch is activated. It appends '_r' to
    colorscale names to indicate reversal, or removes it when deactivated.

    Args:
        switch_value (bool): State of the reverse colors switch.
        checklist_value (str): Currently selected colorscale value.
        checklist_options (List[Dict[str, str]]):
            List of dictionaries containing current checklist options.

    Returns:
        tuple[str, List[Dict[str, str]]]: Contains the following elements:
            - str: Updated selected colorscale value.
            - List[Dict[str, str]]: Updated list of checklist options.
    """
    def modify(main_string: str) -> str:
        """Modify string based on switch state."""
        return main_string + '_r' if switch_value else \
            main_string.replace('_r', '')

    new_checklist_options = [
        {'label': modify(item['label']), 'value': modify(item['value'])}
        for item in checklist_options]

    new_checklist_value = modify(checklist_value)

    return new_checklist_value, new_checklist_options


@callback(
    Output({'type': 'treemap', 'index': MATCH}, 'figure'),
    Output({'type': 'treemap', 'index': MATCH}, 'style'),
    Output({'type': 'store_len_lev_1', 'index': MATCH}, 'data'),
    Output({'type': 'slider_2', 'index': MATCH}, 'max'),
    Output({'type': 'slider_3', 'index': MATCH}, 'max'),
    Input({'type': 'checklist_colorscale', 'index': MATCH}, 'value'),
    Input('theme_switch_value_store', 'data'),
    Input({'type': 'store_split', 'index': MATCH}, 'data'),
    Input({'type': 'sort_switch', 'index': MATCH}, 'value'),
    State({'type': 'store_len_lev_1', 'index': MATCH}, 'data'),
    State('checklist', 'value')
)
def update_treemap_and_store(
        checklist: str, switch: bool, split: Any, sort_switch: bool,
        store_len_lev_1: int | None, main_checklist: str
) -> Tuple[go.Figure, Dict[str, str], int, int, int]:
    """
    Update the treemap visualization and related data storage.

    This function creates or updates a treemap based on user selections,
    applying theme settings and storing relevant data for future use.

    Args:
        checklist (str): Selected color scale option.
        switch (bool): Theme switch state (True for light, False for dark).
        split (Any): Split data from store.
        sort_switch (bool): Sort switch state.
        store_len_lev_1 (Optional[int]): Previously stored level 1 length.
        main_checklist (str): Main category selection.

    Returns:
        Tuple[go.Figure, Dict[str, str], int, int, int]: Contains:
            - go.Figure: Updated treemap figure.
            - Dict[str, str]: Style dictionary for treemap visibility.
            - int: Updated count of level 1 items.
            - int: Max value for slider 2.
            - int: Max value for slider 3.
    """
    treee_fig = go.Figure(layout=fig_u.TEMPLATE)
    theme = {
        'template': 'plotly' if switch else 'plotly_dark',
        'paper_bgcolor': 'white' if switch else '#222222',
        'plot_bgcolor': 'white' if switch else '#222222',
        'font_color': 'black' if switch else 'white',
        'title_text': None, 'uniformtext': {"minsize": 16, "mode": False}
    }
    treee_fig.update_layout(**theme)

    treee_fig.add_trace(go.Treemap(
        marker={"cornerradius": 5}, maxdepth=4, sort=sort_switch))

    parents, labels, ids, len_levels = fig_u.keys_search(
        fig_u.GO_INFO[main_checklist]['object'], split)

    treee_fig.update_traces(
        go.Treemap(
            parents=parents, labels=labels, ids=ids, textfont={"size": 18},
            textposition="middle center", marker_colorscale=checklist,))

    callback_count = \
        store_len_lev_1 if store_len_lev_1 is not None else len_levels[0]

    return treee_fig, {'display': ''}, \
        callback_count, len_levels[1], len_levels[2]


@callback(
    Output({'type': 'store_split', 'index': MATCH}, 'data'),
    Input({'type': 'slider_1', 'index': MATCH}, 'value'),
    Input({'type': 'slider_2', 'index': MATCH}, 'value'),
    Input({'type': 'slider_3', 'index': MATCH}, 'value'),
)
def update_treemap_based_on_slider_inputs(
        slider_1_value: List[int], slider_2_value: List[int],
        slider_3_value: List[int]
) -> Dict[str, Dict[str, int]]:
    """
    Update the treemap visualization based on slider inputs.

    This function takes the values from three sliders and uses them to create
    a dictionary that defines the split ranges for each level of the treemap.

    Args:
        slider_1_value (List[int]): Start and end values for level 1 slider.
        slider_2_value (List[int]): Start and end values for level 2 slider.
        slider_3_value (List[int]): Start and end values for level 3 slider.

    Returns:
        Dict[str, Dict[str, int]]: A nested dictionary containing the split
        ranges for each level of the treemap.
    """
    split = {
        "level_1": {"start": slider_1_value[0], "end": slider_1_value[1]},
        "level_2": {"start": slider_2_value[0], "end": slider_2_value[1]},
        "level_3": {"start": slider_3_value[0], "end": slider_3_value[1]}
    }
    return split


@callback(
    Output({'type': 'slider_3', 'index': MATCH}, 'disabled'),
    Output({'type': 'slider_3', 'index': MATCH}, 'value'),
    Input({'type': 'slider_2', 'index': MATCH}, 'value'),
    State({'type': 'store_split', 'index': MATCH}, 'data'),
    prevent_initial_call=True
)
def disable_slider(
        slider_2_value: List[int], store_split: Dict[str, Dict[str, int]]
) -> Tuple[bool, List[int]]:
    """
    Update the state of slider 3 based on slider 2's value.

    This function disables slider 3 if the end value of slider 2 is 0,
    and updates slider 3's value based on the stored split data.

    Args:
        slider_2_value (List[int]): Start and end values for slider 2.
        store_split (Dict[str, Dict[str, int]]):
            Stored split data for all levels.

    Returns:
        Tuple[bool, List[int]]: A tuple containing:
            - bool: Whether slider 3 should be disabled.
            - List[int]: Updated values for slider 3.
    """
    level_3_values = list(store_split['level_3'].values())
    if slider_2_value[1] == 0:
        return True, level_3_values
    return False, level_3_values


@callback(
    Output({'type': 'click_data', 'index': MATCH}, 'children'),
    Output({'type': 'click_data', 'index': MATCH}, 'href'),
    Output({'type': 'iframe', 'index': MATCH}, 'src'),
    Output({'type': 'iframe', 'index': MATCH}, 'style'),
    Output({'type': 'col_graph', 'index': MATCH}, 'md'),
    Output({'type': 'col_iframe', 'index': MATCH}, 'style'),
    Input({'type': 'treemap', 'index': MATCH}, 'clickData'),
    State('checklist', 'value'),
    State({'type': 'iframe', 'index': MATCH}, 'style'),
)
def update_click_data_display(
        click_data: Dict[str, Any] | None, checklist: str,
        iframe_style: Dict[str, Any]
) -> Tuple[str, str, str, Dict[str, Any], Dict[str, int], Dict[str, str]]:
    """
    Update the display of click data for a treemap visualization.

    This function processes the click event data from a treemap and updates
    a text display. If no data point has been clicked, it shows a default
    message. Otherwise, it displays the ID of the clicked data point and
    updates the iframe source and style based on the click data.

    Args:
        click_data (Union[Dict[str, Any], None]):
            The click event data from the treemap.
            If None, no data point has been clicked.
        checklist (str): The selected value from the checklist.
        iframe_style (Dict[str, Any]): The style dictionary for the iframe.

    Returns:
        tuple: Contains the following elements:
            - str: The URL for the clicked data point.
            - str: The href for the clicked data point.
            - str: The src URL for the iframe.
            - Dict[str, Any]: The updated style dictionary for the iframe.
            - Dict[str, int]: The md size for the column containing the graph.
            - Dict[str, str]:
                The style dictionary for the column containing the iframe.
    """
    if click_data is None:
        raise PreventUpdate

    click_keys = list(click_data["points"][0].keys())
    if all(key in click_keys for key in ['id', 'root']):
        clicked_id = click_data["points"][0]["id"]
    elif all(key in click_keys for key in ['entry']):
        clicked_id = click_data["points"][0]["entry"]
    else:
        raise PreventUpdate

    clicked_id_split = clicked_id.split('*')

    url_post = fig_u.GO_INFO[checklist]['url_post']
    url_pre_section = fig_u.GO_INFO[checklist]['url_pre_section']

    url_pre = 'https://plotly.com/python/reference/'
    doc_url = f"{url_pre}{url_post}/#{url_pre_section}"

    doc_url += ''.join(f'-{pat_str}' for pat_str in clicked_id_split)

    iframe_style['display'] = '' if web_u.check_section_exists(
        doc_url) else 'none'

    if clicked_id_split[0][0].isupper():
        doc_url = doc_url.split('#')[0]
        iframe_style['display'] = ''

    return f'{doc_url}', f'{doc_url}', doc_url, \
        iframe_style, {"size": 6}, {'display': ''}


@callback(
    Output({'type': 'slider_1', 'index': MATCH}, 'max'),
    Output({'type': 'accordion_item', 'index': MATCH}, 'style'),
    Output({'type': 'accordion_item', 'index': MATCH}, 'title'),
    Input({'type': 'treemap', 'index': MATCH}, 'figure'),
    State({'type': 'store_len_lev_1', 'index': MATCH}, 'data'),
    State('checklist', 'value')
)
def update_accordion_and_slider_based_on_treemap(
        _: Any, store: int, checklist: str
) -> Tuple[int, Dict[str, Any], str, str, str]:
    """
    Update accordion items and range slider based on treemap selection.

    This function updates the maximum value of a range slider, the visibility
    of an accordion item, and the titles of two accordion items. It uses the
    selected checklist value to determine the appropriate graph object class.

    Args:
        _ (Any): Placeholder for unused treemap figure input.
        store (int): The maximum value for the range slider.
        checklist (str): The selected value from the checklist.

    Returns:
        tuple: Contains the following elements:
            - int: Maximum value for the range slider.
            - dict: Style dictionary for accordion item visibility.
            - str: Title for the main accordion item.
            - str: Title for the theme accordion item.
            - str: Title for the options accordion item.
    """
    obj_class_name = fig_u.GO_INFO[checklist]['object'].__class__.__name__
    main_title = styles.style_accordionitem_title(
        f"Options for {obj_class_name} object")
    accordion_item_style = styles.accordionitem_style
    accordion_item_style.update({'display': ''})
    return store, accordion_item_style, main_title


# graph_objs_list = [
#     obj for obj in dir(go)
#     if not obj.startswith('_') and not obj.islower()]
# class_instances = {
#     name: getattr(go, name)() for name in graph_objs_list}
# filtered_dict = {
#     key: value for key, value in class_instances.items() if value}
# print(filtered_dict)
