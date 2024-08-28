"""
Figure Utilities for Plotly

This module provides utility functions and constants for creating and
manipulating Plotly figures. It includes:

- Constants for graph configuration and color scales
- A default figure template
- Functions for building hierarchical structures of Plotly objects
- A dictionary of Plotly graph object information

Main functions:
    find_last_options: Find and add last options to the tree structure
    find_mid_options: Find and add middle options to the tree structure
    find_first_options: Find first options and initialize the tree structure
    keys_search: Search keys in a hierarchical structure
    create_go_info_item: Generate a sub-dictionary for a Plotly graph object

The module is designed to assist in the creation and customization of Plotly
figures, providing tools for exploring and manipulating Plotly object
structures.
"""

import inspect
from typing import Any, Dict, List, Optional, Tuple
import plotly.graph_objects as go
from _plotly_utils.exceptions import PlotlyKeyError


GRAPH_CONFIG = {
    'displayModeBar': "hover", 'displaylogo': False, 'editable': False,
    'modeBarButtonsToRemove': [
        'zoom2d', 'pan2d', 'zoomIn2d', 'lasso2d', 'select2d',
        'zoomOut2d', 'autoScale2d', 'resetScale2d'],
    'modeBarButtonsToAdd': [
        'drawline', 'drawopenpath', 'drawclosedpath',
        'drawcircle', 'drawrect', 'eraseshape'],
    'doubleClickDelay': 600, 'scrollZoom': False,
    'toImageButtonOptions': {
        'format': 'jpeg', 'height': None, 'width': None, 'scale': 1}}

MARKER_COLORSCALE = [
    'aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody',
    'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu',
    'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense',
    'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray',
    'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno',
    'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
    'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg',
    'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd',
    'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu',
    'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset',
    'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal',
    'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu',
    'ylorbr', 'ylorrd']


TEMPLATE = go.Layout(
    margin={"l": 0, "r": 0, "t": 0, "b": 0}, showlegend=True,
    hoverlabel={"font_family": 'Droid Sans', "namelength": -1},
    title_font={"family": 'Droid Sans', "color": '#000000'},
    title_text="Graph Title", title_xanchor="center", title_x=0.5,
    bargap=0.05, bargroupgap=0.1, autosize=True, height=500,
    paper_bgcolor="#ffffff", plot_bgcolor='#ffffff',
    legend={
        "itemsizing": 'constant', "bgcolor": '#ffffff',
        "font": {'family': 'Droid Sans', 'color': '#000000'}},
    xaxis={
        "autorange": True, "gridcolor": "#808080", "zerolinecolor": "#808080",
        "title": {"standoff": 0, "text": "X Axis"},
        "titlefont": {"family": 'Droid Sans', "color": '#000000'},
        "showgrid": True, "gridwidth": 1, "griddash": "dash",
        "zeroline": False, "zerolinewidth": 1,
        "tickfont": {"family": 'Droid Sans', "color": '#000000'}},
    yaxis={
        "gridcolor": "#808080", "zerolinecolor": "#808080",
        "title": {"standoff": 0, "text": "Y Axis"},
        "titlefont": {"family": 'Droid Sans', "color": '#000000'},
        "showgrid": True, "gridwidth": 1, "griddash": "dash",
        "zeroline": False, "zerolinewidth": 1,
        "tickfont": {"family": 'Droid Sans', "color": '#000000'}})


