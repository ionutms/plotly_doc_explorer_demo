# Plotly Documentation Explorer

## Overview

The Plotly Documentation Explorer is an interactive web application designed for visualizing and exploring the structure of Plotly graph objects. It offers a powerful and user-friendly interface for understanding the hierarchical nature of Plotly's graph objects, allowing users to navigate through different levels of the object structure and access corresponding documentation.

This tool is particularly useful for developers and data scientists working with Plotly, enabling efficient exploration of the extensive Plotly graph object library and its associated properties.

## Live Demo

You can try out the Plotly Documentation Explorer without any installation here:

**[https://plotly-doc-explorer-demo.onrender.com](https://plotly-doc-explorer-demo.onrender.com)**

Feel free to explore the features and functionality of the application directly in your web browser.

## Features

- Interactive treemap visualization of Plotly graph objects
- Dynamic filtering of treemap levels using range sliders
- Sorting option for treemap items
- Theme switching between light and dark modes
- Clickable treemap nodes that display corresponding documentation in an iframe
- Responsive layout adapting to various screen sizes
- Integration with official Plotly documentation for instant access to detailed information

## Installation

### Prerequisites

- Python 3.11 or higher
- pipenv

### Setting up the environment

1. Clone the repository:
   ```
   git clone https://github.com/ionutms/plotly_doc_explorer_demo.git
   cd plotly_doc_explorer_demo
   ```

2. Create a virtual environment and install dependencies using pipenv:
   ```
   pipenv install
   ```

3. Activate the virtual environment:
   ```
   pipenv shell
   ```

4. Run the application:
   ```
   python app.py
   ```

The application should now be running on `http://localhost:8050` (or another port if specified).
## Usage

1. Select a Plotly graph object type from the radio button options at the top of the page.
2. Use the range sliders to filter the levels of the treemap visualization:
   - Level 1 items: Filter the top-level properties
   - Level 2 items: Filter the second-level properties
   - Level 3 items: Filter the third-level properties
3. Toggle the "Sort graph items" switch to change the ordering of items in the treemap.
4. Click on any node in the treemap to view its corresponding documentation in the iframe on the right.
5. Use the theme switch in the top right corner to toggle between light and dark modes.

## Components

The Plotly Documentation Explorer consists of several key components:

- Radio buttons for selecting the main Plotly graph object type
- Range sliders for filtering treemap levels
- Interactive treemap visualization
- Documentation iframe for displaying selected item details
- Theme switch for toggling between light and dark modes

## Screenshots

Here are some key screenshots of the Plotly Documentation Explorer in action:

1. Main Interface

<img src="/docs/images/main-interface-800x600.png" alt="Plotly Documentation Explorer main interface" width="100%" max-width="800px">

*The main interface of the Plotly Documentation Explorer, showing the treemap visualization and control panels.*

2. Documentation View

<img src="/docs/images/documentation-view-800x600.png" alt="Documentation view for selected item" width="100%" max-width="800px">

*An example of the documentation view when a specific item is selected in the treemap.*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses the [Plotly](https://plotly.com/) library for graph object visualization and documentation.
- Built with [Dash](https://dash.plotly.com/), a productive Python framework for building analytical web applications.
