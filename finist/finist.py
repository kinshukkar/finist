# -*- coding: utf-8 -*-


class Finist:
    _SCRIPT = """local curr = redis.call("GET", KEYS[1])
                local next = redis.call("HGET", KEYS[2], curr)
                if next then
                  redis.call("SET", KEYS[1], next)
                  return { next, true }
                else
                  return { curr, false }
                end
                """

    def __init__(self, redis, name, initializer):
        self._name = "finist:%s" % name
        self.redis = redis
        self.redis.setnx(self._name, initializer)

    def event_key(self, ev):
        return "%s:%s" % (self._name, ev)

    def on(self, ev, curr_state, next_state):
        return self.redis.hset(self.event_key(ev), curr_state, next_state)

    def rm(self, ev):
        return self.redis.delete(self.event_key(ev))

    def state(self):
        return self.redis.get(self._name)

    def send_event(self, ev):
        return self.redis.eval(self._SCRIPT, "2", self._name,
                               self.event_key(ev))

    def trigger(self, ev):
        result = self.send_event(ev)
        return result[0], result[1] != None