def find_last_options(
    tree: Dict[str, List[str]], zipped: List[List[str]],
    root_go_obj: go.Figure, root_key: str, split: Dict[str, int]
) -> Dict[str, List[str]]:
    """Find and add last options to the tree structure.

    Args:
        tree (Dict[str, List[str]]): The current tree structure
            containing 'parents', 'labels', and 'ids'.
        zipped (List[List[str]]): The zipped list of existing tree
            nodes to compare against.
        root_go_obj (go.Figure): The source dictionary with possible
            options for each label.
        root_key (str): The root key prefix for the current level
            of the tree.

    Returns:
        Dict[str, List[str]]: The updated tree structure with added
            last options.
    """

    # Find differences between current zipped list and tree's zip
    zip_diff = [
        item for item in
        sorted(list(set(zip(tree["parents"], tree["labels"], tree["ids"]))))
        if item not in zipped
    ]
    list_max: int = 0

    # Process each difference
    for parent, label, zip_id in zip_diff:
        # Adjust the parent key by removing the root_key prefix
        parent = parent.replace(f'{root_key}*', '')
        try:
            # Get and sort new labels from the root_go_obj
            if not isinstance(root_go_obj[parent][label], (str, tuple)):
                new_labels = [
                    key for key in sorted(
                        list(set(root_go_obj[parent][label])))
                    if not key.endswith('src')]
                list_max = max(list_max, len(new_labels))
                if split is not None:
                    try:
                        new_labels = new_labels[
                            split['level_3']['start']:split['level_3']['end']]
                    except KeyError:
                        pass
                # Extend tree with new labels
                tree["labels"].extend(new_labels)
                tree["parents"].extend([zip_id] * len(new_labels))
                tree["ids"].extend(
                    [f'{zip_id}*{new_label}' for new_label in new_labels])

        except (TypeError, PlotlyKeyError):
            # Continue on TypeError or PlotlyKeyError
            continue

    return tree, list_max


def find_mid_options(
    tree: Dict[str, List[str]], root_go_obj: Dict[str, List[str]],
    root_key: str, split: Dict[str, int]
) -> Dict[str, List[str]]:
    """Find and add middle options to the tree structure.

    Args:
        tree (Dict[str, List[str]]): The current tree structure
            containing 'parents', 'labels', and 'ids'.
        root_go_obj (Dict[str, List[str]]): The source dictionary
            with possible options for each label.
        root_key (str): The root key prefix for the current level
            of the tree.

    Returns:
        Dict[str, List[str]]: The updated tree structure with added
            middle options.
    """

    # Dictionary to store options for each label
    options: Dict[str, List[str]] = {}
    list_max: int = 0

    # Iterate over each label in the current tree structure
    for label in tree["labels"]:
        try:
            # Attempt to get and sort unique options from root_go_obj
            if not isinstance(root_go_obj[label], (str, tuple)):
                options[label] = [
                    key for key in sorted(set(root_go_obj[label]))
                    if not key.endswith('src')
                    and not key.endswith('defaults')]
                list_max = max(list_max, len(options[label]))
            if split is not None:
                try:
                    options[label] = options[label][
                        split['level_2']['start']:split['level_2']['end']]
                except KeyError:
                    pass
        except (TypeError, KeyError, PlotlyKeyError):
            # If there's a TypeError or PlotlyKeyError, skip this label
            continue

    # Iterate over the collected options to extend the tree structure
    for new_key, new_options in options.items():
        # Extend the 'parents' list in the tree with new parent keys
        tree["parents"].extend([
            f'{root_key}*{new_key}'
            if root_key != "" else f'{new_key}'] * len(new_options))

        # Extend the 'labels' list in the tree with new options
        tree["labels"].extend(new_options)

        # Extend the 'ids' list in the tree with new unique IDs
        tree["ids"].extend(
            [f'{root_key}*{new_key}*{option}' if root_key != "" else
             f'{new_key}*{option}' for option in new_options])

    # Return the updated tree structure
    return tree, list_max


def find_first_options(
    figure: Dict[str, List[str]], root_key: str,
    split: Optional[Dict[str, int]] = None
) -> Tuple[
        Dict[str, List[str]], Dict[str, List[str]],
        List[Tuple[str, str, str]], int]:
    """Find first options and initialize the tree structure.

    Args:
        figure (Dict[str, List[str]]): The source dictionary with
            possible options.
        root_key (str): The root key prefix for the current level
            of the tree.

    Returns:
        Tuple containing the tree structure, the root figure, and
        the zipped list of tree nodes.
    """

    tree = {}

    signature = inspect.signature(figure.__init__)

    to_remove = [
        'self', 'arg', 'kwargs', 'annotations', 'coloraxis', 'geo', 'images',
        'mapbox', 'polar', 'scene', 'selections', 'shapes', 'sliders',
        'smith', 'ternary', 'updatemenus', 'xaxis', 'yaxis'
    ]
    main_keys = []
    for param_name, _ in signature.parameters.items():
        if param_name not in to_remove \
                and not param_name.endswith('src')\
                and not param_name.endswith('defaults'):
            main_keys.append(param_name)

    class_name = figure.__class__.__name__

    # Initialize labels, parents, and ids for the tree
    labels = [class_name] + main_keys
    parents = [''] + [class_name] * len(main_keys)
    ids = [class_name] + [
        f'{parent}*{label}' if root_key != "" else f'{label}'
        for parent, label in zip(parents[1:], labels[1:])
    ]

    # Split and zip list of parents, labels, and ids
    zipped = list(zip(parents, labels, ids))
    if split is not None:
        try:
            zipped = zipped[split['level_1']['start']:split['level_1']['end']]
        except KeyError:
            pass

    # Unzip the sorted and deduplicated list into separate lists
    parents, labels, ids = zip(*zipped)
    tree["parents"], tree["labels"], tree["ids"] = (
        list(parents), list(labels), list(ids)
    )

    # Return the initialized tree, root figure, and zipped list
    return tree, figure, zipped, len(zipped)


