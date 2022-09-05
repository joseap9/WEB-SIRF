from .entities.Profesor import Profesor


class ModelUser():

    @classmethod
    def login(self, db, profesor):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_profesor, nombre, password, rut FROM profesor WHERE rut = '{}'""".format(profesor.rut)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                profesor = Profesor(row[0], row[1], Profesor.check_password(row[2],profesor.password), row[3])
                return profesor
            else:
                return None    
        except Exception as ex:
            raise Exception(ex)