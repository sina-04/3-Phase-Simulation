# README — Discrete-Event Queue Simulation (OOP)

## Overview

This program is a minimal **discrete-event simulation** of a single-server queue (think M/M/1) implemented in Python with an explicit **Future Event List (FEL)** and three phases: **arrival (b1)**, **service start (c1)**, and **service completion (b2)**. It advances the simulation clock to the next scheduled event, updates system state (queue length, server busy/idle), and collects simple counters for arrivals and completions. 

---

## Features

* **Event-driven kernel:** time jumps to the next FEL event; no fixed time step. 
* **Stochastic inputs:** exponential **interarrival** (mean 3) and **service** times (mean 2). 
* **Reproducibility:** fixed NumPy RNG seed (`np.random.seed(0)`). 
* **Simple KPIs:** total **number_in** (arrivals) and **number_out** (departures) at the end of the run. 

---

## How it works (system design)

* **Class `Simulation`** encapsulates state: `clock`, `FEL`, `queue1`, `operator1` (server idle/busy), and counters. On init, the FEL is seeded with the first **arrival** event `['b1', 0]`. 
* **Event loop:** `main()`

  1. `time_forwarding()` pops the next event (min time) from the FEL and sets `clock`.
  2. Executes handler for **b1** (arrival → schedule next arrival) or **b2** (completion → free server).
  3. If server is **idle** and there’s a **queue**, trigger **c1** (start service) and schedule **b2** at `clock + service_time`. 
* **Stopping rule:** while `clock < 10000` keep processing. (The final printed time may exceed 10,000 slightly if the last event jumps past it.) 

**Event glossary**

* **b1 (arrival):** increment `number_in` & `queue1`; schedule next arrival at `clock + Exp(mean=3)`. 
* **c1 (service start):** decrement `queue1`, set server busy, schedule completion. 
* **b2 (service completion):** free server, increment `number_out`. 

---

## Installation

* **Python 3.8+** recommended
* **Dependencies:** `numpy`

```bash
pip install numpy
```

---

## Running the simulation

From the project directory:

```bash
python "3 phase sim (oop).py"
```

You’ll see output like:

```
Simulation Clock is:  10001.234
number in is: 3333
number out is: 3332
```

(Values vary with randomness; seed is set for reproducibility.) 

---

## Configuration

Tune these directly in the class methods:

* **Interarrival mean:** `generate_interarrival()` → `np.random.exponential(scale=3)` → change `scale`. 
* **Service mean:** `generate_service()` → `np.random.exponential(scale=2)` → change `scale`. 
* **Run length:** `while s.clock < 10000:` → change threshold. 
* **Random seed:** `np.random.seed(0)` at top-level. 

---

## Interpreting results

* **Stability check:** With mean interarrival 3 and mean service 2, arrival rate λ≈0.333, service rate μ=0.5 → ρ=λ/μ≈0.667 (<1), so the queue is stable in expectation.
* **Counters:** `number_in` and `number_out` let you sanity-check flow balance over long horizons. 

---

## Extending the model

Ideas to grow this into a richer simulator:

1. **Warm-up & stats:** add a warm-up period and track time-averaged queue length, wait times, and server utilization.
2. **Multiple servers / priority:** add more operators or priority queues.
3. **Logging & tracing:** keep a history of events for debugging and plots.
4. **Stop conditions:** stop after N completions or when the FEL time exceeds a target, then drain in-service jobs.
5. **CLI args / config file:** pass rates, seed, and horizon via command-line or a YAML/JSON config.

---

## Assumptions & limitations (critical review)

* **Poisson/Exponential assumption:** Arrivals and services are memoryless; real systems often aren’t. Consider general (G/G/1) distributions. 
* **Single queue, single server:** No balking/reneging, no breakdowns, no shift changes.
* **No metrics beyond counts:** Add wait-time and queue-length statistics for proper performance analysis.
* **Time jump side-effect:** The last processed event can move `clock` past the time horizon; if you need strict truncation, guard scheduling or post-process. 

---

## File layout

* `3 phase sim (oop).py` — all source code (OOP simulator, event loop, and printout). 

---

## License

If you plan to share this, add a license (e.g., MIT) here.

---

## Citation

This README describes and references the source code provided in `3 phase sim (oop).py`. 
