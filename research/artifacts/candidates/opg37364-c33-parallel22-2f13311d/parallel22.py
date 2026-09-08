"""Exact edge-instance controls for C33; finite checks, not a root verifier.
Standard library only. A cycle code is (left, right, smaller_colour, larger_colour).
An incidence witness is an UNORDERED pair, represented in increasing code order.
"""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, factorial
import json
import sys


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def falling(n, k):
    ans = 1
    for i in range(k):
        ans *= max(0, n-i)
    return ans


def cycles(omega, n):
    buckets = {}
    for c, pi in enumerate(omega):
        for x, y in enumerate(pi):
            buckets.setdefault((x, y), []).append(c)
    return sorted((x, y, a, b) for (x, y), cs in buckets.items()
                  for a, b in combinations(cs, 2))


def shape(a, b):
    if a == b:
        raise ValueError('A witness must use two distinct cycles')
    if a[0] == b[0] and a[1] == b[1]:
        return 'T' if len(set(a[2:]) & set(b[2:])) == 1 else 'Q'
    if a[0] == b[0]:
        return 'L'
    if a[1] == b[1]:
        return 'R'
    return None


def constraints(a, b):
    """Repeated identical coloured pairs are a SET, not extra constraints."""
    out = {}
    for x, y, c, d in (a, b):
        for j in (c, d):
            out.setdefault(j, set()).add((x, y))
    return out


def assignment_count(n, q, requirements):
    """General compatible-prescription formula; no independence of slots."""
    ans = 1
    for c in range(q):
        pairs = set(requirements.get(c, ()))
        if any(not (0 <= x < n and 0 <= y < n) for x, y in pairs):
            return 0
        if len({x for x, _ in pairs}) != len(pairs):
            return 0
        if len({y for _, y in pairs}) != len(pairs):
            return 0
        ans *= factorial(n-len(pairs))
    return ans


def witness_counts(n, q):
    return {'T': 3*choose(q, 3)*n*n,
            'Q': 3*choose(q, 4)*n*n,
            'L': 3*choose(q, 4)*n*n*max(0, n-1),
            'R': 3*choose(q, 4)*n*n*max(0, n-1)}


def incidence_formula(n, q):
    """Exact cardinality of tuple--overlapping-two-cycle-pair incidences."""
    if n == 0:
        return 0
    z = factorial(n)**q
    wc = witness_counts(n, q)
    mass = Fraction(wc['T'], n**3) + Fraction(wc['Q']+wc['L']+wc['R'], n**4)
    ans = z*mass
    assert ans.denominator == 1
    return ans.numerator


def one_case(n, q):
    pis = tuple(permutations(range(n)))
    frequencies = Counter()
    hist = Counter()
    bad = 0
    single_count = 0
    checked = 0
    for omega in product(pis, repeat=q):
        cs = cycles(omega, n)
        single_count += len(cs)
        seen = []
        for a, b in combinations(cs, 2):
            kind = shape(a, b)
            if kind is None:
                continue
            req = constraints(a, b)
            assert all(len(v) == 1 for v in req.values())
            assert len(req) == (3 if kind == 'T' else 4)
            if kind in ('L', 'R'):
                assert not (set(a[2:]) & set(b[2:]))
            witness = (a, b)
            frequencies[witness] += 1
            hist[kind] += 1
            seen.append(witness)
        bad += bool(seen)
        # A section chooses the least witness; projection sends it back to omega.
        if seen:
            chosen = min(seen)
            assert chosen in frequencies and shape(*chosen) is not None
        checked += 1
    z = factorial(n)**q
    assert checked == z
    assert bad <= sum(hist.values()) == incidence_formula(n, q)
    if n:
        assert single_count == choose(q, 2)*z
        assert Counter(shape(*w) for w in frequencies) == Counter({k:v for k,v in witness_counts(n,q).items() if v})
    for (a, b), count in frequencies.items():
        assert count == assignment_count(n, q, constraints(a, b))
    return {'N': n, 'q': q, 'tuples': z, 'bad_union': bad,
            'incidences': sum(hist.values()), 'by_shape': dict(sorted(hist.items())),
            'feasible_witnesses': len(frequencies), 'single_2cycle_incidences': single_count}


