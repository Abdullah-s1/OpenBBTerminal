```
usage: attrib [-p TIME PERIOD [TIME PERIOD ...]] [-t] [-r] [-h]
```

Display attributions of sector performance in terms of the S&P 500 benchmark (SPY), and the user's portfolio. Graph visualisation and tabular values available.

Default output is the graph visualisation of relative sector attribution, which gives attribution as a percentage. 

```
optional arguments:
  -p TIME PERIOD [TIME PERIOD ...]
                        Set the time period for the portfolio. (default: all)
  -t, --type            Allows user to choose between relative or absolute. Relative gives as percentage and absolute gives raw values. (default: relative)
  -r, --raw             Allows user to also display tabular format of data (default: False)
  -h, --help            Show this help message (default: False)
```
Example:
```
Filtering to a specific time period is executed via the -p argument.
2022 Nov 03, 23:37 (🦋) /portfolio/ $ attrib -p 3m
<img width="853" alt="Screen Shot 2022-11-04 at 14 38 20" src="https://user-images.githubusercontent.com/74476622/199880234-75e09a47-e44a-486a-a668-14f69e23aeb3.png">

If I would call attrib (or attrib --type relative) I would get the graph of the relative performance and nothing else.
2022 Nov 03, 23:31 (🦋) /portfolio/ $ attrib
<img width="774" alt="Screen Shot 2022-11-04 at 14 32 10" src="https://user-images.githubusercontent.com/74476622/199879420-386bc9a9-8087-429f-b142-3e11f4dd8844.png">

If I would call attrib --type absolute I would get the graph of the absolute performance and nothing else.
2022 Nov 03, 23:32 (🦋) /portfolio/ $ attrib --type absolute
<img width="777" alt="Screen Shot 2022-11-04 at 14 32 48" src="https://user-images.githubusercontent.com/74476622/199879501-8dcdb3ff-8399-48e1-ad2c-66a44b4a99b4.png">

If I would call attrib --raw I would get the graph of the relative performance (see above at attrib command for visual) and the table of relative performance.
2022 Nov 03, 23:32 (🦋) /portfolio/ $ attrib --raw

     Contributions as % of PF: Portfolio vs. Benchmark Attribution Categorisation all      
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃            ┃            ┃            ┃            ┃            ┃ Attributi… ┃           ┃
┃            ┃            ┃ Portfolio  ┃ Excess     ┃ Attributi… ┃ Direction  ┃ Attribut… ┃
┃            ┃ S&P500 [%] ┃ [%]        ┃ Attributi… ┃ Ratio      ┃ [+/-]      ┃ Sensitiv… ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ S&P 500    │ 12.86      │ 34.83      │ 21.97      │ 2.71       │ Correlated │ High      │
│ Consumer   │            │            │            │            │ (+)        │           │
│ Discretio… │            │            │            │            │            │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 5.59       │ 0.00       │ -5.59      │ 0.00       │ Correlated │ Low       │
│ Consumer   │            │            │            │            │ (+)        │           │
│ Staples    │            │            │            │            │            │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 2.94       │ 0.00       │ -2.94      │ 0.00       │ Correlated │ Low       │
│ Energy     │            │            │            │            │ (+)        │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 11.66      │ 0.00       │ -11.66     │ 0.00       │ Correlated │ Low       │
│ Financials │            │            │            │            │ (+)        │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 17.30      │ 5.04       │ -12.26     │ 0.29       │ Correlated │ Low       │
│ Health     │            │            │            │            │ (+)        │           │
│ Care       │            │            │            │            │            │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 7.29       │ 0.00       │ -7.29      │ 0.00       │ Correlated │ Low       │
│ Industria… │            │            │            │            │ (+)        │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 33.69      │ 58.56      │ 24.86      │ 1.74       │ Correlated │ High      │
│ Informati… │            │            │            │            │ (+)        │           │
│ Technology │            │            │            │            │            │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 1.71       │ 0.00       │ -1.71      │ 0.00       │ Correlated │ Low       │
│ Materials  │            │            │            │            │ (+)        │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 1.93       │ 0.00       │ -1.93      │ 0.00       │ Correlated │ Low       │
│ Real       │            │            │            │            │ (+)        │           │
│ Estate     │            │            │            │            │            │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 3.34       │ 1.57       │ -1.77      │ 0.47       │ Correlated │ Low       │
│ Telecommu… │            │            │            │            │ (+)        │           │
│ Services   │            │            │            │            │            │           │
│ (Sector)   │            │            │            │            │            │           │
├────────────┼────────────┼────────────┼────────────┼────────────┼────────────┼───────────┤
│ S&P 500    │ 1.68       │ 0.00       │ -1.68      │ 0.00       │ Correlated │ Low       │
│ Utilities  │            │            │            │            │ (+)        │           │
│ (Sector)   │            │            │            │            │            │           │
└────────────┴────────────┴────────────┴────────────┴────────────┴────────────┴───────────┘

If I would call attrib --type absolute --raw I would get the graph of the absolute performance (see above at attrib --type absolute for visual) and the table of absolute performance.
2022 Nov 03, 23:33 (🦋) /portfolio/ $ attrib --type absolute --raw

Raw contributions (Return x PF Weight): Portfolio vs. Benchmark Attribution Categorisation all
┏━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃             ┃        ┃           ┃             ┃             ┃ Attribution ┃            ┃
┃             ┃        ┃           ┃ Excess      ┃ Attribution ┃ Direction   ┃ Attributi… ┃
┃             ┃ S&P500 ┃ Portfolio ┃ Attribution ┃ Ratio       ┃ [+/-]       ┃ Sensitivi… ┃
┡━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ S&P 500     │ 0.18   │ 1.05      │ 0.87        │ 5.80        │ Correlated  │ High       │
│ Consumer    │        │           │             │             │ (+)         │            │
│ Discretion… │        │           │             │             │             │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.08   │ 0.00      │ -0.08       │ 0.00        │ Correlated  │ Low        │
│ Consumer    │        │           │             │             │ (+)         │            │
│ Staples     │        │           │             │             │             │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.04   │ 0.00      │ -0.04       │ 0.00        │ Correlated  │ Low        │
│ Energy      │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.16   │ 0.00      │ -0.16       │ 0.00        │ Correlated  │ Low        │
│ Financials  │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.24   │ 0.15      │ -0.09       │ 0.62        │ Correlated  │ Low        │
│ Health Care │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.10   │ 0.00      │ -0.10       │ 0.00        │ Correlated  │ Low        │
│ Industrials │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.48   │ 1.77      │ 1.29        │ 3.72        │ Correlated  │ High       │
│ Information │        │           │             │             │ (+)         │            │
│ Technology  │        │           │             │             │             │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.02   │ 0.00      │ -0.02       │ 0.00        │ Correlated  │ Low        │
│ Materials   │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.03   │ 0.00      │ -0.03       │ 0.00        │ Correlated  │ Low        │
│ Real Estate │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.05   │ 0.05      │ 0.00        │ 1.01        │ Correlated  │ Normal     │
│ Telecommun… │        │           │             │             │ (+)         │            │
│ Services    │        │           │             │             │             │            │
│ (Sector)    │        │           │             │             │             │            │
├─────────────┼────────┼───────────┼─────────────┼─────────────┼─────────────┼────────────┤
│ S&P 500     │ 0.02   │ 0.00      │ -0.02       │ 0.00        │ Correlated  │ Low        │
│ Utilities   │        │           │             │             │ (+)         │            │
│ (Sector)    │        │           │             │             │             │            │
└─────────────┴────────┴───────────┴─────────────┴─────────────┴─────────────┴────────────┘
