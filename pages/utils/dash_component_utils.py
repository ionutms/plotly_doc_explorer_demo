"""Structural Utilities for Dash Components.

This module provides utility functions for creating and managing various
Dash Bootstrap Components (dbc) and Dash Core Components (dcc).
It includes functions for creating labeled inputs, counter buttons,
range sliders, radioitems, and associated callbacks.

Functions:
    labeled_range_slider: Create a labeled range slider component.
    labeled_counter_trio: Create a 3-button counter group component.
    callback_labeled_counter_trio: Generate callback for trio counter.
    labeled_counter_quintet: Create a 5-button counter group component.
    callback_labeled_counter_quintet: Generate callback for quintet counter.
    extract_info_from_zip_as_int: Extract integer information from a ZIP file.
    callback_update_store_at_upload:
        Generate callback to update store on upload.
    create_labeled_input: Create a labeled input component.
    create_labeled_button: Create a labeled button component.
    callback_update_range_slider_value:
        Generate callback to update slider value.
    callback_update_range_slider_max_and_label: Update slider max and label.
    callback_update_range_slider_pushable_and_value: Update slider properties.
    callbacks_radioitems: Generate callbacks for radio items.
    app_description: Create an app description component.

These utilities simplify the creation of common UI elements in Dash
applications, providing consistent styling and behavior for various
interactive components such as range sliders, counter buttons,
labeled inputs, and radioitems.

The module also includes callback functions to handle user interactions
with these components and process uploaded files.
"""

from typing import Any, Callable, Dict, List, Union, Tuple

from dash import html, dcc
from dash import callback
from dash import no_update, ctx
from dash.dependencies import ALL, MATCH, Input, Output, State
import dash_bootstrap_components as dbc

import pages.utils.style_utils as styles
import pages.utils.signal_processing_utils as spu


def labeled_range_slider(
        id_section: str,
        label: str,
        default_value: List[int],
        min_value: int = 1,
        md=9,
) -> dbc.Col:
    """Create a labeled range slider column.

    Args:
        id_section (str): ID prefix for the range slider component.
        label (str): Label text to display above the range slider.
        default_value (List[int]):
            Default values for the range slider (two ints).
        min_value (int, optional):
            Minimum value for the range slider. Defaults to 1.
        marks (dict, optional): Dictionary of marks to display on the slider.

    Returns:
        dbc.Col: Dash Bootstrap column containing the labeled range slider.
    """
    labeled_range_slider_column = dbc.Col([
        dbc.Label(label, className=styles.CENTER_CLASS_NAME),
        dcc.RangeSlider(
            id=f"{id_section}_range_slider", min=min_value,
            value=default_value, pushable=1, step=1, marks=None, tooltip={
                "placement": "topLeft", "always_visible": False,
                "style": {"fontSize": "12px"}}),
        html.Br()], xs=12, md=md)
    return labeled_range_slider_column


def labeled_counter_trio(
        id_section: str,
        label: str,
        limits: Dict[str, float],
        default_count: int = 1,
        md: int = 3
) -> dbc.Col:
    """Create a labeled button group for incrementing and decrementing a count.

    Args:
        id_section (str): Unique identifier for component IDs.
        label (str): Text to display above the button group.
        default_count (int, optional): Initial count value. Defaults to 1.
        max_count (int, optional):
            Maximum value for the counter. Defaults to 1.
        md (int, optional):
            Column width for medium and larger screens. Defaults to 3.

    Returns:
        dbc.Col:
            Bootstrap column containing the label and counter button group.
    """
    counter_button_group = dbc.Col([
        dcc.Store(id=f'{id_section}_store', data=limits),
        dbc.Label(
            children=label, id=f'{id_section}_label',
            className=styles.CENTER_CLASS_NAME),
        dbc.ButtonGroup([
            dbc.Button(
                "<", id=f'{id_section}_decrement_button',
                outline=False, color="secondary"),
            dbc.Button(
                f"{default_count}", id=f'{id_section}_button',
                outline=False, color="secondary", disabled=True),
            dbc.Button(
                ">", id=f'{id_section}_increment_button',
                outline=False, color="secondary")
        ], className="d-flex flex-wrap"),
        html.Br()], xs=12, md=md)
    return counter_button_group


