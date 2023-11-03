from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_ssh_private_key
from cryptography.hazmat.primitives.serialization import load_ssh_public_identity
from cryptography.hazmat.primitives import serialization
from django.conf import settings
import os
from Adminserver.crypt.keys import Keys

def load_keys():
    basedir=str(settings.BASE_DIR)
    with open(basedir+"\Authserver.pub","rb") as f:
        pub=f.read()
        auth_pub=load_ssh_public_identity(bytes(pub))
        if isinstance(auth_pub, rsa.RSAPublicKey):
            pb=True
        else:
            Exception("loading key exception ")

    with open(basedir+"\Admin.pub","rb") as f:
        pub=f.read()
        pub=load_ssh_public_identity(bytes(pub))
        if isinstance(pub, rsa.RSAPublicKey):
            pass
        else:
            Exception("loading key exception ")

    with open(basedir+"\Admin_pk","rb") as f:
        pk=f.read()
        pb_key=load_ssh_private_key(bytes(pk),None)
        if isinstance(pb_key, rsa.RSAPrivateKey):
            pk=True
        else:
            Exception("loading key exception ")

    return pb_key,pub,auth_pub

def create_keys(basefilename):

    basedir=str(settings.BASE_DIR)
    secure=os.path.join(basedir,'Adminserver','crypt','secure')
    key=rsa.generate_private_key(public_exponent=65537, key_size=1024)
    pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.OpenSSH,
            encryption_algorithm=serialization.NoEncryption()
    )
    with open(f"{secure}\{basefilename}_pk",mode="wb") as f:
        f.write(pem)

    pub=key.public_key().public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    with open(f"{secure}\{basefilename}.pub",mode="wb") as f:
        f.write(pub)
    
    return key.public_key().public_numbers().e,key.public_key().public_numbers().n,key.private_numbers().d

class Publickey:
    def __init__(self) -> None:
        pk,pub,auth_pub=load_keys()
        self.pk=Keys(pk)
        self.pub=pub
        self.auth_pub=auth_pub

global_key=Publickey()
