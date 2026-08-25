import unittest

from simulation import Simulation


class SimulationTests(unittest.TestCase):
    def test_repeated_seed_is_deterministic(self):
        first = Simulation(seed=42).run(500)
        second = Simulation(seed=42).run(500)
        self.assertEqual(first, second)

    def test_flow_balance_and_horizon(self):
        result = Simulation(seed=0).run(1_000)
        self.assertGreaterEqual(result.clock, 1_000)
        self.assertEqual(
            result.arrivals,
            result.departures + result.queued + (0 if result.server_idle else 1),
        )

    def test_invalid_configuration_is_rejected(self):
        with self.assertRaises(ValueError):
            Simulation(interarrival_mean=0)
        with self.assertRaises(ValueError):
            Simulation().run(0)


if __name__ == "__main__":
    unittest.main()
