from flask import Flask, render_template, request, jsonify
import random
import svgwrite
from io import BytesIO
import base64

app = Flask(__name__)

# Définir les valeurs et les couleurs des cartes
valeurs = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14','15','16','17','18','19','20',]
couleurs = ['Coeur']

# Créer un jeu de cartes
def creer_jeu_de_cartes():
    jeu = [(v, c) for v in valeurs for c in couleurs]
    random.shuffle(jeu)
    return jeu

# Fonction pour obtenir la valeur numérique d'une carte
def valeur_carte(carte):
    valeur, _ = carte
    if valeur == 'J':
        return 11
    elif valeur == 'Q':
        return 12
    elif valeur == 'K':
        return 13
    elif valeur == 'A':
        return 14
    else:
        return int(valeur)

# Tri à bulles
def tri_bulle(jeu):
    # On obtient la taille de la liste 'jeu', c'est-à-dire le nombre de cartes à trier
    n = len(jeu)
    
    # On initialise un compteur pour le nombre de fois où on parcourt la liste
    i = 0
    
    # Tant qu'on n'a pas parcouru toutes les cartes
    while i < n:
        
        # On initialise le compteur pour les paires de cartes à comparer
        j = 0
        
        # On compare chaque carte avec la suivante, sauf les cartes déjà triées
        while j < n - i - 1:
            
            # Si la carte actuelle est plus grande que la suivante
            if valeur_carte(jeu[j]) > valeur_carte(jeu[j + 1]):
                
                # On échange les cartes pour les mettre dans le bon ordre
                jeu[j], jeu[j + 1] = jeu[j + 1], jeu[j]
                
            # On passe à la carte suivante pour la comparaison
            j += 1
        
        # On a terminé un parcours, on recommence avec une carte de moins à comparer
        i += 1

# Générer une image SVG d'une carte
def generer_svg_carte(carte):
    valeur, couleur = carte
    dwg = svgwrite.Drawing(size=(100, 150))

    # Ajouter un fond avec un dégradé
    dwg.add(dwg.rect((0, 0), (100, 150), fill='url(#grad1)', stroke='black', rx=10, ry=10))
    grad = dwg.defs.add(dwg.linearGradient(id='grad1', x1="0%", y1="0%", x2="0%", y2="100%"))
    grad.add_stop_color(0, 'white')
    grad.add_stop_color(1, 'lightgrey')

    # Ajouter la valeur de la carte avec une police personnalisée
    dwg.add(dwg.text(valeur, insert=(10, 30), font_size=20, fill='black', font_family="Arial", text_anchor="start"))
    dwg.add(dwg.text(valeur, insert=(90, 130), font_size=20, fill='black', font_family="Arial", text_anchor="end"))

    # Ajouter le symbole de la couleur avec une police personnalisée
    if couleur == 'Coeur':
        symbole = '♥'
        couleur_symbole = 'red'
    elif couleur == 'Carreau':
        symbole = '♦'
        couleur_symbole = 'red'
    elif couleur == 'Trèfle':
        symbole = '♣'
        couleur_symbole = 'black'
    elif couleur == 'Pique':
        symbole = '♠'
        couleur_symbole = 'black'

    dwg.add(dwg.text(symbole, insert=(10, 50), font_size=30, fill=couleur_symbole, font_family="Arial", text_anchor="start"))
    dwg.add(dwg.text(symbole, insert=(90, 110), font_size=30, fill=couleur_symbole, font_family="Arial", text_anchor="end"))
    
    return dwg.tostring()
# Convertir SVG en base64
def svg_to_base64(svg):
    return base64.b64encode(svg.encode('utf-8')).decode('utf-8')
# Route principale
@app.route('/')
def index():
    jeu_de_cartes = creer_jeu_de_cartes()
    svg_cartes = [svg_to_base64(generer_svg_carte(carte)) for carte in jeu_de_cartes]
    return render_template('index.html', cartes=svg_cartes)

# Route pour trier les cartes
@app.route('/trier', methods=['POST'])
def trier():
    jeu_de_cartes = creer_jeu_de_cartes()
    tri_bulle(jeu_de_cartes)
    svg_cartes = [svg_to_base64(generer_svg_carte(carte)) for carte in jeu_de_cartes]
    return jsonify(cartes=svg_cartes)

# Route pour réinitialiser les cartes
@app.route('/reinitialiser', methods=['POST'])
def reinitialiser():
    jeu_de_cartes = creer_jeu_de_cartes()
    svg_cartes = [svg_to_base64(generer_svg_carte(carte)) for carte in jeu_de_cartes]
    return jsonify(cartes=svg_cartes)

if __name__ == '__main__':
    app.run(debug=True)
