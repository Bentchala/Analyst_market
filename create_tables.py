import sqlite3

def creer_structure():
    conn = sqlite3.connect('ventes_magasin.db')
    cursor = conn.cursor()
    
    # 1. Suppression des tables existantes (pour repartir à zéro)
    cursor.execute("DROP TABLE IF EXISTS Ventes")
    cursor.execute("DROP TABLE IF EXISTS Promotions")
    cursor.execute("DROP TABLE IF EXISTS Produits")
    cursor.execute("DROP TABLE IF EXISTS Clients")
    cursor.execute("DROP TABLE IF EXISTS Categories")
    
    # 2. Création des tables avec la nouvelle structure
    cursor.execute("""
    CREATE TABLE Categories (
        id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_categorie TEXT NOT NULL,
        description TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE Clients (
        id_client INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_client TEXT NOT NULL,
        telephone TEXT,
        quartier TEXT,
        type_client TEXT CHECK(type_client IN ('Particulier', 'Entreprise', 'Revendeur'))
    )
    """)
    
    cursor.execute("""
    CREATE TABLE Produits (
        id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_produit TEXT NOT NULL,
        id_categorie INTEGER,
        prix_unitaire INTEGER NOT NULL, -- Prix en XOF sans décimales
        code_barres TEXT UNIQUE,
        FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE Promotions (
        id_promotion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produit INTEGER,
        nom_promotion TEXT,
        remise_xof INTEGER, -- Remise fixe en XOF
        date_debut DATE NOT NULL,
        date_fin DATE NOT NULL,
        FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE Ventes (
        id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produit INTEGER NOT NULL,
        nom_produit TEXT NOT NULL, -- Duplication pour affichage direct
        id_client INTEGER NOT NULL,
        nom_client TEXT NOT NULL,  -- Duplication pour affichage direct
        date_vente DATETIME NOT NULL,
        quantite INTEGER NOT NULL,
        montant_total INTEGER NOT NULL, -- En XOF
        mode_paiement TEXT CHECK(mode_paiement IN ('Espèces', 'Wave', ' MixByYas', 'Carte Bancaire')),
        FOREIGN KEY (id_produit) REFERENCES Produits(id_produit),
        FOREIGN KEY (id_client) REFERENCES Clients(id_client)
    )
    """)
    
    conn.commit()
    conn.close()
    print("Structure créée avec succès ! Tables prêtes à être remplies.")

if __name__ == "__main__":
    creer_structure()