# 🧠 Agent Cognitive Framework (Lightweight SDLC + Memory Loop)

## Introduction

Efficient AI memory management is the foundation to empower AI and Human collaboration.

AI *intuition* works differently from a human user using a large language model. It can
systematically and creatively infer the next optimal knowledge path, iteratively derive a 
solution with human inputs to tackle complex problem to arrive at an outcome that the human
user asks.

The creativity is the essence of generative AI. Memory management provides guidance
for the AI agent to balance between systematic and creative thinking.

Our goal of this framework is not to reduce the creativity of AI and human user because
it is the very foundation to tackle complex problem without going into a rabbit hole.

Poor memory management leads to intent and design drift, over-analysis or deadlock.

This framework enriches the agent-memory-tool to provide light-weight but
powerful guardrails for efficient memory management to deliver deterministic outcome.

## 🎯 Purpose

This framework provides a **minimal cognitive scaffold** for AI agents to:

- Think systematically without rigidity  
- Maintain creativity while preserving structure  
- Continuously learn and evolve through feedback  

> **Principle:** Guide thinking, not prescribe execution.

---

# 🔷 Core Primitives

## 1. Vision
**Definition:** Target future state  
**Question:** *What should exist?*

## 2. Mission
**Definition:** Current state of reality  
**Question:** *What exists now?*

## 3. Blueprint
**Definition:** Required capabilities / gaps  
**Question:** *What is missing?*

## 4. Design
**Definition:** Structure and approach  
**Question:** *How should it work?*

## 5. Implementation
**Definition:** Execution of actions  
**Question:** *What do we do next?*

## 6. Feedback
**Definition:** Learning from reality  
**Question:** *What changed or did we learn?*

---

# 🔁 Core Execution Model (Loop-Based)

> This framework is **not linear**. It operates as a continuous loop.

```
Mission → Vision → Blueprint → Design → Implementation → Feedback → (repeat)
```

---

## 🧠 Agent Thinking Loop

```
1. Understand
   - Mission (current state)
   - Vision (target state)

2. Plan
   - Blueprint (gap analysis)

3. Shape
   - Design (approach)

4. Act
   - Implementation (execute)

5. Learn
   - Feedback (update memory)

→ Repeat until goal achieved
```

---

# 🔗 Memory Integration (Critical)

## Mapping to Memory System

| Framework | Memory Behavior |
|----------|----------------|
| Mission | Memory read (current state reconstruction) |
| Vision | Goal context |
| Blueprint | Gap inferred from memory |
| Design | Reasoning using memory + tools |
| Implementation | Tool execution / actions |
| Feedback | Memory write / update |

---

## 🧠 Memory Loop (Underlying System)

```
Capture → Store → Retrieve → Reflect → Update
```

---

# ⚖️ Structural Model (Agent-Friendly Grouping)

```
STATE
- Mission (current)
- Vision (target)

PLAN
- Blueprint (what is missing)
- Design (how to approach)

ACT
- Implementation (execute)
- Feedback (learn)
```

---

# 🧠 Cognitive Rules

- Always anchor to **Mission (reality)**
- Always align with **Vision (goal)**
- Always identify **gaps before action**
- Prefer **simple designs over complex abstractions**
- Learn continuously from **Feedback**
- Treat every iteration as part of a **loop, not a step**

---

# 🚨 Anti-Patterns

## ❌ Linear Thinking
```
Step 1 → Step 2 → Step 3 → Done
```

## ✅ Correct Model
```
Loop → Adapt → Loop → Adapt
```

---

## ❌ Over-Engineering
- Too many layers
- Premature abstraction
- Heavy frameworks

## ✅ Preferred
- Minimal primitives
- Composable thinking
- Incremental evolution

---

# 🔁 Greenfield → Brownfield Rule

> Every implemented system becomes the new **Mission** for the next iteration.

---

# 🧠 One-Line Mental Model

> Move from current state to target state through gap identification, structured action, and continuous learning.

---

# ✅ Key Design Principles

- Loop over process
- Simplicity over completeness
- Memory-driven evolution
- Structure enables creativity (not restricts it)
