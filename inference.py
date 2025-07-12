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
import pickle
import zlib

##### Constants #####
# Chinese characters for base 8192 encoding
CHINESE_CHARS = [chr(0x4E00 + i) for i in range(8192)]
CHAR_TO_VAL = {ch: i for i, ch in enumerate(CHINESE_CHARS)}

ENCODED = "<YOUR_ENCODED_STRING_HERE>"


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
    model = decompress_model_from_chinese(ENCODED)
    
    # TODO ...
