"""Three-phase discrete-event simulation for an M/M/1 queue."""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SimulationResult:
    clock: float
    arrivals: int
    departures: int
    queued: int
    server_idle: bool


class Simulation:
    """Minimal A-B-C event simulation with an explicit future-event list."""

    def __init__(
        self,
        *,
        interarrival_mean: float = 3.0,
        service_mean: float = 2.0,
        seed: int = 0,
    ) -> None:
        if interarrival_mean <= 0 or service_mean <= 0:
            raise ValueError("Distribution means must be positive.")

        self.interarrival_mean = interarrival_mean
        self.service_mean = service_mean
        self.rng = np.random.default_rng(seed)
        self.clock = 0.0
        self.FEL: list[list[object]] = [["b1", 0.0]]
        self.queue1 = 0
        self.operator1 = True
        self.tempEvent: list[object] = ["b1", 0.0]
        self.number_out = 0
        self.number_in = 0

    def time_forwarding(self) -> None:
        if not self.FEL:
            raise RuntimeError("The future-event list is empty.")
        index = min(range(len(self.FEL)), key=lambda i: float(self.FEL[i][1]))
        self.tempEvent = self.FEL.pop(index)
        self.clock = float(self.tempEvent[1])

    def procedure_b1(self) -> None:
        self.number_in += 1
        self.queue1 += 1
        self.FEL.append(["b1", self.clock + self.generate_interarrival()])

    def procedure_b2(self) -> None:
        self.operator1 = True
        self.number_out += 1

    def procedure_c1(self) -> None:
        self.queue1 -= 1
        self.operator1 = False
        self.FEL.append(["b2", self.clock + self.generate_service()])

    def step(self) -> None:
        self.time_forwarding()
        if self.tempEvent[0] == "b1":
            self.procedure_b1()
        elif self.tempEvent[0] == "b2":
            self.procedure_b2()
        else:
            raise ValueError(f"Unknown event type: {self.tempEvent[0]}")

        if self.operator1 and self.queue1 > 0:
            self.procedure_c1()

    def main(self) -> None:
        """Backward-compatible alias for one simulation step."""
        self.step()

    def run(self, horizon: float = 10_000.0) -> SimulationResult:
        if horizon <= 0:
            raise ValueError("The time horizon must be positive.")
        while self.clock < horizon:
            self.step()
        return SimulationResult(
            clock=self.clock,
            arrivals=self.number_in,
            departures=self.number_out,
            queued=self.queue1,
            server_idle=self.operator1,
        )

    def generate_interarrival(self) -> float:
        return float(self.rng.exponential(scale=self.interarrival_mean))

    def generate_service(self) -> float:
        return float(self.rng.exponential(scale=self.service_mean))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--horizon", type=float, default=10_000.0)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--interarrival-mean", type=float, default=3.0)
    parser.add_argument("--service-mean", type=float, default=2.0)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    result = Simulation(
        interarrival_mean=args.interarrival_mean,
        service_mean=args.service_mean,
        seed=args.seed,
    ).run(args.horizon)
    print(f"Simulation Clock is: {result.clock:.3f}")
    print(f"number in is: {result.arrivals}")
    print(f"number out is: {result.departures}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
