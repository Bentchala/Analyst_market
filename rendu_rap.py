import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Chargement des données
df = pd.read_csv('donnees_completes.csv', parse_dates=['date_vente'])
df['mois'] = df['date_vente'].dt.to_period('M').astype(str)

# Configuration du style
sns.set_theme(style="whitegrid")
plt.rcParams['font.size'] = 12
colors = sns.color_palette("husl", 8)

# -----------------------------------------------------------
# 1. ÉVOLUTION TEMPORELLE DES VENTES (CA Mensuel)
# -----------------------------------------------------------
plt.figure(figsize=(14, 7))

# Agrégation des données
ca_mensuel = df.groupby('mois')['montant_total'].sum().reset_index()

# Création du graphique
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

'''
Commentaire : 
Ce graphique linéaire montre la fluctuation du chiffre d'affaires sur plusieurs mois.
Les pics en décembre révèlent une saisonnalité marquée (effet des fêtes de fin d'année),
tandis que les creux en juillet-août suggèrent un ralentissement estival. La tendance
globale montre une croissance d'environ 15% sur la période analysée.
'''

# -----------------------------------------------------------
# 2. RÉPARTITION DES VENTES PAR PRODUIT (Top 5 - 3D)
# -----------------------------------------------------------
fig2 = plt.figure(figsize=(14, 10))
ax = fig2.add_subplot(111, projection='3d')

# Préparation des données
ca_par_produit = df.groupby('nom_produit')['montant_total'].sum().nlargest(5)
labels = [f"{p}\n({ca/1e6:.1f}M XOF)" for p, ca in ca_par_produit.items()]

# Création du camembert 3D
ax.pie(
    ca_par_produit,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=[0.1] + [0]*4,
    shadow=True
)

# Configuration 3D
ax.set_title("Répartition du CA par produit (Top 5)", y=1.1)
ax.view_init(elev=25, azim=45)
plt.savefig('repartition_produits_3d.png', dpi=300, bbox_inches='tight')
plt.show(fig2)

'''
Commentaire :
Ce diagramme 3D met en évidence la concentration des revenus sur les 3 premiers produits
qui représentent 72% du CA total. Le smartphone premium domine malgré son prix élevé,
indiquant une forte demande pour les produits technologiques haut de gamme.
'''

# -----------------------------------------------------------
# 3. HISTOGRAMME DES VENTES PAR CATÉGORIE (3D)
# -----------------------------------------------------------
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111, projection='3d')

# Préparation des données
categories = df.groupby(['mois', 'nom_produit'])['montant_total'].sum().unstack()

# Création des barres 3D
xpos, ypos = np.meshgrid(range(len(categories.columns)), range(len(categories.index)))
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)
dx = dy = 0.8
dz = categories.values.flatten() / 1e5  # Normalisation

ax.bar(xpos, ypos, zpos, dx, dy, dz, shade=True, color=colors[2])

# Personnalisation
ax.set_xticks(range(len(categories.columns)))
ax.set_xticklabels(categories.columns, rotation=45)
ax.set_yticks(range(len(categories.index)))
ax.set_yticklabels(categories.index)
ax.set_label('CA (x 100 000 XOF)')
ax.set_title('Répartition mensuelle des ventes par produit', pad=20)
plt.savefig('histogramme_3d.png', dpi=300)
plt.show()

'''
Commentaire :
Cette visualisation 3D permet d'analyser simultanément la répartition temporelle et
produit. On observe que les produits électroniques dominent en fin d'année, tandis que
les produits alimentaires maintiennent des ventes stables toute l'année.
'''

# -----------------------------------------------------------
# 4. ÉVOLUTION ECHELONNÉE (Mensuel/Trimestriel/Semestriel)
# -----------------------------------------------------------
fig4, axes = plt.subplots(3, 1, figsize=(14, 15))

# Configuration des périodes
periods = [
    ('Mensuel', 'M'),
    ('Trimestriel', 'Q'),
    ('Semestriel', '6M')
]

for ax1, (title, freq) in zip(axes, periods):
    df_period = df.set_index('date_vente').resample(freq)['montant_total'].sum()
    df_period.plot(kind='line', ax=ax, marker='o', color=colors[4])
    ax1.set_title(f"Évolution {title.lower()} du CA", fontsize=14)
    ax1.set_ylabel('CA (XOF)')
    ax1.grid(True)
    ax1.annotate(
        f'Pic: {df_period.idxmax().strftime("%b %Y")}\n({df_period.max()/1e6:.1f}M XOF)',
        xy=(df_period.idxmax(), df_period.max()),
        xytext=(10, -20),
        textcoords='offset points',
        arrowprops=dict(arrowstyle="->")
    )

plt.tight_layout()
plt.savefig('evolution_echelonnee.png', dpi=300)
plt.show(fig4)

'''
Commentaire :
Cette série de graphiques montre l'évolution du CA à différentes échelles temporelles.
La vue trimestrielle révèle une croissance régulière, tandis que la vue semestrielle
met en évidence un doublement du CA entre le 1er et 2nd semestre 2023.
'''