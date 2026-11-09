# BCA151 – Operating Systems Laboratory Activity 3
## Multilevel Queue and Real-Time CPU Scheduling

**Student Name:** [Your Name]
**Section:** [Your Section]
**Course:** BCA151 – Operating Systems
**Activity:** Laboratory Activity 3

---

## I. Introduction

CPU scheduling is an important function of an operating system. It determines which process or task receives CPU time and when it will execute.

This activity implements three CPU scheduling algorithms: Multilevel Queue Scheduling (MLQ), Rate Monotonic Scheduling (RMS), and Earliest Deadline First (EDF). The programs simulate process and task execution, display Gantt charts, and calculate scheduling measurements.

## II. Objectives

1. Understand the operation of Multilevel Queue Scheduling.
2. Implement Round Robin and First Come First Served scheduling.
3. Understand fixed-priority real-time scheduling using RMS.
4. Implement dynamic-priority real-time scheduling using EDF.
5. Calculate CPU utilization and analyze deadline compliance.
6. Compare the behavior of different scheduling algorithms.

## III. Algorithms

### A. Multilevel Queue Scheduling (MLQ)

Multilevel Queue Scheduling separates processes into different queues according to their categories.

- Queue 1 – Interactive: Round Robin with a time quantum of 2 ms.
- Queue 2 – Batch: First Come First Served (FCFS).
- Queue 1 has higher priority than Queue 2.
- A Queue 1 process arriving while Queue 2 is running interrupts Queue 2. The interrupted process resumes later.

### B. Rate Monotonic Scheduling (RMS)

RMS is a preemptive, fixed-priority real-time scheduling algorithm. Tasks with shorter periods receive higher priority.

| Task | Execution Time | Period | Deadline |
|---|---:|---:|---:|
| T1 | 1 ms | 4 ms | 4 ms |
| T2 | 1 ms | 5 ms | 5 ms |
| T3 | 2 ms | 10 ms | 10 ms |

CPU utilization formula:

U = (C1/T1) + (C2/T2) + (C3/T3)

The RMS utilization bound for three tasks is approximately 77.98%.

### C. Earliest Deadline First (EDF)

EDF is a preemptive, dynamic-priority scheduling algorithm. The ready task with the earliest absolute deadline receives the CPU first.

Absolute Deadline = Release Time + Relative Deadline

Under standard assumptions, EDF can schedule independent periodic tasks on a preemptive uniprocessor when total CPU utilization does not exceed 100%.

The same task configuration used in RMS is used for EDF.


## IV. Implementation

The project was implemented using Python.

### Project Structure

- README.md
- multilevel_queue/mlq.py
- real_time_scheduling/rms.py
- real_time_scheduling/edf.py
- outputs/mlq_output.txt
- outputs/rms_output.txt
- outputs/edf_output.txt
- screenshots/

## V. Results and Discussion

### A. Multilevel Queue Scheduling

Gantt Chart:

P1 (0-2) | P2 (2-4) | P1 (4-6) | P5 (6-8) | P2 (8-10) | P1 (10-11) | P3 (11-17) | P4 (17-20)

| Process | Arrival | Burst | Completion | Turnaround | Waiting |
|---|---:|---:|---:|---:|---:|
| P1 | 0 | 5 | 11 | 11 | 6 |
| P2 | 1 | 4 | 10 | 9 | 5 |
| P3 | 0 | 6 | 17 | 17 | 11 |
| P4 | 2 | 3 | 20 | 18 | 15 |
| P5 | 3 | 2 | 8 | 5 | 3 |

- Average Waiting Time: 8.00 ms
- Average Turnaround Time: 12.00 ms
- Total Execution Time: 20 ms

Queue 1 processes received priority over Queue 2. Round Robin scheduled interactive processes, while FCFS handled batch processes.

### B. Rate Monotonic Scheduling (RMS)

Gantt Chart:

