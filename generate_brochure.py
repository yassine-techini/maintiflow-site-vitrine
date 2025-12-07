#!/usr/bin/env python3
"""
Génération de la brochure MaintiFlow
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Couleurs
PRIMARY = HexColor('#0d47a1')
PRIMARY_LIGHT = HexColor('#1565c0')
ACCENT = HexColor('#42a5f5')
SUCCESS = HexColor('#22c55e')
GRAY_900 = HexColor('#111827')
GRAY_700 = HexColor('#374151')
GRAY_500 = HexColor('#6b7280')
GRAY_100 = HexColor('#f3f4f6')

def draw_header(c, width, height):
    """Dessine l'en-tête avec le logo"""
    # Bande bleue en haut
    c.setFillColor(PRIMARY)
    c.rect(0, height - 40*mm, width, 40*mm, fill=True, stroke=False)
    
    # Logo
    c.setFillColor(white)
    c.roundRect(15*mm, height - 32*mm, 12*mm, 12*mm, 3*mm, fill=True, stroke=False)
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(21*mm, height - 28*mm, "M")
    
    # Nom
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(32*mm, height - 27*mm, "MaintiFlow")
    
    # Tagline
    c.setFont("Helvetica", 10)
    c.drawString(32*mm, height - 35*mm, "GMAO Professionnelle")

def draw_footer(c, width, page_num):
    """Dessine le pied de page"""
    c.setFillColor(GRAY_500)
    c.setFont("Helvetica", 8)
    c.drawString(15*mm, 10*mm, "MaintiFlow - Un produit DevFactory | contact@maintiflow.com | +216 58 130 482")
    c.drawRightString(width - 15*mm, 10*mm, f"Page {page_num}")

