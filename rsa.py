from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def main():
    # prv_key = RSA.generate(2048)
    prv_key = RSA.generate(2048, e=1009)
    pub_key = prv_key.public_key()

    print(f"---")
    n_bytes = prv_key.n.to_bytes((prv_key.n.bit_length() + 7) // 8, byteorder="big")
    arr = ",".join([f"0x{b:02X}" for b in n_bytes])
    print(f"RSA modulus hex:\n{arr}\n---")
    print(f"RSA public exponent:\n{prv_key.e}\n0x{prv_key.e:X}\n---")

    prv_pem = prv_key.export_key(format="PEM", pkcs=1)
    prv_der = prv_key.export_key(format="DER", pkcs=1)

    with open("data/rsa/prv_pem.txt", "wb") as f:
        f.write(prv_pem)
    with open("data/rsa/prv_der.txt", "w") as f:
        f.write(prv_der.hex())

    pub_pem = pub_key.export_key(format="PEM", pkcs=1)
    pub_der = pub_key.export_key(format="DER", pkcs=1)

    with open("data/rsa/pub_pem.txt", "wb") as f:
        f.write(pub_pem)
    with open("data/rsa/pub_der.txt", "w") as f:
        f.write(pub_der.hex())

    message = b"helloworld"
    h = SHA256.new(message)
    pkcs = pkcs1_15.new(prv_key)
    signature = pkcs.sign(h)
    pkcs.verify(h, signature)

    print(f"message text:\n{message}\n0x{message.hex()}\n---")

    hash_bytes = h.digest()
    hash_arr = ",".join([f"0x{b:02X}" for b in hash_bytes])
    print(f"hash hex:\n{h.hexdigest()}\n\n{hash_arr}\n---")

    arr = ",".join([f"0x{i:02X}" for i in signature])
    print(f"signature hex:\n{signature.hex()}\n\n{arr}\n---")


if __name__ == "__main__":
    main()
