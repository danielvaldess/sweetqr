#!/usr/bin/env python3
"""SweetQR CLI: generate a QR code from the terminal."""
import os
import sys
from datetime import datetime

try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
except ImportError:
    sys.exit(
        "Missing dependencies. Install them with:\n"
        "  python3 -m pip install qrcode pillow"
    )

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "generados")


def get_url() -> str:
    while True:
        url = input("Enter the URL: ").strip()
        if not url:
            print("The URL cannot be empty.")
            continue
        if not url.startswith(("http://", "https://")):
            confirm = (
                input(f'The URL "{url}" has no http(s)://. Add "https://"? [Y/n]: ')
                .strip()
                .lower()
            )
            if confirm != "n":
                url = "https://" + url
        return url


def main() -> None:
    url = get_url()
    name = input("File name (no extension, Enter for timestamp): ").strip()
    if not name:
        name = datetime.now().strftime("qr_%Y%m%d_%H%M%S")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, name + ".png")

    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(out)

    print(f"QR saved: {os.path.normpath(out)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(1)