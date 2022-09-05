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

    @classmethod
    def get_by_id(self, db, id_):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_profesor, rut, nombre FROM profesor WHERE id_profesor = '{}'""".format(id_)

            cursor.execute(sql)
            row = cursor.fetchone()

            if row != None:
                return Profesor(row[0], row[1], None,row[2])
            else:
                return None    
        except Exception as ex:
            raise Exception(ex)