from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_ssh_private_key
from cryptography.hazmat.primitives.serialization import load_ssh_public_identity
def main():
    key=rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption()
    )
    with open("Admin_pk","wb+") as f:
        f.write(pem)

    pub=key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    with open("Admin.pub","wb") as f:
        f.write(pub)

    with open("Admin.pub","rb") as f:
        pub=f.read()
        pb_key=load_ssh_public_identity(pub)
        if isinstance(pb_key, rsa.RSAPublicKey):
            print("rsa pub")

    with open("Admin_pk","rb") as f:
        pk=f.read()
        pb_key=load_ssh_private_key(pk,None)
        if isinstance(pb_key, rsa.RSAPrivateKey):
            print("rsa pk")

if __name__=="__main__":
    main()
