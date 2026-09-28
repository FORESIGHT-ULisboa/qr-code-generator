# Copyright (C) 2026 José Pedro Matos
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version. See the LICENSE file for details.

"""Minimal QR-code generator: library helpers, Jupyter widget app and CLI."""

import argparse
import base64
import io

import segno


def make_qr(data, error="m"):
    data = (data or "").strip()
    if not data:
        raise ValueError("Nothing to encode.")
    return segno.make(data, error=error, boost_error=False)


def to_bytes(qr, kind="png", scale=10, dark="#000000", light="#ffffff", border=4):
    buf = io.BytesIO()
    qr.save(buf, kind=kind, scale=scale, dark=dark, light=light, border=border)
    return buf.getvalue()


def _download_link(data, kind, label):
    mime = "image/svg+xml" if kind == "svg" else "image/png"
    b64 = base64.b64encode(data).decode()
    return (f'<a download="qrcode.{kind}" href="data:{mime};base64,{b64}" '
            f'style="margin-right:1em">{label}</a>')


def app(url="https://"):
    """Return an ipywidgets UI with live preview and PNG/SVG download links."""
    import ipywidgets as w

    text = w.Text(value=url, description="URL / text", continuous_update=False,
                  layout=w.Layout(width="600px"))
    error = w.Dropdown(options=[("L (7%)", "l"), ("M (15%)", "m"), ("Q (25%)", "q"), ("H (30%)", "h")],
                       value="m", description="Error corr.")
    scale = w.IntSlider(value=10, min=2, max=40, description="Scale", continuous_update=False)
    border = w.IntSlider(value=4, min=0, max=10, description="Border", continuous_update=False)
    dark = w.ColorPicker(value="#000000", description="Dark")
    light = w.ColorPicker(value="#ffffff", description="Light")
    image = w.Image(format="png")
    links = w.HTML()
    msg = w.HTML()

    def update(_=None):
        try:
            qr = make_qr(text.value, error.value)
        except Exception as e:  # segno raises DataOverflowError for too-long input
            image.layout.display = "none"
            links.value = ""
            msg.value = f"<span style='color:#c00'>{e}</span>"
            return
        opts = dict(scale=scale.value, dark=dark.value, light=light.value, border=border.value)
        png = to_bytes(qr, "png", **opts)
        svg = to_bytes(qr, "svg", **opts)
        image.value = png
        image.layout.display = None
        links.value = _download_link(png, "png", "⬇ Download PNG") + _download_link(svg, "svg", "⬇ Download SVG")
        n = qr.symbol_size(scale=1, border=0)[0]
        msg.value = f"<small>QR version {qr.version}, {n}×{n} modules</small>"

    for widget in (text, error, scale, border, dark, light):
        widget.observe(update, names="value")
    update()

    return w.VBox([text, w.HBox([error, scale, border]), w.HBox([dark, light]), msg, image, links])


def main():
    p = argparse.ArgumentParser(description="Generate a QR code from a URL or text.")
    p.add_argument("data", help="URL or text to encode")
    p.add_argument("-o", "--output", default="qrcode.png", help="output file (.png, .svg, .pdf, ...)")
    p.add_argument("-e", "--error", default="m", choices="lmqh", help="error correction level")
    p.add_argument("-s", "--scale", type=int, default=10)
    p.add_argument("--dark", default="#000000")
    p.add_argument("--light", default="#ffffff")
    a = p.parse_args()
    make_qr(a.data, a.error).save(a.output, scale=a.scale, dark=a.dark, light=a.light)
    print(f"Saved {a.output}")


if __name__ == "__main__":
    main()
