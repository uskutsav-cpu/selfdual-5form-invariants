from pathlib import Path
import hashlib,json,subprocess
base=Path(__file__).resolve().parents[1]
root=base/'repair-checkout'
out=base/'literature-review'
files=['paper/manuscript.tex','manuscript/main.tex','submission_candidate/main.tex',
       'manuscript/jhep/main.tex','manuscript/prd/main.tex','manuscript/prd_letter/main.tex',
       'manuscript/prl/main.tex','manuscript/prd/build_prd.py','manuscript/prd_letter/references.bib',
       'manuscript/prl/make_prl_figures.py','manuscript/prl/figures/prl_spaces.pdf',
       'manuscript/prl/figures/prl_crossvalidation.pdf']
files += [f'manuscript/{venue}/appendices/{name}.tex' for venue in ['jhep','prd']
          for name in ['app_h_closure','app_i_gten','app_g_rank81','app_j_b10']]
commit='2b7663bbf5a06d1340973434f195a84ae2773e8f'
records=[]
for f in files:
    old=subprocess.check_output(['git','show',commit+':'+f],cwd=root)
    new=(root/f).read_bytes()
    records.append({'path':f,'frozen_sha256':hashlib.sha256(old).hexdigest(),
                    'repaired_sha256':hashlib.sha256(new).hexdigest(),
                    'changed':old!=new})
diff=subprocess.check_output(['git','diff',commit,'--',*files],cwd=root)
(out/'qualified-manuscripts.diff').write_bytes(diff)
(out/'final-owned-file-manifest.json').write_text(json.dumps({'frozen_commit':commit,'files':records,
    'diff_sha256':hashlib.sha256(diff).hexdigest()},indent=2)+'\n')
print(json.dumps({'owned_files':len(files),'changed_files':sum(x['changed'] for x in records),
                  'diff_bytes':len(diff),'diff_sha256':hashlib.sha256(diff).hexdigest()},indent=2))
