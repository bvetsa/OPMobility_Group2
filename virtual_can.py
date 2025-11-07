import time, random
from dataclasses import dataclass
from typing import List, Dict
from mac_implementation import LightweightMAC

@dataclass
class CANFrame:
    id: int
    data: bytes
    sequence: int
    mac: int
    timestamp: float

class VirtualProbe:
    def __init__(self, probe_id: int, secret_key: bytes):
        self.probe_id = probe_id
        self.mac_calculator = LightweightMAC(secret_key, probe_id=probe_id)
        self.sequence_counter = random.randint(0, 1000)

    def generate_frame(self, sensor_data: bytes, nonce: int) -> CANFrame:
        self.sequence_counter += 1
        tag = self.mac_calculator.compute_mac(sensor_data, nonce, self.sequence_counter)
        return CANFrame(
            id=self.probe_id,
            data=sensor_data,
            sequence=self.sequence_counter,
            mac=tag,
            timestamp=time.time()
        )

class VirtualECU:
    def __init__(self):
        self.probe_keys: Dict[int, bytes] = {}
        self.current_nonce = 0
        self.received_frames: List[CANFrame] = []
        self.security_log: List[str] = []

    def register_probe(self, probe_id: int, secret_key: bytes):
        self.probe_keys[probe_id] = secret_key

    def generate_nonce(self) -> int:
        self.current_nonce = random.randint(0, 65535)
        return self.current_nonce

    def verify_frame(self, frame: CANFrame) -> bool:
        if frame.id not in self.probe_keys:
            self.security_log.append(f"UNKNOWN_PROBE: ID {frame.id:03X}")
            return False

        mac_calc = LightweightMAC(self.probe_keys[frame.id], probe_id=frame.id)

        if not mac_calc.verify_mac(frame.data, self.current_nonce, frame.sequence, frame.mac):
            self.security_log.append(f"INVALID_MAC: Probe {frame.id:03X}")
            return False

        if not self._check_sequence(frame):
            self.security_log.append(f"REPLAY_ATTACK: Probe {frame.id:03X}, Seq {frame.sequence}")
            return False

        self.received_frames.append(frame)
        return True

    def _check_sequence(self, frame: CANFrame) -> bool:
        prior = [f.sequence for f in self.received_frames if f.id == frame.id]
        return frame.sequence > max(prior) if prior else True

class VirtualCANNetwork:
    def __init__(self):
        self.ecu = VirtualECU()
        self.probes: List[VirtualProbe] = []

    def add_probe(self, probe_id: int, secret_key: bytes):
        probe = VirtualProbe(probe_id, secret_key)
        self.probes.append(probe)
        self.ecu.register_probe(probe_id, secret_key)
        return probe

    def simulate_communication(self) -> bool:
        nonce = self.ecu.generate_nonce()
        for probe in self.probes:
            sensor_data = f"data_{probe.probe_id}_{time.time():.6f}".encode()
            frame = probe.generate_frame(sensor_data, nonce)
            if not self.ecu.verify_frame(frame):
                return False
        return True
