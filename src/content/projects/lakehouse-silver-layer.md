---
title: Medallion lakehouse, silver layer
summary: Redesigned how the data lake publishes data, using a medallion layout, and built the clean, enriched silver layer that revenue and ML teams use.
org: Rokt
period: 2025 – now
stack: [Apache Spark, Apache Iceberg]
order: 2
---

## What I did

I redesigned the lakehouse output around the medallion pattern: raw data, then cleaned data, then business-ready data. I built the middle (silver) layer: clean, enriched business signals for conversions, impressions and referrals.

## Who uses it

All of Rokt's revenue and ML teams: 50+ people, 20+ applications and 30+ tables.
