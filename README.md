# Running

Swagger is served at `/`. (This is my extra credit 🙂)

## Gitpod

Will drop you into a VSCode browser and start the app for you. Just click the link:

https://gitpod.io/#https://github.com/helgridly/conc-tht

VSCode will give a toast notification in the bottom-right corner saying a service is available on port 5000. Hit "Open Browser" and it'll pop open another tab with Swagger in it.

## Locally

```
python -m virtualenv venv
source venv/bin/activate
pip install --no-cache-dir -r requirements.txt
python -c "from app import db, create_app; db.create_all(app=create_app())"
FLASK_ENV development flask run
```

## Testing

```
pytest
```

# Notes and assumptions

* Since the `Tube` has a FK relationship to a user, the POST to register a new tube needs to take a user email.

## Off-spec changes

* Moved service endpoints to `/tubes`, Swagger is at `/`
    * Serving endpoints out of `/` and moving Swagger elsewhere upsets flask-restx, see [here](https://github.com/noirbizarre/flask-restplus/issues/712).
* Renamed `User` to `Patient` because User makes me think of logins.
* Move `README.md` -> `SPEC.md` so this doc shows up on GitHub first :)

## Extra credit

Tests are at `pytest`.

Swagger integration with [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/). This also gives some nice perks like validating user inputs.

## Things I didn't do

### DB-level testing

Just a time thing. Could have tested that e.g. creating new patients from email works correctly.

### Authn/z

[Flask-HTTPAuth](https://flask-httpauth.readthedocs.io/en/latest/index.html) would be simple to integrate, but real-world applications typically need something like role-based access control and something better than basic auth.

A sketch might look something like:

* Patients can query for their own samples.
* The test operator can create new samples with `POST /tubes`.
* The lab can `GET` and `PATCH /tubes`.

### Creating the same user twice at once

Two requests to create the same user at the same time will result in one of them failing the unique constraint on the email address. This will bubble up to the user as a 500. Having `Patient.get_or_create` catch that error and retry once would be a better experience.
