# ethereum-blocks

## FastAPI app to call BlockChain API queries  

A simple wrapper on etherscan.io to extract daily block data from Ethereum.

### API
- async calls wrapping etherscan endpoint
- result data is cached.
- datetimes are UTC
- specify api_key instructions in setting_template.json 

usage:
```
% # export PYTHONPATH=.:$PYTHONPATH  # to ensure imports work 
% python ethereum-blocks/main.py

% curl -X 'GET' \
  'http://127.0.0.1:8000/blocks/?start=2021-01-01&end=2021-12-31' \
  -H 'accept: application/json'
```

result:
```
["2021-01-01 11571563","2021-01-02 11578164","2021-01-03 11584640", ... ,"2021-12-30 13909786","2021-12-31 13916165"]                 
```

### Command line
- standard command line: good for testing etc.
- result data is not cached 
- datetimes are UTC
- api_key in variable 

```
ethereum-blocks/cli/getblocks.py
```
Usage:
```
% # export PYTHONPATH=.:$PYTHONPATH  # to ensure imports work 
% getblocks.py [OPTIONS]

  Simple program that prints last block id for date range (inclusive)

Options:
  --start-date TEXT  Start date in YYYY-MM-DD
  --end-date TEXT    End date in YYYY-MM-DD
  --help             Show this message and exit
```
```
% python getblocks.py --start-date=2021-01-01 --end-date=2021-12-31 > blockids.txt
% cat blockids.txt
2021-01-02 11571563
2021-01-03 11578164
2021-01-04 11584640
...
2021-12-30 13909786
2021-12-31 13916165
```

- entire year 2021 is in file
```
blockids-2021.txt
```