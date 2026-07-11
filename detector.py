from collections import defaultdict

def get_mac_prefix(mac):
    return mac.upper()[0:8]   # First 3 bytes (OUI)

def detect_fake(networks):
    ssid_map = defaultdict(list)

    for net in networks:
        ssid_map[net["SSID"]].append(net)

    for ssid, entries in ssid_map.items():

        # Only one network → Safe (no reason needed)
        if len(entries) == 1:
            entries[0]["Status"] = "Safe"
            entries[0]["Reason"] = ""
            continue

        security_set = set(e["Security"] for e in entries)
        prefix_set   = set(get_mac_prefix(e["MAC"]) for e in entries)

        # Security mismatch → Highly Suspicious
        if len(security_set) > 1:
            security_list = " vs ".join(sorted(security_set))
            for e in entries:
                e["Status"] = "⚠ Security Mismatch (Highly Suspicious)"
                e["Reason"] = (
                    f"Multiple networks share this SSID but use different security protocols "
                    f"({security_list}). This is a classic Evil Twin tactic — an attacker broadcasts "
                    f"the same name with weaker/open security to lure victims onto a rogue access point."
                )
            continue

        # MAC prefix (vendor) mismatch → Possible Evil Twin
        if len(prefix_set) > 1:
            prefix_list = ", ".join(sorted(prefix_set))
            for e in entries:
                e["Status"] = "⚠ Different Vendor (Possible Evil Twin)"
                e["Reason"] = (
                    f"Two or more access points broadcast the same SSID but have different OUI "
                    f"vendor prefixes ({prefix_list}). Legitimate dual-band routers share the same "
                    f"hardware vendor. A mismatched prefix strongly suggests a rogue device is spoofing "
                    f"this network to perform a man-in-the-middle attack."
                )
            continue

        # Same vendor + same security → Dual Band (no reason needed)
        for e in entries:
            e["Status"] = "Safe (Dual Band Router)"
            e["Reason"] = ""

    return networks