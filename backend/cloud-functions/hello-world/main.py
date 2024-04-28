import flask


def hello_world(request: flask.Request) -> flask.Response:
    """HTTP Cloud Function.

    Returns:
    - "Hello World! 👋"
    """
    response = "Hello World! 👋"

    return flask.Response(response, mimetype="text/plain")