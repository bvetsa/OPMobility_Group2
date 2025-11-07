# performance_analyzer.py
import time
from statistics import mean
from virtual_can import VirtualCANNetwork
from mac_implementation import LightweightMAC

def measure_auth_latency(iterations=200):
    net = VirtualCANNetwork()
    for i in (0x100, 0x101, 0x102):
        net.add_probe(i, f"k{i}".encode())

    timings = []
    for _ in range(iterations):
        t0 = time.perf_counter()
        ok = net.simulate_communication()
        t1 = time.perf_counter()
        if not ok:
            raise RuntimeError("Authentication failed during benchmark")
        timings.append((t1 - t0) * 1000.0)  # ms

    return {
        "avg_ms": round(mean(timings), 4),
        "min_ms": round(min(timings), 4),
        "p95_ms": round(sorted(timings)[int(0.95 * len(timings)) - 1], 4),
        "cycles": iterations,
    }

def measure_throughput(messages=5000):
    mac = LightweightMAC(b"bench_key", probe_id=0x100)
    n = 1
    s = 0
    t0 = time.perf_counter()
    for _ in range(messages):
        s += 1
        mac.compute_mac(b"payload", n, s)
    t1 = time.perf_counter()
    sec = t1 - t0
    return {
        "msgs": messages,
        "seconds": round(sec, 4),
        "msg_per_sec": int(messages / sec) if sec > 0 else float("inf"),
    }

if __name__ == "__main__":
    print("⚡ Performance Analyzer\n")
    print("Measuring auth latency (this may take a moment)...")
    latency = measure_auth_latency(100)
    print("Latency:", latency)

    print("\nMeasuring MAC throughput...")
    throughput = measure_throughput(20000)
    print("Throughput:", throughput)
