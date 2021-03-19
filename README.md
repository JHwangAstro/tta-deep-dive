# TTA deep dive
> Collection of analyses related to through the ages tournament data.

## Reports
**[Player order investigation](player_order_investigation.ipynb)** - Perform a statistical analysis, using both an analytical approximation and a Monte Carlo method, to determine if there is evidence of non-random player seating.

## fetch
Local module used for ergonomically fetching data. Leverages a yaml file for human-readable documentation of the data source. Thanks to cwbishop [github](https://github.com/cwbishop) for introducing the idea of leveraging polymorphism to standardize data reading and writing.

### Example use
```python
import fetch

data_source = fetch.data_source(node="game_results")

df = data_source.as_pandas()
```
