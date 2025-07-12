# Copyright 2025 Colin de Seroux alias Phenix333 (https://colindeseroux.fr)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##### Standard #####
import numpy as np
import pickle
import zlib
import time

##### Constants #####
# Chinese characters for base 8192 encoding
CHINESE_CHARS = [chr(0x4E00 + i) for i in range(8192)]
CHAR_TO_VAL = {ch: i for i, ch in enumerate(CHINESE_CHARS)}


def float16_dict_from_npz(npz_path: str) -> dict:
    """
    Load a .npz file and convert all float arrays to float16.
    
    :param npz_path: Path to the .npz file.
    :type npz_path: str
    
    :return: Dictionary with float arrays converted to float16.
    :rtype: dict
    """
    
    data = np.load(npz_path)
    
    return {k: (v.astype(np.float16) if v.dtype.kind == "f" else v) for k, v in data.items()}


def to_chinese_base8192(data: bytes) -> str:
    """
    Encode bytes to a string in base 8192 using Chinese characters.
    
    :param data: Bytes to encode.
    :type data: bytes
    
    :return: Encoded string using Chinese characters.
    :rtype: str
    """
    
    bits = "".join(f"{byte:08b}" for byte in data)
    
    # Pad bits for 13-bit grouping
    if len(bits) % 13 != 0:
        bits += "0" * (13 - len(bits) % 13)
        
    chars = [CHINESE_CHARS[int(bits[i:i+13], 2)] for i in range(0, len(bits), 13)]
    
    return "".join(chars)


def from_chinese_base8192(text: str) -> bytes:
    """
    Decode a string in base 8192 using Chinese characters back to bytes.
    
    :param text: Encoded string using Chinese characters.
    :type text: str
    
    :return: Decoded bytes.
    :rtype: bytes
    """
    
    bits = "".join(f"{CHAR_TO_VAL[ch]:013b}" for ch in text)
    
    # Convert bits to bytes (8 bits per byte)
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]
    
    # Delete any incomplete bytes
    bytes_list = [b for b in bytes_list if len(b) == 8]
    
    return bytes(int(b, 2) for b in bytes_list)


def compress_model_to_chinese(npz_path: str, output_path: str) -> None:
    """
    Load a .npz file, convert it to float16, pickle it, compress it, and encode it to Chinese base8192.
    
    :param npz_path: Path to the .npz file.
    :type npz_path: str
    :param output_path: Path to save the compressed model.
    :type output_path: str
    """
    
    print("Loading and converting to float16...")
    obj = float16_dict_from_npz(npz_path)

    print("Pickling...")
    raw = pickle.dumps(obj)
    print(f"Raw size (bytes): {len(raw)}")

    print("Compressing...")
    compressed = zlib.compress(raw, level=9)
    print(f"Compressed size (bytes): {len(compressed)}")

    print("Encoding to Chinese base8192...")
    encoded = to_chinese_base8192(compressed)
    print(f"Encoded length (chars): {len(encoded)}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encoded)
    
    print(f"Saved compressed model to {output_path}")


def decompress_model_from_chinese(encoded: str) -> dict:
    """
    Decode a string in Chinese base8192, decompress it, and unpickle it to get the model.
    
    :param encoded: Encoded string using Chinese characters.
    :type encoded: str
    
    :return: Dictionary with the decompressed model.
    :rtype: dict
    """

    print("Decoding from Chinese base8192...")
    compressed = from_chinese_base8192(encoded)

    print("Decompressing...")
    raw = zlib.decompress(compressed)

    print("Unpickling...")
    weights = pickle.loads(raw)
    
    return weights


if __name__ == "__main__":
    npz_path = "model.npz"
    compressed_file = "model.txt"

    compress_model_to_chinese(npz_path, compressed_file)
    
    print(f"Reading compressed model from {compressed_file}...")
    with open(compressed_file, "r", encoding="utf-8") as f:
        encoded = f.read()
    
    start = time.time()
    model = decompress_model_from_chinese(encoded)
    end = time.time()
    
    print(f"Decompression time: {end - start:.3f} seconds")

    # Check if the decompressed model matches the original
    original = float16_dict_from_npz(npz_path)
    
    for k in original:
        if np.allclose(original[k], model[k], atol=1e-2):
            print(f"{k}: OK")
        else:
            print(f"{k}: MISMATCH")