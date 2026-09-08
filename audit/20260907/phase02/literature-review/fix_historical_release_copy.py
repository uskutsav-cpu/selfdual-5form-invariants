from pathlib import Path
import hashlib,json
base=Path(__file__).resolve().parents[1]
path=base/'repair-checkout/scripts/build_release_candidate.py'
old=path.read_text()
anchor='\ndef scan(path: Path) -> list[str]:\n'
addition='''
def release_copy_ignore(directory: str, names: list[str]) -> set[str]:
    """Exclude local build debris and the separate independent-audit bundle."""
    ignored = set(shutil.ignore_patterns(
        "__pycache__", "*.pyc", ".pytest_cache", "reproduction-logs"
    )(directory, names))
    # Keep results required by the historical tensor tests. The independent
    # audit has its own release and preserves original machine-specific paths.
    # Exclude only this exact subtree, not unrelated directories named audit.
    if Path(directory).resolve() == (ROOT / "results").resolve():
        ignored.add("audit")
    return ignored

'''
assert old.count(anchor)==1
new=old.replace(anchor,'\n'+addition+anchor,1)
block='''                                ignore=shutil.ignore_patterns(
                                    "__pycache__", "*.pyc", ".pytest_cache",
                                    # Raw step logs from a local reproduction
                                    # run. They are machine-specific, they are
                                    # gitignored, and they carry absolute paths.
                                    "reproduction-logs"))'''
assert new.count(block)==1
new=new.replace(block,'                                ignore=release_copy_ignore)',1)
path.write_text(new)
print(json.dumps({'path':'scripts/build_release_candidate.py',
                  'before_sha256':hashlib.sha256(old.encode()).hexdigest(),
                  'after_sha256':hashlib.sha256(new.encode()).hexdigest(),
                  'scope':'Exclude exact results/audit subtree only; preserve INCLUDE and scanner functions.'},indent=2))