def callback_labeled_counter_trio(
    base_id: str,
    resolution: int = 1
) -> None:
    """Generate a Dash callback for incrementing and decrementing a count.

    Args:
        base_id (str): Base ID for the related Dash components.
        resolution (int, optional):
            Step size for incrementing/decrementing. Defaults to 1.

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(f'{base_id}_button', 'children'),
        Input(f'{base_id}_decrement_button', 'n_clicks'),
        Input(f'{base_id}_increment_button', 'n_clicks'),
        State(f'{base_id}_store', 'data'),
        State(f'{base_id}_button', 'children'),
        prevent_initial_call=True
    )
    def labeled_counter_trio_callback(
        _decrement: int,
        _increment: int,
        stored_data: Dict[str, Any],
        current_count: str
    ) -> Union[int, Any]:
        """
        Updates the count when increment/decrement buttons are clicked.

        This function adjusts the current count, ensuring it stays within
        the range of 'resolution' to the maximum count stored in the data.

        Args:
            _increment: Number of times increment button clicked (unused).
            _decrement: Number of times decrement button clicked (unused).
            stored_data: Dictionary containing the maximum count.
            current_count: Current count as a string.

        Returns:
            Updated count, or no_update if no change.
        """
        try:
            max_count = stored_data["max_count"]
            min_count = stored_data["min_count"]
            current = int(current_count)
        except (KeyError, ValueError):
            return no_update

        if ctx.triggered_id == f'{base_id}_decrement_button':
            current -= resolution
        elif ctx.triggered_id == f'{base_id}_increment_button':
            current += resolution

        return max(min(current, max_count), min_count)


def labeled_counter_quintet(
        id_section: str,
        label: str,
        limits: Dict[str, float],
        default_count: int = 1,
        md: int = 3
) -> dbc.Col:
    """Create a labeled button group with five buttons for count manipulation.

    Args:
        id_section (str): Unique identifier for component IDs.
        label (str): Text to display above the button group.
        limits (Dict[str, float]):
            Dictionary containing min and max count limits.
        default_count (int, optional): Initial count value. Defaults to 1.
        md (int, optional):
            Column width for medium and larger screens. Defaults to 3.

    Returns:
        dbc.Col:
            Bootstrap column containing the label and counter button group.
    """
    counter_button_group = dbc.Col([
        dcc.Store(id=f'{id_section}_store', data=limits),
        dbc.Label(
            children=label, id=f'{id_section}_label',
            className=styles.CENTER_CLASS_NAME
        ),
        dbc.ButtonGroup([
            dbc.Button(
                "<<", id=f'{id_section}_divide_button',
                outline=False, color="secondary"),
            dbc.Button(
                "<", id=f'{id_section}_decrement_button',
                outline=False, color="secondary"),
            dbc.Button(
                f"{default_count}", id=f'{id_section}_button',
                outline=False, color="secondary", disabled=True),
            dbc.Button(
                ">", id=f'{id_section}_increment_button',
                outline=False, color="secondary"),
            dbc.Button(
                ">>", id=f'{id_section}_multiply_button',
                outline=False, color="secondary"),
        ], className="d-flex flex-wrap"),
        html.Br()], xs=12, md=md)
    return counter_button_group


def callback_labeled_counter_quintet(
    base_id: str,
    resolution: Union[int, float],
    decimal_places: Union[int, None] = None
) -> None:
    """
    Creates a Dash callback for incrementing and decrementing a count.

    Args:
        base_id: Base ID for the related Dash components.
        resolution: Step size for incrementing/decrementing.
        decimal_places: Number of decimal places to round to.

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(f'{base_id}_button', 'children'),
        Input(f'{base_id}_divide_button', 'n_clicks'),
        Input(f'{base_id}_decrement_button', 'n_clicks'),
        Input(f'{base_id}_increment_button', 'n_clicks'),
        Input(f'{base_id}_multiply_button', 'n_clicks'),
        State(f'{base_id}_store', 'data'),
        State(f'{base_id}_button', 'children'),
        prevent_initial_call=True
    )
    def labeled_counter_quintet_callback(
        _divide: int,
        _decrement: int,
        _increment: int,
        _multiply: int,
        stored_data: Dict[str, Any],
        current_count: str
    ) -> Union[float, Any]:
        """
        Updates the count when increment/decrement buttons are clicked.

        This function adjusts the current count, ensuring it stays within
        the range of min_count to max_count stored in the data.

        Args:
            _divide: Number of times divide button clicked (unused).
            _increment: Number of times increment button clicked (unused).
            _decrement: Number of times decrement button clicked (unused).
            _multiply: Number of times multiply button clicked (unused).
            stored_data: Dictionary containing min and max counts.
            current_count: Current count as a string.

        Returns:
            Updated count, or no_update if no change.
        """
        try:
            max_count = stored_data["max_count"]
            min_count = stored_data["min_count"]
            current = float(current_count)
        except (KeyError, ValueError):
            return no_update

        if ctx.triggered_id == f'{base_id}_divide_button':
            current /= 10
        elif ctx.triggered_id == f'{base_id}_decrement_button':
            current -= resolution
        elif ctx.triggered_id == f'{base_id}_increment_button':
            current += resolution
        elif ctx.triggered_id == f'{base_id}_multiply_button':
            current *= 10

        return round(
            float(max(min(current, max_count), min_count)), decimal_places)