def hit_controls(max_n):
    cases = 0
    for n in range(max_n+1):
        pis = tuple(permutations(range(n)))
        for k in range(n+1):
            for us in combinations(range(n), k):
                for mask in range(1 << n):
                    target = {i for i in range(n) if mask >> i & 1}
                    exact = sum(all(pi[x] in target for x in us) for pi in pis)
                    assert exact == falling(len(target), k)*factorial(n-k)
                    p = Fraction(exact, factorial(n))
                    p2 = Fraction(1)
                    for i in range(k):
                        p2 *= Fraction(len(target)-i, n-i)
                    assert p == p2
                    rhs = Fraction(len(target), n)**k if n else Fraction(1)
                    assert p <= rhs
                    cases += 1
    return cases


def mutations():
    out = []
    def reject(name, bad_value, correct_value):
        assert bad_value != correct_value
        out.append({'id': name, 'incorrect': str(bad_value), 'correct': str(correct_value), 'detected': True})
    # The two witnesses below are genuine edge-instance pairs, with repeated common edge.
    a, b = (0,0,0,1), (0,0,0,2)
    reject('M01-repeated-common-edge-counted-twice', Fraction(1,2**4), Fraction(assignment_count(2,3,constraints(a,b)),factorial(2)**3))
    reject('M02-same-input-two-distinct-outputs', Fraction(1,9), Fraction(assignment_count(3,1,{0:{(0,0),(0,1)}}),factorial(3)))
    reject('M03-two-inputs-singleton-target-b-less-k', Fraction(1,9), Fraction(assignment_count(3,1,{0:{(0,0),(1,0)}}),factorial(3)))
    reject('M04-distinct-prescribed-pairs-not-independent', Fraction(1,9), Fraction(assignment_count(3,1,{0:{(0,0),(1,1)}}),factorial(3)))
    reject('M05-two-hit-slots-with-replacement', Fraction(4,9), Fraction(falling(2,2)*factorial(1),factorial(3)))
    reject('M06-incidence-equals-bad-union', incidence_formula(1,4), 1)
    reject('M07-ordered-instead-of-unordered-cycle-pair', 2*incidence_formula(1,4), incidence_formula(1,4))
    reject('M08-omit-Q-from-exact-incidence', 3*choose(4,3), incidence_formula(1,4))
    cs = cycles(((0,1),(0,1)),2)
    reject('M09-single-two-cycle-treated-as-overlap', bool(cs), any(shape(a,b) for a,b in combinations(cs,2)))
    cs = cycles(((0,1),(0,1),(1,0),(1,0)),2)
    actual = Counter(shape(a,b) for a,b in combinations(cs,2) if shape(a,b))
    reject('M10-omit-one-endpoint-forks', 0, actual['L']+actual['R'])
    reject('M11-merge-coloured-parallel-edges', 0, choose(4,2))
    reject('M12-allow-identical-cycle-pair', incidence_formula(1,4)+choose(4,2), incidence_formula(1,4))
    # Conflicting same-coordinate forks are NOT covered by singleton-slot independence.
    reject('M13-left-fork-reusing-coordinate', Fraction(1,16), Fraction(assignment_count(2,3,constraints((0,0,0,1),(0,1,0,2))),8))
    reject('M14-right-fork-reusing-coordinate', Fraction(1,16), Fraction(assignment_count(2,3,constraints((0,0,0,1),(1,0,0,2))),8))
    return out


def main():
    inp = json.load(open(sys.argv[1], encoding='utf-8'))
    results = [one_case(*case) for case in inp['cases']]
    nc = hit_controls(inp['max_hit_N'])
    ms = mutations()
    assert 3*choose(24,3)+6*choose(24,4) == 69828
    assert 3*choose(24,4) == 31878
    print(json.dumps({'scope':'finite controls only; candidate_only',
          'cases':results, 'total_enumerated_tuples':sum(r['tuples'] for r in results),
          'hit_count_cases':nc, 'mutations':ms,
          'q24_formula':'Pr(Bad22) <= 69828/N - 31878/N^2 < 69828/N (N>=1)',
          'general_proof':'proof.md, not extrapolation from this execution'}, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
