from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():
        @staticmethod
        def getAllGenres():
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = "select distinct g.Name from genre g order by g.Name"

            cursor.execute(query)

            for row in cursor:
                results.append(row["Name"])

            cursor.close()
            conn.close()
            return results

        @staticmethod
        def getAllArtistsByGenre(genere):
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = """select distinct a.ArtistId as ArtistId, a.Name as Name
                      from artist a , album a2 , track t, genre g 
                      where a.ArtistId = a2.ArtistId and a2.AlbumId = t.AlbumId and g.GenreId = t.GenreId 
                      and g.Name  = %s"""

            cursor.execute(query, (genere,))

            for row in cursor:
                results.append(Artist(**row))

            cursor.close()
            conn.close()
            return results

        @staticmethod
        def getCostumerArtistsCount(genere):
            conn = DBConnect.get_connection()

            results = []

            cursor = conn.cursor(dictionary=True)
            query = """select i.CustomerId , a2.ArtistId, count(*) as ntracks
                       from invoice i , invoiceline i2 , track t , album a , artist a2 , genre g 
                       where i.InvoiceId = i2.InvoiceId and i2.TrackId = t.TrackId and t.GenreId = g.GenreId 
                       and t.AlbumId = a.AlbumId and a.ArtistId = a2.ArtistId  and g.Name  = %s
                       group by i.CustomerId , a2.ArtistId"""

            cursor.execute(query, (genere,))

            for row in cursor:
                results.append((row["CustomerId"], row["ArtistId"], row["ntracks"]))

            cursor.close()
            conn.close()
            return results


