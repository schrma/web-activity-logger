from dash.dependencies import Input, Output


def create_callbacks(app, activity_class):
    @app.callback(Output("item-graph", "figure"), [Input("item-graph", "relayout_data")])
    def update_graph(relayout_data):  # pylint: disable='unused-argument'
        # Fetch data from the Flask-SQLAlchemy database (Item model)
        items = activity_class.query.all()

        # Create a graph or chart using the data
        # Example: Bar chart of item names and their counts
        item_names = [item.my_activity.activity_type for item in items]
        item_counts = [item.value for item in items]

        figure = {
            "data": [
                {"x": item_names, "y": item_counts, "type": "bar", "name": "Items"},
            ],
            "layout": {
                "title": "Item Counts",
            },
        }

        return figure
