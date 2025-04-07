import sqlite3
import pandas as pd
import sys

def extraire_donnees():
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('ventes_magasin.db')
        
        # Requêtes SQL de base
        requetes = {
            'ventes': "SELECT * FROM Ventes",
            'produits': "SELECT * FROM Produits",
            'clients': "SELECT * FROM Clients",
            'categories': "SELECT * FROM Categories"
        }
        
        # Dictionnaire pour stocker les DataFrames
        dataframes = {}
        
        # Extraction des données avec gestion d'erreur pour chaque table
        for nom_table, requete in requetes.items():
            try:
                dataframes[nom_table] = pd.read_sql_query(requete, conn)
                print(f"✅ {len(dataframes[nom_table])} lignes extraites de la table {nom_table}")
            except sqlite3.Error as e:
                print(f"❌ Erreur lors de l'extraction de {nom_table}: {str(e)}")
                dataframes[nom_table] = pd.DataFrame()  # DataFrame vide en cas d'erreur
        
        # Vérification basique des données
        if dataframes['ventes'].empty:
            raise ValueError("Aucune donnée de vente trouvée - vérifiez la base de données")
            
        # Fermeture de la connexion
        conn.close()
        
        return dataframes
        
    except Exception as e:
        print(f"🚨 Erreur critique: {str(e)}", file=sys.stderr)
        if 'conn' in locals():
            conn.close()
        sys.exit(1)

if __name__ == "__main__":
    print("Début de l'extraction des données...")
    dfs = extraire_donnees()
    
    # Affichage des aperçus
    for nom, df in dfs.items():
        if not df.empty:
            print(f"\nAperçu de la table {nom}:")
            print(df.head(3))
            print(f"Colonnes: {list(df.columns)}")
            
            