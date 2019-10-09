Implementation of geocode lookup proxy HTTP service.

# Server operation

The server expects the existance of a Python 3 environment.

The server delegates the geocode requests to the [Google Maps API](https://developers.google.com/maps/documentation/geocoding/start).
It also uses the [HERE API](https://developer.here.com/documentation/geocoder/topics/quick-start.html) as a backup, should the first service fail to produce any results.

---

**IMPORTANT**

In order to operate correctly, you need to fill in the `provider_config.json` file
and specify a valid Google Platform API key as well as a valid HERE app id and app code

---

To start the server run:

```
python3 server.py
```

Note that all the server logging is directed towards standard output, for simplicity.

# HTTP API

The server provides a single method which returns a JSON response

```
GET /geo_lookup.json?address="Civic Center, San Francisco"
```

The address parameter must be a non-empty address line.

The service returns as a result an object echoing the provided query and a list
of results:

```
{
    query: 'Civic Center, San Francisco',
    results: [...]
}
```

The array of results can contain 0, 1 or more results depending on whether the
address could not be located, it could be located unambiguously or the address could
not be resolved to single certain location.

The results are records which contain the latitude and longitude numeric coordinates for the location as well as a `formatted_address` field that returns a complete address
line to disambiguate the query.

E.g. for the following request made with curl:

```
curl -G -X GET -v localhost:8000/geo_lookup.json --data-urlencode "address=Civic Center, San Francisco"
```

we would get this response:

```
{
  "query": "Civic Center, San Francisco",
  "results": [
    {
      "latitude": 37.7815533,
      "longitude": -122.4156427,
      "formatted_address": "Civic Center, San Francisco, CA 94102, USA"
    }
  ]
}
```

Note that subsequent requests made with for the same address query may return different
results, for example if a different provider ends up handling the query. For example,
if the HERE provider is used for the same request, we get the following:

```
{
  "query": "Civic Center, San Francisco",
  "results": [
    {
      "latitude": 37.77863,
      "longitude": -122.41683,
      "formatted_address": "Civic Center, San Francisco, CA, United States"
    }
  ]
}
```

# Unit tests

To run the unit tests, execute:

```
python3 -m unittest
```

# Codebase rundown

Here is a short description for the modules in the implementation:

- server: entry point to the app, implements the server plumbing

- geocode_service: the business logic implementation for the geocode lookup request

- geocode: data models for geocode providers

- fallback_provider: implementation for the geocode provider fallback logic

- logging_provider: add logging capabilities to geocode provider for observability

- google_maps_provider: an implementation for the geocode provider based on the Google Maps API

- here_provider: an implementation for the geocode provider based on the HERE API

- http_client: utility to simply perform HTTP GET requests

- http_service: simplified data models to implement HTTP services
