import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement et préparation des données
df = pd.read_csv('donnees_completes.csv', parse_dates=['date_vente'])
df['mois'] = df['date_vente'].dt.to_period('M').astype(str)
ca_mensuel = df.groupby('mois')['montant_total'].sum().reset_index()

# Configuration style
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 12
colors = sns.color_palette("husl", 8)

# Création du graphique
plt.figure(figsize=(14, 7))
sns.lineplot(
    x='mois', 
    y='montant_total', 
    data=ca_mensuel,
    marker='o',
    linewidth=2,
    color=colors[0]
)

# Personnalisation
plt.title("Évolution du chiffre d'affaires mensuel", pad=20)
plt.xlabel('Mois')
plt.ylabel('CA (XOF)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# Ajout des valeurs
for x, y in zip(ca_mensuel.index, ca_mensuel.montant_total):
    plt.text(x, y, f'{y/1e6:.1f}M', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('evolution_ca_mensuel.png', dpi=300)
plt.show()