def extract_info_from_zip_as_int(
    contents: str,
    file_name: str,
    search_key: str
) -> int:
    """
    Extract information from a ZIP file and return it as an integer.

    This function uses the `extract_info_from_zip` function to extract
    information based on a given search key from a ZIP file's contents.
    It then converts the first extracted value to an integer.

    Args:
        contents (str): Base64 encoded string of the ZIP file contents.
        search_key (str): The key to search for in the ZIP file's CSV contents.

    Returns:
        int: The first extracted value converted to an integer.

    Raises:
        ValueError: If the extracted value cannot be converted to an integer.
        IndexError: If no value is found for the given search key.

    Note:
        This function assumes that the `extract_info_from_zip` function returns
        a dictionary where values are either strings or lists of strings.
    """
    if file_name.lower().endswith('.zip'):
        return int(next(iter(spu.extract_info_from_zip(
            contents, [search_key]).values())))
    return no_update


def callback_update_store_at_upload(
    base_id: str,
    upload_id: str,
    store_id: str,
    process: Callable,
    search_key: str | None = None
) -> None:
    """
    Create a callback function to update a store when a ZIP file is uploaded.

    This function generates a callback that processes ZIP file uploads,
    extracts specific information based on the provided search key,
    and updates the corresponding store.

    Args:
        base_id (str): Base ID for the store component.
        upload_id (str): ID of the upload component.
        search_key (str): Key to search for in the ZIP file contents.

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(f'{base_id}_store', 'data'),
        Output(f'{base_id}_range_slider', 'marks'),
        Input(f'{upload_id}', 'contents'),
        State(f'{upload_id}', 'filename'),
        State(f'{store_id}', 'data'),
        State(f'{base_id}_store', 'data'),
        prevent_initial_call=True
    )
    def update_count_from_zip(
        contents: str,
        filename: str,
        global_store: Dict[str, Any],
        store: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update the store with information extracted from the uploaded ZIP file.

        This callback function processes ZIP file uploads, extracting specific
        information based on the search_key and updating the store accordingly.

        Args:
            contents (str): Base64 encoded contents of the uploaded file.
            filename (str): Name of the uploaded file.
            store (Dict[str, Any]): Current state of the store.

        Returns:
            Dict[str, Any]:
                Updated store with new information extracted from the ZIP file.

        Raises:
            PreventUpdate: If the uploaded file is not a ZIP file.
        """

        if filename.lower().endswith('.zip'):
            if process.__name__ == "extract_info_from_zip_as_int":
                store['max_count'] = process(contents, filename, search_key)
                return store, None
            if process.__name__ == "count_csv_files_from_zip":
                store['max_count'] = process(contents)
                return store, None
            if process.__name__ == "extract_data_frame_from_zip_contents":
                names = process(contents, filename, global_store)
                store['max_count'] = len(names)
                marks = dict(enumerate(names, 1))
                return store, marks
        return no_update, no_update


