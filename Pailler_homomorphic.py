import tkinter as tk
from tkinter import messagebox
import random
from sympy import isprime, mod_inverse, lcm, gcd

# Функция для генерации большого простого числа
def generate_large_prime(bits=256):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate

# Генерация ключей для системы Пейе
def generate_keys(bits=256):
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    n = p * q
    lamb = lcm(p - 1, q - 1)
    g = n + 1
    mu = mod_inverse(lamb, n)
    return (n, g), (lamb, mu)

# Шифрование в системе Пайе
def encrypt(public_key, plaintext):
    n, g = public_key
    r = random.randint(1, n - 1)
    while gcd(r, n) != 1:
        r = random.randint(1, n - 1)
    c = (pow(g, plaintext, n**2) * pow(r, n, n**2)) % n**2
    return c

# Дешифрование в системе Пайе
def decrypt(private_key, public_key, ciphertext):
    n, g = public_key
    lamb, mu = private_key
    u = pow(int(ciphertext), int(lamb), int(n)**2)
    l = (u - 1) // n
    plaintext = (l * mu) % n
    return plaintext

# Функция демонстрации гомоморфного шифрования по сложению
def homomorphic_encryption(public_key, ciphertext1, ciphertext2):
    n, g = public_key
    c_homomorphic = (ciphertext1 * ciphertext2) % n**2
    return c_homomorphic

# Создание GUI с использованием tkinter
class PaillierApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Paillier Cryptosystem")

        # Установка размера окна
        self.root.geometry("800x600")
        self.root.minsize(800, 600)

        # Генерация ключей
        self.public_key, self.private_key = generate_keys()

        # Элементы интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Ввод первого числа
        tk.Label(self.root, text="Введите первое число:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry1 = tk.Entry(self.root, width=30)
        self.entry1.grid(row=0, column=1, padx=10, pady=10)

        # Ввод второго числа
        tk.Label(self.root, text="Введите второе число:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry2 = tk.Entry(self.root, width=30)
        self.entry2.grid(row=1, column=1, padx=10, pady=10)

        # Кнопка для шифрования и дешифрования
        self.encrypt_button = tk.Button(self.root, text="Шифровать и дешифровать", command=self.encrypt_decrypt)
        self.encrypt_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Текстовые поля для отображения результатов
        self.result_text = tk.Text(self.root, height=20, width=90)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def encrypt_decrypt(self):
        try:
            plaintext1 = int(self.entry1.get())
            plaintext2 = int(self.entry2.get())

            # Шифрование
            ciphertext1 = encrypt(self.public_key, plaintext1)
            ciphertext2 = encrypt(self.public_key, plaintext2)

            # Дешифрование
            decrypted1 = decrypt(self.private_key, self.public_key, ciphertext1)
            decrypted2 = decrypt(self.private_key, self.public_key, ciphertext2)

            # Гомоморфное шифрование
            ciphertext_homomorphic = homomorphic_encryption(self.public_key, ciphertext1, ciphertext2)
            decrypted_homomorphic = decrypt(self.private_key, self.public_key, ciphertext_homomorphic)

            # Формула гомоморфного сложения
            formula = f"({ciphertext1} * {ciphertext2}) % {self.public_key[0]}**2"

            # Отображение результатов
            result = (
                f"Открытый текст 1: {plaintext1}\n"
                f"Зашифрованный текст 1: {ciphertext1}\n"
                f"Дешифрованный текст 1: {decrypted1}\n\n"
                f"Открытый текст 2: {plaintext2}\n"
                f"Зашифрованный текст 2: {ciphertext2}\n"
                f"Дешифрованный текст 2: {decrypted2}\n\n"
                f"Гомоморфный шифротекст: {ciphertext_homomorphic}\n"
                f"Дешифрованный гомоморфный результат: {decrypted_homomorphic}\n"
                f"Ожидаемый гомоморфный результат: {(plaintext1 + plaintext2) % self.public_key[0]}\n\n"
                f"Формула гомоморфного сложения: {formula}"
            )
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
        except ValueError:
            messagebox.showerror("Ошибка ввода", "Пожалуйста, введите корректные числа")

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PaillierApp(root)
    root.mainloop()
