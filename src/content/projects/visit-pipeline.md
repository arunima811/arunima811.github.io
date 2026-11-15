---
title: Unified visit pipeline
summary: A Flink pipeline that brings mParticle events into Rokt at about 10× the earlier volume, and joins browsing, referral and conversion events into one history per user.
org: Rokt
period: 2025 – now
stack: [Apache Flink, Kafka, Apache Iceberg]
order: 1
---

## The problem

When mParticle became part of Rokt, its event stream had to flow into Rokt's advertiser events. That meant about ten times the volume the earlier pipeline handled: around 50,000 events per second.

## What I built

- A Flink pipeline that brings the mParticle stream into Rokt's advertiser events.
- Visit processing that combines browsing, referral and conversion activity into one ordered history per user.

## Why it matters

These histories are the base for partner-to-advertiser journeys and for ML feature work.
