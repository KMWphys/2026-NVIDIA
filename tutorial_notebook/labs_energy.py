# labs_energy.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

def bits01_to_pm1(bits01: List[int]):   
    return [1 if b == 0 else -1 for b in bits01]
def labs_energy_pm1(s: List[int]) -> int:
    """LABS objective E(s)=sum_{k=1}^{N-1} C_k^2 with s_i in {+1,-1}."""
    n = len(s)
    e = 0
    for k in range(1, n):
        ck = 0
        for i in range(n - k):
            ck += s[i] * s[i + k]
        e += ck * ck
    return e

cong = [1,0,0,1]
print(labs_energy_pm1(bits01_to_pm1(cong)))

@dataclass(frozen=True)
class PauliTerm:
    word: str      # length N string of I/X/Y/Z
    coeff: float   # coefficient in H (we'll treat H as sum coeff * Z...Z)

def labs_ising_terms_Z(N: int) -> List[PauliTerm]:
    """
    Build Z-only Pauli terms whose classical energies reproduce LABS energy
    up to an additive constant / scaling.

    Implementation note:
    - The exact coefficient pattern depends on your chosen mapping convention.
    - For Phase 2 validation, the most important part is INTERNAL CONSISTENCY:
      (i) your classical energy function
      (ii) your Hamiltonian energy evaluation built from these terms
      match on all bitstrings for small N.
    """

    terms: List[PauliTerm] = []
    for k in range(1, N):
        pairs = [(i, i + k) for i in range(N - k)]
        # i<j over pairs
        for a in range(len(pairs)):
            for b in range(a + 1, len(pairs)):
                (i1, i2) = pairs[a]
                (j1, j2) = pairs[b]
                word = ["I"] * N
                for idx in (i1, i2, j1, j2):
                    word[idx] = "Z"
                terms.append(PauliTerm("".join(word), coeff=2.0))

    return terms

def ham_energy_from_terms_pm1(s_pm1: List[int], terms: List[PauliTerm]) -> float:
    """Evaluate sum coeff * product_{Z sites} s_i for Z-only terms."""
    n = len(s_pm1)
    e = 0.0
    for t in terms:
        assert len(t.word) == n
        prod = 1
        for i, p in enumerate(t.word):
            if p == "Z":
                prod *= s_pm1[i]
            elif p != "I":
                raise ValueError("This evaluator supports Z-only terms.")
        e += t.coeff * prod
    return e