# kiosk-server
[Falcon](https://falconframework.org/) based url list supplier. Doesn't really do anything yet.

##### Quickstart 
`docker run -p 80:80 dutchsecniels/kiosk-server:latest`

## Description
Hacky, barebones API to collect and return lists of websites (pages) stored in so called 'channels'.

Run the server, then talk json to it through whatever you like.

## Does not come with
Batteries excluded!
- Input validation
- Error handling
- Much more!

## Storage
Channels cannot be stored at the moment. Considering leaving this client side ('backup to file'?)

# API overview

## Overview

| Path        | Method | Keywords           | Description                        | Codes         |
| ---         | ---    | ---                | ---                                | ---           |
| `/`         | GET    | *None*             | Returns 200 if server is running   | 200           |
| `/channels` | GET    | *None*             | Return all channels                | 200           |
| `/channel`  | GET    | `channel`          | Return pages for *channel*         | 200, 400, 404 |
| `/channel`  | POST   | `channel`, `pages` | Create or update *channel* *pages* | 200, 400      |
| `/channel`  | DELETE | `channel`          | Delete *channel*                   | 200, 400, 404 |


## /
Can be used to test if the server is alive, without touching anything channels related.

#### Returns
Returns a json `{dict}` with keyword `Kiosk-server`.
```json
{
  "Kiosk-server": "https://github.com/nielsds/kiosk-server"
}
```

## /channels
Can be used to retreive a json `{dict}` of all available channels and their contents.  
The default setup stores pages as `[lists]`.

#### Returns
Returns a json `{dict}` with keyword `channels`.
```json
{
  'channels': 
    {
      '_standby': 
        [
          'https://dutchsec.com'
        ]
    }
}
```
or when empty:
```json
{}
```

## /channel
Can be used to create, change or delete channels.

### GET
Expects `channel` keyword. Must be an existing channel name. Returns channel pages.

#### Returns
```json
{'channel': ['https://dutchsec.com']}
```

### POST
Expects `channel` and `pages` keywords.
Using an existing channels name will overwrite the existing channels data.
Returns contents of the channel.

#### Returns
```json
{'channel': ['https://dutchsec.com', 'https://github.com']}
```
> The server does (currently) not care what kind of data it receives in pages. The `[list]` structure is advised for clients.

### Delete
Expects `channel` keyword. Must be an existing channel name. Deletes channel.

#### Returns
```json
{'channel': 'Succesfully deleted channel "_standby"'}
```

# Run it

## rebuild.py
You can use the supplied `rebuild.py` script to delete old builds, build a new container and start the new container all at once. By default, the script is set to run the container with `-p 80:80`.

```
python3 rebuild.py 
```

## Build it yourself
```
docker build -t kiosk-server .
```

## Docker hub
```
docker run -p 80:80 dutchsecniels/kiosk-server:latest
```

# Usage examples

## Python requests

```python3
# Import requests
>>> import requests
# Get request on server root
>>> r = requests.get('http://localhost/', json={})
>>> r.status_code
200
>>> r.json()
{'Kiosk-server': 'https://github.com/nielsds/kiosk-server'}
# Get a list of all channels
>>> r = requests.get('http://localhost/channels', json={})
>>> r.json()
{'channels': {'_standby': ['https://dutchsec.com']}}
# Get pages for channel '_standby'
>>> r = requests.get('http://localhost/channel', json={'channel':'_standby'})
>>> r.json()
{'channel': ['https://dutchsec.com']}
# Post new channel
>>> r = requests.post('http://localhost/channel', json={'channel':'test', 'pages':['https://github.com', 'https://dutchsec.com']})
>>> r.json()
{'channel': ['https://github.com', 'https://dutchsec.com']}
>>> r = requests.get('http://localhost/channels', json={})
>>> r.json()
{'channels': {'_standby': ['https://dutchsec.com'], 'test': ['https://github.com', 'https://dutchsec.com']}}
>>> r = requests.get('http://localhost/channel', json={'channel':'test'})
>>> r.json()
{'channel': ['https://github.com', 'https://dutchsec.com']}
# Delete channel
>>> r = requests.delete('http://localhost/channel', json={'channel':'test'})
>>> r.json()
{'channel': 'Succesfully deleted channel "test"'}
>>> r = requests.get('http://localhost/channels', json={})
>>> r.json()
{'channels': {'_standby': ['https://dutchsec.com']}}
```

# Thanks

Thanks to https://eshlox.net/2017/08/02/falcon-framework-json-middleware-loads-dumps/ for the falcon middleware!
