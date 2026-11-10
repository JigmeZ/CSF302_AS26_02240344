"""
Lab 7 - Question 2: Huffman coding.

Run without arguments for three sample texts, or pass text-file paths:
    python Lab7_Q2.py file1.txt file2.txt file3.txt
"""

import heapq
import sys
from itertools import count


class Node:
    def __init__(self, frequency, character=None, left=None, right=None):
        self.frequency = frequency
        self.character = character
        self.left = left
        self.right = right


def build_tree(text):
    frequencies = {}
    for character in text:
        frequencies[character] = frequencies.get(character, 0) + 1
    heap = []
    order = count()
    for character, frequency in frequencies.items():
        heapq.heappush(heap, (frequency, next(order), Node(frequency, character)))
    if not heap:
        return None
    while len(heap) > 1:
        f1, _, left = heapq.heappop(heap)
        f2, _, right = heapq.heappop(heap)
        parent = Node(f1 + f2, left=left, right=right)
        heapq.heappush(heap, (parent.frequency, next(order), parent))
    return heap[0][2]


def make_codes(node, prefix="", codes=None):
    if codes is None:
        codes = {}
    if node.character is not None:
        codes[node.character] = prefix or "0"
        return codes
    make_codes(node.left, prefix + "0", codes)
    make_codes(node.right, prefix + "1", codes)
    return codes


def encode(text, codes):
    return "".join(codes[character] for character in text)


def decode(bits, root):
    if root is None:
        return ""
    if root.character is not None:
        return root.character * len(bits)
    text = []
    node = root
    for bit in bits:
        node = node.left if bit == "0" else node.right
        if node.character is not None:
            text.append(node.character)
            node = root
    return "".join(text)


def show_report(name, text):
    root = build_tree(text)
    codes = make_codes(root)
    bits = encode(text, codes)
    decoded = decode(bits, root)
    assert decoded == text
    print("\n---", name, "---")
    print("Code table:")
    for character in sorted(codes, key=repr):
        print(repr(character), ":", codes[character])
    original_bits = len(text) * 8
    ratio = len(bits) / original_bits if original_bits else 0
    print("characters:", len(text), "encoded bits:", len(bits))
    print("compression ratio (Huffman / 8-bit):", round(ratio, 3))
    print("decoded correctly:", decoded == text)


def main():
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            with open(filename, "r", encoding="utf-8") as file:
                show_report(filename, file.read())
    else:
        samples = {
            "short": "this is a simple example of huffman coding",
            "repeated": "aaaaabbbbccccccccccccdddddddddd",
            "paragraph": (
                "Greedy algorithms make the locally best choice. "
                "Huffman coding uses frequencies to save bits."
            ),
        }
        for name, text in samples.items():
            show_report(name, text)


if __name__ == "__main__":
    main()