def has_duplicates(lst):
    """Check duplicates."""
    result = len(lst) != len(set(lst))

    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1
        else:
            counts[item] = 1

    duplicates = [item for item, count in counts.items() if count > 1]

    if result:
        print("Duplicated items:", duplicates)
    return result


def keys_search(
    go_obj: go, split=None, root_key: str = "",
) -> Tuple[List[str], List[str], List[str]]:
    """Searches keys in a hierarchical structure and returns tree components.

    This function searches through a hierarchical structure represented
    by `go_obj`, starting from a specified `root_key`, and optionally
    ignoring certain keys. It combines the results of `find_first_options`,
    `find_mid_options`, and `find_last_options` functions to build a tree
    structure of parents, labels, and ids.

    Args:
        go_obj (go.Figure): The source hierarchical structure with possible
            options.
        root_key (str, optional): The root key prefix for the current level
            of the tree. Defaults to "".
        ignore (List[str], optional): List of keys to ignore. Defaults to None.

    Returns:
        Tuple[List[str], List[str], List[str]]:
            A tuple containing three lists:
            - parents: List of parent keys in the tree structure.
            - labels: List of labels in the tree structure.
            - ids: List of ids in the tree structure.
    """

    # Initialize the tree structure with first options
    tree, root_go_obj, zipped, zipped_len = find_first_options(
        go_obj, root_key, split)

    # Find and add middle options to the tree structure
    tree, len_lv_2 = find_mid_options(tree, root_go_obj, root_key, split)

    # Find and add last options to the tree structure
    tree, len_lv_3 = find_last_options(
        tree, zipped, root_go_obj, root_key, split)

    # Return the tree components
    return tree["parents"], tree["labels"], tree["ids"], \
        (zipped_len, len_lv_2, len_lv_3)


