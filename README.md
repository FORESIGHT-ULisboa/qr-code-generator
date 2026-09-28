# qr-code-generator
Lightweight open-source QR generation tool. No accounts, no paywalls, no tracking.

[![App (Voilà)](https://img.shields.io/badge/launch-app-579ACA.svg?logo=jupyter)](https://mybinder.org/v2/gh/FORESIGHT-ULisboa/qr-code-generator/main?urlpath=voila/render/app.ipynb)
[![Notebook](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/FORESIGHT-ULisboa/qr-code-generator/main?urlpath=lab/tree/app.ipynb)

- **launch app** — clean, code-free UI (Voilà).
- **launch binder** — the same notebook in JupyterLab.

## Usage

Type a URL or any text, press Enter, adjust error correction / size / colors, and download the PNG or SVG.

### Locally

```bash
pip install -r requirements.txt
jupyter lab app.ipynb      # or: voila app.ipynb
```

### Command line

```bash
python qrgen.py https://example.com -o example.png
python qrgen.py "any text" -o code.svg -e h --dark "#1a237e"
```

### From Python

```python
from qrgen import make_qr
make_qr("https://example.com").save("example.png", scale=10)
```

Built on [segno](https://github.com/heuer/segno) (pure Python, no dependencies).

## License

[GPL-3.0-or-later](LICENSE). Dependencies (segno, ipywidgets, voila) are BSD-3-Clause, which is GPL-compatible.
