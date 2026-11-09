# Earliest Deadline First (EDF) Scheduling
# Preemptive dynamic-priority scheduling.
# The job with the earliest absolute deadline runs first.

tasks = [
    {"id": "T1", "execution": 1, "period": 4, "deadline": 4},
    {"id": "T2", "execution": 1, "period": 5, "deadline": 5},
    {"id": "T3", "execution": 2, "period": 10, "deadline": 10},
]

SIMULATION_TIME = 20

# Calculate total CPU utilization.
utilization = sum(
    task["execution"] / task["period"] for task in tasks
)

# Generate periodic task instances.
jobs = []

for task in tasks:
    for release in range(0, SIMULATION_TIME, task["period"]):
        jobs.append({
            "id": task["id"],
            "release": release,
            "absolute_deadline": release + task["deadline"],
            "remaining": task["execution"],
        })

gantt = []
missed = []
time = 0

while time < SIMULATION_TIME:

    # Check for jobs that have reached their deadlines unfinished.
    for job in jobs:
        if (
            job["absolute_deadline"] == time
            and job["remaining"] > 0
            and job not in missed
        ):
            missed.append(job)

    ready = [
        job for job in jobs
        if job["release"] <= time and job["remaining"] > 0
    ]

    if ready:
        # EDF: earliest absolute deadline has highest priority.
        current = min(
            ready,
            key=lambda job: (
                job["absolute_deadline"],
                job["release"],
                job["id"]
            )
        )

        current["remaining"] -= 1
        pid = current["id"]
    else:
        pid = "IDLE"

    # Combine consecutive intervals of the same task.
    if gantt and gantt[-1][0] == pid:
        gantt[-1] = (pid, gantt[-1][1], time + 1)
    else:
        gantt.append((pid, time, time + 1))

    time += 1

# Check deadlines exactly at the simulation endpoint.
for job in jobs:
    if (
        job["absolute_deadline"] == SIMULATION_TIME
        and job["remaining"] > 0
        and job not in missed
    ):
        missed.append(job)

print("\nEARLIEST DEADLINE FIRST (EDF) SCHEDULING")
print("=" * 55)

print("\nGANTT CHART:")
for pid, start, end in gantt:
    print(f"| {pid} ({start}-{end}) ", end="")
print("|")

print("\nTASK CONFIGURATION")
print("-" * 50)
print(f"{'Task':<10}{'Execution':<12}{'Period':<12}{'Deadline'}")

for task in tasks:
    print(
        f"{task['id']:<10}{task['execution']:<12}"
        f"{task['period']:<12}{task['deadline']}"
    )

print("\nCPU UTILIZATION")
print(f"Total Utilization: {utilization * 100:.2f}%")
print(
    "EDF Utilization Test:",
    "PASS (utilization is at or below 100%)"
    if utilization <= 1
    else "FAIL (utilization exceeds 100%)"
)

print("\nDEADLINE ANALYSIS")
print(f"Missed Deadlines: {len(missed)}")

if missed:
    for job in missed:
        print(
            f"{job['id']} released at {job['release']} "
            f"missed deadline {job['absolute_deadline']}"
        )
else:
    print("All task deadlines were met.")

print(f"\nSimulation Duration: {SIMULATION_TIME} ms")
