# Canvas To Todoist

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)

## About <a name = "about"></a>

A Python script to export Canvas assignments to projects in Todoist.

## Getting Started <a name = "getting_started"></a>
### Prerequisites

Generate a Canvas API key
```
1. Log into your institutions canvas portal
2. Navigate to Account->Settings
3. Scroll down to Approved Integrates and
generate a new access token.
```

Get your Todoist API key
```
1. Log into your todoist account at https://todoist.com/
2. Go to Settings->Integrations
3. Copy your API key located at the bottom.
```

### Installing

Clone the repo with
```
git clone https://github.com/ZachJBurns/CanvasToTodoist
```

Install the required modules
```
pip3 install -r requirements.txt
```

## Usage <a name = "usage"></a>

Import the classes you would like to track by running
```
python3 import_classes.py
```
You will be asked to enter your api keys and the courses you want to track

Import the assignments to Todoist by running
```
python3 import_tasks.py
```

At any point if you want to reset what courses are having assignments tracked you can run
```
python3 import_classes.py -r
```
