# labs_energy.py
from typing import List
from dataclasses import dataclass

def bits01_to_pm1(bits):
    # 0 -> +1, 1 -> -1
    return [1 if b == 0 else -1 for b in bits]

def labs_energy_pm1(s: List[int]) -> int:
    """
    LABS energy:
        E = sum_{k=1}^{N-1} (sum_i s_i s_{i+k})^2
    """
    n = len(s)
    E = 0
    for k in range(1, n):
        ck = 0
        for i in range(n - k):
            ck += s[i] * s[i + k]
        E += ck * ck
    return E

@dataclass
class PauliTerm:
    word: str     # e.g. "IZZIZ"
    coeff: float

def labs_ising_terms_Z(N: int):
    """
    Generate Z-only Ising terms whose minimum matches LABS minimum
    (constant offsets ignored).
    """
    terms = []

    for k in range(1, N):
        pairs = [(i, i + k) for i in range(N - k)]
        for a in range(len(pairs)):
            for b in range(a + 1, len(pairs)):
                i1, i2 = pairs[a]
                j1, j2 = pairs[b]
                word = ["I"] * N
                for idx in (i1, i2, j1, j2):
                    word[idx] = "Z"
                terms.append(PauliTerm("".join(word), 2.0))

    return terms
# qa_anneal.py
import cudaq
from labs_energy import bits01_to_pm1, labs_energy_pm1

@cudaq.kernel
def qa_anneal_kernel(
    num_qubits: int,
    terms_words: list[str],
    terms_coeffs: list[float],
    total_time: float,
    steps: int
):
    q = cudaq.qvector(num_qubits)

    # |+>^N
    for i in range(num_qubits):
        h(q[i])

    dt = total_time / steps

    for m in range(steps):
        s = (m + 1) / steps
        A = 1.0 - s
        B = s

        # Mixer: exp(-i A sum X)
        theta_x = 2.0 * dt * A
        for i in range(num_qubits):
            rx(theta_x, q[i])

        # Problem: exp(-i B H_Ising)
        for j in range(len(terms_words)):
            angle = -dt * B * terms_coeffs[j]

            pauli_ops = []
            for idx, p in enumerate(terms_words[j]):
                if p == "Z":
                    pauli_ops.append(("Z", q[idx]))

            if pauli_ops:
                exp_pauli(angle, pauli_ops)

def sample_anneal_best(
    N,
    terms,
    shots=500,
    total_time=1.0,
    steps=30,
    target="qpp"
):
    cudaq.set_target(target)

    words = [t.word for t in terms]
    coeffs = [t.coeff for t in terms]

    counts = cudaq.sample(
        qa_anneal_kernel,
        N,
        words,
        coeffs,
        total_time,
        steps,
        shots_count=shots
    )

    best_E = None
    best_b = None

    for bitstring, cnt in counts.items():
        bits = [int(b) for b in bitstring]
        s = bits01_to_pm1(bits)
        E = labs_energy_pm1(s)

        if best_E is None or E < best_E:
            best_E = E
            best_b = bitstring

    return best_b, best_E
# test_run.py
from labs_energy import labs_ising_terms_Z
from qa_anneal import sample_anneal_best

N = 6
terms = labs_ising_terms_Z(N)

best_bitstring, best_energy = sample_anneal_best(
    N,
    terms,
    shots=500,
    total_time=1.0,
    steps=30,
    target="qpp"
)

print("Best bitstring:", best_bitstring)
print("LABS energy:", best_energy)
