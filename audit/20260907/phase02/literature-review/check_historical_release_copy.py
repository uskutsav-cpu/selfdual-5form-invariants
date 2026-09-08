from pathlib import Path
import importlib.util,tempfile,json,shutil,hashlib
base=Path(__file__).resolve().parents[1]
builder=base/'repair-checkout/scripts/build_release_candidate.py'
spec=importlib.util.spec_from_file_location('historical_builder_under_test',builder)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
checks={}
assert {'scripts','results','verification'}.issubset(dict(module.INCLUDE)['trace-code'])
checks['required_historical_source_roots_retained']=True
assert not any('self_dual_5_invariant_enumerator' in p for _,paths in module.INCLUDE for p in paths)
checks['third_party_archive_not_in_include_list']=True
with tempfile.TemporaryDirectory(prefix='historical-copy-check-',dir=base/'literature-review') as folder:
    fixture=Path(folder);source=fixture/'source';target=fixture/'copied';source.mkdir()
    original_root=module.ROOT;module.ROOT=source
    files={
        'scripts/required.py':'print("required")\n',
        'results/required.json':'{"value":14}\n',
        'verification/required.json':'{"verified":true}\n',
        'results/audit/original-command.json':json.dumps({'path':'/Users/'+'auditfixture'+'/work'}),
        'results/audit/third-party-source.pdf':'excluded fixture',
        'results/nested/audit/legitimate.json':'{"keep":true}\n',
        'scripts/__pycache__/ignore.pyc':'ignored',
        'results/reproduction-logs/local.log':'ignored'
    }
    for rel,content in files.items():
        p=source/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content)
    for rel in ['scripts','results','verification']:
        shutil.copytree(source/rel,target/rel,ignore=module.release_copy_ignore)
    assert all((target/rel).is_file() for rel in ['scripts/required.py','results/required.json','verification/required.json'])
    checks['required_inputs_copy_successfully']=True
    assert not (target/'results/audit').exists()
    checks['local_audit_subtree_and_source_pdf_excluded']=True
    assert (target/'results/nested/audit/legitimate.json').is_file()
    checks['unrelated_audit_name_retained']=True
    assert not (target/'scripts/__pycache__').exists() and not (target/'results/reproduction-logs').exists()
    checks['existing_cache_log_exclusions_preserved']=True
    assert not [issue for p in target.rglob('*') if p.is_file() for issue in module.scan(p)]
    checks['clean_included_fixture_passes_scan']=True
    bad=target/'scripts/absolute-path.txt';bad.write_text('/Users/'+'auditfixture'+'/must-still-be-rejected')
    assert any('absolute home path' in x for x in module.scan(bad))
    checks['home_path_scanner_still_rejects']=True
    bad.write_text('-----BEGIN '+'PRIVATE KEY-----')
    assert any('private key' in x for x in module.scan(bad))
    checks['secret_scanner_still_rejects']=True
    module.ROOT=original_root
result={'status':'PASS','checks':checks,'main_executed':False,'release_candidate_tree_written':False,
        'builder_sha256':hashlib.sha256(builder.read_bytes()).hexdigest()}
(base/'literature-review/historical-release-copy-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
