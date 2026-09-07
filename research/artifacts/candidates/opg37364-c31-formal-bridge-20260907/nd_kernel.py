"""Small classical many-sorted natural-deduction replay checker, version 1.

No graph facts, solver answers, or caller-provided axioms are accepted.
Equality is an uninterpreted binary predicate here: interpreting it as actual
vertex equality is a sound specialization. This is unregistered candidate code.
"""
from __future__ import annotations
from typing import Any

class Rejected(ValueError):
    pass

def need(test: bool, message: str) -> None:
    if not test:
        raise Rejected(message)

def fv(f: list) -> set[str]:
    k = f[0]
    if k == 'atom': return set(f[2:])
    if k == 'bot': return set()
    if k in ('all', 'ex'): return fv(f[3]) - {f[1]}
    return fv(f[1]) | fv(f[2])

def sub(f: list, x: str, y: str) -> list:
    k = f[0]
    if k == 'atom': return f[:2] + [y if t == x else t for t in f[2:]]
    if k == 'bot': return f[:]
    if k in ('all', 'ex'):
        if f[1] == x: return f
        need(f[1] != y or x not in fv(f[3]), 'variable capture')
        return f[:3] + [sub(f[3], x, y)]
    return [k, sub(f[1], x, y), sub(f[2], x, y)]

def normal(f: list, bound: tuple[str, ...] = ()) -> Any:
    k = f[0]
    if k == 'atom':
        return (k, f[1], *[('b', bound[::-1].index(t)) if t in bound else ('f', t) for t in f[2:]])
    if k == 'bot': return ('bot',)
    if k in ('all', 'ex'): return (k, f[2], normal(f[3], bound + (f[1],)))
    return (k, normal(f[1], bound), normal(f[2], bound))

def same(f: list, g: list) -> bool:
    return normal(f) == normal(g)

