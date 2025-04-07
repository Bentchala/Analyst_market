import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
df = pd.read_csv('donnees_completes.csv', parse_dates=['date_vente'])
ca_par_produit = df.groupby('nom_produit')['montant_total'].sum().nlargest(5).reset_index()

# Configuration du style
colors = sns.color_palette("husl", 8)
plt.rcParams['font.size'] = 10

# Création d'un camembert 2D (solution recommandée)
plt.figure(figsize=(10, 10))
plt.pie(
    ca_par_produit['montant_total'],
    labels=ca_par_produit['nom_produit'],
    autopct=lambda p: f'{p:.1f}%\n({p*sum(ca_par_produit["montant_total"])/1e6:.1f}M XOF)',
    startangle=90,
    colors=colors,
    explode=[0.1] + [0]*(len(ca_par_produit)-1),
    shadow=True,
    textprops={'ha': 'center', 'va': 'center'}  # Alignement du texte
)

plt.title("Répartition du CA par produit (Top 5)", pad=20)
plt.tight_layout()
plt.savefig('repartition_produits.png', dpi=300, bbox_inches='tight')
plt.show()