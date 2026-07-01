import tkinter as tk
import functions as func

def clear_window():
    for widget in main.winfo_children():
        widget.destroy()

def copy(text):
    main.clipboard_clear()
    main.clipboard_append(text)
    main.update()

main = tk.Tk()
main.title("Encryption")
main.geometry("500x500")

main_choice = tk.StringVar(value="DHKE")
autofills = {
    "prime" : 23,
    "base" : 11,
    "secret" : 6,
    "public" : 10,  
    "shared" : 6,
    "sha256" : "b253668f6b59f1ff28522831931e4d3c5a3de533965af22e961735437c0172cb",
    "text" : "Attack at dawn!",
    "cipher" : "a4cefb9e24c08289d7d9f897cef1cfa8"
}

def main_menu():
    clear_window()
    tk.Label(main, text="What do you want to do?").pack()
    tk.Button(main, text="Make a public key", command=lambda: build_dhke(0)).pack()
    tk.Button(main, text="Calculate the private key", command=lambda: calculate_dhke(0)).pack()
    tk.Button(main, text="Convert a private key to SHA-256", command=lambda: sha_256(0)).pack()
    tk.Button(main, text="Encrypt plaintext", command=lambda: encrypt(0)).pack()
    tk.Button(main, text="Decrypt ciphertext", command=lambda: decrypt(0)).pack()

def build_dhke(offset):
    if offset == 0:
        clear_window()
    tk.Label(main, text="Building a public key").grid(row=0 + offset, column=1)
    
    tk.Label(main, text="What shared prime did you choose?").grid(row=1 + offset, column=0)
    prime = tk.Entry(main)
    prime.insert(0, autofills["prime"])
    prime.grid(row=1 + offset, column=2)
    
    tk.Label(main, text="What shared base did you choose?").grid(row=2 + offset, column=0)
    base = tk.Entry(main)
    base.insert(0, autofills["base"])
    base.grid(row=2 + offset, column=2)

    tk.Label(main, text="What's your secret key?").grid(row=3 + offset,   column=0)
    secret = tk.Entry(main)
    secret.insert(0, autofills["secret"])
    secret.grid(row=3 + offset, column=2)

    tk.Button(main, text="Submit", command=lambda: build_dhke_answer(prime, base, secret)).grid(row=4 + offset, column=1)
    tk.Button(main, text="Back to main menu", command=main_menu).grid(row=5 + offset, column=1)

def build_dhke_answer(prime, base, secret):
    global autofills
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
        build_dhke(1, (23, 11, 6))
        return
    
    if func.check_prime(prime) == False:
        tk.Label(main, text=f"{prime} isn't prime!").grid(row=0, column=1)
        build_dhke(1, (23, str(base), str(secret)))
        return
    
    key = func.make_dhke(prime, base, secret)

    autofills.update({
        "prime" : prime,
        "base" : base,
        "secret" : secret
    })
    tk.Label(main, text=f"Your public key is {key}").pack()
    tk.Button(main, text="Add to clipboard", command=lambda: copy(str(key))).pack()
    tk.Button(main, text="Back to main menu", command=main_menu).pack()


def calculate_dhke(offset):
    if offset == 0:
        clear_window()
    
    tk.Label(main, text="Calculating the shared private key").grid(row=0 + offset, column=1)
    
    tk.Label(main, text="What shared prime did you choose?").grid(row=1 + offset, column=0)
    prime = tk.Entry(main)
    prime.insert(0, autofills["prime"])
    prime.grid(row=1 + offset, column=2)
    
    tk.Label(main, text="What was your secret?").grid(row=2 + offset, column=0)
    secret = tk.Entry(main)
    secret.insert(0, autofills["secret"])
    secret.grid(row=2 + offset, column=2)

    tk.Label(main, text="What was the other person's public key?").grid(row=3 + offset,   column=0)
    public = tk.Entry(main)
    public.insert(0, autofills["public"])
    public.grid(row=3 + offset, column=2)

    tk.Button(main, text="Submit", command=lambda: calculate_dhke_answer(prime, secret, public)).grid(row=4 + offset, column=1)
    tk.Button(main, text="Back to main menu", command=main_menu).grid(row=5 + offset, column= 1)