def create_labeled_input(
    id_section: str,
    label: str,
    placeholder: str,
    value: Any,
    md: int = 3
) -> dbc.Col:
    """Create a labeled input column.

    Args:
        id_section: ID for the input element.
        label: Text for the input label.
        placeholder: Placeholder text for the input.
        value: Default value for the input.
        md: Column width for medium screens and up. Defaults to 3.

    Returns:
        A Bootstrap column containing a labeled input and horizontal rule.
    """
    labeled_input_column = dbc.Col([
        dbc.Label(label, className=styles.CENTER_CLASS_NAME),
        dbc.Input(
            id=id_section, type="text", placeholder=placeholder,
            value=value, className="d-flex flex-wrap"),
        html.Br(),
    ], xs=12, md=md)
    return labeled_input_column


def create_labeled_button(
    id_section: str,
    label: str,
    button_label: str,
    md: int = 6
) -> dbc.Col:
    """Create a labeled button column.

    Args:
        id_section: ID for the button element.
        label: Text for the button label.
        button_label: Text for the button.
        md: Column width for medium screens and up. Defaults to 6.

    Returns:
        A Bootstrap column containing a labeled button and horizontal rule.
    """
    labeled_button_column = dbc.Col([
        dbc.Label(
            label, id=f'{id_section}_label',
            className=styles.CENTER_CLASS_NAME),
        dbc.Button(
            button_label, id=f'{id_section}_button',
            className=styles.CENTER_CLASS_NAME),
        html.Br(),
    ], xs=12, md=md)
    return labeled_button_column


def callback_update_range_slider_value(
        base_id: str,
        lock: int | None = None,
) -> None:
    """
    Creates a Dash callback to update the range slider value.

    Args:
        base_id: Base ID for the related Dash components.

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(f'{base_id}_range_slider', 'value'),
        Input(f'{base_id}_button', 'children'),
        Input(f'{base_id}_range_slider', 'value'),
        prevent_initial_call=True
    )
    def update_range_slider_value(
        current_count: str,
        range_slider_input
    ) -> List[int]:
        """
        Updates the range slider value based on the current count.

        Args:
            current_count: Current count as a string.

        Returns:
            A list of integers from 1 to the current count.
        """
        if ctx.triggered_id == f'{base_id}_range_slider':
            if lock is not None:
                if range_slider_input[lock] != 1:
                    range_slider_input[lock] = 1
                    return range_slider_input
            return no_update

        current = int(current_count)
        return list(range(1, current + 1))


def callback_update_range_slider_max_and_label(
    base_id: str,
    upload_id: str,
    reset_value: int = 1
) -> None:
    """Generate Dash callbacks to update range slider max value and label.

    This function sets up three callback functions for handling updates to
    range slider, label, and style based on file uploads and data changes.

    Args:
        base_id: Base ID for the related Dash components.
        upload_id: ID of the upload component.
        reset_value: Value to reset the counter to on upload (default: 1).

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(f'{base_id}_label', 'children'),
        Output(f'{base_id}_range_slider', 'max'),
        Input(f'{base_id}_store', 'data'),
        State(f'{base_id}_label', 'children'),
        prevent_initial_call=True
    )
    def update_range_slider_max_and_label(
        store: Dict[str, Any],
        label: str
    ) -> Tuple[str, int]:
        """Update UI components based on the number of detected files.

        Args:
            store: A dictionary containing the count of detected files.
            label: The current label text for detected files.

        Returns:
            A tuple containing the updated label text and new max slider value.
        """
        try:
            new_label = label.replace(label.split(
                ' ')[0], str(store["max_count"]))
            return new_label, store["max_count"]
        except KeyError:
            return label, 0

    @callback(
        Output(f'{base_id}_button', 'children', allow_duplicate=True),
        Input(f'{upload_id}', 'contents'),
        prevent_initial_call=True
    )
    def reset_labeled_counter_callback(_upload: str) -> int:
        """Reset the counter when an upload event occurs.

        Args:
            _upload: The contents of the upload component (unused).

        Returns:
            The reset value for the counter.
        """
        return reset_value

    @callback(
        Output(f'{base_id}_row', 'style'),
        Input(f'{base_id}_store', 'data'),
        prevent_initial_call=True
    )
    def control_style(
        store: Dict[str, Any]
    ) -> Dict[str, str]:
        """Control the visibility of the row based on max count.

        Args:
            store: A dictionary containing the max count of items.

        Returns:
            A dictionary specifying the display style for the row.
        """
        return {'display': 'none'} \
            if store['max_count'] == 1 else {'display': ''}


