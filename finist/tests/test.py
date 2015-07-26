import unittest
import redis
redis_conn = redis.Redis()


class FinistTest(unittest.TestCase):
    """docstring for FinistTest"""
    def __init__(self, *args, **kwargs):
        super(FinistTest, self).__init__(*args, **kwargs)
        self.setup_finist()

    def setup_finist(self):
        redis_conn.flushdb()
        self.fsm = Finist(redis_conn, "myfsm", "pending")
        self.fsm.on("approve", "pending", "approved")
        self.fsm.on("cancel", "pending", "cancelled")
        self.fsm.on("cancel", "approved", "cancelled")
        self.fsm.on("reset", "cancelled", "pending")

    def send_event(self, event):
        # Change event for the FSM
        self.fsm.trigger(event)

    def setup_finist_with_client(self):
        self.fsm2 = Finist(redis_conn, "myfsm", "pending")

    def test_run(self):
        # Verify initial state
        self.assertEqual("pending", self.fsm.state())
        # Send an event
        self.send_event("approve")
        # Verify transition to "approved"
        self.assertEqual("approved", self.fsm.state())
        # Send an event
        self.send_event("cancel")
        # Verify transition to "cancelled"
        self.assertEqual("cancelled", self.fsm.state())
        # Send an event
        self.send_event("approve")
        # Verify state remains as "cancelled"
        self.assertEqual("cancelled", self.fsm.state())
        # Create a different fsm with client
        self.setup_finist_with_client()
        # Verify state remains as "cancelled"
        self.assertEqual("cancelled", self.fsm2.state())
        state, changed = self.fsm.trigger("reset")
        # A successful event returns true
        self.assertEqual(True, changed)
        self.assertEqual("pending", state)
        state, changed = self.fsm.trigger("reset")
        # An unsuccessful event returns false
        self.assertEqual(False, changed)
        self.assertEqual("pending", state)
        # Delete an event
        self.fsm.rm("approve")
        state, changed = self.fsm.trigger("approve")
        # Non existent events return false
        self.assertEqual(False, changed)
        self.assertEqual("pending", state)

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from finist import Finist
    else:
        from ..finist import Finist
    unittest.main()
