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
* **Algorithm:** Quantum Annealing
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

* **Motivation:** 
    * Problem–Method Alignment:
The objective 

Q naturally defines an energy landscape with many local minima. Annealing-based methods are well suited for exploring such landscapes and escaping local optima.
    *  GPU Friendliness:
The core operations of annealing—energy evaluation, local updates, acceptance tests, and replica evolution—are highly parallelizable and map naturally to GPU execution.
    * Scalability:
By running thousands of annealing replicas and parameter schedules simultaneously, we trade depth for width, achieving faster time-to-solution through parallel sampling.

### Literature Review

Variational Quantum Annealing for Quantum Chemistry Ka-Wa Yip, Kübra Yeter-Aydeniz, Sijia S. Dong et al.,https://doi.org/10.48550/arXiv.2503.15473 this paper introduce a variational quantum annealing (VarQA) algorithm for electronic structure theory, in which we use the quantum annealer as a sampler and prepare an ansatz state through its statistics. We also introduce a strategy called the "digitizer" for searching the space of variational parameters efficiently. We demonstrate the effectiveness of VarQA by evaluating the ground-state potential energy surface for molecules with up to 20 spin orbitals as well as an excited-state potential energy surface. This approach resembles the workings of the quantum Boltzmann Machines (QBMs), but is generalized to handle distributions beyond the Boltzmann distribution. In VarQA, with the number of required logical qubits equal to the number of spin orbitals, a fully connected Ising Hamiltonian can be readily implemented in a large-scale quantum annealer as a scalable ansatz for electronic structure calculations.

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
   The clssical MTS provided in the totourial is run sequentially. We try to implement it on GPU, which can apply parallel accerating

### Hardware Targets
* **Dev Environment:**  Qbraid (CPU) for logic, Brev L4 for initial GPU testing.
* **Production Environment:** 4 nodes with 8x H100-80GB GPUs per node for final N=38 benchmarks.

---

## 4. The Verification Plan
**Owner:** Ming RU Liu

### Unit Testing Strategy
* **Framework:** ruff, mypy

   
### Core Correctness Checks

** Check 1 (Exact energy)

The table in the references: T. Packebusch and S. Mertens, "Low autocorrelation binary sequences",
Journal of Physics A: Mathematical and Theoretical.
49, 165001 (2016).

Test N = 10, the energy E = 13 etc.

** Check 2 (blocks in equation B3)

We print the circuit of two qubits rotations and four qubits rotations to make sure the decompsition of the circuit is valid.

## 5. Execution Strategy & Success Metrics
**Owner:** Ming Chin Ho

### Agentic Workflow

IDE: VS Code

### Success Metrics
 ＊Metric 1 (Approximation): Obtain Merit Factor F = N² / (2E) > 6.0 for N=40.
 
 ＊Metric 2 (Speedup): Achieve 10× speedup for classical MTS.
 
 ＊Metric 3 (Scalability): Successfully execute GQE-MTS for N =35,40,45.
 
 ＊Metric 4 (Quantum Advantage): Ｑuantum seed demonstrates advantages over random initialization.

### Visualization Plan
*Plot 1: Solution Time as a Function of Problem Size (N) Across CPU and GPU Architectures.
Plot 2: Convergence Rate (Energy vs Iteration) for Quantum vs Random vs Classical.
---

## 6. Resource Management Plan
**Owner:** GPU Acceleration PIC 

* **Plan:** 
    * All development will be conducted on Qbraid using CPU resources until all unit tests pass. Brev will be used only for proof-of-concept validation, after which final benchmarking will be performed on local hardware.
The GPU Acceleration PIC is responsible for manually shutting down the Brev instance whenever the team is not actively working.
