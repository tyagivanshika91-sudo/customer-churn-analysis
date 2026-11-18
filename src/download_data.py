from pathlib import Path
from urllib.request import urlopen
import hashlib

URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
EXPECTED_SHA256 = "16320c9c1ec72448db59aa0a26a0b95401046bef5d02fd3aeb906448e3055e91"
DEST = Path("data/raw/Telco-Customer-Churn.csv")

def main():
    DEST.parent.mkdir(parents=True, exist_ok=True)
    print("Downloading the IBM Telco Customer Churn sample dataset...")
    with urlopen(URL, timeout=60) as response:
        content = response.read()
    actual = hashlib.sha256(content).hexdigest()
    if actual != EXPECTED_SHA256:
        raise ValueError(
            "Downloaded file checksum did not match the expected source file. "
            f"Expected {EXPECTED_SHA256}, got {actual}. Do not use an unverified file."
        )
    DEST.write_bytes(content)
    print(f"Saved: {DEST} ({len(content):,} bytes)")
    print(f"SHA-256 verified: {actual}")

if __name__ == "__main__":
    main()
