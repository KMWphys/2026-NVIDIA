## AI Report

### 1. The Workflow

We primarily used **ChatGPT** and **Gemini** as AI assistants throughout the project, their main roles were to generate example code, help supplement prerequisite knowledge, and assist in drafting descriptive text.

Rather than directly adopting AI-generated outputs, our team was responsible for modifying the generated content, organizing all components into a coherent structure, and carefully reviewing the logic and consistency of the overall implementation. All architectural decisions and final integrations were handled manually to ensure correctness.

This workflow allowed us to leverage AI for efficiency while maintaining full human control over the system design and logical validity.

---

### 2. Verification Strategy

We validated the AI-generated code by running and testing it locally using VS Code, the code was executed in the intended development environment, where we checked for syntax errors, runtime errors. 

We also verified that the outputs matched expected results and iteratively fixed any issues identified during execution, this hands-on testing ensured the generated code was functional and reliable.

---

### 3. The "Vibe" Log

#### Win

Objectively, it would have been difficult to independently complete the full code implementation within a single day.  
In this regard, AI provided substantial assistance by offering initial code structures and examples, which significantly reduced development time. This allowed us to focus more on refining the logic and integrating the system rather than starting entirely from scratch.

#### Learn

Through this process, we learned that effectively using AI-generated content requires skill and critical thinking.  
Instead of blindly trusting AI outputs, it is important to understand the underlying logic and structure of the generated solutions. Actively analyzing and adapting AI suggestions proved to be far more effective than passive acceptance.

#### Fail

AI-generated code was not always correct and occasionally contained errors. For example, issues arose when generating qubit gate implementations, where the produced code did not fully match the expected behavior. In such cases, we needed to identify the source of the problem and provide clearer, more precise instructions to guide the AI toward a correct solution.

#### Context Dump

Below is an example of the context and instructions provided to the AI during development:

> "Let me verify the case. I use quantum annealing to generate a bitstring, i.e., an eigenstate of the Ising Hamiltonian, and repeat this procedure several times to create a population for performing MTS. Then we execute MTS to obtain the final result.  
> The overall algorithm for solving the LABS problem is hybrid: the quantum part is used to generate the population, which is then processed by classical MTS."

This description was provided to guide AI understanding of the workflow and to ensure that generated code and explanations aligned with the intended hybrid quantum-classical approach.

