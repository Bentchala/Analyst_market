import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement et préparation des données
df = pd.read_csv('donnees_completes.csv', parse_dates=['date_vente'])
df['mois'] = df['date_vente'].dt.to_period('M').astype(str)
df['mois_dt'] = df['date_vente'].dt.to_period('M').dt.to_timestamp()

# Configuration style
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 10
colors = sns.color_palette("husl", 8)

# -----------------------------------------------------------
# 1. Heatmap des ventes (Mois x Produit)
# -----------------------------------------------------------
plt.figure(figsize=(12, 8))
pivot_table = df.pivot_table(
    index='mois_dt',
    columns='nom_produit',
    values='montant_total',
    aggfunc='sum',
    fill_value=0
)

sns.heatmap(
    pivot_table / 1e6,  # Conversion en millions
    cmap="YlGnBu",
    annot=True,
    fmt=".1f",
    linewidths=.5,
    cbar_kws={'label': 'CA (Millions XOF)'}
)

plt.title('Répartition mensuelle du CA par produit (en millions XOF)')
plt.xlabel('Produit')
plt.ylabel('Mois')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('heatmap_ventes.png', dpi=300)
plt.close()

# -----------------------------------------------------------
# 2. Barres empilées mensuelles
# -----------------------------------------------------------
plt.figure(figsize=(14, 7))
df_grouped = df.groupby(['mois_dt', 'nom_produit'])['montant_total'].sum().unstack()

df_grouped.plot(
    kind='bar',
    stacked=True,
    color=colors,
    edgecolor='black',
    width=0.9
)

plt.title('Décomposition mensuelle des ventes par produit')
plt.xlabel('Mois')
plt.ylabel('CA (XOF)')
plt.grid(axis='y', alpha=0.3)
plt.legend(title='Produits', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('stacked_bars.png', dpi=300)
plt.close()

# -----------------------------------------------------------
# 3. Courbes d'évolution par produit
# -----------------------------------------------------------
plt.figure(figsize=(14, 7))
sns.lineplot(
    data=df,
    x='mois_dt',
    y='montant_total',
    hue='nom_produit',
    estimator='sum',
    palette=colors,
    marker='o'
)

plt.title('Évolution comparative des ventes par produit')
plt.xlabel('Mois')
plt.ylabel('CA (XOF)')
plt.legend(bbox_to_anchor=(1.05, 1))
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('courbes_produits.png', dpi=300)
plt.show()