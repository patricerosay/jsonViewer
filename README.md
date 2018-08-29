# jsonviewer

## A better way to present your json file
This script creates a tree and presents it in an a D3 HTML so you can drill down into it 
and view the first item and the last one at the same time 
plus, you can comment your nodes and subnodes 
### Example:
```
"GlossDiv": {
			"//comments":"this is a comment in a sub node",
```
![screenshot](./sample/screenshot.png)
### Execution command
```
python3 ./jsonViewer.py -i yourfile.json -o destinationFile.html -t "the title"  
```

## Installation
Download the projet
change directory to jsonViewer
Install the package by typing 
```
pip install .
```

