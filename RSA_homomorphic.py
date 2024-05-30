from sympy import mod_inverse, isprime
import random
import tkinter as tk
from tkinter import messagebox

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_prime_number(length=1024):
    p = 4
    while not isprime(p):
        p = generate_prime_candidate(length)
    return p

def generate_keys(bit_length=1024):
    p = generate_prime_number(bit_length // 2)
    q = generate_prime_number(bit_length // 2)
    n = p * q
    k = 65537
    phi = (p - 1) * (q - 1)
    d = mod_inverse(k, phi)
    return (k, n), (d, n)

def encrypt(plaintext, pubkey):
    k, n = pubkey
    ciphertext = pow(plaintext, k, n)
    return ciphertext

def decrypt(ciphertext, privkey):
    d, n = privkey
    plaintext = pow(ciphertext, d, n)
    return plaintext

def check_homomorphism(t1, t2, pubkey, privkey):
    # Шифруем t1 и t2
    E_t1 = encrypt(t1, pubkey)
    E_t2 = encrypt(t2, pubkey)

    # Дешифруем t1 и t2
    D_t1 = decrypt(E_t1, privkey)
    D_t2 = decrypt(E_t2, privkey)

    # Вывод зашифрованных значений и используемой формулы
    formula = f"E(t1 * t2) = E(t1) * E(t2) mod n = {E_t1} * {E_t2} mod {pubkey[1]}"
    print("Формула гомоморфного умножения:", formula)

    # Проверяем гомоморфное свойство
    E_t1_t2 = (E_t1 * E_t2) % pubkey[1]
    E_t1_mult_t2 = encrypt(t1 * t2, pubkey)
    return E_t1_t2 == E_t1_mult_t2, formula, E_t1, E_t2, E_t1_t2, E_t1_mult_t2

class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Cryptosystem")

        # Установка размера окна
        self.root.geometry("800x500")
        self.root.minsize(800, 500)

        # Генерация ключей
        self.pubkey, self.privkey = generate_keys()

        # Элементы интерфейса
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Введите первое число t1:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry1 = tk.Entry(self.root, width=20)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Введите второе число t2:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry2 = tk.Entry(self.root, width=20)
        self.entry2.grid(row=1, column=1, padx=10, pady=10)

        self.check_button = tk.Button(self.root, text="Проверить гомоморфное свойство", command=self.check_homomorphism)
        self.check_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.result_text = tk.Text(self.root, height=20, width=90)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def check_homomorphism(self):
        try:
            t1 = int(self.entry1.get())
            t2 = int(self.entry2.get())

            is_homomorphic, formula, E_t1, E_t2, E_t1_t2, E_t1_mult_t2 = check_homomorphism(t1, t2, self.pubkey, self.privkey)

            D_t1 = decrypt(E_t1, self.privkey)
            D_t2 = decrypt(E_t2, self.privkey)
            D_t1_t2 = decrypt(E_t1_t2, self.privkey)
            D_t1_mult_t2 = decrypt(E_t1_mult_t2, self.privkey)

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Зашифрованное значение для t1: {E_t1}\n")
            self.result_text.insert(tk.END, f"Зашифрованное значение для t2: {E_t2}\n")
            self.result_text.insert(tk.END, f"Результат умножения зашифрованных значений: {E_t1_t2}\n")
            self.result_text.insert(tk.END, f"Зашифрованное значение для t1 * t2: {E_t1_mult_t2}\n\n")
            self.result_text.insert(tk.END, "Формула гомоморфного умножения:\n" + formula + "\n\n")
            if is_homomorphic:
                self.result_text.insert(tk.END, "Гомоморфное свойство выполняется.\n\n")
            else:
                self.result_text.insert(tk.END, "Гомоморфное свойство не выполняется.\n\n")
            self.result_text.insert(tk.END, f"Дешифрованное значение для t1: {D_t1}\n")
            self.result_text.insert(tk.END, f"Дешифрованное значение для t2: {D_t2}\n")
            self.result_text.insert(tk.END, f"Дешифрованное значение для умножения зашифрованных значений: {D_t1_t2}\n")
            self.result_text.insert(tk.END, f"Дешифрованное значение для t1 * t2: {D_t1_mult_t2}\n\n")
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числа.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.mainloop()
