# TTA deep dive
> Collection of analyses related to through the ages tournament data.

## Reports
**[Player order investigation](./notebooks/player_order_investigation.ipynb)** - Perform a statistical analysis, using both an analytical approximation and a Monte Carlo method, to determine if there is evidence of non-random player seating.
**[Starting position analysis](./notebooks/starting_position_analysis.ipynb)** - Perform a statistical analysis to determine if seating is likely to impact the outcome of a three player game. We perform a logistic regression on the outcome of a game, taking into account estimated player skill.

## fetch
Local module used for ergonomically fetching data. Leverages a yaml file for human-readable documentation of the data source. Thanks to [cwbishop](https://github.com/cwbishop) for introducing the idea of leveraging polymorphism to standardize data reading and writing.

Also can return transformed data as defined in the `views.yaml` file, where the input dataframes are passed in as a dictionary of pandas dataframes into a python script returning a transformed dataframe. This allows the dataframe construction to be centralized.

### Example use
```python
import fetch

# Return a dataframe from a data source.
data_source = fetch.data_source(node="game_results_with_seating")

df = data_source.as_pandas()

# Return a transformed dataframe following the logic defined in
# ./views/game_results_by_player.py
view = fetch.view(node="game_results_by_player")

transformed_df = view.as_pandas()
```
