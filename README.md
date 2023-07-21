# SerWO-Lite

Lightweight Serverless Workflow Orchestrator (Experimental)

## Setup Python Virtual Environment

`python3 -m venv ./` (creates python virtual environment on the root directory)

## Installation Instructions

`pip3 -r install requirements.txt`

## Run XFaaS Lite Server

### Get into the orchestrator directory

`cd orchestrator/`

### Run the server

`python3 manage.py runserver` (This starts an instance of XFaaS Lite on your local machine on `127.0.0.1`)

### API details for execution (Use Postman to send a request)

`Url  - http://127.0.0.1:8000/api/v1/xfaaslite/execute`
`Type - POST request`
`Payload type - JSON`

```json
{
 "path": "/Users/tuhinkhare/Work/IISc/DREAM-Lab/serwo-project/serwo-lite/SerWO-Lite/orchestrator/examples/sample2/dag-description.json",
 "input_num": 1
}
```
