# attack_simulator.py
import time
from virtual_can import VirtualCANNetwork, CANFrame

def simulate_replay():
    net = VirtualCANNetwork()
    p = net.add_probe(0x200, b"replay_key_200")
    nonce = net.ecu.generate_nonce()
    frame = p.generate_frame(b"temp=22", nonce)

    first_ok = net.ecu.verify_frame(frame)      # expected True
    second_ok = net.ecu.verify_frame(frame)     # expected False (replay)
    return first_ok, second_ok, net.ecu.security_log

def simulate_spoof():
    net = VirtualCANNetwork()
    good = net.add_probe(0x300, b"goodkey")
    bad = net.add_probe(0x301, b"badkey")
    nonce = net.ecu.generate_nonce()

    # bad probe creates a frame, then tries to spoof good's ID
    f_bad = bad.generate_frame(b"value=1", nonce)
    spoof = CANFrame(id=0x300, data=f_bad.data, sequence=f_bad.sequence, mac=f_bad.mac, timestamp=time.time())
    result = net.ecu.verify_frame(spoof)  # expected False
    return result, net.ecu.security_log

if __name__ == "__main__":
    print("🛡️ Attack Simulator\n")
    r1, r2, logr = simulate_replay()
    print(f"Replay: first accept={r1}, replay accept={r2}")
    print("Replay security log:", logr)

    print("\n🎭 Spoofing test")
    ok, logs = simulate_spoof()
    print("Spoof accepted:", ok)
    print("Spoof security log:", logs)
