"""All verification in one command: PYTHONPATH=. python3 tests/run_all.py

  gradebook  -- does the score CATCH known defects and rank correctly? (ground truth)
  safety     -- positive + negative controls, incl. the corpus's real false positives
  framework  -- do the import-time refusals bite?
"""
import subprocess, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
suites = ["tests/test_gradebook.py", "tests/test_safety.py"]
total_pass = total_fail = 0
for s in suites:
    print(f"\n{'#'*72}\n# {s}\n{'#'*72}")
    r = subprocess.run([sys.executable, s], cwd=root,
                       env={"PYTHONPATH": ".", "PATH": __import__("os").environ["PATH"]})
    if r.returncode: total_fail += 1
    else: total_pass += 1
print(f"\n{'='*72}\n{total_pass}/{len(suites)} suites green")
sys.exit(1 if total_fail else 0)
