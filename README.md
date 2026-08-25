# Three-Phase Queue Simulation

[![CI](https://github.com/sina-04/3-Phase-Simulation/actions/workflows/ci.yml/badge.svg)](https://github.com/sina-04/3-Phase-Simulation/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A compact discrete-event simulation of an M/M/1 queue using the three-phase
A-B-C method and an explicit future-event list.

## Model

- **B1 — arrival:** adds a customer and schedules the next arrival.
- **C1 — service start:** starts service whenever the server is idle and the
  queue is non-empty.
- **B2 — departure:** completes service and releases the server.
- Exponential interarrival and service times default to means of 3 and 2.
- A local NumPy random generator makes seeded runs reproducible.

## Run

```bash
python -m pip install -r requirements.txt
python simulation.py
python simulation.py --horizon 5000 --seed 42
```

The original command remains supported:

```bash
python "3 phase sim (oop).py"
```

Available options include `--horizon`, `--seed`,
`--interarrival-mean`, and `--service-mean`.

## Use as a module

```python
from simulation import Simulation

result = Simulation(seed=7).run(horizon=1_000)
print(result.arrivals, result.departures)
```

## Validation

```bash
python -m unittest discover -s tests -v
```

The tests check deterministic seeded runs, flow conservation, and invalid
configuration handling.

## Limitations

This educational model has one queue and one server, assumes memoryless
arrivals and service, and reports flow counters rather than warm-up-corrected
waiting-time or utilization estimates.

## License

Released under the [MIT License](LICENSE).
