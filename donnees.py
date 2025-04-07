import sqlite3
import random
from datetime import datetime, timedelta

def creer_tables():
    conn = sqlite3.connect('ventes_magasin.db')
    cursor = conn.cursor()
    
    # Suppression des tables existantes
    cursor.execute("DROP TABLE IF EXISTS Ventes")
    cursor.execute("DROP TABLE IF EXISTS Promotions")
    cursor.execute("DROP TABLE IF EXISTS Produits")
    cursor.execute("DROP TABLE IF EXISTS Clients")
    cursor.execute("DROP TABLE IF EXISTS Categories")
    
    # Recréation des tables avec la contrainte CHECK corrigée
    cursor.execute("""
    CREATE TABLE Categories (
        id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_categorie TEXT NOT NULL,
        description TEXT
    )""")
    
    cursor.execute("""
    CREATE TABLE Clients (
        id_client INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_client TEXT NOT NULL,
        telephone TEXT,
        quartier TEXT,
        type_client TEXT CHECK(type_client IN ('Particulier', 'Entreprise', 'Revendeur'))
    )""")
    
    cursor.execute("""
    CREATE TABLE Produits (
        id_produit INTEGER PRIMARY KEY AUTOINCREMENT,
        id_categorie INTEGER,
        nom_produit TEXT NOT NULL,
        prix_unitaire INTEGER NOT NULL,
        code_barres TEXT UNIQUE,
        FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
    )""")
    
    cursor.execute("""
    CREATE TABLE Promotions (
        id_promotion INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produit INTEGER,
        nom_promotion TEXT,
        remise_xof INTEGER,
        date_debut DATE NOT NULL,
        date_fin DATE NOT NULL,
        FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
    )""")
    
    cursor.execute("""
    CREATE TABLE Ventes (
        id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
        id_produit INTEGER NOT NULL,
        nom_produit TEXT NOT NULL,
        id_client INTEGER NOT NULL,
        nom_client TEXT NOT NULL,
        date_vente DATETIME NOT NULL,
        quantite INTEGER NOT NULL,
        montant_total INTEGER NOT NULL,
        mode_paiement TEXT CHECK(mode_paiement IN ('Espèces', 'Wave', 'MixByYas', 'Carte Bancaire')),
        FOREIGN KEY (id_produit) REFERENCES Produits(id_produit),
        FOREIGN KEY (id_client) REFERENCES Clients(id_client)
    )""")
    
    conn.commit()
    conn.close()

