<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Lightweight Authentication for LIN/CAN Probes — README</title>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial; line-height:1.5; color:#0b1220; padding:28px; max-width:980px; margin:auto; }
    h1 { font-size:1.9rem; margin-bottom:0.2rem; color:#0b2330; }
    h2 { font-size:1.25rem; margin-top:1.2rem; color:#0b3b4a; }
    p.lead { color:#25323c; margin-top:0.2rem; }
    pre { background:#0f1720; color:#e6edf3; padding:12px; overflow:auto; border-radius:8px; font-size:0.95rem;}
    code { background:#eef6fb; padding:3px 6px; border-radius:4px; font-family:ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", "Courier New", monospace; font-size:0.95rem; }
    ul { margin-left:1.05rem; }
    table { border-collapse: collapse; width:100%; margin-top:0.6rem; }
    table th, table td { text-align:left; padding:8px; border-bottom:1px solid #e6eef3; }
    .note { background:#fff7d6; border-left:4px solid #ffd24a; padding:10px; border-radius:6px; margin:10px 0; color:#3b2f00; }
    .kbd { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, "Roboto Mono", monospace; background:#eee; padding:2px 6px; border-radius:4px; }
    footer { margin-top:28px; font-size:0.9rem; color:#526170; }
    .cta { background:#0b6bff; color:white; padding:8px 12px; border-radius:6px; display:inline-block; text-decoration:none; margin-top:8px;}
  </style>
</head>
<body>
  <h1>Lightweight Authentication for LIN/CAN Probes — README</h1>
  <p class="lead">
    A software-only hackathon prototype to demonstrate authenticated sensor data on classic in-vehicle buses (CAN/LIN).  
    This project includes runnable Python scripts that emulate a <strong>secure probe (sender)</strong>, an <strong>ECU/receiver (verifier)</strong>, and an <strong>attacker</strong> on a virtual CAN interface (SocketCAN / <code>vcan0</code>).
  </p>

  <h2>Project overview</h2>
  <p>
    Classic automotive buses (LIN/CAN) lack message authentication. This prototype shows a pragmatic, lightweight approach:
  </p>
  <ul>
    <li>Append a small <strong>Message Authentication Code (MAC)</strong> (truncated 32-bit) and an 8-bit rolling <strong>counter</strong> to CAN frames.</li>
    <li>Receiver verifies MAC and rejects spoofed or replayed frames.</li>
    <li>All simulated in software using <code>vcan0</code> (SocketCAN) and <code>python-can</code>. No hardware required.</li>
  </ul>

  <div class="note">
    <strong>Note:</strong> This repository intentionally builds on the baseline approaches described in the hackathon brief, and extends them with demoable, judge-friendly novelty (see <em>Novelty & tradeoffs</em> below).
  </div>

  <h2>What’s included</h2>
  <ul>
    <li><code>sender.py</code> — simulated secure probe (produces payload + counter + truncated BLAKE2s tag).</li>
    <li><code>receiver.py</code> — ECU that verifies MACs and enforces a sliding counter window.</li>
    <li><code>attacker.py</code> — captures/replays frames and forges invalid frames to demonstrate rejection.</li>
    <li>Detailed run & demo instructions (below) plus guidance to extend with aggregated auth and a simulated secure element.</li>
  </ul>

  <h2>Why this is hackathon-appropriate</h2>
  <ul>
    <li>Fully reproducible on a single laptop (fast iteration & reliable demo).</li>
    <li>Shows a real-world defence (MAC + freshness) with measurable KPIs: CPU cost, latency, bus load, rejection counts.</li>
    <li>Stretchable: add aggregate authentication, secure-element simulation, timing-based detection or an MCU port.</li>
  </ul>

  <h2>Novelty & tradeoffs (recommended additions)</h2>
  <p>To stand out from baseline work in the company brief, consider implementing one or more of these:</p>
  <table>
    <tr><th>Feature</th><th>Why it’s interesting</th></tr>
    <tr><td><strong>Aggregated Authentication</strong> (batch N frames, send one auth)</td><td>Reduces bus overhead while showing concrete detection latency vs bandwidth tradeoff.</td></tr>
    <tr><td><strong>Simulated Secure Element</strong> (separate process holding keys)</td><td>Demonstrates secure key storage & operation without physical hardware—helps answer provisioning/key-extraction questions.</td></tr>
    <tr><td><strong>Timing Anomaly Detector</strong></td><td>Layered defense: detects attackers who replay/forge but fail to match timing fingerprints.</td></tr>
  </table>

  <h2>Packet format (classic CAN prototype)</h2>
  <p>We use a single 8-byte CAN data payload (Mode A):</p>
  <pre><code>
// Byte index (0..7)
0: sensor value (uint8, compressed)
1: counter (uint8, rolling)
2-5: truncated MAC (4 bytes)
6-7: reserved / padding (0x00)
  </code></pre>

  <h2>Requirements</h2>
  <ul>
    <li>Linux (native or WSL2 with kernel vcan support). Ubuntu recommended.</li>
    <li>Python 3.8+</li>
    <li>Python packages: <code>python-can</code> (and optionally <code>pyblake2</code> / <code>cantools</code>).</li>
  </ul>

  <h2>Quick setup (copy & paste)</h2>
  <pre><code class="bash"># Create a virtual CAN interface (vcan0)
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Install Python deps
python3 -m pip install --user python-can
</code></pre>

  <h2>Usage — run the demo</h2>
  <p>Open <strong>three terminals</strong> and run:</p>
  <pre><code class="bash"># Terminal 1: Receiver (verifier)
python3 receiver.py

# Terminal 2: Sender (secure probe)
python3 sender.py

# Terminal 3: Attacker (after sender is running)
python3 attacker.py
</code></pre>

  <p><strong>Expected behaviour:</strong> the receiver prints <code>ACCEPT</code> for valid frames, and prints <code>REJECT ... bad_mac</code> for forged frames and <code>REJECT ... replay</code> for replays.</p>

  <h2>Key implementation details</h2>
  <h3>Crypto</h3>
  <p>The prototype uses <code>BLAKE2s</code> (available as <code>hashlib.blake2s</code>) and truncates the digest to 4 bytes (32 bits) in order to fit classic CAN frames. In production you'd consider longer tags or AEAD on CAN-FD.</p>

  <h3>Freshness & replay protection</h3>
  <p>An 8-bit rolling counter is included in each frame. The receiver keeps the last accepted counter and allows accepted counters that are within a sliding window (e.g. <code>W = 16</code>). This reduces false rejects due to slight reordering while blocking replays.</p>

  <h2>Extending the prototype — suggested branches</h2>
  <p><strong>Branch: <code>agg-mac</code></strong></p>
  <ol>
    <li>Sender buffers <code>N</code> frames (e.g. N=4) then sends an <em>Auth</em> frame containing the MAC over concatenated frames+ids+counters.</li>
    <li>Receiver pairs the last N data frames with the auth frame and validates the batch.</li>
    <li>Measure bus occupancy and detection latency for per-frame vs aggregated modes and present the tradeoff chart.</li>
  </ol>

  <p><strong>Branch: <code>secure-element</code></strong></p>
  <ol>
    <li>Run a process <code>secure_element.py</code> that holds per-device keys and exposes a local RPC (UNIX socket / simple HTTP) to compute MACs on behalf of the sender.</li>
    <li>Sender requests MACs (simulate restricted access to key material). This demonstrates secure key handling without hardware.</li>
  </ol>

  <h2>Tests & automation</h2>
  <ul>
    <li>Add unit tests for MAC correctness, counter window logic and replay detection using <code>pytest</code>.</li>
    <li>Create an automated demo runner (<code>demo_runner.py</code>) that launches the three processes, injects the attack sequence, collects logs and produces a short text/video recording for backup.</li>
  </ul>

  <h2>Metrics to capture for judges</h2>
  <ul>
    <li>MAC compute time (use <code>time.perf_counter()</code> around MAC calls).</li>
    <li>Frames/sec observed vs intended (use sleep in sender and measure actual send rate).</li>
    <li>Bus load estimate (frames/sec * 8 bytes * 8 bits / 500000 bits/s).</li>
    <li>Rejection counts (bad_mac, replay, out_of_window).</li>
  </ul>

  <h2>Demo script (3 minutes)</h2>
  <ol>
    <li>30s: Problem + one-sentence solution & novelty.</li>
    <li>30s: Architecture + packet format (show diagram).</li>
    <li>90s: Live demo — start sender & receiver (show green accept), run attacker to show forged and replay rejections, toggle aggregate mode (if implemented) and show reduced bus load.</li>
    <li>30s: Results & next steps (secure element, MCU port, CAN-FD).</li>
  </ol>

  <h2>How to port to real MCU (short checklist)</h2>
  <ol>
    <li>Choose MCU: Cortex-M0+/M3/M4 (e.g. STM32 Nucleo series).</li>
    <li>Pick lightweight crypto implementation: ASCON or BLAKE2s C port, or mbed TLS / TinyCrypt for HMAC.</li>
    <li>Use a hardware CAN transceiver (e.g. SN65HVD230) and proper 120Ω termination.</li>
    <li>For secure key storage, use ATECC608A or a dedicated secure element; implement provisioning & revocation flow.</li>
    <li>Measure MAC compute time on MCU and tune tag size / aggregation strategy to meet timing & bandwidth constraints.</li>
  </ol>

  <h2>Repository structure (recommended)</h2>
  <pre><code>
/README.html            <-- this file (HTML)
sender.py               <-- probe (python)
receiver.py             <-- verifier (python)
attacker.py             <-- attacker (python)
demo_runner.py          <-- optional: spawn all components & record logs
docs/
  architecture.png
  slides.pdf
tests/
  test_mac.py
  test_replay.py
</code></pre>

  <h2>Security & ethical note</h2>
  <p>
    This repository is a defensive demonstration. Do not use the code to attack real vehicles or networks. Always obtain permission before performing security testing on hardware or networks you do not own.
  </p>

  <h2>Credits & references</h2>
  <ul>
    <li>Hackathon brief provided by the organizing company (used to align the prototype to constraints and expectations).</li>
    <li>Prototype design: lightweight MAC + counter + sliding window (industry-typical baseline).</li>
  </ul>

  <h2>License</h2>
  <p>MIT License — see <code>LICENSE</code> in the repo.</p>

  <footer>
    <p>Prepared for the hackathon &mdash; to generate runnable scripts and slides, run the demo instructions above. If you want, I can now add the <strong>aggregated-auth</strong> code branch and the <strong>secure-element</strong> emulator files directly in this repo.</p>
    <a class="cta" href="#run">Ready to generate the code files</a>
  </footer>
</body>
</html>