def calculate_dhke_answer(prime, secret, public):
    global autofills
    prime = prime.get()
    secret = secret.get()
    public = public.get()
    clear_window()

    try:
        prime = int(prime)
        secret = int(secret)
        public = int(public)
    except ValueError:
        tk.Label(main, text="Invalid integers").grid(row=0, column=1)
        build_dhke(1, (23, 11, 6))
        return
    
    if func.check_prime(prime) == False:
        tk.Label(main, text=f"{prime} isn't prime!").grid(row=0, column=1)
        build_dhke(1, (23, str(base), str(secret)))
        return
    
    key = func.calculate_dhke(prime, secret, public)
    autofills["shared"] = key
    tk.Label(main, text=f"Your shared private key is {key}").pack()
    tk.Button(main, text="Add to clipboard", command=lambda: copy(str(key))).pack()
    tk.Button(main, text="Back to main menu", command=main_menu).pack()


def sha_256(offset):
    if offset == 0:
        clear_window()
    tk.Label(main, text="Hash your shared secret through SHA-256").grid(row=0 + offset, column=1)

    tk.Label(main, text="The shared key to hash").grid(row=1 + offset, column=0)
    shared = tk.Entry(main)
    shared.insert(0, autofills["shared"])
    shared.grid(row=1 + offset, column=2)
    
    tk.Button(main, text="Submit", command=lambda: sha_256_answer(shared)).grid(row=2 + offset, column=1)
    tk.Button(main, text="Back to main menu", command=main_menu).grid(row=3 + offset, column=1)

def sha_256_answer(shared):
    global autofills
    shared = shared.get()
    clear_window()

    try:
        shared = int(shared)
    except ValueError:
        tk.Label(main, "Invalid integer").grid(row=0, column=1)
        sha_256(1)
    
    key = func.sha256(shared)
    autofills["sha256"] = key
    tk.Label(main, text=f"Your SHA-256 hash is:").pack()
    tk.Label(main, text=key).pack()
    tk.Button(main, text="Add to clipboard", command=lambda: copy(str(key))).pack()
    tk.Button(main, text="Back to main menu", command=main_menu).pack()

def encrypt(offset):
    if offset == 0:
        clear_window()
    
    tk.Label(main, text="Encrypt using your SHA-256 Hash").grid(row=0 + offset, column=1)

    tk.Label(main, text="The SHA-256 Hash to use").grid(row=1 + offset, column=0)
    sha = tk.Entry(main)
    sha.insert(0, autofills["sha256"])
    sha.grid(row=1 + offset, column=2)

    tk.Label(main, text="The plaintext to encrypt").grid(row=2 + offset, column=0)
    text = tk.Entry(main)
    text.insert(0, autofills["text"])
    text.grid(row=2 + offset, column=2)

    tk.Button(main, text="Submit", command=lambda: cipher(sha, text, True)).grid(row=3 + offset, column=1)
    tk.Button(main, text="Back to main menu", command=main_menu).grid(row=4 + offset, column=1)

def cipher(sha, text, encrypt):
    global autofills
    sha = sha.get()
    text = text.get()
    clear_window()

    result = func.aes256(sha, text, encrypt)

    if result is None:
        result = "Invalid cyphertext or SHA-256 key"

    if encrypt == True:
        autofills["text"] = text
        tk.Label(main, text="Your AES-256 encrypted message is:").pack()
        output = tk.Text(main, width=70, height=8)
        output.pack()

        output.delete("1.0", "end")
        output.insert("1.0", result)
        output.config(state="disabled")
    else:
        tk.Label(main, text="Your decrypted text is:").pack()
        output = tk.Text(main, width=70, height=8)
        output.pack()

        output.delete("1.0", "end")
        output.insert("1.0", result)
        output.config(state="disabled")
    
    tk.Button(main, text="Add to clipboard", command=lambda: copy(result)).pack()
    tk.Button(main, text="Back to main menu", command=main_menu).pack()
    


def decrypt(offset):
    if offset == 0:
        clear_window()
    
    tk.Label(main, text="Decrypt using your SHA-256 Hash").grid(row=0 + offset, column=1)

    tk.Label(main, text="The SHA-256 Hash to use").grid(row=1 + offset, column=0)
    sha = tk.Entry(main)
    sha.insert(0, autofills["sha256"])
    sha.grid(row=1 + offset, column=2)

    tk.Label(main, text="The ciphertext to decrypt").grid(row=2 + offset, column=0)
    text = tk.Entry(main)
    text.insert(0, autofills["cipher"])
    text.grid(row=2 + offset, column=2)

    tk.Button(main, text="Submit", command=lambda: cipher(sha, text, False)).grid(row=3 + offset, column=1)
    tk.Button(main, text="Back to main menu", command=main_menu).grid(row=4 + offset, column=1)

main_menu()

main.mainloop()