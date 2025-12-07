/**
 * API Brochure - Génère un lien de téléchargement avec expiration 24h
 * Envoie un email au demandeur avec le lien
 */

// Fonction pour générer un token unique
function generateToken() {
    const array = new Uint8Array(32);
    crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
}

export async function onRequestPost(context) {
    const { request, env } = context;
    
    try {
        const data = await request.json();
        
        // Validation des champs requis
        if (!data.prenom || !data.nom || !data.email) {
            return new Response(JSON.stringify({ 
                error: 'Les champs prénom, nom et email sont requis' 
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Générer un token unique
        const token = generateToken();
        const expiresAt = Date.now() + (24 * 60 * 60 * 1000); // 24 heures
        
        // URL de base (à adapter selon votre domaine)
        const baseUrl = new URL(request.url).origin;
        const downloadUrl = `${baseUrl}/download?token=${token}`;
        
        // Stocker le token dans KV
        if (env.MAINTIFLOW_KV) {
            await env.MAINTIFLOW_KV.put(`brochure_token_${token}`, JSON.stringify({
                email: data.email,
                prenom: data.prenom,
                nom: data.nom,
                entreprise: data.entreprise || '',
                telephone: data.telephone || '',
                createdAt: new Date().toISOString(),
                expiresAt: new Date(expiresAt).toISOString()
            }), { 
                expirationTtl: 24 * 60 * 60 // 24 heures en secondes
            });
        }
        
        // Contenu de l'email pour le demandeur
        const emailHtml = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #0d47a1; color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }
        .button { display: inline-block; background: #0d47a1; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; margin: 20px 0; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 20px; }
        .warning { background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 4px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin:0;">MaintiFlow</h1>
            <p style="margin:10px 0 0 0;">GMAO Professionnelle</p>
        </div>
        <div class="content">
            <p>Bonjour ${data.prenom},</p>
            
            <p>Merci pour votre intérêt pour MaintiFlow !</p>
            
            <p>Vous trouverez ci-dessous le lien pour télécharger notre brochure de présentation :</p>
            
            <p style="text-align: center;">
                <a href="${downloadUrl}" class="button">📄 Télécharger la brochure</a>
            </p>
            
            <div class="warning">
                <strong>⏰ Attention :</strong> Ce lien est valide pendant <strong>24 heures</strong>. Passé ce délai, vous devrez faire une nouvelle demande sur notre site.
            </div>
            
            <p>Si vous avez des questions ou souhaitez planifier une démonstration personnalisée, n'hésitez pas à nous contacter :</p>
            
            <ul>
                <li>📧 <a href="mailto:contact@maintiflow.com">contact@maintiflow.com</a></li>
                <li>📞 +216 58 130 482</li>
            </ul>
            
            <p>Cordialement,<br>L'équipe MaintiFlow</p>
        </div>
        <div class="footer">
            <p>MaintiFlow - Un produit DevFactory<br>
            Tunis, Tunisie | <a href="https://maintiflow.com">maintiflow.com</a></p>
        </div>
    </div>
</body>
</html>
        `;
        
        const emailText = `
Bonjour ${data.prenom},

Merci pour votre intérêt pour MaintiFlow !

Voici le lien pour télécharger notre brochure de présentation :
${downloadUrl}

⏰ ATTENTION : Ce lien est valide pendant 24 heures. Passé ce délai, vous devrez faire une nouvelle demande sur notre site.

Si vous avez des questions ou souhaitez planifier une démonstration personnalisée, n'hésitez pas à nous contacter :
- Email : contact@maintiflow.com
- Téléphone : +216 58 130 482

Cordialement,
L'équipe MaintiFlow

---
MaintiFlow - Un produit DevFactory
Tunis, Tunisie | maintiflow.com
        `;
        
        // Envoyer l'email au demandeur
        // Option 1: Resend
        if (env.RESEND_API_KEY) {
            await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    from: 'MaintiFlow <noreply@maintiflow.com>',
                    to: [data.email],
                    subject: 'Votre brochure MaintiFlow',
                    html: emailHtml,
                    text: emailText
                })
            });
        }
        // Option 2: MailChannels
        else {
            await fetch('https://api.mailchannels.net/tx/v1/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    personalizations: [{
                        to: [{ email: data.email, name: `${data.prenom} ${data.nom}` }]
                    }],
                    from: { email: 'noreply@maintiflow.com', name: 'MaintiFlow' },
                    subject: 'Votre brochure MaintiFlow',
                    content: [
                        { type: 'text/plain', value: emailText },
                        { type: 'text/html', value: emailHtml }
                    ]
                })
            });
        }
        
        // Envoyer aussi une notification à MaintiFlow
        const notificationContent = `
Nouvelle demande de brochure MaintiFlow

Demandeur: ${data.prenom} ${data.nom}
Email: ${data.email}
Entreprise: ${data.entreprise || 'Non renseigné'}
Téléphone: ${data.telephone || 'Non renseigné'}
Date: ${new Date().toLocaleString('fr-TN', { timeZone: 'Africa/Tunis' })}
        `;
        
        if (env.RESEND_API_KEY) {
            await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    from: 'MaintiFlow <noreply@maintiflow.com>',
                    to: ['contact@maintiflow.com'],
                    subject: `[MaintiFlow] Téléchargement brochure - ${data.email}`,
                    text: notificationContent
                })
            });
        }
        
        return new Response(JSON.stringify({ 
            success: true,
            message: 'Email envoyé avec le lien de téléchargement'
        }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
        
    } catch (error) {
        console.error('Error:', error);
        return new Response(JSON.stringify({ 
            error: 'Erreur serveur',
            details: error.message 
        }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