def inserer_donnees():
    conn = sqlite3.connect('ventes_magasin.db')
    cursor = conn.cursor()
    
    try:
        # 1. Insertion des catégories
        categories = [
            ("Téléphonie", "Smartphones et accessoires"),
            ("Électroménager", "Appareils ménagers"),
            ("Alimentation", "Produits alimentaires de base"),
            ("Cosmétiques", "Produits de beauté"),
            ("Habillement", "Vêtements et chaussures"),
            ("Bureau", "Fournitures scolaires et de bureau"),
            ("Bricolage", "Matériaux de construction")
        ]
        cursor.executemany("INSERT INTO Categories (nom_categorie, description) VALUES (?, ?)", categories)
        
        # 2. Insertion des clients
        clients = [
            ("Moussa Diop", "771234567", "Plateau", "Revendeur"),
            ("Amina Sy", "761234567", "Mermoz", "Particulier"),
            ("Papa Sow", "701234567", "Fass", "Entreprise"),
            ("Fatou Ndiaye", "781234567", "Ouakam", "Particulier"),
            ("Ibrahima Fall", "751234567", "Grand Dakar", "Revendeur"),
            ("Adama Ba", "772345678", "Liberté", "Particulier"),
            ("Khadija Diallo", "762345678", "HLM", "Revendeur"),
            ("Oumar Kane", "702345678", "Gueule Tapée", "Entreprise")
        ]
        cursor.executemany("INSERT INTO Clients (nom_client, telephone, quartier, type_client) VALUES (?, ?, ?, ?)", clients)
        
        # 3. Insertion des produits (prix en XOF)
        produits = [
            (1, "Samsung Galaxy A23", 85000, "123456789012"),
            (1, "Tecno Spark 10", 65000, "234567890123"),
            (2, "Climatiseur 12000 BTU", 450000, "345678901234"),
            (2, "Réfrigérateur 300L", 325000, "456789012345"),
            (3, "Riz 5kg", 3500, "567890123456"),
            (3, "Huile végétale 5L", 6000, "678901234567"),
            (4, "Lait hydratant Nivea", 7500, "789012345678"),
            (5, "Jeans homme", 12500, "890123456789"),
            (6, "Cahier 200 pages", 1500, "901234567890"),
            (7, "Ciment 50kg", 55000, "012345678901"),
            (1, "iPhone 13", 650000, "112345678901"),
            (3, "Sucre 1kg", 1200, "212345678901")
        ]
        cursor.executemany("INSERT INTO Produits (id_categorie, nom_produit, prix_unitaire, code_barres) VALUES (?, ?, ?, ?)", produits)
        
        # 4. Insertion des promotions
        promotions = [
            (1, "Promo Ramadan", 10000, "2024-03-01", "2024-04-15"),
            (3, "Promo Rentrée", 500, "2024-09-01", "2024-10-15"),
            (5, "Soldes été", 2500, "2024-06-01", "2024-07-31"),
            (11, "Black Friday", 50000, "2024-11-25", "2024-11-30")
        ]
        cursor.executemany("INSERT INTO Promotions (id_produit, nom_promotion, remise_xof, date_debut, date_fin) VALUES (?, ?, ?, ?, ?)", promotions)
        
        conn.commit()
        
        # 5. Génération de 1200 ventes
        modes_paiement = ['Espèces', 'Wave', 'MixByYas', 'Carte Bancaire']
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        # Récupération des IDs produits et clients
        cursor.execute("SELECT id_produit, nom_produit, prix_unitaire FROM Produits")
        produits_data = cursor.fetchall()
        
        cursor.execute("SELECT id_client, nom_client FROM Clients")
        clients_data = cursor.fetchall()
        
        # Poids pour les best-sellers
        weights = [0.1, 0.15, 0.05, 0.08, 0.2, 0.15, 0.05, 0.05, 0.1, 0.02, 0.03, 0.02]
        
        for i in range(1200):  # 1200 ventes au total
            # Choix aléatoire pondéré
            id_produit, nom_produit, prix = random.choices(produits_data, weights=weights, k=1)[0]
            id_client, nom_client = random.choice(clients_data)
            
            # Date aléatoire avec plus de ventes en décembre
            if random.random() < 0.15:  # 15% en décembre
                year = random.choice([2023, 2024])
                date_vente = datetime(year, 12, random.randint(1, 31))
            else:
                delta = end_date - start_date
                date_vente = start_date + timedelta(days=random.randint(0, delta.days))
            
            # Quantité selon type de produit
            if id_produit in [5, 6]:  # Produits alimentaires
                quantite = random.randint(1, 15)
            elif id_produit in [3, 4, 11]:  # Gros articles
                quantite = random.randint(1, 3)
            else:
                quantite = random.randint(1, 5)
            
            # Vérification promotion
            promo = None
            cursor.execute("""
            SELECT remise_xof FROM Promotions 
            WHERE id_produit = ? AND date_debut <= ? AND date_fin >= ?
            """, (id_produit, date_vente.date(), date_vente.date()))
            promo_result = cursor.fetchone()
            if promo_result:
                promo = promo_result[0]
            
            # Calcul montant
            montant = prix * quantite - (promo if promo else 0)
            
            # Insertion
            cursor.execute("""
            INSERT INTO Ventes 
            (id_produit, nom_produit, id_client, nom_client, date_vente, quantite, montant_total, mode_paiement) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_produit,
                nom_produit,
                id_client,
                nom_client,
                date_vente.strftime("%Y-%m-%d %H:%M:%S"),
                quantite,
                montant,
                random.choice(modes_paiement)
            ))
            
            # Commit périodique
            if i % 100 == 0:
                conn.commit()
                print(f"{i} ventes insérées...")
        
        conn.commit()
        print("1200 ventes générées avec succès !")
        
    except Exception as e:
        conn.rollback()
        print(f"Erreur: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    creer_tables()
    inserer_donnees()