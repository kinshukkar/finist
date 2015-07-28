# -*- coding: utf-8 -*-


class Finist(object):
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

    def _event_key(self, ev):
        return "%s:%s" % (self._name, ev)

    def on(self, ev, curr_state, next_state):
        return self.redis.hset(self._event_key(ev), curr_state, next_state)

    def rm(self, ev):
        return self.redis.delete(self._event_key(ev))

    def state(self):
        return self.redis.get(self._name)

    def _send_event(self, ev):
        return self.redis.eval(self._SCRIPT, "2", self._name,
                               self._event_key(ev))

    def trigger(self, ev):
        result = self._send_event(ev)
        return result[0], result[1] != None
