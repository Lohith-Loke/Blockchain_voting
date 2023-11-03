from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_ssh_private_key
from cryptography.hazmat.primitives.serialization import load_ssh_public_identity
from django.conf import settings

def load_keys():
    basedir=str(settings.BASE_DIR)
    with open(basedir+"\server.pub","rb") as f:
        pub=f.read()
        pb_key=load_ssh_public_identity(bytes(pub))
        if isinstance(pb_key, rsa.RSAPublicKey):
            pb=True
            

    with open(basedir+"\server_pk","rb") as f:
        pk=f.read()
        pb_key=load_ssh_private_key(bytes(pk),None)
        if isinstance(pb_key, rsa.RSAPrivateKey):
            pk=True

    return pb_key
class key:
    def __init__(self) -> None:
        self.pk=load_keys()
        

global_key=key()