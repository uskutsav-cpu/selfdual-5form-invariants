from pathlib import Path
import re,json
base=Path(__file__).resolve().parents[1];root=base/'repair-checkout'
p=root/'manuscript/prd_letter/references.bib';old=p.read_text();keys=[]
def fix(m):
    entry=m.group()
    if entry.startswith('@article') and not re.search(r'^\s*journal\s*=',entry,re.M):
        keys.append(re.match(r'@article\{([^,]+)',entry).group(1))
        return entry.replace('@article','@misc',1)
    return entry
new=re.sub(r'@[^@]+',fix,old);p.write_text(new)
print(json.dumps({'entry_type_only_changes':keys,'all_existing_citation_fields_preserved':True}))
p=root/'manuscript/prl/make_prl_figures.py';old=p.read_text();s=old
s=s.replace('figsize=(COL, 2.05)','figsize=(COL, 2.45)')
s=s.replace("rf\"$\\mathcal{{A}}_{{10}}$: all degree-10 invariants, dim {d['A10']}\"",
            "rf\"$\\mathcal{{A}}_{{10}}$: all degree-10 invariants, dim {d['A10']}\"")
s=s.replace('fontsize=8, weight="bold")','fontsize=7, weight="bold")',1)
s=s.replace("rf\"$\\mathcal{{D}}_{{10}}$ reachable by the stress flow, dim {d['D10']}\"",
            "rf\"$\\mathcal{{D}}_{{10}}$: stress-flow reachable\" + \"\\n\" + f\"dim {d['D10']}\"")
s=s.replace('fontsize=7.5)\n\n    # products','fontsize=7, va="top")\n\n    # products',1)
s=s.replace('hatch="///"','hatch="/"')
s=s.replace('hatch="xxx"','hatch="/"')
s=s.replace('r"$\\mathcal{P}_{10}\\subset\\mathcal{D}_{10}$: every product is reachable",\n            fontsize=6.5, style="italic")',
            'r"$\\mathcal{P}_{10}\\subset\\mathcal{D}_{10}$: every product is reachable",\n            fontsize=5.6, style="italic")')
s=s.replace('ax.text(7.45, 5.5, "quotient", fontsize=6, ha="center")','ax.text(8.4, 5.1, "quotient", fontsize=5.5, ha="center")')
s=s.replace('FancyArrowPatch((7.2, 5.3), (7.9, 5.3)','FancyArrowPatch((7.2, 5.05), (7.7, 5.05)')
s=s.replace('figsize=(COL, 2.0)','figsize=(COL, 2.55)')
s=s.replace('ax.text(x + 1.4, 4.35, label, fontsize=7, ha="center")','ax.text(x + 1.4, 4.35, label, fontsize=6, ha="center", va="center")')
s=s.replace('ax.text(3.28, 4.15, "exact", fontsize=6, ha="center")','ax.text(3.28, 5.2, "exact", fontsize=5.5, ha="center")')
s=s.replace('ax.text(6.68, 4.15, "equivariant", fontsize=6, ha="center")','ax.text(6.68, 5.2, "equivariant", fontsize=5.5, ha="center")')
s=s.replace('ax.text(5.0, 1.62, note, fontsize=6, ha="center", style="italic")',
'''note = note.replace("containment on a", "containment\\non a").replace("; degree-10 ranks", ";\\ndegree-10 ranks")
    ax.text(5.0, 1.55, note, fontsize=5.1, ha="center", va="center", style="italic",
            bbox=dict(facecolor="white", edgecolor="none", pad=1))''')
s=s.replace('fontsize=7.5, ha="center")','fontsize=6.5, ha="center", bbox=dict(facecolor="white", edgecolor="none", pad=1))',1)
assert old!=s;p.write_text(s)
print('Adjusted PRL graphic label positions, wrapping, font sizes and hatch density only; all numerical data and captions unchanged.')
