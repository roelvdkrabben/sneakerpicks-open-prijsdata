# SneakerPicks open sneaker price data (Netherlands)

Daily lowest prices and the 30-day normal price for popular sneaker models across Dutch web shops, collected by [SneakerPicks.nl](https://sneakerpicks.nl/data). Free to use under [CC BY 4.0](LICENSE). Attribution: **"Source: SneakerPicks.nl"** with a link to https://sneakerpicks.nl/data.

SneakerPicks launched in October 2026, so the history is short. A GitHub Action fetches the live data every day and appends it to [`data/prices.csv`](data/prices.csv), so this file grows into a full history.

*Nederlands: zie [onderaan](#nederlands).*

## Files

| File | What |
|---|---|
| [`data/prices.csv`](data/prices.csv) | One row per model per day. Grows daily. |
| [`scripts/update.py`](scripts/update.py) | Fetches the live per-model JSON from sneakerpicks.nl and merges it into the CSV. No dependencies. |
| [`.github/workflows/update.yml`](.github/workflows/update.yml) | Runs the script daily at 06:30 UTC. |

Live JSON and CSV per model (last 90 days, CORS enabled, no key): https://sneakerpicks.nl/data, for example https://sneakerpicks.nl/data/adidas/campus.json.

## Columns

| Column | Meaning |
|---|---|
| `date` | Day (Europe/Amsterdam), ISO format. |
| `brand_slug`, `model_slug` | Identifiers as used in the sneakerpicks.nl URLs. |
| `brand`, `model` | Display names. |
| `lowest_price_eur` | Lowest price seen that day across all colourways and web shops, in EUR incl. VAT, excluding shipping. Adult sizes only. |
| `normal_price_30d_eur` | Normal price: the median of the daily lowest prices over the previous 30 days (up to and including that day). Empty when fewer than 7 days of data are available. |
| `shops` | Number of web shops with a price for this model that day. |
| `model_url` | Model page on sneakerpicks.nl. |

## Coverage and caveats

- Prices come from affiliate product feeds of Dutch web shops, refreshed hourly to every four hours. Method: https://sneakerpicks.nl/methodologie.
- History restarted on 2026-10-16 after a feed outage from 9 July to 15 October 2026. Data from 1 to 8 July 2026 is included as an earlier period.
- Kids' sizes are excluded where recognisable; a daily price below 60% of the current lowest price is treated as a kids' size and ignored.
- The model list follows the popular models on https://sneakerpicks.nl/data and may change over time.

## Cite

See [`CITATION.cff`](CITATION.cff). Suggested: *SneakerPicks.nl (2026). SneakerPicks open sneaker price data (Netherlands). CC BY 4.0. https://github.com/roelvdkrabben/sneakerpicks-open-prijsdata*

## Nederlands

Dagelijkse laagste prijs en de normale prijs (30 dagen) van populaire sneakermodellen bij Nederlandse webshops, verzameld door [SneakerPicks.nl](https://sneakerpicks.nl/data). Vrij te gebruiken onder CC BY 4.0, met bronvermelding **"Bron: SneakerPicks.nl"** en een link naar https://sneakerpicks.nl/data.

We zijn in oktober 2026 begonnen, dus de historie is nog kort. Elke dag haalt een GitHub Action de live data op en voegt die toe aan `data/prices.csv`. Vragen of meer data nodig voor onderzoek? https://sneakerpicks.nl/contact

Built by Roel van der Krabben ([Taigers.ai](https://taigers.ai)), founder of SneakerPicks.nl.
