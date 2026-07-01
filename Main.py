import tkinter as tk
import functions as func

def clear_window():
    for widget in main.winfo_children():
        widget.destroy()

main = tk.Tk()
main.title("Encryption")
main.geometry("500x500")

main_choice = tk.StringVar(value="DHKE")

def main_menu():
    tk.Label(main, text="What do you want to do?").pack()
    tk.Radiobutton(main, text="Make a public key", variable=main_choice, value="DHKE public").pack()
    tk.Radiobutton(main, text="Calculate the private key", variable=main_choice, value="DHKE private").pack()
    tk.Radiobutton(main, text="Convert a private key to SHA-256", variable=main_choice, value="SHA-256").pack()
    tk.Radiobutton(main, text="Encrypt plaintext", variable=main_choice, value="Encrypt").pack()
    tk.Radiobutton(main, text="Decrypt ciphertext", variable=main_choice, value="Decrypt").pack()
    tk.Button(main, text="Submit", command=main_menu_answer).pack()

def main_menu_answer():
    clear_window()
    selection = main_choice.get()
    if selection == "DHKE public":
        build_dhke(0, (23, 11, 5))
    elif selection == "DHKE private":
        calculate_dhke()
    elif selection == "SHA-256":
        sha_256()
    elif selection == "Encrypt":
        encrypt()
    elif selection == "Decrypt":
        decrypt()
    else:
        print("Something's gone wrong")

def build_dhke(offset, default):
    tk.Label(main, text="Building a public key").grid(row=0 + offset, column=1)
    
    tk.Label(main, text="What shared prime did you choose?").grid(row=1 + offset, column=0)
    prime = tk.Entry(main)
    prime.insert(0, default[0])
    prime.grid(row=1 + offset, column=2)
    
    tk.Label(main, text="What shared base did you choose?").grid(row=2 + offset, column=0)
    base = tk.Entry(main)
    base.insert(0, default[1])
    base.grid(row=2 + offset, column=2)

    tk.Label(main, text="What's your secret key?").grid(row=3 + offset,   column=0)
    secret = tk.Entry(main)
    secret.insert(0, default[2])
    secret.grid(row=3 + offset, column=2)

    tk.Button(main, text="Submit", command=lambda: build_dhke_answer(prime, base, secret)).grid(row=4 + offset, column=1)


def build_dhke_answer(prime, base, secret):
    prime = prime.get()
    base = base.get()
    secret = secret.get()
    clear_window()

    try:
        prime = int(prime)
        base = int(base)
        secret = int(secret)
    except ValueError:
        tk.Label(main, text="Invalid integers").grid(row=0, column=1)
        build_dhke(1, (23, 11, 5))
    
    if func.check_prime(prime) == False:
        tk.Label(main, text=f"{prime} isn't prime!").grid(row=0, column=1)
        build_dhke(1, (23, str(base), str(secret)))
        


def calculate_dhke():
    pass

def sha_256():
    pass

def encrypt():
    pass

def decrypt():
    pass
#dhke = func.make_dhke()
#print(f"DHKE: {dhke}")
#bits = func.pad_sha256(dhke)
#W_list = func.make_words_sha256(bits)
#sha256 = func.sha256(W_list)
#print(f"SHA256: {sha256}")
#matrices = func.make_matrix(sha256)
#AES = func.aes256(matrices)
#print(f"AES: {AES}")
main_menu()

main.mainloop()