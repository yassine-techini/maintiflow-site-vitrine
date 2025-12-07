# CLAUDE.md - Documentation pour Claude Code

Ce fichier contient les informations nécessaires pour que Claude Code puisse comprendre et modifier ce projet.

## Vue d'ensemble

**MaintiFlow** est un site vitrine pour une solution GMAO (Gestion de Maintenance Assistée par Ordinateur) développée par DevFactory. Le site est déployé sur **Cloudflare Pages** avec des **Functions** pour les APIs.

## Stack technique

- **Frontend** : HTML/CSS/JS vanilla (pas de framework)
- **Hébergement** : Cloudflare Pages
- **Backend** : Cloudflare Pages Functions (JavaScript)
- **Stockage** : Cloudflare KV (optionnel)
- **Emails** : Resend ou MailChannels

## Structure du projet

```
site-vitrine/
├── index.html              # Page principale du site
├── download.html           # Page de téléchargement de la brochure
├── brochure-maintiflow.pdf # Brochure PDF (5 pages)
├── favicon.svg             # Favicon vectoriel
├── favicon.png             # Favicon 32x32
├── apple-touch-icon.png    # Icône Apple 180x180
├── og-image.png            # Image OpenGraph 1200x630
├── og-image.svg            # Source de l'image OG
├── generate_brochure.py    # Script Python pour régénérer la brochure
├── wrangler.toml           # Configuration Cloudflare Pages
├── _redirects              # Règles de redirections Cloudflare
├── README.md               # Documentation utilisateur
├── CLAUDE.md               # Ce fichier
└── functions/
    └── api/
        ├── contact.js      # API POST /api/contact - Demande de démo
        ├── brochure.js     # API POST /api/brochure - Demande brochure
        └── verify-token.js # API GET /api/verify-token - Vérification token
```

## URLs de déploiement

- **Production** : https://maintiflow.pages.dev
- **GitHub** : https://github.com/yassine-techini/maintiflow-site-vitrine

## Commandes de déploiement

```bash
# Déployer sur Cloudflare Pages
wrangler pages deploy . --project-name=maintiflow

# Créer un KV namespace (si nécessaire)
wrangler kv:namespace create "MAINTIFLOW_KV"
```

## APIs disponibles

### POST /api/contact
Envoie une demande de démonstration.

**Payload requis** :
```json
{
  "prenom": "string",
  "nom": "string",
  "email": "string",
  "telephone": "string",
  "entreprise": "string",
  "fonction": "string (optionnel)",
  "taille": "string (optionnel)",
  "message": "string (optionnel)"
}
```

### POST /api/brochure
Génère un lien de téléchargement avec expiration 24h.

**Payload requis** :
```json
{
  "prenom": "string",
  "nom": "string",
  "email": "string",
  "entreprise": "string (optionnel)",
  "telephone": "string (optionnel)"
}
```

### GET /api/verify-token?token=xxx
Vérifie la validité d'un token de téléchargement.

## Variables d'environnement Cloudflare

| Variable | Description | Requis |
|----------|-------------|--------|
| `RESEND_API_KEY` | Clé API Resend pour l'envoi d'emails | Non (fallback MailChannels) |
| `MAINTIFLOW_KV` | KV namespace binding | Non (stockage backup) |

## Styles CSS

Les variables CSS sont définies dans `index.html` :

```css
:root {
    --primary: #0d47a1;       /* Bleu principal */
    --primary-light: #1565c0; /* Bleu clair */
    --primary-dark: #002171;  /* Bleu foncé */
    --secondary: #ff6f00;     /* Orange accent */
    --text: #1a1a2e;          /* Texte principal */
    --text-light: #4a4a68;    /* Texte secondaire */
    --bg: #ffffff;            /* Fond principal */
    --bg-alt: #f8f9fa;        /* Fond alternatif */
}
```

## Sections de la page principale (index.html)

1. **Header** : Navigation + CTA
2. **Hero** : Titre principal + formulaire de contact rapide
3. **Stats** : Statistiques clés (40% réduction, 500+ entreprises, etc.)
4. **Fonctionnalités** : 6 modules principaux avec icônes
5. **Déploiement** : Options Cloud/SaaS vs On-Premise
6. **Brochure** : Formulaire de téléchargement brochure
7. **Démo** : Formulaire complet de demande de démo
8. **Footer** : Informations de contact + liens

## Informations de contact

- **Email** : contact@maintiflow.com
- **Téléphone** : +216 58 130 482
- **Adresse** : Tunis, Tunisie
- **Entreprise** : DevFactory

## SEO

Le site inclut :
- Meta tags SEO complets
- Open Graph pour Facebook/LinkedIn
- Twitter Cards
- Schema.org JSON-LD (SoftwareApplication + Organization)
- Sitemap implicite via Cloudflare

## Pour modifier le contenu

### Changer les textes
Éditer directement `index.html` - tout le contenu est inline.

### Changer les couleurs
Modifier les variables CSS dans la section `<style>` de `index.html`.

### Ajouter une nouvelle page
1. Créer le fichier HTML à la racine
2. Ajouter une redirection dans `_redirects` si nécessaire

### Ajouter une nouvelle API
1. Créer un fichier dans `functions/api/`
2. Exporter `onRequestPost` ou `onRequestGet`
3. Redéployer avec `wrangler pages deploy`

### Régénérer la brochure PDF
```bash
python generate_brochure.py
```
Nécessite : `reportlab`, `svglib`

## Notes importantes

- Le site est **full responsive** (mobile-first)
- Pas de dépendances npm - tout est vanilla
- Les formulaires utilisent `fetch()` pour les appels API
- Les tokens de brochure expirent après **24 heures**
- Les emails de contact sont envoyés à `contact@maintiflow.com`
