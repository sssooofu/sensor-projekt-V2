"""WiFi connect/disconnect with exponential backoff."""

import network
import time


def connect(ssid, password, timeout_s=20):
    """
    Activate WiFi and connect. Returns True on success, False on timeout.
    Retries with exponential backoff up to timeout_s.
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        return True

    wlan.connect(ssid, password)
    deadline = time.time() + timeout_s
    delay = 1
    while time.time() < deadline:
        if wlan.isconnected():
            print("WiFi connected:", wlan.ifconfig()[0])
            return True
        time.sleep(min(delay, deadline - time.time()))
        delay = min(delay * 2, 8)

    print("WiFi timeout")
    wlan.active(False)
    return False


def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)


def ip():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        return wlan.ifconfig()[0]
    return None
