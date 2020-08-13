# 100_millions_requests
Making 100 million requests with Python aiohttp

### Description

Service using ``python 3.7+``.

Framework — ``aiohttp``. 

The app config is located: [/config/config.toml](config/config.toml)

### Performance

    100         request handle for 1.652 sec    (0.028 min)
    1_000       request handle for 12.627 sec   (0.21 min)
    100_000     request handle for 1095.444 sec (18,25 min)
    1_000_000   request handle for ...
    10_000_000  request handle for ...
    100_000_000 request handle for ...

### TODO

    - Add interface for asyncio.Queue
    
    - Add interface for asyncio.Semaphore
    
    - Handle different urls
    
    - client.py and server.py
    
    - use timeit for perfomance
