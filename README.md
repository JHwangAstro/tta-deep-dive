# TTA deep dive
> Collection of analyses related to through the ages tournament data.

## Reports
**[Player order investigation](player_order_investigation.ipynb)** - Perform a statistical analysis, using both an analytical approximation and a Monte Carlo method, to determine if there is evidence of non-random player seating.

## fetch
Local module used for ergonomically fetching data. Leverages a yaml file for human-readable documentation of the data source. Thanks to [cwbishop](https://github.com/cwbishop) for introducing the idea of leveraging polymorphism to standardize data reading and writing.

Also can return transformed data as defined in the `views.yaml` file, where the input dataframes are passed in as a dictionary of pandas dataframes into a python script returning a transformed dataframe. This allows the dataframe construction to be centralized.

### Example use
```python
import fetch

# Return a dataframe from a data source.
data_source = fetch.data_source(node="game_results_with_seating")

df = data_source.as_pandas()

# Return a transformed dataframe.
view = fetch.view(node="game_results_by_player")

transformed_df = view.as_pandas()
```
