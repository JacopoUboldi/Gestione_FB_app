import pymssql

class WrapperDB:
    
    conn = 0
    
    def __init__(self, server="213.140.22.237\\SQLEXPRESS", user="CRD2122", \
               password="xxx123##", database="CRD2122"):
        self._server=server
        self._user=user
        self._password=password
        self._database=database
        
        
    def connetti(self):
        #connessione
        try:
            WrapperDB.conn = pymssql.connect(server = self._server, user = self._user, \
                        password = self._password, database = self._database)
            return WrapperDB.conn	

        except:
            print(f"\nConnessione NON riuscita! (DB: {self._database})\n")
            return 0
        
            
    def disconnetti(self, co):
        #disconnessione	
        try:
            co.close()   
        except:
            print(f"\nCHIUSURA connessione NON riuscita! (DB: {self._database})\n")
            return 0
        

    def elencoPost(self, as_dict = False):
        #restituisce una lista di tuple se as_dict = False
        #altrimenti restituisce una lista di coppie chiave/valore (dictionary)
        conn = self.connetti()
        lista = []
        try:
            cur = conn.cursor(as_dict = as_dict)
            sql = "SELECT Id, Autore, Testo, [Like] FROM UBOL_FB_Post ORDER BY [Like] DESC"
            cur.execute(sql)
            lista = cur.fetchall()
        except:
            err = "Bisogna risolvere questo problema"
            print(f"[elencoPost] {err}")
        self.disconnetti(conn)
        return lista

    
    def singoloPost(self, id):
        #restituisce un singolo post
        ret = {}
        conn = self.connetti()
        try:
            cursore = conn.cursor(as_dict = True)
            sql = f"""
                SELECT Id, Autore, Testo, [Like] 
                FROM UBOL_FB_Post 
                WHERE id = {id}   
                """
            cursore.execute(sql)
            ret = cursore.fetchone()
        except:
            err = "Bisogna risolvere un problema..."
            print(f"[singoloPost] {err}")
        self.disconnetti(conn)
        return ret    


    def inserisciPost(self, parametri):
        #inserisce un nuovo post
        #parametri: (autore, testo)
        try:
            c = self.connetti() 
            cursore = c.cursor()
            sql = "INSERT INTO UBOL_FB_Post (Autore, Testo) VALUES (%s , %s)"
            cursore.execute(sql, parametri)
            c.commit()
            self.disconnetti(c)
            return True            
        except:
            #print("\INSERIMENTO POST/i: Si sono verificati degli errori!")
            self.disconnetti(c)
            return False

    def daiLikeAPost(self, id, is_like = True):
        #mette like a post
        #se is_like è False toglie un like
        try:
            c = self.connetti() 
            cursore = c.cursor()
            sql = "UPDATE UBOL_FB_Post SET [Like] = "
            if is_like == True: 
                sql += "[Like] + 1 "
            else:
                sql += "[Like] - 1 "
            sql += "WHERE id = %d"
            cursore.execute(sql, id)
            c.commit()
            #print("LIKE A POST AVVENUTO")
            self.disconnetti(c)
            return True                        
        except:
            #print("\LIKE A POST/i: Si sono verificati degli errori!")
            self.disconnetti(c)
            return False


    def eliminaPost(self, id):
        #elimina un post
        try:
            c = self.connetti() 
            cursore = c.cursor()
            sql = "DELETE UBOL_FB_Post WHERE id = %d"
            cursore.execute(sql, id)
            c.commit()
            #print("ELIMINA POST AVVENUTO")
            self.disconnetti(c)
            return True            
            
        except:
            #print("\ELIMINA POST/i: Si sono verificati degli errori!")
            self.disconnetti(c)
            return False


         