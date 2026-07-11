from flask import Flask, render_template, jsonify, request
from scanner import scan_wifi
from detector import detect_fake
import subprocess, re, os, tempfile

app = Flask(__name__)

# ── helpers ──────────────────────────────────────────────────

def get_connected_ssid():
    """Return the SSID the machine is currently connected to, or None."""
    try:
        out = subprocess.check_output(
            "netsh wlan show interfaces", shell=True, text=True, stderr=subprocess.DEVNULL
        )
        for line in out.splitlines():
            line = line.strip()
            # Match "    SSID                   : MyNetwork"
            # but NOT "    BSSID                  : ..."
            m = re.match(r"^SSID\s*:\s*(.+)$", line)
            if m:
                return m.group(1).strip()
    except Exception:
        pass
    return None

def build_wpa2_profile(ssid, password):
    return f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID><name>{ssid}</name></SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""

def build_open_profile(ssid):
    return f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{ssid}</name>
    <SSIDConfig>
        <SSID><name>{ssid}</name></SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>manual</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>open</authentication>
                <encryption>none</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
        </security>
    </MSM>
</WLANProfile>"""

# ── routes ───────────────────────────────────────────────────

@app.route("/")
@app.route("/landing")
def landing():
    return render_template("landing.html")

@app.route("/scanner")
def scanner_page():
    return render_template("index.html")

@app.route("/scan")
def scan():

    try:
        networks = scan_wifi()
        networks = detect_fake(networks)

        connected = get_connected_ssid()

        for net in networks:
            net["Connected"] = (
                connected is not None and
                net.get("SSID") == connected
            )

        return jsonify({
            "networks": networks,
            "connected_ssid": connected
        })

    except Exception as e:
        print("SCAN ROUTE ERROR:", e)

        return jsonify({
            "networks": [],
            "connected_ssid": None
        })

@app.route("/connect", methods=["POST"])
def connect():
    data     = request.get_json()
    ssid     = (data.get("ssid") or "").strip()
    password = (data.get("password") or "").strip()
    is_open  = data.get("is_open", False)

    if not ssid:
        return jsonify({"success": False, "message": "SSID is required."}), 400

    try:
        ssid_safe = ssid.replace('"', '\\"')

        # 🔹 STEP 1: Try direct connect (if profile already exists)
        quick_conn = subprocess.run(
            f'netsh wlan connect name="{ssid_safe}"',
            shell=True, capture_output=True, text=True
        )

        if quick_conn.returncode == 0:
            print("Quick connect success")
            return jsonify({
                "success": True,
                "message": f"Connecting to \"{ssid}\"…"
            })

        # 🔹 STEP 2: Delete old profile (ignore errors)
        subprocess.run(
            f'netsh wlan delete profile name="{ssid_safe}"',
            shell=True, capture_output=True, text=True
        )

        # 🔹 STEP 3: Build profile XML
        xml = build_open_profile(ssid_safe) if is_open else build_wpa2_profile(ssid_safe, password)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xml", mode="w", encoding="utf-8")
        tmp.write(xml)
        tmp.close()

        # 🔹 STEP 4: Add profile
        add = subprocess.run(
            f'netsh wlan add profile filename="{tmp.name}" user=current',
            shell=True, capture_output=True, text=True
        )

        os.unlink(tmp.name)

        print("ADD PROFILE OUTPUT:", add.stdout)
        print("ADD PROFILE ERROR:", add.stderr)

        if add.returncode != 0:
            return jsonify({
                "success": False,
                "message": add.stderr.strip() or add.stdout.strip()
            }), 500

        # 🔹 STEP 5: Connect (final)
        conn = subprocess.run(
            f'netsh wlan connect name="{ssid_safe}" ssid="{ssid_safe}" interface="Wi-Fi"',
            shell=True, capture_output=True, text=True, timeout=15
        )

        print("CONNECT OUTPUT:", conn.stdout)
        print("CONNECT ERROR:", conn.stderr)

        if conn.returncode == 0:
            return jsonify({
                "success": True,
                "message": f"Connecting to \"{ssid}\"…"
            })
        else:
            return jsonify({
                "success": False,
                "message": conn.stderr.strip() or conn.stdout.strip() or "Connection failed"
            })

    except subprocess.TimeoutExpired:
        return jsonify({
            "success": False,
            "message": "Connection timed out"
        }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/disconnect", methods=["POST"])
def disconnect():
    try:
        r = subprocess.run(
            "netsh wlan disconnect",
            shell=True, capture_output=True, text=True, timeout=8
        )
        if r.returncode == 0:
            return jsonify({"success": True,  "message": "Disconnected from WiFi."})
        else:
            return jsonify({"success": False, "message": r.stderr.strip() or "Disconnect failed."})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/connected-ssid")
def connected_ssid():
    """Lightweight endpoint — just returns which SSID is active right now."""
    return jsonify({"connected_ssid": get_connected_ssid()})

if __name__ == "__main__":
    app.run(debug=True)