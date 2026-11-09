
# Multilevel Queue CPU Scheduling
# Queue 1: Interactive - Round Robin (Quantum = 2 ms)
# Queue 2: Batch - First Come, First Served (FCFS)
# Queue 1 has strict priority over Queue 2.

QUANTUM = 2

processes = [
    {"pid": "P1", "arrival": 0, "burst": 5, "queue": 1},
    {"pid": "P2", "arrival": 1, "burst": 4, "queue": 1},
    {"pid": "P3", "arrival": 0, "burst": 6, "queue": 2},
    {"pid": "P4", "arrival": 2, "burst": 3, "queue": 2},
    {"pid": "P5", "arrival": 3, "burst": 2, "queue": 1},
]

for p in processes:
    p["remaining"] = p["burst"]
    p["completion"] = 0
    p["admitted"] = False

queue1 = []
queue2 = []
active_q2 = None
gantt = []
time = 0
completed = 0


def admit_arrivals(current_time):
    """Add newly arrived processes to their respective queues."""
    for p in processes:
        if not p["admitted"] and p["arrival"] <= current_time:
            p["admitted"] = True

            if p["queue"] == 1:
                queue1.append(p)
            else:
                queue2.append(p)


def add_gantt(pid, start, end):
    """Record a CPU execution interval."""
    if start < end:
        gantt.append((pid, start, end))


while completed < len(processes):

    admit_arrivals(time)

    # Queue 1 has strict priority.
    if queue1:
        current = queue1.pop(0)

        start = time
        run_time = min(QUANTUM, current["remaining"])

        time += run_time
        current["remaining"] -= run_time

        add_gantt(current["pid"], start, time)

        # Admit arrivals that occurred during this time slice.
        admit_arrivals(time)

        if current["remaining"] == 0:
            current["completion"] = time
            completed += 1
        else:
            # Return unfinished process to the end of Queue 1.
            queue1.append(current)

    else:
        # Resume a preempted Queue 2 process before the next batch job.
        if active_q2 is None:
            if queue2:
                active_q2 = queue2.pop(0)
            else:
                # No process is ready. Advance to the next arrival.
                next_arrival = min(
                    p["arrival"] for p in processes if not p["admitted"]
                )
                add_gantt("IDLE", time, next_arrival)
                time = next_arrival
                continue

        current = active_q2
        start = time

        # Queue 2 runs until completion or the next Queue 1 arrival.
        next_q1_arrivals = [
            p["arrival"]
            for p in processes
            if not p["admitted"]
            and p["queue"] == 1
            and p["arrival"] > time
        ]

        if next_q1_arrivals:
            next_q1 = min(next_q1_arrivals)
            run_time = min(current["remaining"], next_q1 - time)
        else:
            run_time = current["remaining"]

        time += run_time
        current["remaining"] -= run_time

        add_gantt(current["pid"], start, time)

        if current["remaining"] == 0:
            current["completion"] = time
            completed += 1
            active_q2 = None


# Calculate performance metrics.
for p in processes:
    p["turnaround"] = p["completion"] - p["arrival"]
    p["waiting"] = p["turnaround"] - p["burst"]


# Display results.
print("\nMULTILEVEL QUEUE CPU SCHEDULING")
print("=" * 55)

print("\nGANTT CHART:")
for pid, start, end in gantt:
    print(f"| {pid} ({start}-{end}) ", end="")
print("|")

print("\nPROCESS SCHEDULING RESULTS")
print("-" * 65)
print(f"{'PID':<8}{'Arrival':<10}{'Burst':<10}{'Completion':<13}{'Turnaround':<13}{'Waiting'}")
print("-" * 65)

for p in processes:
    print(
        f"{p['pid']:<8}{p['arrival']:<10}{p['burst']:<10}"
        f"{p['completion']:<13}{p['turnaround']:<13}{p['waiting']}"
    )

avg_waiting = sum(p["waiting"] for p in processes) / len(processes)
avg_turnaround = sum(p["turnaround"] for p in processes) / len(processes)

print("-" * 65)
print(f"Average Waiting Time: {avg_waiting:.2f} ms")
print(f"Average Turnaround Time: {avg_turnaround:.2f} ms")
print(f"Total Execution Time: {time} ms")
