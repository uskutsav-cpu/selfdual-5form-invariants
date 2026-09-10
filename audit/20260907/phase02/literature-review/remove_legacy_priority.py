from pathlib import Path
root=Path(__file__).resolve().parents[1]/'repair-checkout'
for f in ['manuscript/jhep/main.tex','manuscript/prd/main.tex']:
    p=root/f;s=p.read_text()
    a='''comparison is theirs, not ours. Read that way, the ten-dimensional degree-ten
sector may be the first place in this programme where the flow provably fails to
be exhaustive --- but establishing that it is the first would require a survey we
have not done. Whether the missed directions correspond to genuinely inaccessible'''
    b='''comparison is theirs, not ours. We make no priority claim for the
ten-dimensional degree-ten comparison. Whether the missed directions correspond to inaccessible'''
    assert a in s
    p.write_text(s.replace(a,b))
for f in ['manuscript/main.tex','submission_candidate/main.tex']:
    p=root/f;s=p.read_text()
    a='''The physics interpretation of section~\\ref{sec:physics} and the novelty
statements require coauthor confirmation. Not for distribution.'''
    b='''The physics interpretation of section~\\ref{sec:physics} requires coauthor
confirmation. This draft makes no priority claim. Not for distribution.'''
    assert a in s;s=s.replace(a,b)
    a='''--- but the two implementations use different frames, and no map between them had
been constructed, so their agreement had never been tested at the level of
values.'''
    b='''--- the two implementations use different frames. A convention-controlled map
is needed to compare their values on common field inputs.'''
    assert a in s;s=s.replace(a,b)
    a=r'\paragraph{Results.} We answer all three, exactly.'
    b=r'\paragraph{Results.} We record the archived coordinate evidence for all three.'
    assert a in s;s=s.replace(a,b)
    p.write_text(s)
print('Removed speculative priority and unverified historical absence language from four legacy main variants.')
