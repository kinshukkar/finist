Finist
======

Redis based Finite State Machine.

Description
-----------

Finist is a finite state machine that is defined and persisted in
[Redis][redis].

Community
---------

Meet us on IRC: [#lesscode](irc://chat.freenode.net/#lesscode) on
[freenode.net](http://freenode.net/).

Related projects
----------------

* [Finist implemented in Lua][finist.lua]
* [Finist implemented in Ruby][finist.lua]
* [Finist implemented in Rust][finist.ruby]

Getting started
---------------

Install [Redis][redis]. On most platforms it's as easy as grabbing
the sources, running make and then putting the `redis-server` binary
in the PATH.

Once you have it installed, you can execute `redis-server` and it
will run on `localhost:6379` by default. Check the `redis.conf`
file that comes with the sources if you want to change some settings.

Usage
-----

Finist requires a [Redic][redic] compatible client. To make things
easier, `redic` is listed as a runtime dependency so the examples
in this document will work.

```python
from finist import Finist
import redis
redis_conn = redis.Redis()

# Initialize with a Redis client, the name of the machine and the
# initial state. In this example, the machine is called "order" and
# the initial status is "pending". The Redis client is connected to
# the default host (127.0.0.1:6379).
machine = Finist(redis_conn, "order", "pending")

# Available transitions are defined with the `on` method
# `machine.on(<event>, <initial_state>, <final_state>)`
machine.on("approve", "pending", "approved")
machine.on("cancel", "pending", "cancelled")
machine.on("cancel", "approved", "cancelled")
machine.on("reset", "cancelled", "pending")
```

Now that the possible transitions are defined, we can check the
current state:

```python
machine.state()
# => "pending"
```

And we can trigger an event:

```python
machine.trigger("approve")
# => ["approved", true]
```

The `trigger` method returns an array of two values: the first
represents the current state, and the second represents whether
a transition occurred.

Here's what happens if an event doesn't cause a transition:

```python
machine.trigger("reset")
# => ["approved", false]
```

Here's a convenient way to use this flag:

```python
state, changed = machine.trigger("reset")

if changed
  print "State changed to %s\n" %state
```

If you need to remove all the transitions for a given event, you
can use `rm`:

```python
machine.rm("reset")
```

Note that every change is persisted in Redis.

Representation
--------------

Each event is represented as a hash in Redis, and its field/value
pairs are the possible transitions.

For the FSM described in the examples above, the keys are laid out
as follows:

```ini
# Current state
finist:order (string)

# Transitions for event `approve`
finist:order:approve (hash)
	pending   -> approved

# Transitions for event `cancel`
finist:order:cancel (hash)
	pending   -> cancelled
	approved  -> cancelled

# Transitions for event `reset`
finist:order:reset (hash)
	cancelled -> pending
```

Installation
------------

```
$ python setup.py install
or 
$ pip install finist
```

[redis]: http://redis.io
[Python Redis]: https://github.com/andymccurdy/redis-py
[finist.lua]: https://github.com/soveran/finist.lua
[finist.rust]: https://github.com/badboy/finist
[finist.ruby]: https://github.com/soveran/finist
