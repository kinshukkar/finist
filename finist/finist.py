# -*- coding: utf-8 -*-


class Finist(object):
    _SCRIPT = """local next = redis.call("HGET", KEYS[2], KEYS[3])
                if next then
                  return { next, true }
                else
                  return { KEYS[3], false }
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

    def _send_event(self, ev, state):
        return self.redis.eval(self._SCRIPT, "2", self._name,
                               self._event_key(ev), state)

    def trigger(self, ev, state):
        result = self._send_event(ev, state)
        return result[0], result[1] != None
