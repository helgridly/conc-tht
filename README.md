

## Notes


### Off-spec changes

* Moved service endpoints to `/tubes`, Swagger is at `/`
    * Serving endpoints out of `/` and moving Swagger elsewhere upsets flask-restx, see [here](https://github.com/noirbizarre/flask-restplus/issues/712)
* Renamed `User` to `Patient` because User makes me think of logins.
* Move `README.md` -> `SPEC.md` so this doc shows up on GitHub first :)
