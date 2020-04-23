import random


def is_prime(n: int) -> bool:
    prime = True
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            prime = False
    return prime


def gcd(a: int, b: int) -> int:
    res = 1
    for i in range(min(a, b), 1, -1):
        if (a % i == 0) and (b % i == 0):
            res = i
            break
    return res


def multiplicative_inverse(e: int, phi: int) -> int:
    data = []
    m = phi
    while True:
        mas = []
        mas.append(phi // e)
        mas.append(0)
        mas.append(0)
        data.append(mas)
        if phi % e == 0:
            break
        c = phi % e
        phi = e
        e = c
    data[len(data) - 1][2] = 1
    for i in range(len(data) - 1, 0, -1):
        data[i - 1][2] = data[i][1] - data[i][2] * data[i - 1][0]
        data[i - 1][1] = data[i][2]
    return (data[0][2] + m) % m


def generate_keypair(p=17, q=23):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 1505
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = multiplicative_inverse(e, phi)
    return ((e, n), (d, n))


def encrypt(pk, plaintext):
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk, ciphertext):
    # Unpack the key into its components
    key, n = pk
    key = int(key)
    n = int(n)
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return ''.join(plain)
