# Notipy Client
> Python client for [Notipy Server](https://github.com/michaelimfeld/notipy-server)

A Python client which talks to the [Notipy Server](https://github.com/michaelimfeld/notipy-server)-REST-API.

## Basic Usage
The following code snippet sends a Hello World message to the Telegram user
with the username _myuser_.

```python
from notipy import Notipy, BackendType

# Hostname and port of the notipy-server instance
HOST = "localhost"
PORT = 8000

notifier = Notipy(HOST, PORT)
notifier.send(BackendType.TELEGRAM, "myuser", "Hello World")
```

## Templating
The client uses the [Jinja2](https://github.com/pallets/jinja) Templating Engine to support templated messages.
All the parameters for Jinja2 can be passed as keyword arguments to the `send_templated` function.

```python
from pathlib import Path
from notipy import Notipy, BackendType

# Hostname and port of the notipy-server instance
HOST = "localhost"
PORT = 8000
# Template directory
TEMPLATE_DIR = Path("/var/lib/templates")

notifier = Notipy(HOST, PORT, template_dir=TEMPLATE_DIR)
notifier.send_templated(BackendType.TELEGRAMGROUP, "mygroup", "mytemplate", foo="bar")
```
Templates always have the file name suffix `.tmpl`. The _mytemplate.tmpl_ file in the _/var/lib/templates_ directory
would look like this:
```jinja
Hello {{ foo }}!
```
So _mygroup_ would recive the message: `Hello bar!`.