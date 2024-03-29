# research_project


## TODO

1. update makefile to use venv instead of conda (use a single py311 condaenv or smth like that)
2. use the configurator from nano-gpt

## Installation

Find and replace `research_project` with the name of your module. Rename the folder `research_project` as well. Do not use any dashes. Then delete this line.

```
make install
```

## Usage

Use json to modify the config:
```
research_project --conf '{"block_size": 10}'
```

Reuse an old config file by specifying the path:
```
research_project --config $PWD/runs/<YYYY-MM-DD>---<HH-MM-SS>/config.json
```
