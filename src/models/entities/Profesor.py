
from werkzeug.security import check_password_hash, generate_password_hash


class Profesor():

    def __init__(self,id_profesor,rut,password,nombre="") -> None:
        self.id = id_profesor
        self.rut = rut
        self.password = password
        self.nombre = nombre

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)