T1 (0-1) | T2 (1-2) | T3 (2-4) | T1 (4-5) | T2 (5-6) | IDLE (6-8) | T1 (8-9) | IDLE (9-10) | T2 (10-11) | T3 (11-12) | T1 (12-13) | T3 (13-14) | IDLE (14-15) | T2 (15-16) | T1 (16-17) | IDLE (17-20)

- Total CPU Utilization: 65.00%
- RMS Utilization Bound: 77.98%
- Utilization Test: PASS
- Missed Deadlines: 0
- Simulation Duration: 20 ms

The task with the shortest period, T1, received the highest fixed priority. All task deadlines were met.

### C. Earliest Deadline First (EDF)

Gantt Chart:

T1 (0-1) | T2 (1-2) | T3 (2-4) | T1 (4-5) | T2 (5-6) | IDLE (6-8) | T1 (8-9) | IDLE (9-10) | T2 (10-11) | T3 (11-12) | T1 (12-13) | T3 (13-14) | IDLE (14-15) | T2 (15-16) | T1 (16-17) | IDLE (17-20)

- Total CPU Utilization: 65.00%
- EDF Utilization Limit: 100%
- Utilization Test: PASS
- Missed Deadlines: 0
- Simulation Duration: 20 ms

EDF selected the ready task with the earliest absolute deadline. All task deadlines were met.

Both RMS and EDF produced the same Gantt chart for this particular task configuration. This does not mean that the two algorithms always produce identical schedules.

## VI. Algorithm Comparison

| Algorithm | Priority Type | Scheduling Basis | Main Characteristic |
|---|---|---|---|
| MLQ | Queue-based | Process category | Uses different scheduling methods for separate queues. |
| RMS | Fixed priority | Task period | Shorter-period tasks always have higher priority. |
| EDF | Dynamic priority | Absolute deadline | The task with the earliest deadline receives the CPU first. |

MLQ organizes processes according to their categories, while RMS and EDF are designed for real-time task scheduling. RMS uses fixed priorities, whereas EDF changes priorities according to absolute deadlines.

## VII. Guide Questions

**37. What is the difference between Multilevel Queue and Multilevel Feedback Queue Scheduling?**
MLQ assigns processes to fixed queues, while MLFQ allows processes to move between queues based on their behavior and CPU usage.

**38. Why can different queues use different scheduling algorithms?**
Different process categories have different needs. Round Robin provides responsiveness for interactive processes, while FCFS is simple for batch processes.

**39. How does RMS assign priorities?**
RMS gives higher priority to tasks with shorter periods.

**40. Why is RMS considered a fixed-priority algorithm?**
A task keeps the same priority based on its period throughout the scheduling process.

**41. How does EDF select the next task?**
EDF selects the ready task with the earliest absolute deadline.

**42. What happens when a task with an earlier deadline arrives?**
The newly arrived task may preempt the currently running task if its absolute deadline is earlier.

**43. Why is CPU utilization important in real-time scheduling?**
CPU utilization measures the portion of processor time required by tasks. It helps determine whether the processor can handle the workload.

**44. Can a task set with utilization below 100% still miss deadlines?**
Yes. Utilization below 100% alone does not guarantee that every scheduling algorithm will meet all deadlines. Task characteristics, scheduling policy, blocking, and overhead can affect deadline compliance. Under standard EDF assumptions with deadlines equal to periods, utilization at or below 100% is sufficient.

**45. Which is more flexible, RMS or EDF?**
EDF is generally more flexible because it dynamically selects tasks according to their absolute deadlines, while RMS uses fixed priorities.

**46. When is RMS a suitable choice?**
RMS is suitable for predictable periodic tasks when a simpler fixed-priority scheduling method is preferred.

## VIII. Conclusion

This activity demonstrated three CPU scheduling algorithms: Multilevel Queue Scheduling, Rate Monotonic Scheduling, and Earliest Deadline First. The MLQ simulation showed how interactive and batch processes can be handled using different queues and scheduling methods. The RMS and EDF simulations both achieved 65% CPU utilization and completed the 20 ms simulation without missed deadlines. The activity helped demonstrate the differences between queue-based, fixed-priority, and dynamic-priority scheduling.


