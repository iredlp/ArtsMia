from database.DB_connect import DBConnect
from model.arco import Arco


#from model.artObject import artObject


class DAO():

    @staticmethod
    def getAllNodes():
        from model.artObject import artObject
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from objects o "
        cursor.execute(query)

        for row in cursor:
            result.append(artObject(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdgePeso(v1, v2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo, exhibition_objects eo2 
                    where eo.exhibition_id=eo2.exhibition_id 
                    and eo.object_id<eo2.object_id 
                    and eo.object_id =%s and eo2.object_id =%s
                    group by  eo.object_id, eo2.object_id """
        cursor.execute(query, (v1.object_id, v2.object_id))

        for row in cursor:
            result.append(row["peso"])



        cursor.close()
        conn.close()

        if len(result) == 0:
            return None

        return result

    @staticmethod
    def getAllEdges(idMapAO):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """  select eo.object_id as o1, eo2.object_id as o2, count(*) as peso
                    from exhibition_objects eo, exhibition_objects eo2 
                    where eo.exhibition_id=eo2.exhibition_id 
                    and eo.object_id<eo2.object_id 
                    group by  eo.object_id, eo2.object_id
                    ORDER BY peso desc"""
        cursor.execute(query)

        for row in cursor:
            #result.append(o1,o2,peso)
            result.append(Arco(idMapAO[row["o1"]],idMapAO[row["o2"]] ,row["peso"]))
        cursor.close()
        conn.close()

        if len(result) == 0:
            return None
        return result
