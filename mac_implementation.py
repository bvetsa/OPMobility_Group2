# mac_implementation.py
import hashlib
import struct
import hmac
from typing import Optional


class LightweightMAC:
    """
    Lightweight Message Authentication Code (MAC) implementation.
    Uses SHA-256 with truncation to produce a 15-bit tag.
    """
    def __init__(self, secret_key: bytes, probe_id: Optional[int] = None):
        self.secret_key = secret_key
        self.probe_id = probe_id

    def compute_mac(self, data: bytes, nonce: int, sequence: int) -> int:
        """Compute 15-bit MAC based on SHA-256 digest"""
        probe_bytes = struct.pack(">H", self.probe_id if self.probe_id is not None else 0)
        message = self.secret_key + probe_bytes + data + struct.pack(">HH", nonce, sequence)

        hash_result = hashlib.sha256(message).digest()
        offset = hash_result[-1] & 0x0F
        mac_bytes = hash_result[offset:offset + 2]
        mac = struct.unpack(">H", mac_bytes)[0] & 0x7FFF
        return mac

    def verify_mac(self, data: bytes, nonce: int, sequence: int, received_mac: int) -> bool:
        """Verify received MAC with constant-time comparison"""
        computed = self.compute_mac(data, nonce, sequence)
        return hmac.compare_digest(struct.pack(">H", computed), struct.pack(">H", received_mac))


class SimpleMAC:
    """
    Ultra-lightweight MAC using a polynomial rolling hash.
    Suitable for demonstration or very constrained devices.
    """
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key

    def compute_simple_mac(self, data: bytes, nonce: int, sequence: int) -> int:
        prime = 31
        mod = 32768  # 15-bit space
        combined = self.secret_key + data + struct.pack(">HH", nonce, sequence)
        hash_value = 0
        for byte in combined:
            hash_value = (hash_value * prime + byte) % mod
        return hash_value


if __name__ == "__main__":
    # Quick self-test
    secret = b"automotive_secret_2024"
    mac = LightweightMAC(secret, probe_id=0x100)
    test_data = b"temp_sensor_25.5C"
    nonce = 12345
    sequence = 1

    computed = mac.compute_mac(test_data, nonce, sequence)
    verified = mac.verify_mac(test_data, nonce, sequence, computed)

    print("MAC Implementation Test:")
    print(f"Data: {test_data}")
    print(f"Nonce: {nonce}, Sequence: {sequence}")
    print(f"Computed: {computed} (0x{computed:04X})")
    print(f"Verified: {verified}")
