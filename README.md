# Canvas-To-Todoist

## About 

A Python app to export Canvas assignments to projects in Todoist.

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
#### Heroku recently canceled it's free Dynos so application may be down. Applying for student credits as soon as possible
See : https://canvas2todoist.herokuapp.com 
## Run Locally <a name = "Run Locally"></a>

Clone the repo

Install the required modules
```
pip3 install -r requirements.txt
```
```
export FLASK_APP=server.py
flask run
```

