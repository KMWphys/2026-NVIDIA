# Product Requirements Document (PRD)

**Project Name:** [e.g., LABS-Solv-V1]
**Team Name:** [e.g., QuantumVibes]
**GitHub Repository:** [Insert Link Here]

---

> **Note to Students:** > The questions and examples provided in the specific sections below are **prompts to guide your thinking**, not a rigid checklist. 
> * **Adaptability:** If a specific question doesn't fit your strategy, you may skip or adapt it.
> * **Depth:** You are encouraged to go beyond these examples. If there are other critical technical details relevant to your specific approach, please include them.
> * **Goal:** The objective is to convince the reader that you have a solid plan, not just to fill in boxes.

---

## 1. Team Roles & Responsibilities [You can DM the judges this information instead of including it in the repository]

| Role | Name | GitHub Handle | Discord Handle
| :--- | :--- | :--- | :--- |
| **Project Lead** (Architect) | Kai Ming Wu | KMWphys | wukyle0608 |
| **GPU Acceleration PIC** (Builder) | Yi Xin Zhan | YI-XIN-Zhan| yudimao |
| **GPU Acceleration PIC** (Builder) | Hsiang Heng Liu | seanliugo-maker| wau_constant_55914 |
| **Quality Assurance PIC** (Verifier) | Ming RU Liu | Mingru | liumr1 |
| **Technical Marketing PIC** (Storyteller) | Ming Chin Ho | DraemiusHo| mcho0208 |

---

## 2. The Architecture
**Owner:** Kai Ming Wu

### Choice of Quantum Algorithm
* **Algorithm:** [Quantum Annealing]
    * An annealing-based optimization approach, inspired by quantum annealing / adiabatic evolution, implemented as a GPU-accelerated annealing simulation.
The method targets direct minimization of the objective function 
Q, which is formulated as an Ising / QUBO-style energy landscape.

  * Annealing Schedule / Ansatz:
We use a parameterized annealing schedule 
s
(
t
)
∈
[
0
,
1
]
, evolving from a driver term to the problem Hamiltonian.
The schedule is discretized into a small number of segments (piecewise-constant or piecewise-linear), keeping the parameter count low and optimization stable.
Multiple annealing paths and random initial states are evaluated in parallel.

* **Motivation:** [Why this algorithm? Connect it to the problem structure or learning goals.]
    * Problem–Method Alignment:
The objective 
Q
Q naturally defines an energy landscape with many local minima. Annealing-based methods are well suited for exploring such landscapes and escaping local optima.
    *  GPU Friendliness:
The core operations of annealing—energy evaluation, local updates, acceptance tests, and replica evolution—are highly parallelizable and map naturally to GPU execution.
    * Scalability:
By running thousands of annealing replicas and parameter schedules simultaneously, we trade depth for width, achieving faster time-to-solution through parallel sampling.

### Literature Review
* **Reference:** 
* **Relevance:** 
---

## 3. The Acceleration Strategy
**Owner:** YI-XIN-Zhan| Hsiang Heng Liu

### Quantum Acceleration (CUDA-Q)
* **Strategy:** CUDA-Q is used to support and validate annealing-inspired quantum workflows and simulations:

  *For digitized annealing, CUDA-Q executes parameterized circuits corresponding to discretized annealing steps, evaluated in batch across multiple schedules and seeds.

   *For annealing simulations, CUDA-Q is used to validate small-scale quantum-inspired evolution and benchmark against classical annealing results.

Parallelization Approach:

 *Multi-seed parallelism: Evaluate many random initial states simultaneously.
 
  *Multi-schedule parallelism: Test multiple annealing schedules in parallel.
 
  *Replica-based parallelism: Run independent replicas to estimate success probabilities and best-energy distributions.

### Classical Acceleration (MTS)
* **Strategy:**

  ＊ The annealing engine is fully GPU-accelerated, with the following components implemented as GPU kernels:
Energy Evaluation Kernel:

Computes the Ising/QUBO energy efficiently using vectorized and memory-coalesced operations.

  ＊Batch Neighbor Proposals:

Generates and evaluates many candidate bit flips in parallel, computing 
Δ
E
ΔE using local updates.

  ＊Acceptance and RNG:

Acceptance decisions are computed on-GPU using parallel random number generation, avoiding CPU–GPU synchronization.

  ＊Replica Exchange (Optional):

Parallel tempering is implemented by periodically swapping replicas at different effective temperatures to improve global exploration.
Computes the Ising/QUBO energy efficiently using vectorized and memory-coalesced operations.
* **SHardware Targets:**
* **Dev Environment:** 
* **Production Environment:** 

---

## 4. The Verification Plan
**Owner:** Ming RU Liu

### Unit Testing Strategy
* **Framework:** [e.g., `pytest`, `unittest`]
* **AI Hallucination Guardrails:** [How do you know the AI code is right?]
    * *Example:* "We will require AI-generated kernels to pass a 'property test' (Hypothesis library) ensuring outputs are always within theoretical energy bounds before they are integrated."

### Core Correctness Checks
* **Check 1 (Symmetry):** [Describe a specific physics check]
    * *Example:* "LABS sequence $S$ and its negation $-S$ must have identical energies. We will assert `energy(S) == energy(-S)`."
* **Check 2 (Ground Truth):**
    * *Example:* "For $N=3$, the known optimal energy is 1.0. Our test suite will assert that our GPU kernel returns exactly 1.0 for the sequence `[1, 1, -1]`."

---

## 5. Execution Strategy & Success Metrics
**Owner:** Technical Marketing PIC

### Agentic Workflow
* **Plan:** [How will you orchestrate your tools?]
    * *Example:* "We are using Cursor as the IDE. We have created a `skills.md` file containing the CUDA-Q documentation so the agent doesn't hallucinate API calls. The QA Lead runs the tests, and if they fail, pastes the error log back into the Agent to refactor."

### Success Metrics
* **Metric 1 (Approximation):** [e.g., Target Ratio > 0.9 for N=30]
* **Metric 2 (Speedup):** [e.g., 10x speedup over the CPU-only Tutorial baseline]
* **Metric 3 (Scale):** [e.g., Successfully run a simulation for N=40]

### Visualization Plan
* **Plot 1:** [e.g., "Time-to-Solution vs. Problem Size (N)" comparing CPU vs. GPU]
* **Plot 2:** [e.g., "Convergence Rate" (Energy vs. Iteration count) for the Quantum Seed vs. Random Seed]

---

## 6. Resource Management Plan
**Owner:** GPU Acceleration PIC 

* **Plan:** [How will you avoid burning all your credits?]
    * *Example:* "We will develop entirely on Qbraid (CPU) until the unit tests pass. We will then spin up a cheap L4 instance on Brev for porting. We will only spin up the expensive A100 instance for the final 2 hours of benchmarking."
    * *Example:* "The GPU Acceleration PIC is responsible for manually shutting down the Brev instance whenever the team takes a meal break."
