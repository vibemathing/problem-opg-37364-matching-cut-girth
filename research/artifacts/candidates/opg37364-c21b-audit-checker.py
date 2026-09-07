"""Bounded exact tests of C20/C22 and C21B; not a universal proof checker.
Standard library only. Run with the companion JSON input. No network.
All graph edges have distinct instance indices until simplicity is checked.
"""
from __future__ import annotations
import hashlib
import itertools as it
import json
import math
import sys
from collections import Counter, deque
from fractions import Fraction as Q
from pathlib import Path

VERSION = "opg37364-c21b-audit-v2"
INF = 1 << 30  # Exact sentinel, above every configured graph order and girth cutoff.
TALLY: Counter[str] = Counter()
MUTATIONS: dict[str, object] = {}


def check(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)
    TALLY[label] += 1


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def coefficients(N: int, a: int, b: int) -> list[int]:
    if N < 1 or not 0 <= a <= N or not 0 <= b <= N:
        raise ValueError("invalid coefficient domain")
    return [choose(a, j) * choose(N-a, b-j) * math.factorial(b)
            * math.factorial(N-b) for j in range(min(a, b)+1)]


def convolve(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def histogram(N: int, a: int, b: int, q: int) -> list[int]:
    c, h = coefficients(N, a, b), [1]
    for _ in range(q):
        h = convolve(h, c)
    return h


def bad_count(N: int, a: int, b: int, q: int) -> int:
    # General q control: q*s-2*t <= 2*s; q=24 is the frozen interface.
    lo = max(0, ((q-2)*(a+b)+1)//2)
    return sum(histogram(N, a, b, q)[lo:])


def incidence(N: int, q: int) -> int:
    return sum((1 if a == b else 2)*choose(N, a)*choose(N, b)
               *bad_count(N, a, b, q)
               for a in range(N+1) for b in range(a, N+1)
               if 1 <= a+b <= N)


def edges_of(tup: tuple[tuple[int, ...], ...], N: int) -> list[tuple[int, int]]:
    return [(u, N+p[u]) for p in tup for u in range(N)]


def boundary(edges: list[tuple[int, int]], s: int) -> int:
    return sum(((s >> u) ^ (s >> v)) & 1 for u, v in edges)


def vertices(edges: list[tuple[int, int]], ids: frozenset[int]) -> set[int]:
    return {v for e in ids for v in edges[e]}


def connected(n: int, edges: list[tuple[int, int]], removed: int | None = None) -> bool:
    vs = [v for v in range(n) if v != removed]
    if not vs:
        return False
    adj = [[] for _ in range(n)]
    for u, v in edges:
        if removed not in (u, v):
            adj[u].append(v); adj[v].append(u)
    seen, stack = {vs[0]}, [vs[0]]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v); stack.append(v)
    return len(seen) == len(vs)


def two_connected(n: int, edges: list[tuple[int, int]]) -> bool:
    return n >= 3 and connected(n, edges) and all(connected(n, edges, v) for v in range(n))


def distances(n: int, edges: list[tuple[int, int]], u: int) -> list[int]:
    adj = [[] for _ in range(n)]
    for x, y in edges:
        adj[x].append(y); adj[y].append(x)
    d, todo = [INF]*n, deque([u]); d[u] = 0
    while todo:
        x = todo.popleft()
        for y in adj[x]:
            if d[y] == INF:
                d[y] = d[x]+1; todo.append(y)
    return d


def girth(n: int, edges: list[tuple[int, int]]) -> int:
    # INF means infinity; unlike n+1 it also exceeds girth cutoffs above the order.
    best = INF
    for i, (u, v) in enumerate(edges):
        if u == v:
            return 1
        d = distances(n, edges[:i]+edges[i+1:], u)[v]
        if d < INF:
            best = min(best, d+1)
    return best


def short_cycles(n: int, edges: list[tuple[int, int]], g: int) -> list[frozenset[int]]:
    out: list[frozenset[int]] = []
    # A connected 2-regular edge-instance subgraph is an unoriented cycle.
    for size in range(2, min(g-1, len(edges))+1):
        for ids0 in it.combinations(range(len(edges)), size):
            deg: Counter[int] = Counter(v for i in ids0 for v in edges[i])
            if not all(x == 2 for x in deg.values()):
                continue
            reached, todo = {edges[ids0[0]][0]}, [edges[ids0[0]][0]]
            adj = {v: [] for v in deg}
            for i in ids0:
                u, v = edges[i]; adj[u].append(v); adj[v].append(u)
            while todo:
                for v in adj[todo.pop()]:
                    if v not in reached:
                        reached.add(v); todo.append(v)
            if len(reached) == len(deg):
                out.append(frozenset(ids0))
    return out


def is_matching(edges: list[tuple[int, int]]) -> bool:
    deg = Counter(v for e in edges for v in e)
    return max(deg.values(), default=0) <= 1


def mc(n: int, edges: list[tuple[int, int]]) -> int | None:
    for s in range(1, (1 << n)-1):
        cross = [e for e in edges if ((s >> e[0]) ^ (s >> e[1])) & 1]
        if is_matching(cross):
            return s
    return None


def simple(edges: list[tuple[int, int]]) -> bool:
    return all(u != v for u, v in edges) and len({tuple(sorted(e)) for e in edges}) == len(edges)


def bipartite(n: int, edges: list[tuple[int, int]]) -> bool:
    col: dict[int, int] = {}; adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for root in range(n):
        if root in col:
            continue
        col[root] = 0; todo = [root]
        while todo:
            u = todo.pop()
            for v in adj[u]:
                if v in col:
                    if col[v] == col[u]:
                        return False
                else:
                    col[v] = 1-col[u]; todo.append(v)
    return True


def subdivide(n: int, kept: list[tuple[int, int]], artificial: list[tuple[int, int]]) -> tuple[int, list[tuple[int, int]]]:
    out = list(kept)
    for i, (u, v) in enumerate(artificial):
        out += [(u, n+i), (v, n+i)]
    return n+len(artificial), out


def arithmetic_tests(cfg: dict) -> dict:
    for N in range(1, cfg["coefficient_max_N"]+1):
        perms = list(it.permutations(range(N)))
        for a in range(N+1):
            for b in range(N+1):
                c = coefficients(N, a, b)
                actual = Counter(sum(p[u] < b for u in range(a)) for p in perms)
                check(c == [actual[j] for j in range(len(c))], "A.coefficient_enumeration")
                check(c == coefficients(N, b, a), "A.inversion_symmetry")
                h = [1]
                for q in range(cfg["recurrence_max_q"]+1):
                    check(sum(h) == math.factorial(N)**q, "A.recurrence_mass")
                    check(len(h) == q*min(a, b)+1, "A.recurrence_support")
                    if q < cfg["recurrence_max_q"]:
                        h = convolve(h, c)
    for N, q in cfg["tuple_enumeration"]:
        perms = list(it.permutations(range(N)))
        shores = [s for s in range(1, (1 << (2*N))-1) if s.bit_count() <= N]
        actual_inc = actual_union = 0
        counts = {(a, b): Counter() for a in range(N+1) for b in range(N+1)}
        for tup in it.product(perms, repeat=q):
            edges = edges_of(tup, N)
            num = sum(boundary(edges, s) <= 2*s.bit_count() for s in shores)
            actual_inc += num; actual_union += bool(num)
            for a, b in counts:
                counts[a, b][sum(p[u] < b for p in tup for u in range(a))] += 1
        for (a, b), h0 in counts.items():
            h = histogram(N, a, b, q)
            check(h == [h0[t] for t in range(len(h))], "A.tuple_recurrence_enumeration")
        check(actual_inc == incidence(N, q), "A.incidence_enumeration")
        check(actual_union <= actual_inc, "A.union_not_incidence")
    for n in range(1, 31):
        for j in range(1, n+1):
            check(choose(n, j)*j**j <= (3*n)**j, "A.binomial_bound")
    bracket = 69984*Q(13, 24)**19
    check(bracket < Q(2, 3), "A.large_shore_constant")
    check(bracket > Q(1, 4), "mutation.old_quarter_bound_rejected")
    theta = 69984*Q(2, 1000)**19
    check(theta < Q(1, 100), "A.small_theta")
    check(4*theta/(1-theta)**2 < Q(1, 20), "A.small_shore_bound")
    for x in [Q(0), Q(1, 100), Q(1, 4), Q(2, 3), Q(99, 100)]:
        for T in range(1, 21):
            lhs = (1-x)**2*sum(a*x**a for a in range(1, T+1))
            check(lhs == x-(T+1)*x**(T+1)+T*x**(T+2) and lhs <= x, "A.finite_sum_identity")
    check(24*Q(5, 6)**64 < Q(1, 1000), "A.finite_tail_constant")
    check(Q(1, 20)+Q(1, 1000)+Q(1, 4000) == Q(41, 800) < 1, "AB.strict_good_count")
    check(bad_count(2, 1, 1, 24) == 301 and incidence(2, 24) == 1204, "A.C22_reference")
    # Compress the 2^24 tuples by number of identity coordinates, retaining exact weights.
    union = inc = overlap = 0
    for r in range(25):
        w = choose(24, r)
        edges = edges_of(((0, 1),)*r + ((1, 0),)*(24-r), 2)
        bad = sum(boundary(edges, s) <= 2*s.bit_count() for s in range(1, 15) if s.bit_count() <= 2)
        union += w*bool(bad); inc += w*bad
        overlap += w*(max(Counter(edges).values()) >= 3)
    check((inc, union, overlap) == (1204, 602, 2**24), "AB.N2_full_weighted_count")
    MUTATIONS["incidence_equals_union"] = {"incidence": inc, "union": union}
    MUTATIONS["omit_overlap"] = {"N": 2, "q": 24, "overlap_tuples": overlap, "all_tuples": 2**24}
    # Same-permutation slots are not independent: two inputs cannot both land in a singleton.
    check(sum(p[0] == 0 and p[1] == 0 for p in it.permutations(range(2))) == 0, "mutation.slot_independence_rejected")
    MUTATIONS["slot_independence"] = {"actual_probability": "0", "false_product": "1/4"}
    return {"N2_q24": {"fixed_shore": 301, "incidence": inc, "bad_union": union, "bad_overlap": overlap},
            "large_shore_bracket": {"numerator": bracket.numerator, "denominator": bracket.denominator}}


def pattern_tests(cfg: dict) -> None:
    # Enumerate prescribed coloured edges and compare extension formula with actual tuples.
    N, q = 3, 2
    tuples = list(it.product(list(it.permutations(range(N))), repeat=q))
    universe = list(it.product(range(q), range(N), range(N)))
    for size in range(4):
        for pattern in it.combinations(universe, size):
            actual = sum(all(tup[i][u] == v for i, u, v in pattern) for tup in tuples)
            count = 1
            for i in range(q):
                pairs = [(u, v) for c, u, v in pattern if c == i]
                if len({u for u, v in pairs}) != len(pairs) or len({v for u, v in pairs}) != len(pairs):
                    count = 0; break
                count *= math.factorial(N-len(pairs))
            check(actual == count, "B.pattern_extension_enumeration")
    for N, q in cfg["cycle_enumeration"]:
        perms = list(it.permutations(range(N)))
        for tup in it.product(perms, repeat=q):
            edges = edges_of(tup, N)
            for g in [3, 4, 5]:
                cycles = short_cycles(2*N, edges, g)
                check(len(cycles) == len(set(cycles)), "B.unoriented_cycle_dedup")
                overlap = False
                for a, b in it.combinations(cycles, 2):
                    if vertices(edges, a) & vertices(edges, b):
                        overlap = True; both = a | b
                        check(len(both) >= len(vertices(edges, both))+1, "B.cycle_union_excess")
                        check(len(both) <= 2*g and len(vertices(edges, both)) <= 2*g, "B.pattern_size")
                if not overlap:
                    deleted = {min(c) for c in cycles}
                    check(is_matching([edges[i] for i in deleted]), "C.deleted_edges_matching")
                    out = [e for i, e in enumerate(edges) if i not in deleted]
                    check(simple(out) and girth(2*N, out) >= g, "C.simple_and_girth")
                    for s in range(1, (1 << (2*N))-1):
                        check(boundary(edges, s)-boundary(out, s) <= s.bit_count(), "C.cut_loss_bound")
    fixtures = {
        "parallel_triple": (2, [(0, 1)]*3, 3),
        "shared_path": (5, [(u, v) for u in (0, 1) for v in (2, 3, 4)], 5),
        "shared_edge": (6, [(0,1),(1,2),(2,3),(3,0),(1,4),(4,5),(5,0)], 5),
        "shared_vertex": (7, [(0,1),(1,2),(2,3),(3,0),(0,4),(4,5),(5,6),(6,0)], 5)
    }
    for name, (n, edges, g) in fixtures.items():
        pairs = [(a, b) for a, b in it.combinations(short_cycles(n, edges, g), 2)
                 if vertices(edges, a) & vertices(edges, b)]
        check(bool(pairs), "B.fixture."+name)
        for a, b in pairs:
            check(len(a | b) >= len(vertices(edges, a | b))+1, "B.fixture_excess")
    # Duplicating a cycle by orientation invalidates the excess claim.
    cyc = [(0,1),(1,2),(2,3),(3,0)]
    check(len(short_cycles(4, cyc, 5)) == 1, "mutation.orientation_duplicate_rejected")
    MUTATIONS["cycle_orientation"] = {"actual_distinct_cycles": 1, "false_union_excess": "e=v=4"}
    # Positive, non-vacuous matching-deletion and one-extra-edge control.
    N = 8
    edges = [(u, N+v) for u in range(N) for v in range(N) if u != v]
    edges += [(u, N+(u+1)%N) for u in range(N)]
    cycles = short_cycles(16, edges, 3)
    check(len(cycles) == 8, "C.positive_parallel_pair_count")
    deleted = {min(c) for c in cycles}
    out = [e for i, e in enumerate(edges) if i not in deleted]
    out2 = out[1:]
    for s in range(1, (1 << 16)-1):
        size = s.bit_count()
        if size <= 8:
            check(boundary(edges, s) >= 2*size+2, "C.positive_even_margin")
            check(boundary(out, s) >= size+2 and boundary(out2, s) > size, "C.positive_extra_deletion")
    check(simple(out2) and two_connected(16, out2), "C.positive_two_connected")
    check(2*len(out2) <= 8*16-2, "C.positive_degree_deficit")
    check(not is_matching([(0, 1), (0, 1)]), "mutation.distinct_neighbour_multigraph_rejected")
    MUTATIONS["parallel_neighbour_collapse"] = {"edge_instances": 2, "distinct_opposite_neighbours": 1}


def switched(n: int, edges: list[tuple[int,int]], u: int, v: int, edge: tuple[int,int]) -> list[tuple[int,int]]:
    x, y = edge
    return [e for e in edges if e != edge] + [(u, x), (v, y)]


def exchange_tests(cfg: dict) -> None:
    for n in range(3, cfg["switch_max_n"]+1):
        universe = list(it.combinations(range(n), 2))
        for mask in range(1 << len(universe)):
            edges = [e for i, e in enumerate(universe) if (mask >> i) & 1]
            oldg = girth(n, edges)
            ds = [distances(n, edges, u) for u in range(n)]
            for g in [3, 4, 5]:
                if oldg < g:
                    continue
                for xy in edges:
                    x, y = xy
                    centres = [u for u in range(n) if u not in xy and min(ds[u][x], ds[u][y]) >= g-1]
                    for u, v in it.product(centres, repeat=2):
                        out = switched(n, edges, u, v, xy)
                        check(simple(out) and len(out) == len(edges)+1 and girth(n, out) >= g, "D.exhaustive_local_switch")
    controls = [
        (6, [(0,1),(2,3),(3,4),(4,5),(5,2)], 0,1,(2,3),4,6,"uv_xy_pairing"),
        (8, [(0,4),(4,5),(5,3),(1,6),(6,7),(7,2),(2,3)],0,1,(2,3),4,8,"uy_vx_pairing"),
        (5, [(1,2),(2,3),(3,4),(4,1)],0,0,(1,2),4,5,"coincident_centres")]
    for n, edges, u, v, xy, g, newg, name in controls:
        check(girth(n, edges) >= g, "D.control_initial_girth")
        check(all(distances(n, edges, z)[w] >= g-1 for z in (u,v) for w in xy), "D.control_current_distance")
        check(girth(n, switched(n, edges, u,v,xy)) == newg, "D.control."+name)
    # Satisfies B1's full numeric conditions, but inclusion-maximal F has one deficit centre.
    N, k, g, r = 52, 2, 4, 1
    H = [(u, N+u) for u in range(N)]
    F = [(u, u+1) for u in range(1,N-1)] + [(N-1,1)]
    F += [(N+u, N+(u+1)%N) for u in range(N)]
    J = H+F; D = r+k; B = 1+D*sum((D-1)**j for j in range(g-2))
    check(N > 5*B and k*N % 2 == 0 and girth(2*N, J) >= g, "D.full_control_hypotheses")
    fdeg = Counter(v for e in F for v in e)
    check([u for u in range(2*N) if fdeg[u] < k] == [0], "D.maximal_not_maximum")
    check(all(distances(2*N,J,0)[x] >= g-1 for x in (1,2)), "D.full_control_far_edge")
    J2 = switched(2*N, J, 0,0,(1,2))
    F2 = [e for e in F if e != (1,2)] + [(0,1),(0,2)]
    check(all(Counter(v for e in F2 for v in e)[u] == k for u in range(2*N)) and girth(2*N, J2) >= g,
          "D.full_control_exact_regularization")
    MUTATIONS["maximal_equals_maximum"] = {"N": N, "k": k, "g": g, "B": B, "deficit_vertex": 0,
                                            "F_edges_before":len(F), "F_edges_after":len(F2)}
    # Old H distances would allow the switch; current J distances forbid it.
    old = [(0,4),(4,2),(2,3)]
    check(girth(5, old) >= 4 and girth(5, switched(5,old,0,1,(2,3))) == 3, "mutation.stale_distance_rejected")
    MUTATIONS["stale_distance"] = {"J_edges":old,"u":0,"v":1,"xy":[2,3],"target_girth":4,"new_girth":3}
    check(11 > 5*2 and 11 % 2 == 1, "mutation.parity_rejected")
    MUTATIONS["omit_parity"] = {"N":11,"k":1,"r":0,"g":3,"B":2,"obstruction":"odd degree sum"}


def subdivision_tests() -> None:
    n = 5
    pairs = [(u,v) for u in (0,1) for v in (2,3,4)]
    artificial = [(0,1),(2,3),(2,4),(3,4)]
    positive = 0
    for hm in range(1 << len(pairs)):
        H = [e for i,e in enumerate(pairs) if (hm >> i) & 1]
        coregood = two_connected(n,H) and mc(n,H) is None
        for fm in range(1 << len(artificial)):
            F = [e for i,e in enumerate(artificial) if (fm >> i) & 1]
            nn,G = subdivide(n,H,F)
            check(simple(G) and bipartite(nn,G), "E.simple_bipartite")
            gj = girth(n,H+F); gg = girth(nn,G)
            check((gj == INF and gg == INF) or (gj < INF and gg >= gj), "E.girth_projection")
            if coregood:
                positive += 1
                check(two_connected(nn,G) and mc(nn,G) is None, "E.immune_core_preservation")
    check(positive > 0, "E.nonvacuous_controls")
    H = pairs
    nn,G = subdivide(n,[],H)
    witness = mc(nn,G)
    check(mc(n,H) is None and witness is not None, "mutation.subdivide_core_rejected")
    MUTATIONS["arbitrary_subdivision"] = {"core":"K2,3","subdivided_all_edges":True,"new_order":nn,"matching_cut_mask":witness}
    check(mc(1,[]) is None and mc(2,[]) is not None, "EG.nonempty_shores_and_empty_crossing")
    check(girth(1,[]) == INF and girth(3,[(0,1)]) >= 5, "EG.forest_infinite_girth")
    MUTATIONS["allow_empty_shore"] = {"graph":"K1","empty_shore_would_accept":True}
    # Integer arithmetic controls only: n is not asserted to encode a small degree-24 seed.
    for n in [2,4,10,100]:
        t = 19*n; nn = n+t; twice_m = 24*n-2+4*t
        check(twice_m+2 == 5*nn, "F.strict_integer_arithmetic")
        check(24*n+4*t == 5*nn, "mutation.missing_deficit_rejected")
    MUTATIONS["omit_extra_seed_deletion"] = {"k":38,"worst_case_average":"5 exactly","strict_hypothesis_met":False}
    for g in range(3,51):
        K = 2*g; C = K*K*(96*K*K)**K; M = 4*C
        B = 1+62*sum(61**j for j in range(g-2))
        check(M % 2 == 0 and M >= max(1000,K,5*B+1), "F.parameter_controls")
        check(40*M*M == 10240*g**4*(384*g*g)**(4*g), "F.order_identity_controls")


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError("usage: python checker.py input.json")
    raw = Path(sys.argv[1]).read_bytes(); cfg = json.loads(raw)
    check(cfg["format"] == "r10-c21b-audit-input-v1", "input.format")
    check(1 <= cfg["coefficient_max_N"] <= 6 and 1 <= cfg["recurrence_max_q"] <= 24,
          "input.arithmetic_limits")
    check(3 <= cfg["switch_max_n"] <= 5, "input.switch_limit")
    check(all(1 <= N <= 4 and 1 <= q <= 3 and math.factorial(N)**q <= 1000
              for N,q in cfg["tuple_enumeration"]+cfg["cycle_enumeration"]), "input.enumeration_limits")
    refs = arithmetic_tests(cfg); pattern_tests(cfg); exchange_tests(cfg); subdivision_tests()
    payload = {"format":"r10-c21b-audit-output-v1", "verdict":"candidate_only", "checker_version":VERSION,
               "input_sha256":hashlib.sha256(raw).hexdigest(), "checks":dict(sorted(TALLY.items())),
               "assertions_passed":sum(TALLY.values()), "references":refs,
               "mutations_detected":MUTATIONS,
               "scope":"Exact bounded generator checks only; no general good tuple enumerated, no universal proof or trusted verification inferred."}
    text = json.dumps(payload,sort_keys=True,indent=2)+"\n"
    if len(text.encode()) > 65536:
        raise ValueError("output budget exceeded")
    print(text,end="")

if __name__ == "__main__":
    main()
