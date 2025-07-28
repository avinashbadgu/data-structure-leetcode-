import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# --- Encryption Helper Class (copied from your utility.py) ---
class EncryptionHelper:
    def __init__(self, key: str):
        if not key or len(key.encode('utf-8')) != 32:
            raise ValueError("Encryption key must be 32 bytes long.")
        self.key = key.encode('utf-8')
        self.backend = default_backend()

    def decrypt(self, encrypted_text: str) -> str:
        base64_str = encrypted_text.replace('-', '+').replace('_', '/')
        padding_needed = 4 - (len(base64_str) % 4)
        if padding_needed < 4:
            base64_str += '=' * padding_needed
        
        combined = base64.b64decode(base64_str)
        iv = combined[:16]
        encrypted = combined[16:]

        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        decrypted_padded_data = decryptor.update(encrypted) + decryptor.finalize()
        unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        
        return unpadded_data.decode('utf-8')

# --- New Decryption and Parsing Function ---
def decrypt_and_parse_agent_id(global_agent_unique_identifier: str, key: str) -> dict:
    """
    Decrypts and parses the agent identifier string.
    Expected decrypted format: region_id_regionname_regionalAccountId_botid
    """
    try:
        decrypted = EncryptionHelper(key).decrypt(global_agent_unique_identifier)
        parts = decrypted.split("_")
        
        if len(parts) != 4:
            raise ValueError(f"Invalid decrypted format (expected 4 parts, got {len(parts)})")
            
        return {
            "region_id": int(parts[0]),
            "region_name": parts[1],
            "account_id": parts[2],
            "bot_id": parts[3],
            "unique_identifier": decrypted
        }
    except Exception as e:
        # Re-raise with more context
        raise Exception(f"Failed to decrypt or parse agent identifier: {e}")


# --- DEMO USAGE ---
if __name__ == "__main__":
    # The key you use to encrypt (must be 32 chars)
    key = "N8oMKbH4JXdT29jVgQWpF2szxL6YT1e5"  # <-- REPLACE WITH YOUR REAL KEY

    # The encrypted string you provided
    encrypted_string = "77SWNcz4FpoiUgYZ2Ry1lmXfiBcaBdBkfrR3h6_24rdkD07d_RIZUF4a_AmuaU3j"

    print(f"Testing with encrypted string: {encrypted_string}")
    
    try:
        parsed_data = decrypt_and_parse_agent_id(encrypted_string, key)
        print("\n✅ Decrypted and parsed successfully:")
        print(parsed_data)
    except Exception as e:
        print(f"\n❌ FAILED:")
        print(e)