# MaintiFlow - Site Vitrine

Site vitrine pour le produit GMAO MaintiFlow, développé par DevFactory.

## 📁 Structure des fichiers

```
maintiflow/
├── index.html              # Page principale
├── download.html           # Page de téléchargement brochure
├── brochure-maintiflow.pdf # Brochure PDF 5 pages
├── favicon.svg             # Favicon vectoriel
├── favicon.png             # Favicon 32x32
├── apple-touch-icon.png    # Icône Apple 180x180
├── og-image.png            # Image OpenGraph 1200x630
├── og-image.svg            # Image OpenGraph vectoriel
├── generate_brochure.py    # Script génération PDF
├── wrangler.toml           # Config Cloudflare
├── _redirects              # Redirections
├── README.md               # Documentation
└── functions/
    └── api/
        ├── contact.js      # API demande de démo
        ├── brochure.js     # API génération lien brochure
        └── verify-token.js # API vérification token
```

## 🔍 SEO & Meta Tags

Le site inclut :

- **Meta tags SEO** : title, description, keywords, author, robots
- **Open Graph** : og:title, og:description, og:image, og:url, og:type
- **Twitter Cards** : summary_large_image avec image dédiée
- **Schema.org JSON-LD** : 
  - SoftwareApplication (pour le produit MaintiFlow)
  - Organization (pour les infos de contact)
- **Favicons** : SVG, PNG 32x32, Apple Touch Icon 180x180

## 🚀 Déploiement sur Cloudflare Pages

### Prérequis

- Compte Cloudflare
- Node.js installé
- Wrangler CLI (`npm install -g wrangler`)

### Étapes de déploiement

#### 1. Authentification Cloudflare

```bash
wrangler login
```

#### 2. Créer le KV Namespace (pour les tokens de brochure)

```bash
wrangler kv:namespace create "MAINTIFLOW_KV"
```

Notez l'ID retourné et mettez-le dans `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "MAINTIFLOW_KV"
id = "votre_id_ici"
```

#### 3. Déployer le site

```bash
wrangler pages deploy . --project-name=maintiflow
```

### Configuration des emails

Le site utilise des APIs d'email. Deux options :

#### Option A: Resend (recommandé)

1. Créez un compte sur [resend.com](https://resend.com)
2. Obtenez votre API Key
3. Ajoutez la variable d'environnement dans Cloudflare Dashboard :
   - Allez dans Pages > maintiflow > Settings > Environment variables
   - Ajoutez `RESEND_API_KEY` avec votre clé

#### Option B: MailChannels (gratuit)

MailChannels fonctionne automatiquement avec Cloudflare Workers, mais nécessite une configuration DNS SPF :

Ajoutez un enregistrement TXT à votre domaine :
```
v=spf1 a mx include:relay.mailchannels.net ~all
```

### Configuration DNS

Pour un domaine personnalisé (ex: maintiflow.com) :

1. Allez dans Cloudflare Dashboard > Pages > maintiflow
2. Custom domains > Add custom domain
3. Suivez les instructions pour configurer les DNS

## 📁 Structure du projet

```
maintiflow/
├── index.html                    # Page principale
├── download.html                 # Page de téléchargement brochure
├── brochure-maintiflow.pdf      # Brochure PDF
├── _redirects                    # Redirections Cloudflare
├── wrangler.toml                # Configuration Wrangler
├── functions/
│   └── api/
│       ├── contact.js           # API demande de démo
│       ├── brochure.js          # API demande brochure
│       └── verify-token.js      # API vérification token
└── README.md
```

## 🔧 Fonctionnalités

### Formulaire Demande de Démo
- Collecte les informations du demandeur
- Envoie un email à contact@maintiflow.com
- Stocke la demande dans KV (backup)

### Formulaire Brochure
- Génère un token unique avec expiration 24h
- Envoie un email au demandeur avec le lien
- Notifie contact@maintiflow.com
- Page de téléchargement avec vérification du token

## 🎨 Personnalisation

### Modifier les couleurs

Éditez les variables CSS dans `index.html` :

```css
:root {
    --primary: #0d47a1;
    --primary-light: #1565c0;
    /* ... */
}
```

### Modifier le contenu

Éditez directement `index.html` pour modifier :
- Les textes
- Les statistiques
- Les fonctionnalités
- Les informations de contact

### Régénérer la brochure

```bash
python generate_brochure.py
```

## 📞 Contact

- Email: contact@maintiflow.com
- Site: https://maintiflow.com

---

Développé par **DevFactory** - AI-Native Startup Studio
