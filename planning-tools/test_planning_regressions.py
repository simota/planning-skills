#!/usr/bin/env python3
"""Structural regression checks; this is NOT an LLM routing benchmark.

The fixture supplies lifecycle and diagnosis. These tests only check that the
registry does not send that known diagnosis to an incompatible owner.
"""
from __future__ import annotations
import argparse
import copy
import sys
from pathlib import Path
import yaml

PHASES = {f'planning-{x}' for x in ('frame','discover','options','decompose','estimate','risk','review')}
MUTATIONS = ('pre-to-replan', 'fixed-decompose', 'wrong-evidence-owner')

def validate(routes: dict, cases: list[dict]) -> list[str]:
    errors=[]
    review=routes.get('review-to-ready',{})
    replan=routes.get('course-correct',{})
    if review.get('chain') != ['planning-review']:
        errors.append('review-to-ready must not insert post-start replanning into a pre-start repair')
    if replan.get('chain') != ['planning-replan']:
        errors.append('course-correct must not append decompose irrespective of diagnosis')
    if review.get('pattern') != 'loop' or review.get('max_cycles') != 3:
        errors.append('review loop pattern/bound were changed unexpectedly')
    if review.get('checker') != 'other-engine':
        errors.append('independent checker policy was changed unexpectedly')
    for name,key in [('review-to-ready','repair'),('course-correct','reenter')]:
        mapping=routes.get(name,{}).get(key,{})
        for diagnosis,target in mapping.items():
            if target not in PHASES | {'none'}:
                errors.append(f'{name}.{key}.{diagnosis}: invalid correction owner {target}')
    for c in cases:
        if c['lifecycle']=='pre':
            actual=review.get('repair',{}).get(c['finding_class'])
        elif c['lifecycle']=='started':
            actual=replan.get('reenter',{}).get(c['divergence_class'])
        else:
            errors.append(f'{c["id"]}: invalid fixture lifecycle'); continue
        if actual != c['expect']:
            errors.append(f'{c["id"]}: {actual!r} != {c["expect"]!r}')
    return errors

def mutate(routes: dict, name: str) -> dict:
    changed=copy.deepcopy(routes)
    if name=='pre-to-replan':
        changed['review-to-ready']['chain']=['planning-review','planning-replan']
    elif name=='fixed-decompose':
        changed['course-correct']['chain']=['planning-replan','planning-decompose']
    elif name=='wrong-evidence-owner':
        changed['review-to-ready']['repair']['evidence']='planning-decompose'
    return changed

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--mutate',choices=MUTATIONS)
    args=parser.parse_args()
    routes=yaml.safe_load((args.root/'planning-registry/routes.yaml').read_text())
    cases=yaml.safe_load((args.root/'planning-registry/phase-regressions.yaml').read_text())['cases']
    tested=mutate(routes,args.mutate) if args.mutate else routes
    errors=validate(tested,cases)
    for error in errors: print('FAIL:',error)
    if args.mutate:
        if errors:
            print(f'PASS: mutation {args.mutate} was rejected with {len(errors)} structural failure(s)')
            return 0
        print(f'FAIL: mutation {args.mutate} escaped the regression checks')
        return 1
    if errors:
        print(f'{len(errors)} structural failures'); return 1
    for name in MUTATIONS:
        if not validate(mutate(routes,name),cases):
            print(f'FAIL: mutation {name} escaped the regression checks')
            return 1
    print(f'PASS: {len(cases)} diagnosed return-owner cases; {len(MUTATIONS)} mutations rejected; natural-language selection was not tested')
    return 0

if __name__=='__main__': sys.exit(main())
