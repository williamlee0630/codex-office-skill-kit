"""執行整套程式測試並保存機器可讀結果，不聲稱自然語言驗收。"""
from pathlib import Path
import importlib.metadata
import io
import json
import platform
import sys
import unittest
import os
from datetime import datetime, timezone, timedelta

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('PYTHONUTF8', '1')
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
sys.path.insert(0, str(ROOT / 'tests'))
output = ROOT / 'docs/qa'
output.mkdir(parents=True, exist_ok=True)
stream = io.StringIO()
suite = unittest.defaultTestLoader.discover(str(ROOT / 'tests'))
result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
(output / 'final-tests.log').write_text(stream.getvalue(), encoding='utf-8')
report = {'date': datetime.now(timezone(timedelta(hours=8))).date().isoformat(), 'scope': '自動化程式測試，非Codex觸發驗收',
          'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
          'skipped': len(result.skipped), 'success': result.wasSuccessful()}
(output / 'test-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
environment = {'python': sys.version, 'executable': sys.executable, 'platform': platform.platform(), 'packages': {}}
for package in ['python-docx', 'python-pptx', 'openpyxl', 'pypdf', 'Pillow', 'reportlab']:
    try:
        environment['packages'][package] = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        environment['packages'][package] = '未安裝'
(output / 'environment.json').write_text(json.dumps(environment, ensure_ascii=False, indent=2), encoding='utf-8')
print(stream.getvalue()[-1800:])
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if result.wasSuccessful() else 1)