def create_go_info_item(
    object_type: go,
    url_post: Optional[str] = None,
    url_pre_section: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a sub-dictionary for a Plotly graph object.

    :param object_type: The Plotly graph object type (e.g., go.Bar)
    :param url_post: The URL post section (optional)
    :param url_pre_section: The URL pre-section (optional)
    :return: A dictionary with 'object', 'url_post', and 'url_pre_section'
    """
    item: Dict[str, Any] = {'object': object_type()}

    if url_post is None:
        url_post = object_type.__name__.lower()
    if url_pre_section is None:
        url_pre_section = url_post

    item['url_post'] = url_post
    item['url_pre_section'] = url_pre_section

    return item


GO_INFO = {
    'Bar': create_go_info_item(go.Bar),
    'Barpolar': create_go_info_item(go.Barpolar),
    'Box': create_go_info_item(go.Box),
    'Candlestick': create_go_info_item(go.Candlestick),
    'Carpet': create_go_info_item(go.Carpet),
    'Choropleth': create_go_info_item(go.Choropleth),
    'Choroplethmapbox': create_go_info_item(go.Choroplethmapbox),
    'Cone': create_go_info_item(go.Cone),
    'Contour': create_go_info_item(go.Contour),
    'Contourcarpet': create_go_info_item(go.Contourcarpet),
    'Densitymapbox': create_go_info_item(go.Densitymapbox),
    'Figure': create_go_info_item(go.Figure),
    'FigureWidget': create_go_info_item(go.FigureWidget),
    'Frame': create_go_info_item(go.Frame),
    'Funnel': create_go_info_item(go.Funnel),
    'Funnelarea': create_go_info_item(go.Funnelarea),
    'Heatmap': create_go_info_item(go.Heatmap),
    'Heatmapgl': create_go_info_item(go.Heatmapgl),
    'Histogram': create_go_info_item(go.Histogram),
    'Histogram2d': create_go_info_item(go.Histogram2d),
    'Histogram2dContour': create_go_info_item(go.Histogram2dContour),
    'Icicle': create_go_info_item(go.Icicle),
    'Image': create_go_info_item(go.Image),
    'Indicator': create_go_info_item(go.Indicator),
    'Isosurface': create_go_info_item(go.Isosurface),

    'Layout': create_go_info_item(go.Layout),
    'Annotation': create_go_info_item(
        go.layout.Annotation, 'layout/annotations',
        'layout-annotations-items-annotation'),
    'Coloraxis': create_go_info_item(
        go.layout.Coloraxis, 'layout/coloraxis', 'layout-coloraxis'),
    'Geo': create_go_info_item(
        go.layout.Geo, 'layout/geo', 'layout-geo'),
    'Layout_Image': create_go_info_item(
        go.layout.Image, 'layout/images', 'layout-images-items-image'),
    'Mapbox': create_go_info_item(
        go.layout.Mapbox, 'layout/mapbox', 'layout-mapbox'),
    'Polar': create_go_info_item(
        go.layout.Polar, 'layout/polar', 'layout-polar'),
    'Scene': create_go_info_item(
        go.layout.Scene, 'layout/scene', 'layout-scene'),
    'Selections': create_go_info_item(
        go.layout.Selection, 'layout/selections',
        'layout-selections-items-selection'),
    'Shapes': create_go_info_item(
        go.layout.Shape, 'layout/shapes', 'layout-shapes-items-shape'),
    'Sliders': create_go_info_item(
        go.layout.Slider, 'layout/sliders', 'layout-sliders-items-slider'),
    'Smith': create_go_info_item(
        go.layout.Smith, 'layout/smith', 'layout-smith'),
    'Ternary': create_go_info_item(
        go.layout.Ternary, 'layout/ternary', 'layout-ternary'),
    'Updatemenus': create_go_info_item(
        go.layout.Updatemenu, 'layout/updatemenus',
        'layout-updatemenus-items-updatemenu'),
    'XAxis': create_go_info_item(
        go.layout.XAxis, 'layout/xaxis', 'layout-xaxis'),
    'YAxis': create_go_info_item(
        go.layout.YAxis, 'layout/yaxis', 'layout-yaxis'),

    'Mesh3d': create_go_info_item(go.Mesh3d),
    'Ohlc': create_go_info_item(go.Ohlc),
    'Parcats': create_go_info_item(go.Parcats),
    'Parcoords': create_go_info_item(go.Parcoords),
    'Pie': create_go_info_item(go.Pie),
    'Pointcloud': create_go_info_item(go.Pointcloud),
    'Sankey': create_go_info_item(go.Sankey),
    'Scatter': create_go_info_item(go.Scatter),
    'Scatter3d': create_go_info_item(go.Scatter3d),
    'Scattercarpet': create_go_info_item(go.Scattercarpet),
    'Scattergeo': create_go_info_item(go.Scattergeo),
    'Scattergl': create_go_info_item(go.Scattergl),
    'Scattermapbox': create_go_info_item(go.Scattermapbox),
    'Scatterpolar': create_go_info_item(go.Scatterpolar),
    'Scatterpolargl': create_go_info_item(go.Scatterpolargl),
    'Scattersmith': create_go_info_item(go.Scattersmith),
    'Scatterternary': create_go_info_item(go.Scatterternary),
    'Splom': create_go_info_item(go.Splom),
    'Streamtube': create_go_info_item(go.Streamtube),
    'Sunburst': create_go_info_item(go.Sunburst),
    'Surface': create_go_info_item(go.Surface),
    'Table': create_go_info_item(go.Table),
    'Treemap': create_go_info_item(go.Treemap),
    'Violin': create_go_info_item(go.Violin),
    'Volume': create_go_info_item(go.Volume),
    'Waterfall': create_go_info_item(go.Waterfall),
}
