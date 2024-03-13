# research_project

## Installation

Find and replace `research_project` with the name of your module. Rename the folder `research_project` as well. Do not use any dashes. Then delete this line.

```
make install
```

## Usage

Put a json config:
```
research_project --conf '{"block_size": 10}'
```

Reuse an old config file by specifying the path:
```
research_project --config $PWD/runs/<YYYY-MM-DD>---<HH-MM-SS>/config.json
```
