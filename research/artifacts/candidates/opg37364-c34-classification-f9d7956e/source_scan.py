"""Lexical source control only; no type checking or axiom inference."""
from __future__ import annotations
import re

def lean_code(text: str) -> str:
    out=[];i=0;depth=0;string=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i):depth+=1;out.extend('  ');i+=2
            elif text.startswith('-/',i):depth-=1;out.extend('  ');i+=2
            else:out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif string:
            if text[i]=='\\':out.extend('  ');i+=2
            elif text[i]=='"':string=False;out.append(' ');i+=1
            else:out.append('\n' if text[i]=='\n' else ' ');i+=1
        elif text.startswith('/-',i):depth=1;out.extend('  ');i+=2
        elif text.startswith('--',i):
            end=text.find('\n',i)
            if end<0:end=len(text)
            out.extend(' '*(end-i));i=end
        elif text[i]=='"':string=True;out.append(' ');i+=1
        else:out.append(text[i]);i+=1
    if depth or string:raise ValueError('unterminated Lean comment/string')
    return ''.join(out)

PATTERN=re.compile(r'\b(?:sorry|admit|axiom|unsafe|native_decide|extern|implemented_by)\b|#(?:eval|run_meta)')
def findings(text: str):
    return sorted(set(PATTERN.findall(lean_code(text))))
