---
title: Faster joins with Iceberg bucketing
summary: Rebuilt the data lake's write path with configuration-driven Iceberg bucketing so Spark can use storage-partitioned joins. Joins got 8× faster and scans shrank by over 90%.
org: Rokt
period: 2025 – now
stack: [Apache Iceberg, Apache Spark]
order: 4
---

## What I did

I rebuilt the write path of the core ingestion engine so tables are bucketed through configuration instead of by hand.

## How it works

When two tables are bucketed the same way, Spark can join them bucket by bucket (a storage-partitioned join) instead of shuffling all the data across the cluster.

## Result

Joins got 8× faster, and data scanned dropped by more than 90% across Spark workloads.
