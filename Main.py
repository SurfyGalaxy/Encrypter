import tkinter as tk
import functions as func

dhke = func.make_dhke()
print(f"DHKE: {dhke}")
bits = func.pad_sha256(dhke)
W_list = func.make_words_sha256(bits)
sha256 = func.sha256(W_list)
print(f"SHA256: {sha256}")
matrices = func.make_matrix(sha256)
AES = func.aes256(matrices)
print(f"AES: {AES}")