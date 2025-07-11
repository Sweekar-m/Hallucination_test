Sure bro, here's a clean and clear README.md for your LLM Intent Routing Framework — meant for showcasing the project (not SoulOS), highlighting the modular multi-LLM architecture, zero hallucination focus, and test achievements.
# 💡 Modular LLM Intent Routing Framework (Zero-Hallucination)

This is a scalable, modular intent-routing framework built using **multi-LLM architecture** with **intent clustering**, designed to reduce hallucinations even at high scale (100+ intents).

Unlike traditional agent frameworks, this project focuses on **precision**, **parallel execution**, and **layered classification** to maintain **zero hallucination** behavior even under complex routing.

---

## 🚀 Features

- ✅ Modular architecture using **Layered LLMs**
- 🧠 Intent clustering for reduced cognitive overload
- ⚡️ Parallel LLM execution using Python threading
- ❌ Zero hallucination (95.7%+ accuracy in real-world test)
- 🔍 Unknown fallback for unmatched prompts
- 📁 Easy to scale: 100 → 1000 intents with cluster hierarchy
- 🧪 Tested with Gemini  API

---

## 🧱 Architecture

## 🧠 Architecture Design

This project follows a modular, parallel LLM-based architecture designed to **minimize hallucination**, **improve intent accuracy**, and **scale with hundreds of tools**.

### 🔧 Key Components

```
                      +-------------------------------+
                      | Parallelly passing user input |
                      +---------------+---------------+
                                      |
          +---------------------------+--------------------------+
          |                                                      |
   +--------------+                                       +--------------+
   |   LLM:       |                                       |   LLM:       |
   | Create_ops   |                                       | System_ops   |
   +------+-------+                                       +------+-------+
          |                                                      |
   +------v-------+                                       +------v-------+
   | Create Router|                                       | System Router|
   +------v-------+                                       +------v-------+
          |                                                      |
   +------v-------+                                       +------v-------+
   |  Response    |                                       |  Response    |
   +--------------+                                       +--------------+
```

### ⚙️ How it Works

- **Parallel Input Dispatch:**  
  User input is simultaneously sent to multiple LLM clusters (e.g., `Create_ops`, `System_ops`) using multi-threading.  

- **Cluster-Level LLMs:**  
  Each LLM is specialized for a category of operations and holds its own set of tightly scoped intents and prompt structure.

- **Dedicated Routers:**  
  Once an LLM classifies an intent, it passes control to a category-specific router (like creating files, launching apps, etc.)

- **Isolated Response Handling:**  
  Each cluster handles its own logic and tools, then returns

### Example:
- Layer 1: Classifies as `file_ops` cluster
- Layer 2: Routes to `create_json` intent
- Layer 3: Calls tool or 3rd LLM for file generation

---

## 📊 Testing Report

- **Total Intents:** 200
- **Test Cases:** 140 random natural prompts
- **Accuracy:** 95.7%
- **Hallucinations:** 0
- **Mismatches:** 6 (due to incomplete/ambiguous prompt)
- **Notes:** Even mismatches were caught via fallback `"unknown"` intent logic.

---

## 🛠️ Tech Stack

- Python 3.10+
- Google Gemini API (2.5 Pro Vision)
- Multithreaded execution (for parallel routing)
- JSON-based test framework


---


🧠 Why This Matters
Large LLMs often fail when loaded with too many instructions. This framework:

Breaks down intent handling using cluster-first architecture
Leverages multiple smaller prompts instead of one long, brittle one
Enables zero hallucination routing even as scale increases




