---
layout: single
title: "Selected Research"
permalink: /projects/
author_profile: true
---

## TLAPS-Bench

[TLAPS-Bench](https://github.com/specula-org/tlaps-bench) evaluates AI systems on completing and constructing machine-checkable TLA+ proofs. My contributions focus on making evaluations more scalable, reliable, and interpretable:

- cache-aware and sharded TLAPM verification for large proofs;
- continuation support for agents that produce useful partial proofs;
- robust retry handling that separates infrastructure failures from proof failures;
- correct resume behavior and reproducible evaluation metadata; and
- model reasoning controls and provider usage telemetry.

[View my TLAPS-Bench contributions](https://github.com/specula-org/tlaps-bench/pulls?q=is%3Apr+author%3Amunimthahmid)

## Agentic SRE with real-world failures

At UIUC, I study how AI agents diagnose, mitigate, and validate production failures. I contributed a reproducible SREGym incident for Kubernetes node conntrack exhaustion. The scenario is designed around an important systems challenge: the failure itself can block the agent's normal SSH or execution path into the affected node.

## Bengali speech representation analysis

My undergraduate research examined the layer-wise separability of Bengali phone-like units across Whisper-small, Whisper-medium, and Whisper-large-v3 under speaker-disjoint evaluation. The study includes XLS-R comparison, ABX discriminability, confidence filtering, duration stratification, and probe ablations. The resulting paper was accepted to INTERSPEECH 2026.
