import sqlite3
import pandas as pd
from datetime import datetime

def exporter_donnees():
    conn = sqlite3.connect('ventes_magasin.db')
    
    # 1. Extraire les ventes
    ventes_df = pd.read_sql_query("SELECT * FROM Ventes", conn)
    
    # 2. Extraire produits et clients
    produits_df = pd.read_sql_query("SELECT * FROM Produits", conn)
    clients_df = pd.read_sql_query("SELECT * FROM Clients", conn)
    
    # 3. Sauvegarder en CSV (sans date dans le nom)
    ventes_df.to_csv("export_ventes.csv", index=False)
    produits_df.to_csv("export_produits.csv", index=False)
    clients_df.to_csv("export_clients.csv", index=False)
    
    conn.close()
    print("Fichiers CSV générés avec succès !")

if __name__ == "__main__":
    exporter_donnees()