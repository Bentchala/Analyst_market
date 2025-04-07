import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
df = pd.read_csv('donnees_completes.csv', parse_dates=['date_vente'])

# Configuration style
sns.set_theme(style="whitegrid")
colors = sns.color_palette("husl", 8)

# Création du graphique
fig, axes = plt.subplots(3, 1, figsize=(14, 15))
periods = [
    ('Mensuel', 'M'),
    ('Trimestriel', 'Q'),
    ('Semestriel', '6M')
]

for ax, (title, freq) in zip(axes, periods):
    df_period = df.set_index('date_vente').resample(freq)['montant_total'].sum()
    df_period.plot(kind='line', ax=ax, marker='o', color=colors[4])
    ax.set_title(f"Évolution {title.lower()} du CA", fontsize=14)
    ax.set_ylabel('CA (XOF)')
    ax.grid(True)
    ax.annotate(
        f'Pic: {df_period.idxmax().strftime("%b %Y")}\n({df_period.max()/1e6:.1f}M XOF)',
        xy=(df_period.idxmax(), df_period.max()),
        xytext=(10, -20),
        textcoords='offset points',
        arrowprops=dict(arrowstyle="->")
    )

plt.tight_layout()
plt.savefig('evolution_echelonnee.png', dpi=300)
plt.show()