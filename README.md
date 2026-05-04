# Real-Time Top Active Users (Kafka + Workers)

## Overview

This project implements a real-time event processing system using Kafka and distributed workers.

It ingests user activity logs and computes the most active users continuously at scale.

The system demonstrates key distributed systems concepts:

- Kafka partitioning
- Consumer groups (worker scaling)
- Stream processing
- Idempotency and fault tolerance
- Real-time aggregation

---

## Problem Statement

Given a stream of logs:


"user1 click 100"
"user2 login 101"
"user1 scroll 102"


We want to:

- Process millions of events
- Scale horizontally
- Compute **most active users in real time**

---

## Architecture


Producer → Kafka (Aiven) → Partitions → Workers → Aggregation


- **Producer** generates logs
- **Kafka** distributes events across partitions
- **Workers** process events in parallel
- Each worker maintains local user counts

---

## Data Flow

1. Producer sends logs to Kafka
2. Kafka partitions data using `user_id` as key
3. Consumer group distributes partitions across workers
4. Workers update local counts
5. Top users are computed continuously

---

## Key Design Decisions

### 1️⃣ Partitioning by User


key = user_id


- Ensures all events for a user go to the same partition
- Guarantees ordering per user
- Eliminates need for distributed locking

---

### 2️⃣ Consumer Groups (Workers)

- Multiple workers share load
- Kafka automatically assigns partitions
- Enables horizontal scaling

---

### 3️⃣ Local Aggregation

Each worker maintains:


counts[user_id] += 1


- Fully parallel
- No cross-worker communication needed

---

### 4️⃣ Idempotency

Kafka provides **at-least-once delivery**.

Workers must handle duplicates:


if event_id already processed:
skip


---

## Setup (Codespaces + Aiven)

### 1️⃣ Install dependencies


pip install kafka-python python-dotenv


---

### 2️⃣ Create Kafka (Aiven)

- Create Kafka service (free tier)
- Create topic: `logs`
- Set partitions: **3–6**
- Download certificates

---

### 3️⃣ Configure environment

`.env`:


BOOTSTRAP_SERVER=host:port
TOPIC=logs


---

### 4️⃣ Add certificates

Place files in `certs/`:

- `ca.pem`
- `service.cert`
- `service.key`

---

## Running the System

### Start workers (multiple terminals)


python app/worker.py
python app/worker.py
python app/worker.py


---

### Run producer


python app/producer.py


---

### Run load test


python app/load_test.py


---

## Example Output


Top users: [('user3', 120), ('user1', 98), ('user7', 85)]


---

## Scaling Behavior

| Workers | Partitions | Throughput |
|--------|------------|-----------|
| 1      | 3          | Low       |
| 3      | 3          | Medium    |
| 6      | 6          | High      |

---

## Key Learnings

### 1️⃣ Partitioning Enables Parallelism

- Partitions are the unit of scaling
- Max parallelism = number of partitions

---

### 2️⃣ Ordering is Per Partition

- Events with same key are ordered
- Global ordering is not guaranteed

---

### 3️⃣ Kafka is At-Least-Once

- Messages may be reprocessed
- Idempotency is required

---

### 4️⃣ Consumer Groups Enable Scaling

- Add workers → automatic rebalancing
- No changes required in producer

---

### 5️⃣ Hot Partition Problem

If one user is extremely active:

- One partition becomes a bottleneck

Solutions:

- Key hashing
- Splitting heavy users
- Hierarchical aggregation

---

## Tradeoffs

| Approach | Pros | Cons |
|--------|------|------|
| Partition by user | Simple, ordered | Hotspots possible |
| Local aggregation | Fast, scalable | Needs global merge |
| Kafka | Durable, scalable | At-least-once semantics |

---

## Extensions (Future Work)

- Redis leaderboard (real-time ranking)
- Sliding window aggregation (last N minutes)
- Dead Letter Queue (DLQ)
- Retry handling
- Persistent storage (Postgres)

---

## Key Takeaways

- Partitioning removes the need for locking
- Workers scale horizontally using consumer groups
- Idempotency is required for correctness
- Distributed systems are about tradeoffs between consistency and scalability