import subprocess
import re

def scan_wifi():
    command = "netsh wlan show networks mode=bssid"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        if result.returncode != 0:
            print("SCAN ERROR:", result.stderr)
            return []

        return parse_output(result.stdout)

    except Exception as e:
        print("SCAN EXCEPTION:", e)
        return []


def parse_output(output):
    networks = []

    ssid = None
    security = None

    for line in output.splitlines():

        line = line.strip()

        # SSID
        if re.match(r"^SSID\s+\d+\s*:", line):
            ssid = line.split(":", 1)[1].strip()
            continue

        # Authentication
        if line.startswith("Authentication"):
            security = line.split(":", 1)[1].strip()
            continue

        # BSSID
        if re.match(r"^BSSID\s+\d+\s*:", line):
            mac = line.split(":", 1)[1].strip()

            networks.append({
                "SSID": ssid,
                "MAC": mac,
                "Signal": "",
                "Security": security,
                "Channel": ""
            })
            continue

        # Signal
        if line.startswith("Signal") and networks:
            networks[-1]["Signal"] = line.split(":",1)[1].strip()
            continue

        # Channel
        if line.startswith("Channel") and networks:
            networks[-1]["Channel"] = line.split(":",1)[1].strip()

    return networks