class Kernel:
    def __init__(self, signature: dict[str, list[str]], sorts: list[str]):
        self.signature = signature
        self.sorts = set(sorts)
        self.nodes = 0
        self.rules: dict[str, int] = {}
        need(len(self.sorts) == len(sorts) and all(isinstance(s, str) for s in sorts), 'sorts')
        need(all(isinstance(p, str) and isinstance(ss, list) and all(s in self.sorts for s in ss)
                 for p, ss in signature.items()), 'signature')

    def wf(self, f: list, vs: dict[str, str], depth: int = 0) -> None:
        need(depth <= 200 and isinstance(f, list) and bool(f), 'formula shape/budget')
        k = f[0]
        if k == 'bot':
            need(len(f) == 1, 'bottom arity')
        elif k == 'atom':
            need(len(f) >= 2 and f[1] in self.signature, 'predicate')
            ss = self.signature[f[1]]
            need(len(f) == len(ss) + 2, 'predicate arity')
            need(all(isinstance(t, str) and vs.get(t) == s for t, s in zip(f[2:], ss)), 'term sort/scope')
        elif k in ('and', 'or', 'imp'):
            need(len(f) == 3, 'connective arity')
            self.wf(f[1], vs, depth + 1); self.wf(f[2], vs, depth + 1)
        elif k in ('all', 'ex'):
            need(len(f) == 4 and isinstance(f[1], str) and f[2] in self.sorts, 'binder')
            self.wf(f[3], {**vs, f[1]: f[2]}, depth + 1)
        else:
            raise Rejected('unknown formula constructor')

    def infer(self, p: list, hs: dict[str, list], vs: dict[str, str], depth: int = 0) -> list:
        need(depth <= 200 and isinstance(p, list) and bool(p), 'proof shape/budget')
        self.nodes += 1
        need(self.nodes <= 100000, 'node budget')
        k = p[0]; self.rules[k] = self.rules.get(k, 0) + 1
        def ar(n: int) -> None: need(len(p) == n, 'rule arity ' + k)
        def go(q: list) -> list: return self.infer(q, hs, vs, depth + 1)
        def fresh(h: str) -> None: need(isinstance(h, str) and h not in hs, 'hypothesis shadowing')
        if k == 'hyp':
            ar(2); need(p[1] in hs, 'unknown hypothesis'); ans = hs[p[1]]
        elif k == 'imp_i':
            ar(4); fresh(p[1]); self.wf(p[2], vs)
            ans = ['imp', p[2], self.infer(p[3], {**hs, p[1]: p[2]}, vs, depth + 1)]
        elif k == 'imp_e':
            ar(3); a, b = go(p[1]), go(p[2])
            need(a[0] == 'imp' and same(a[1], b), 'implication premise mismatch'); ans = a[2]
        elif k == 'and_i':
            ar(3); ans = ['and', go(p[1]), go(p[2])]
        elif k in ('and_l', 'and_r'):
            ar(2); a = go(p[1]); need(a[0] == 'and', 'conjunction elimination'); ans = a[1 if k == 'and_l' else 2]
        elif k == 'or_l':
            ar(3); self.wf(p[2], vs); ans = ['or', go(p[1]), p[2]]
        elif k == 'or_r':
            ar(3); self.wf(p[1], vs); ans = ['or', p[1], go(p[2])]
        elif k == 'or_e':
            ar(6); a = go(p[1]); need(a[0] == 'or', 'disjunction elimination')
            fresh(p[2]); fresh(p[4])
            b = self.infer(p[3], {**hs, p[2]: a[1]}, vs, depth + 1)
            c = self.infer(p[5], {**hs, p[4]: a[2]}, vs, depth + 1)
            need(same(b, c), 'branch conclusions differ'); ans = b
        elif k == 'all_i':
            ar(4); x, s = p[1], p[2]
            need(isinstance(x, str) and x not in vs and s in self.sorts, 'universal eigenvariable')
            need(all(x not in fv(h) for h in hs.values()), 'universal open assumption')
            ans = ['all', x, s, self.infer(p[3], hs, {**vs, x: s}, depth + 1)]
        elif k == 'all_e':
            ar(3); a = go(p[1]); need(a[0] == 'all' and vs.get(p[2]) == a[2], 'universal elimination sort')
            ans = sub(a[3], a[1], p[2])
        elif k == 'ex_i':
            ar(4); self.wf(p[1], vs); a = p[1]
            need(a[0] == 'ex' and vs.get(p[2]) == a[2], 'existential witness sort')
            need(same(go(p[3]), sub(a[3], a[1], p[2])), 'existential premise'); ans = a
        elif k == 'ex_e':
            ar(5); a = go(p[1]); need(a[0] == 'ex', 'existential elimination')
            x, h = p[2], p[3]; fresh(h)
            need(isinstance(x, str) and x not in vs and x not in fv(a), 'existential eigenvariable')
            need(all(x not in fv(f) for f in hs.values()), 'existential open assumption')
            inst = sub(a[3], a[1], x)
            ans = self.infer(p[4], {**hs, h: inst}, {**vs, x: a[2]}, depth + 1)
            need(x not in fv(ans), 'existential variable escaped')
        elif k == 'false_e':
            ar(3); self.wf(p[1], vs); need(go(p[2]) == ['bot'], 'false elimination'); ans = p[1]
        elif k == 'dne':
            ar(2); a = go(p[1])
            need(a[0] == 'imp' and a[2] == ['bot'] and a[1][0] == 'imp' and a[1][2] == ['bot'], 'double negation')
            ans = a[1][1]
        elif k == 'let':
            ar(4); fresh(p[1]); a = go(p[2]); ans = self.infer(p[3], {**hs, p[1]: a}, vs, depth + 1)
        else:
            raise Rejected('unknown inference rule')
        self.wf(ans, vs)
        return ans

def verify(cert: dict) -> dict:
    need(set(cert) == {'format', 'sorts', 'signature', 'goal', 'proof'}, 'certificate fields')
    need(cert['format'] == 'r10-classical-nd-v1', 'certificate format')
    kernel = Kernel(cert['signature'], cert['sorts'])
    kernel.wf(cert['goal'], {})
    inferred = kernel.infer(cert['proof'], {}, {})
    need(same(inferred, cert['goal']), 'conclusion does not match frozen goal')
    return {'nodes': kernel.nodes, 'rules': dict(sorted(kernel.rules.items())), 'open_assumptions': [],
            'logical_system': 'classical many-sorted first-order natural deduction',
            'mathematical_axioms': [], 'scope': 'one general core-extension implication; not the root'}
