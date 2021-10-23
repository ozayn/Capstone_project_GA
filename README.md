# Capstone_project_GA



### Datasets

- [Offshore Leaks](https://offshoreleaks-data.icij.org/offshoreleaks/csv/csv_panama_papers.2018-02-14.zip#_ga=2.95739225.475560190.1633554447-1739250866.1633374289)

- [Kaggle Data](https://www.kaggle.com/zusmani/paradisepanamapapers)

- [provided datasets](https://offshoreleaks.icij.org/pages/database)

- [Pandora Papers](https://www.icij.org/investigations/pandora-papers/about-pandora-papers-leak-dataset/)


### Data Structure



![dataframe](./presentation/images/dataframes/dataframes.png)



|                    |   # rows |   # columns |
|:-------------------|---------:|------------:|
| Nodes Intermediary |     9526 |           8 |
| Nodes Address      |    57600 |           8 |
| Nodes Entity       |   105516 |          17 |
| Nodes Officer      |   107190 |           7 |
| Edges              |   561393 |           8 |


### Null Values for edges


| edges      | Null Percentage   |
|:-----------|:------------------|
| end_date   | 94%               |
| start_date | 58%               |
| link       | 0%                |
| TYPE       | 0%                |
| END_ID     | 0%                |
| START_ID   | 0%                |


### Null Values for nodes

| nodes                    | Null Percentage   |
|:-------------------------|:------------------|
| state                    | 98%               |
| address                  | 79%               |
| ibcRUC                   | 66%               |
| incorporation_date       | 65%               |
| status                   | 65%               |
| company_type             | 63%               |
| service_provider         | 62%               |
| jurisdiction_description | 62%               |
| jurisdiction             | 62%               |
| longitude                | 37%               |
| latitude                 | 37%               |
| name                     | 20%               |
| country_codes            | 0%                |
| continents               | 0%                |
| countries                | 0%                |
| table                    | 0%                |
| node_id                  | 0%                |






![Country Addresses](./presentation/images/top_25_countries__address__intermediary__officer__entity.png)