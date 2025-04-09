from fasthtml import FastHTML
from fasthtml.common import H1, Div, serve, RedirectResponse

import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import Employee, Team

# Import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent

# Create a subclass of base_components/Dropdown
# called `ReportDropdown`


class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    # ensuring it has the same parameters as the parent
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    # Overwrite the `component_data` method
    def component_data(self, entity_id, model):
        return model.names()

# Create a subclass of base_components/BaseComponent
# called `Header`


class Header(BaseComponent):

    def build_component(self, entity_id, model):
        return H1(f"{model.name.title()} Performance")

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`


class LineChart(MatplotlibViz):

    def visualization(self, asset_id, model):
        df = model.event_counts(asset_id)
        df = df.fillna(0)
        df = df.set_index("event_date")
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)

        self.set_axis_styling(
            ax, bordercolor="black", fontcolor="black"
        )

        ax.set_title("Cumulative Performance")
        ax.set_xlabel("Day")
        ax.set_ylabel("Events")

        return fig

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, asset_id, model):
        X = model.model_data(asset_id)
        y_proba = self.predictor.predict_proba(X)[:, 1]

        if model.name == "team":
            pred = y_proba.mean()
        else:
            pred = y_proba[0]

        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        return fig

# Create a subclass of combined_components/CombinedComponent
# called `Visualizations`


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")

# Create a subclass of base_components/DataTable
# called `NotesTable`


class NotesTable(DataTable):

    def component_data(self, entity_id, model):
        return model.notes(entity_id)

# Form with radio buttons and dropdown


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]

# Create a subclass of CombinedComponent called `Report`


class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize a FastHTML app and the report
app = FastHTML()
report = Report()

# Root route: shows default employee report


@app.get('/')
def index():
    return report(1, Employee())

# Route to render individual employee report


@app.get('/employee/{id}')
def get_employee(id: str):
    return report(id, Employee())

# Route to render individual team report


@app.get('/team/{id}')
def get_team(id: str):
    return report(id, Team())

# Dynamic dropdown update based on radio selection


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

# Handle form submission and redirect to proper route


@app.post('/update_data')
async def update_data(r):
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

# Launch the FastHTML app
serve()

# Import QueryBase, Employee, Team from employee_events
from employee_events import Employee, Team

# Import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent

# Create a subclass of base_components/Dropdown
# called `ReportDropdown`


class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    # ensuring it has the same parameters as the parent
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    # Overwrite the `component_data` method
    def component_data(self, entity_id, model):
        return model.names()

# Create a subclass of base_components/BaseComponent
# called `Header`


class Header(BaseComponent):

    def build_component(self, entity_id, model):
        return H1(f"{model.name.title()} Performance")

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`


class LineChart(MatplotlibViz):

    def visualization(self, asset_id, model):
        df = model.event_counts(asset_id)
        df = df.fillna(0)
        df = df.set_index("event_date")
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)

        self.set_axis_styling(
            ax, bordercolor="black", fontcolor="black"
        )

        ax.set_title("Cumulative Performance")
        ax.set_xlabel("Day")
        ax.set_ylabel("Events")

        return fig

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, asset_id, model):
        X = model.model_data(asset_id)
        y_proba = self.predictor.predict_proba(X)[:, 1]

        if model.name == "team":
            pred = y_proba.mean()
        else:
            pred = y_proba[0]

        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        return fig

# Create a subclass of combined_components/CombinedComponent
# called `Visualizations`


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")

# Create a subclass of base_components/DataTable
# called `NotesTable`


class NotesTable(DataTable):

    def component_data(self, entity_id, model):
        return model.notes(entity_id)

# Form with radio buttons and dropdown


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]

# Create a subclass of CombinedComponent called `Report`


class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize a FastHTML app and the report
app = FastHTML()
report = Report()

# Root route: shows default employee report


@app.get('/')
def index():
    return report(1, Employee())

# Route to render individual employee report


@app.get('/employee/{id}')
def get_employee(id: str):
    return report(id, Employee())

# Route to render individual team report


@app.get('/team/{id}')
def get_team(id: str):
    return report(id, Team())

# Dynamic dropdown update based on radio selection


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

# Handle form submission and redirect to proper route


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

# Launch the FastHTML app
serve()
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import Employee, Team

# Import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
)

from combined_components import FormGroup, CombinedComponent

# Create a subclass of base_components/Dropdown
# called `ReportDropdown`


class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    # ensuring it has the same parameters as the parent
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    # Overwrite the `component_data` method
    def component_data(self, entity_id, model):
        return model.names()

# Create a subclass of base_components/BaseComponent
# called `Header`


class Header(BaseComponent):

    def build_component(self, entity_id, model):
        return H1(f"{model.name.title()} Performance")

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`


class LineChart(MatplotlibViz):

    def visualization(self, asset_id, model):
        df = model.event_counts(asset_id)
        df = df.fillna(0)
        df = df.set_index("event_date")
        df = df.sort_index()
        df = df.cumsum()
        df.columns = ["Positive", "Negative"]

        fig, ax = plt.subplots()
        df.plot(ax=ax)

        self.set_axis_styling(
            ax, bordercolor="black", fontcolor="black"
        )

        ax.set_title("Cumulative Performance")
        ax.set_xlabel("Day")
        ax.set_ylabel("Events")

        return fig

# Create a subclass of base_components/MatplotlibViz
# called `BarChart`


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, asset_id, model):
        X = model.model_data(asset_id)
        y_proba = self.predictor.predict_proba(X)[:, 1]

        if model.name == "team":
            pred = y_proba.mean()
        else:
            pred = y_proba[0]

        fig, ax = plt.subplots()
        ax.barh([""], [pred])
        ax.set_xlim(0, 1)
        ax.set_title("Predicted Recruitment Risk", fontsize=20)

        self.set_axis_styling(ax, bordercolor="black", fontcolor="black")

        return fig

# Create a subclass of combined_components/CombinedComponent
# called `Visualizations`


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls="grid")

# Create a subclass of base_components/DataTable
# called `NotesTable`


class NotesTable(DataTable):

    def component_data(self, entity_id, model):
        return model.notes(entity_id)

# Form with radio buttons and dropdown


class DashboardFilters(FormGroup):
    id = "top-filters"
    action = "/update_data"
    method = "POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(
            id="selector",
            name="user-selection"
        )
    ]

# Create a subclass of CombinedComponent called `Report`


class Report(CombinedComponent):
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]


# Initialize a FastHTML app and the report
app = FastHTML()
report = Report()

# Root route: shows default employee report


@app.get('/')
def index():
    return report(1, Employee())

# Route to render individual employee report


@app.get('/employee/{id}')
def get_employee(id: str):
    return report(id, Employee())

# Route to render individual team report


@app.get('/team/{id}')
def get_team(id: str):
    return report(id, Team())

# Dynamic dropdown update based on radio selection


@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())

# Handle form submission and redirect to proper route


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

# Launch the FastHTML app
serve()
