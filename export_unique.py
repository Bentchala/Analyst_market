import sqlite3
import pandas as pd
import sys

def exporter_donnees():
    try:
        # Connexion à la base
        conn = sqlite3.connect('ventes_magasin.db')
        
        # Requête unique avec jointures
        requete = """
        SELECT 
            v.date_vente,
            p.nom_produit,
            p.prix_unitaire,
            v.quantite,
            v.montant_total,
            v.mode_paiement,
            c.nom_client,
            c.type_client
        FROM Ventes v
        JOIN Produits p ON v.id_produit = p.id_produit
        JOIN Clients c ON v.id_client = c.id_client
        """
        
        # Conversion directe en DataFrame
        df = pd.read_sql_query(requete, conn)
        
        # Export unique
        df.to_csv("donnees_completes.csv", index=False)
        
        print("✅ Fichier 'donnees_completes.csv' généré avec succès !")
        print(f"📊 {len(df)} lignes exportées")

    except sqlite3.OperationalError as e:
        print(f"❌ Erreur de base de données: {str(e)}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    exporter_donnees()