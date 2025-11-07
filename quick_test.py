from virtual_can import VirtualCANNetwork

def quick_demo():
    print("🚗 Automotive MAC Protocol Demo\n")
    net = VirtualCANNetwork()

    probes = [
        (0x100, b"temp_sensor_key_001"),
        (0x101, b"press_sensor_key_002"),
        (0x102, b"speed_sensor_key_003"),
    ]
    for pid, key in probes:
        net.add_probe(pid, key)
        print(f"✅ Registered probe 0x{pid:03X}")

    print("\n🔒 Testing Secure Communication...")
    ok = 0
    for i in range(5):
        if net.simulate_communication():
            ok += 1
            print(f"  Cycle {i+1}: ✅ Authenticated")
        else:
            print(f"  Cycle {i+1}: ❌ Failed")

    print(f"\n📊 Results: {ok}/5 successful authentications")
    if net.ecu.received_frames:
        print(f"\n📨 Received {len(net.ecu.received_frames)} authenticated frames")
        for f in net.ecu.received_frames[:3]:
            print(f"  Probe 0x{f.id:03X}: Seq {f.sequence}, MAC 0x{f.mac:04X}")

if __name__ == "__main__":
    quick_demo()
