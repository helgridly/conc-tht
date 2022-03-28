## Problem description

### Context
In our normal day to day operations, a school nurse or administrator will receive test kits in the mail. They swab the test taker's nose, put the swab in a tube and then scan the barcode of the tube in our application to create the tube model object and set it to a "registered" state. Then they ship the box of tubes off to the lab to be tested.

Once the lab receives the physical shipment, they will call an API to find the tubes in a :"registered" state, and call the API to set the tubes to a "received" state. After processing the tests in their wet lab, they call the API again to set the tube to a "positive", "negative" or "indeterminate" state. 

### Problem description
We would like you to implement an API supporting the above process. 

Specfically, provide a "REST" API that implements the following: 
1. When called with POST, will create a new tube with a unique barcode and return that barcode
2. When called with GET, will return all the tubes in a "registered" state
3. When called with PATCH and provided with a body like:
```json
[
    {"barcode": "1234", "status": "positive"},
    {"barcode": "5678", "status": "negative"}
]
```
...will update the tubes to have the appropriate statuses.

### Extra credit
Here's where you get an opportunity to show us what is important to you as a software engineer. A couple possibilities include:
1. You could add unit tests
2. SQA Testing Notes
3. You could add Authentication / Authorization to the API

### Concepts/data-model
The code (found in `app.py`) has models for `Tube`, and `User`. `Tube` represents a sample taken from a single test taker (`User`). It is associated with a user via a foreign-key relationship. The valid values for `Tube.status` are "registered", "received", "positive", "negative", and "indeterminate". 

## Prerequisites
1. Python3
2. pip

## Usage

1. install dependencies
```bash
python3 -m pip install --no-cache-dir -r requirements.txt
```

2. create the database
In the root directory start a python3 interpreter and run:
```bash
>>> from app import db
>>> db.create_all()
```

3. run the web server
```bash
FLASK_ENV=development flask run
```

Assume the above ran cleanly, then your server should be accessible at `http://127.0.0.1:5000/`