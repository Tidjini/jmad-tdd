# Get a Track with Solos
    * URL: /api/tracks/\<pk\>/
    * HTTP Method: GET

## Example Response

    {
        "name":"All Blues",
        "slug":"all-blues",
        "album":{
            "name": "Kind of Blue",
            "url": "http://jmad.us/api/albums/2/"
        },
        "solos": [
            {
                "artist": "Cannonball Adderley",
                "instrument": "saxophone",
                "start_time": "4:05",
                "end_time": "6:04",
                "slug": "cannonball-adderley",
                "url": "http://jmad.us/api/solos/281/" 
            },
            ...
        ]
    }

# Add a Solo to a Track

    * URL: /api/solos/
    * HTTP Method: POST

## Example Request

    {
        "url": "http://jmad.us/api/solos/25/",
        "artist": "Don Cherry",
        "instrument": "cornet",
        "start_time": "2:05",
        "end_time": "3:14",
        "slug": "don-cherry",
        "track": "http://jmad.us/api/tracks/86/"
    }