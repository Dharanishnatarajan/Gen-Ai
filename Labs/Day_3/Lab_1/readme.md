# Day 3 Lab 1: LangGraph ETL Notebook

This lab packages a LangGraph ETL notebook around a compact e-commerce dataset. The workflow reads raw CSV files from `Datasets/`, applies cleanup and quality checks, and writes cleaned outputs plus metrics into `data/clean/`.

## Included assets

- `langgraph_etl_pipeline.ipynb`: notebook-based ETL workflow
- `Datasets/`: source CSV files for users, products, and transactions
- `data/clean/`: generated clean outputs and quality artifacts

## What changed in this repo

- The lab is reorganized under `Labs/Day_3/Lab_1`.
- The documentation is simplified to match the rest of this repository.
- The imported notebook and data remain intact so you can run the workflow locally.

## Run it

1. Install the required packages:

```bash
pip install langgraph pandas pyarrow
```

2. Open the notebook:

```bash
jupyter notebook Labs/Day_3/Lab_1/langgraph_etl_pipeline.ipynb
```

3. Run the notebook cells from top to bottom and inspect the outputs in `data/clean/`.
