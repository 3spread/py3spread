# Exceptions

All exceptions subclass `ThreeSpreadError`. See the
[errors guide](../guides/errors.md) for the status-to-class mapping and
retry behavior.

::: py3spread.exceptions
    options:
      members:
        - ThreeSpreadError
        - APIConnectionError
        - APIError
        - AuthenticationError
        - RateLimitError
        - BadRequestError
        - MissingParameterError
        - WindowTooWideError
        - NotFoundError
        - ValidationError
        - ServerError
        - ServiceUnavailableError
