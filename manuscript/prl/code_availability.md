# Code availability

Repository: recorded at release time.
Tag: `prl-submission-package-v1`.
Environment: Python 3.13, NumPy 2.5.1, locked in `requirements-lock.txt`.
DOI: NOT CREATED --- pending authorisation.

Reproduction:

```
python -m pytest                                   # tensor side
cd spinor_trace_bridge && python -m pytest          # bridge
python spinor_trace_bridge/scripts/run_degree8_span.py
python spinor_trace_bridge/scripts/run_rank81_certificate.py --archive PATH
python manuscript/prl/build.sh
```

Long runs checkpoint per candidate and resume by re-issuing the same command.
