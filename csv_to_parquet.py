import pandas, sys

pandas.read_csv(sys.argv[1]).to_parquet(sys.argv[1].replace('.csv', '.parquet'))
