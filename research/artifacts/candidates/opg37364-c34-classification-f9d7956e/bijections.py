"""C34: explicit local-index bijections, not a native Lean verifier.

The exhaustive run ranges over all colours in the fixed palette and all
endpoint-equality types of two 2-cycles. It does NOT enumerate large graphs,
prove a Lean theorem, or sample permutations. Arbitrary-N transport still
uses the separate, written endpoint-renaming argument.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb, factorial
import json

@dataclass(frozen=True, order=True)
class Cycle:
    x: int
    y: int
    colours: tuple[int, int]

    def __post_init__(self) -> None:
        if min(self.x, self.y) < 0 or len(self.colours) != 2:
            raise ValueError("invalid cycle code")
        if not 0 <= self.colours[0] < self.colours[1]:
            raise ValueError("colours are a strictly increasing two-set")

Witness = tuple[Cycle, Cycle]
Index = tuple

@dataclass(frozen=True)
class Conflict:
    side: str
    colour: int
    first: tuple[int, int]
    second: tuple[int, int]


def canonical(s: Cycle, t: Cycle) -> Witness:
    if s == t:
        raise ValueError("two DISTINCT cycles required")
    if s.x != t.x and s.y != t.y:
        raise ValueError("vertex-disjoint pairs are not Bad22 witnesses")
    return tuple(sorted((s, t)))


def encode(w: Witness) -> Index | Conflict:
    """Decode a graph-defined unordered witness into its unique index."""
    s, t = canonical(*w)
    a, b = set(s.colours), set(t.colours)
    shared = a & b
    union = tuple(sorted(a | b))
    if s.x == t.x and s.y == t.y:
        if len(shared) == 1:
            common = next(iter(shared))
            assert len(union) == 3
            return ("T", s.x, s.y, union, union.index(common))
        if shared:
            raise AssertionError("distinct two-sets cannot share both colours")
        first_colour = union[0]
        containing = a if first_colour in a else b
        partner = next(iter(containing - {first_colour}))
        return ("Q", s.x, s.y, union, union.index(partner))
    if shared:
        c = min(shared)
        return Conflict("input" if s.x == t.x else "output", c,
                        (s.x, s.y), (t.x, t.y))
    if s.x == t.x:
        lo, hi = sorted((s, t), key=lambda z: z.y)
        chosen = tuple(union.index(c) for c in lo.colours)
        return ("L", s.x, lo.y, hi.y, union, chosen)
    lo, hi = sorted((s, t), key=lambda z: z.x)
    chosen = tuple(union.index(c) for c in lo.colours)
    return ("R", s.y, lo.x, hi.x, union, chosen)


def decode(i: Index) -> Witness:
    """Encode a typed T/Q/L/R index as an actual unordered cycle pair."""
    tag = i[0]
    if tag in ("T", "Q"):
        _, x, y, palette, mark = i
        if tuple(sorted(set(palette))) != palette:
            raise ValueError("palette is an increasing set")
        if tag == "T":
            if len(palette) != 3 or mark not in range(3):
                raise ValueError("T needs three colours and one marked common colour")
            common = palette[mark]
            a, b = [c for c in palette if c != common]
            return canonical(Cycle(x, y, tuple(sorted((common, a)))),
                             Cycle(x, y, tuple(sorted((common, b)))))
        if len(palette) != 4 or mark not in (1, 2, 3):
            raise ValueError("Q needs four colours and a nonfirst partner")
        a = (palette[0], palette[mark])
        b = tuple(c for c in palette if c not in a)
        return canonical(Cycle(x, y, a), Cycle(x, y, b))
    if tag not in ("L", "R"):
        raise ValueError("unknown shape")
    _, centre, lo, hi, palette, chosen = i
    if not lo < hi or len(palette) != 4 or tuple(sorted(set(palette))) != palette:
        raise ValueError("invalid ordered endpoint pair or palette")
    if len(chosen) != 2 or not 0 <= chosen[0] < chosen[1] < 4:
        raise ValueError("choose two of the four colours")
    a = tuple(palette[j] for j in chosen)
    b = tuple(c for c in palette if c not in a)
    if tag == "L":
        return canonical(Cycle(centre, lo, a), Cycle(centre, hi, b))
    return canonical(Cycle(lo, centre, a), Cycle(hi, centre, b))


def requirements(w: Witness) -> dict[int, frozenset[tuple[int, int]]]:
    """A SET in each coordinate: a shared edge is only one constraint."""
    ans: dict[int, set[tuple[int, int]]] = {}
    for s in w:
        for c in s.colours:
            ans.setdefault(c, set()).add((s.x, s.y))
    return {c: frozenset(pairs) for c, pairs in ans.items()}


def extension_count(n: int, q: int, req: dict[int, frozenset[tuple[int, int]]]) -> int:
    """Counts fixed corresponding pairs, not arbitrary hits into their range."""
    if n < 0 or q < 0:
        raise ValueError("negative size")
    out = 1
    for c in range(q):
        pairs = req.get(c, frozenset())
        if any(not (0 <= x < n and 0 <= y < n) for x, y in pairs):
            raise ValueError("out of domain")
        xs, ys = {x for x, _ in pairs}, {y for _, y in pairs}
        if len(xs) != len(pairs) or len(ys) != len(pairs):
            return 0
        out *= factorial(n - len(pairs))
    return out


def index_stream(q: int):
    for palette in combinations(range(q), 3):
        for mark in range(3):
            yield ("T", 0, 0, palette, mark)
    for palette in combinations(range(q), 4):
        for mark in (1, 2, 3):
            yield ("Q", 0, 0, palette, mark)
        for chosen in combinations(range(4), 2):
            yield ("L", 0, 0, 1, palette, chosen)
            yield ("R", 0, 0, 1, palette, chosen)


def cycle_data(w: Witness):
    return [[s.x, s.y, list(s.colours)] for s in w]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    args = ap.parse_args()
    config = json.load(open(args.input, encoding="utf-8"))
    q = config["q"]
    if q != 24:
        raise ValueError("this frozen run is exactly the C20 palette of 24 colours")
    pairs = list(combinations(range(q), 2))
    digest = sha256()
    counters = Counter()
    checks = 0
    expected_index_counts = {"T": 3 * comb(q, 3), "Q": 3 * comb(q, 4),
                             "L": 6 * comb(q, 4), "R": 6 * comb(q, 4)}
    # Exhaust the whole colour palette and endpoint equality types. For same
    # endpoints canonical cycle order removes orientation once and only once.
    for a, b in combinations(pairs, 2):
        w = canonical(Cycle(0, 0, a), Cycle(0, 0, b))
        code = encode(w)
        assert not isinstance(code, Conflict)
        assert decode(code) == w and encode(tuple(reversed(w))) == code
        counters[code[0]] += 1
        req = requirements(w)
        d = 3 if code[0] == "T" else 4
        assert len(req) == d and all(len(v) == 1 for v in req.values())
        checks += 4
        digest.update((repr((code, cycle_data(w))) + "\n").encode())
    for tag in ("L", "R"):
        for a, b in product(pairs, repeat=2):
            w = (canonical(Cycle(0, 0, a), Cycle(0, 1, b)) if tag == "L"
                 else canonical(Cycle(0, 0, a), Cycle(1, 0, b)))
            code = encode(w)
            req = requirements(w)
            if isinstance(code, Conflict):
                assert extension_count(2, q, req) == 0
                assert code.side == ("input" if tag == "L" else "output")
                counters[tag + "_zero"] += 1
                checks += 2
            else:
                assert code[0] == tag and decode(code) == w
                assert encode(tuple(reversed(w))) == code
                assert len(req) == 4 and all(len(v) == 1 for v in req.values())
                # Fixed-support exact factorial count: no tuple or slot sample.
                assert extension_count(2, q, req) == factorial(1)**4 * factorial(2)**20
                counters[tag] += 1
                checks += 5
            digest.update((repr((code, cycle_data(w))) + "\n").encode())
    inverse_counts = Counter()
    for code in index_stream(q):
        w = decode(code)
        assert encode(w) == code
        inverse_counts[code[0]] += 1
        checks += 1
    assert dict(inverse_counts) == expected_index_counts
    assert {t: counters[t] for t in expected_index_counts} == expected_index_counts
    checks += 2
    # Disjoint endpoints are outside this bad event, whatever their colours.
    for a, b in product(pairs, repeat=2):
        try:
            canonical(Cycle(0, 0, a), Cycle(1, 1, b))
        except ValueError:
            counters["disjoint_excluded"] += 1
        else:
            raise AssertionError("disjoint-cycle mass leaked into Bad22")
        checks += 1
    for a in pairs:
        try:
            canonical(Cycle(0, 0, a), Cycle(0, 0, a))
        except ValueError:
            counters["diagonal_excluded"] += 1
        else:
            raise AssertionError("diagonal witness allowed")
        checks += 1
    # Explicit finite witnesses to incorrect interfaces. These do not attack
    # the original conventional proof, which already excluded these variants.
    t = canonical(Cycle(0, 0, (0, 1)), Cycle(0, 0, (0, 2)))
    n = 3
    actual = Fraction(extension_count(n, q, requirements(t)), factorial(n)**q)
    controls = {
        "shared_edge_is_three_not_four_constraints": actual == Fraction(1, n**3) != Fraction(1, n**4),
        "same_input_distinct_outputs_zero": extension_count(3, 1, {0:frozenset({(0,0),(0,1)})}) == 0,
        "distinct_inputs_singleton_target_zero": extension_count(3, 1, {0:frozenset({(0,0),(1,0)})}) == 0,
        "duplicated_identical_pair_is_one": extension_count(3,1,{0:frozenset([(0,0),(0,0)])}) == factorial(2),
        "fixed_pairs_not_two_target_hit": factorial(3-2) != 2*factorial(3-2),
        "q_same_endpoints_is_not_t": encode(canonical(Cycle(0,0,(0,1)), Cycle(0,0,(2,3))))[0] == "Q",
        "unrestricted_witness_not_four_feasible_classes": isinstance(encode(canonical(Cycle(0,0,(0,1)),Cycle(0,1,(0,2)))), Conflict),
        "incidence_not_union_n1": 3*comb(24,3)+3*comb(24,4) == 37950 != 1,
    }
    assert all(controls.values())
    # Exact rational reduction of the four class coefficients, not a total
    # short-cycle probability or an independent source of graph existence.
    tcoef, qcoef, lrcoef = expected_index_counts['T'], expected_index_counts['Q'], expected_index_counts['L']
    assert tcoef+lrcoef == 69828 and qcoef-lrcoef == -31878
    checks += len(controls)+1
    out = {
        "format":"r10-c34-complete-colour-atlas-v1", "verdict":"candidate_only",
        "q":q,"colour_pairs":len(pairs),"witness_direction_counts":dict(counters),
        "index_direction_counts":dict(inverse_counts),"assertions":checks,
        "canonical_mapping_stream_sha256":digest.hexdigest(),"negative_controls":controls,
        "symbolic_cardinalities":{
            "T":"6072*N^2", "Q":"31878*N^2", "L":"63756*N*choose(N,2)",
            "R":"63756*N*choose(N,2)",
            "incidence_over_sample":"69828/N-31878/N^2 (N>=1)",
        },
        "scope":[
            "All 24-colour local choices and all endpoint equality types, not small graph samples.",
            "The written support-renaming proof is needed to pass from representatives to arbitrary N.",
            "The program checks the explicit two-way maps; it is not a Lean compiler or trusted verifier.",
            "No whole-catalogue bound, Good tuple or root-family theorem is claimed."
        ]
    }
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