def create_brochure():
    """Crée la brochure PDF"""
    filename = "/home/claude/maintiflow/brochure-maintiflow.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # ===== PAGE 1 - COUVERTURE =====
    # Fond bleu
    c.setFillColor(PRIMARY)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Dégradé simulé avec des rectangles
    c.setFillColor(PRIMARY_LIGHT)
    c.rect(0, 0, width, height/2, fill=True, stroke=False)
    
    # Logo grand
    c.setFillColor(white)
    c.roundRect(width/2 - 25*mm, height - 100*mm, 50*mm, 50*mm, 10*mm, fill=True, stroke=False)
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 60)
    c.drawCentredString(width/2, height - 85*mm, "M")
    
    # Titre
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 42)
    c.drawCentredString(width/2, height - 140*mm, "MaintiFlow")
    
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height - 155*mm, "Solution GMAO Professionnelle")
    
    # Ligne décorative
    c.setStrokeColor(white)
    c.setLineWidth(2)
    c.line(width/2 - 40*mm, height - 170*mm, width/2 + 40*mm, height - 170*mm)
    
    # Sous-titre
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height - 190*mm, "Optimisez la gestion de votre")
    c.drawCentredString(width/2, height - 200*mm, "patrimoine technique")
    
    # Stats en bas
    y_stats = 60*mm
    stats = [("-40%", "Coûts"), ("99.5%", "Disponibilité"), ("+50", "Clients")]
    x_positions = [width/4, width/2, 3*width/4]
    
    for i, (value, label) in enumerate(stats):
        c.setFont("Helvetica-Bold", 32)
        c.drawCentredString(x_positions[i], y_stats + 15*mm, value)
        c.setFont("Helvetica", 11)
        c.drawCentredString(x_positions[i], y_stats, label)
    
    # Pied de page
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, 15*mm, "www.maintiflow.com | contact@maintiflow.com")
    
    c.showPage()
    
    # ===== PAGE 2 - PRÉSENTATION =====
    draw_header(c, width, height)
    
    y = height - 60*mm
    
    c.setFillColor(GRAY_900)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(15*mm, y, "Qu'est-ce que MaintiFlow ?")
    
    y -= 15*mm
    c.setFillColor(GRAY_700)
    c.setFont("Helvetica", 11)
    
    intro_text = [
        "MaintiFlow est une solution de Gestion de Maintenance Assistée par",
        "Ordinateur (GMAO) nouvelle génération, conçue pour répondre aux",
        "besoins spécifiques des entreprises et administrations tunisiennes.",
        "",
        "Disponible en Cloud/SaaS ou On-Premise, notre plateforme permet de",
        "centraliser et d'optimiser l'ensemble de vos opérations de maintenance :",
        "préventive, curative, gestion des stocks, parc automobile, et plus encore."
    ]
    
    for line in intro_text:
        c.drawString(15*mm, y, line)
        y -= 6*mm
    
    y -= 10*mm
    
    # Avantages clés
    c.setFillColor(GRAY_900)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(15*mm, y, "Vos avantages")
    
    y -= 12*mm
    
    avantages = [
        ("✓", "Réduction des coûts de maintenance jusqu'à 40%"),
        ("✓", "Augmentation de la disponibilité des équipements"),
        ("✓", "Traçabilité complète de toutes les interventions"),
        ("✓", "Planification préventive automatisée"),
        ("✓", "Tableaux de bord et KPIs en temps réel"),
        ("✓", "Interface web responsive (PC, tablette, mobile)"),
        ("✓", "Support local en français et arabe"),
    ]
    
    c.setFont("Helvetica", 11)
    for check, text in avantages:
        c.setFillColor(SUCCESS)
        c.drawString(20*mm, y, check)
        c.setFillColor(GRAY_700)
        c.drawString(30*mm, y, text)
        y -= 8*mm
    
    y -= 15*mm
    
    # Encadré
    c.setFillColor(GRAY_100)
    c.roundRect(15*mm, y - 25*mm, width - 30*mm, 30*mm, 3*mm, fill=True, stroke=False)
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y - 5*mm, "Cloud/SaaS ou On-Premise • Sécurisé SSL • Flexible")
    c.setFillColor(GRAY_700)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, y - 15*mm, "Déploiement rapide • Formation incluse • Support dédié")
    
    draw_footer(c, width, 2)
    c.showPage()
    
    # ===== PAGE 3 - FONCTIONNALITÉS =====
    draw_header(c, width, height)
    
    y = height - 60*mm
    
    c.setFillColor(GRAY_900)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(15*mm, y, "Fonctionnalités principales")
    
    y -= 20*mm
    
    features = [
        ("🎯", "Maintenance Préventive", 
         "Planification automatique des interventions selon calendriers ou compteurs. Génération des bons de travaux. Conformité ISO."),
        ("⚡", "Maintenance Curative",
         "Gestion des demandes d'intervention, assignation intelligente des techniciens, suivi en temps réel de l'avancement."),
        ("📦", "Gestion des Stocks",
         "Inventaire des pièces de rechange, alertes de seuil minimum, commandes automatiques, valorisation des consommations."),
        ("🚗", "Parc Automobile",
         "Suivi complet de votre flotte : kilométrage, carburant, assurances, contrôles techniques, historique des interventions."),
        ("📊", "Tableaux de Bord",
         "KPIs en temps réel : MTBF, MTTR, taux de disponibilité, coûts par équipement. Aide à la décision stratégique."),
        ("🌐", "Interface Responsive",
         "Accès web optimisé pour PC, tablette et smartphone. Travaillez efficacement depuis n'importe quel appareil."),
    ]
    
    col_width = (width - 40*mm) / 2
    col = 0
    row_y = y
    
    for i, (icon, title, desc) in enumerate(features):
        x = 15*mm + (col * (col_width + 10*mm))
        
        # Icône
        c.setFillColor(GRAY_100)
        c.roundRect(x, row_y - 8*mm, 12*mm, 12*mm, 2*mm, fill=True, stroke=False)
        c.setFont("Helvetica", 16)
        c.setFillColor(GRAY_900)
        c.drawCentredString(x + 6*mm, row_y - 4*mm, icon)
        
        # Titre
        c.setFillColor(GRAY_900)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x + 16*mm, row_y - 2*mm, title)
        
        # Description
        c.setFillColor(GRAY_500)
        c.setFont("Helvetica", 9)
        
        # Word wrap simple
        words = desc.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if c.stringWidth(test_line, "Helvetica", 9) < col_width - 16*mm:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        desc_y = row_y - 12*mm
        for line in lines[:3]:
            c.drawString(x + 16*mm, desc_y, line)
            desc_y -= 4*mm
        
        col += 1
        if col >= 2:
            col = 0
            row_y -= 45*mm
    
    draw_footer(c, width, 3)
    c.showPage()
    
    # ===== PAGE 4 - MODULES =====
    draw_header(c, width, height)
    
    y = height - 60*mm
    
    c.setFillColor(GRAY_900)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(15*mm, y, "Architecture modulaire")
    
    y -= 10*mm
    c.setFillColor(GRAY_500)
    c.setFont("Helvetica", 11)
    c.drawString(15*mm, y, "Activez uniquement les modules dont vous avez besoin.")
    
    y -= 20*mm
    
    modules = [
        ("🏢", "Patrimoine", "Bâtiments, locaux, installations techniques"),
        ("🚗", "Parc Auto", "Véhicules, carburant, assurances"),
        ("🔧", "Interventions", "DT, BT, maintenance préventive et curative"),
        ("📦", "Stocks", "Pièces de rechange, consommables"),
        ("💰", "Achats", "Demandes d'achat, bons de commande, facturation"),
        ("📄", "Contrats", "Sous-traitance, garanties, SLA"),
        ("👥", "Équipes", "Techniciens, compétences, planning"),
        ("📈", "Reporting", "KPIs, tableaux de bord, exports"),
    ]
    
    col_width = (width - 40*mm) / 4
    
    for i, (icon, name, desc) in enumerate(modules):
        col = i % 4
        row = i // 4
        
        x = 15*mm + (col * (col_width + 3*mm))
        box_y = y - (row * 50*mm)
        
        # Box
        c.setFillColor(GRAY_100)
        c.roundRect(x, box_y - 40*mm, col_width, 45*mm, 3*mm, fill=True, stroke=False)
        
        # Icône
        c.setFont("Helvetica", 24)
        c.setFillColor(GRAY_900)
        c.drawCentredString(x + col_width/2, box_y - 12*mm, icon)
        
        # Nom
        c.setFillColor(GRAY_900)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(x + col_width/2, box_y - 22*mm, name)
        
        # Description
        c.setFillColor(GRAY_500)
        c.setFont("Helvetica", 8)
        # Simple center approximation
        c.drawCentredString(x + col_width/2, box_y - 32*mm, desc[:25])
    
    y -= 120*mm
    
    # Section ROI
    c.setFillColor(PRIMARY)
    c.roundRect(15*mm, y - 50*mm, width - 30*mm, 55*mm, 5*mm, fill=True, stroke=False)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y - 12*mm, "Retour sur investissement garanti")
    
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, y - 25*mm, "Nos clients constatent en moyenne une réduction de 40% de leurs")
    c.drawCentredString(width/2, y - 33*mm, "coûts de maintenance dès la première année d'utilisation.")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, y - 45*mm, "ROI en moins de 6 mois")
    
    draw_footer(c, width, 4)
    c.showPage()
    
    # ===== PAGE 5 - CONTACT =====
    draw_header(c, width, height)
    
    y = height - 70*mm
    
    c.setFillColor(GRAY_900)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, y, "Prêt à optimiser")
    c.drawCentredString(width/2, y - 12*mm, "votre maintenance ?")
    
    y -= 35*mm
    c.setFillColor(GRAY_500)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, "Demandez une démonstration personnalisée gratuite")
    
    y -= 30*mm
    
    # Contact box
    c.setFillColor(GRAY_100)
    c.roundRect(width/2 - 60*mm, y - 70*mm, 120*mm, 75*mm, 5*mm, fill=True, stroke=False)
    
    c.setFillColor(GRAY_900)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width/2, y - 10*mm, "Contactez-nous")
    
    y -= 25*mm
    c.setFillColor(GRAY_700)
    c.setFont("Helvetica", 11)
    
    contacts = [
        "📧  contact@maintiflow.com",
        "📞  +216 58 130 482",
        "🌐  www.maintiflow.com",
        "📍  Tunis, Tunisie"
    ]
    
    for contact in contacts:
        c.drawCentredString(width/2, y, contact)
        y -= 10*mm
    
    y -= 30*mm
    
    # DevFactory
    c.setFillColor(GRAY_500)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, y, "MaintiFlow est un produit développé par")
    
    c.setFillColor(PRIMARY)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y - 12*mm, "DevFactory")
    
    c.setFillColor(GRAY_500)
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, y - 24*mm, "AI-Native Startup Studio • Tunis & Paris")
    
    draw_footer(c, width, 5)
    
    c.save()
    print(f"Brochure créée : {filename}")
    return filename

if __name__ == "__main__":
    create_brochure()
