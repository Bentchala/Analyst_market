import pandas as pd
import numpy as np

# Chargement des données
df = pd.read_csv('donnees_completes.csv', parse_dates=['date_vente'])

# 1. Chiffre d'affaires global
ca_total = df['montant_total'].sum()
print(f"1. Chiffre d'affaires total : {ca_total:,.0f} XOF\n")

# 2. Analyses temporelles
df['mois'] = df['date_vente'].dt.to_period('M')
ca_mensuel = df.groupby('mois')['montant_total'].sum()
print(f"2. CA mensuel moyen : {ca_mensuel.mean():,.0f} XOF")
print(f"   Panier moyen : {df['montant_total'].mean():,.0f} XOF")
print("   CA mensuel détaillé :\n", ca_mensuel.to_string(), "\n")

# 3. Analyse produits
top_produits = df.groupby('nom_produit').agg(
    quantite_totale=('quantite', 'sum'),
    ca_total=('montant_total', 'sum')
).sort_values('quantite_totale', ascending=False)

print("3. Classement des produits :")
print(top_produits.head(5).to_string(), "\n")

# 4. Analyse clients
clients_analysis = df.groupby('nom_client').agg(
    ca_total=('montant_total', 'sum'),
    transactions=('nom_client', 'count')
).sort_values('ca_total', ascending=False)

print("4. Top clients :")
print(clients_analysis.head(3).to_string())
print(f"\n   Transactions moyennes par client : {clients_analysis['transactions'].mean():.1f}\n")

# 5. Statistiques descriptives
stats = df[['quantite', 'montant_total']].describe()
stats.loc['var'] = df[['quantite', 'montant_total']].var()
stats.loc['mediane'] = df[['quantite', 'montant_total']].median()

print("5. Statistiques générales :")
print(stats.round(1).to_string())