def callback_update_range_slider_pushable_and_value(
        base_id: str
) -> None:
    """Generate a callback to update range slider pushable property and value.

    Args:
        base_id (str): Base ID for the Dash components.

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(f'{base_id}_range_slider', 'pushable'),
        Output(f'{base_id}_range_slider', 'value'),
        Input(f'{base_id}_button', 'children'),
        State(f'{base_id}_range_slider', 'value'),
        prevent_initial_call=True
    )
    def update_range_slider_pushable_and_value(
            current_count: str,
            slider_value: List[int],
    ) -> Tuple[int, List[int]]:
        """
        Update range slider pushable and value based on button clicks.

        Args:
            current_count (str): Current count from button clicks.
            slider_value (List[int]): Current slider value.

        Returns:
            Tuple[int, List[int]]: Updated pushable value and slider value.
        """
        slider_value[1] = slider_value[0] + int(current_count)
        return int(current_count), slider_value


def app_description(
    title: str,
    about: Tuple[str],
    features: Tuple[str],
    usage_steps: Tuple[str]
) -> html.Div:
    """Create a description component for any app page.

    Args:
        title (str): The title of the page.
        about (Tuple[str]): A brief description of the page's purpose.
        features (Tuple[str]): A tuple of key features of the page.
        usage_steps (Tuple[str]):
            A tuple of steps describing how to use the page.

    Returns:
        html.Div: A Div component containing the formatted app description.
    """
    left_column_content: dbc.Col = dbc.Col([
        html.H4("Key Features:"),
        html.Ul([html.Li(feature) for feature in features])
    ], xs=12, md=6)

    right_column_content: dbc.Col = dbc.Col([
        html.H4("How to Use:"),
        html.Ol([html.Li(step) for step in usage_steps])
    ], xs=12, md=6)

    description: html.Div = html.Div([
        html.Hr(),
        html.H3(f"About the {title}"), *[
            html.Div(content) if len(about) > 1
            else html.Div(content) for content in about],
        html.Hr(),
        dbc.Row([left_column_content, right_column_content]),
        html.Hr()])
    return description


def callbacks_radioitems(
    id_section: str,
    row_id: str
) -> None:
    """Generate callbacks for radio items in a section.

    This function sets up three callback functions for handling radio items
    in a specific section of a Dash application. The callbacks are registered
    with the Dash app and do not need to be returned.

    Args:
        id_section: The ID of the section.
        row_id: The ID of the row.

    Returns:
        None. The function registers callbacks with the Dash app.
    """
    @callback(
        Output(row_id, "children"),
        Input(f"{id_section}_range_slider", "value"),
        State(f"{id_section}_range_slider", "marks"),
        prevent_initial_call=True
    )
    def generate_radioitems(
        values: List[int],
        marks: Dict[str, str]
    ) -> List[dbc.Col]:
        """Generate radio items based on range slider values.

        Args:
            values: The selected values from the range slider.
            marks: The marks on the range slider.

        Returns:
            A list of Column components containing radio items.
        """
        columns = []
        y_axis_channels = [marks[str(position)] for position in values[1:]]
        options = [
            {"label": f'y{index}' if index > 1 else 'y', "value": index}
            for index, _ in enumerate(y_axis_channels, 1)]

        for index, y_axis_data in enumerate(y_axis_channels[1:], 1):
            columns.append(dbc.Col([dbc.Card([dbc.Row([
                dbc.Col([
                    dbc.Label(
                        f"{y_axis_data} axis selection",
                        id={'type': 'label selection', 'index': index},
                        className=styles.CENTER_CLASS_NAME),
                    dbc.RadioItems(
                        options=options, value=options[0]["value"],
                        id={'type': 'radioitems', 'index': index},
                        className=styles.CENTER_CLASS_NAME, inline=True),
                ], xs=10, md=10),
                dbc.Col([
                    dbc.Label(
                        'Left', id={'type': 'label side', 'index': index}),
                    dbc.Switch(
                        id={'type': 'switch', 'index': index},
                        value=False, className="d-flex justify-content-center")
                ], xs=2, md=2, className=styles.FLEX_CENTER_COLUMN)
            ])], body=True, style={
                "border": "1px dashed", "border-radius": "10px",
                "padding": "1px", "background-color": "transparent"}),
                html.Br()], xs=12, md=4))

        return columns

    @callback(
        Output('filtering_store', 'data', allow_duplicate=True),
        Input("legend_group_switch", 'value'),
        Input('filtering_store', 'data'),
        prevent_initial_call=True
    )
    def update_filtering_store_2(
        legend_group_switch: bool,
        filtering: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        TODO
        """
        try:
            filtering.update({"legend_group": legend_group_switch})
            return filtering
        except (KeyError, IndexError):
            return filtering

    @callback(
        Output('filtering_store', 'data', allow_duplicate=True),
        Output({'type': 'switch', 'index': ALL}, 'value'),
        Input({'type': 'radioitems', 'index': ALL}, 'value'),
        Input({'type': 'switch', 'index': ALL}, 'value'),
        Input('filtering_store', 'data'),
        prevent_initial_call=True
    )
    def update_filtering_store(
        radioitems_values: List[int],
        switch: List[bool],
        filtering: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update the filtering store based on radio item selections.

        Args:
            radioitems_values: The selected values from the radio items.
            filtering: The current filtering data.

        Returns:
            The updated filtering data.
        """
        try:
            selection = {}
            for index, key in enumerate(filtering['y_axis_data'][1:]):
                selection[key] = (
                    f'y{radioitems_values[index]}'
                    if radioitems_values[index] > 1 else 'y')
            filtering.update({"y_axis_selection": selection})

            def update_list(original_list):
                value_states = {}

                for value, state in original_list:
                    if value not in value_states:
                        value_states[value] = state

                result = [
                    (value, value_states[value]) for value, _ in original_list]

                return result

            for index, item in enumerate(radioitems_values):
                if item == 1:
                    switch[index] = False
                if item > 1:
                    unzipped = list(zip(*update_list(
                        list(zip(radioitems_values, switch)))))
                    switch = [list(state) for state in unzipped][1]

            side = {}
            for index, key in enumerate(filtering['y_axis_data'][1:]):
                side[key] = switch[index]
            filtering.update({"y_axis_side": side})

            return filtering, switch
        except (KeyError, IndexError):
            return filtering, no_update

    @callback(
        Output({'type': 'label side', 'index': MATCH}, 'children'),
        Input({'type': 'switch', 'index': MATCH}, 'value'),
        prevent_initial_call=True
    )
    def update_side_label(switch: bool) -> str:
        """Update the side label based on the switch value.

        Args:
            switch: The current state of the switch (True/False).

        Returns:
            The updated label text ('Right' or 'Left').
        """
        return 'Right' if switch else 'Left'
