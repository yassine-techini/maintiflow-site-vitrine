/**
 * API Contact - Demande de démo
 * Envoie un email à contact@maintiflow.com avec les informations du demandeur
 */

export async function onRequestPost(context) {
    const { request, env } = context;
    
    try {
        const data = await request.json();
        
        // Validation des champs requis
        const required = ['prenom', 'nom', 'email', 'telephone', 'entreprise'];
        for (const field of required) {
            if (!data[field]) {
                return new Response(JSON.stringify({ 
                    error: `Le champ ${field} est requis` 
                }), {
                    status: 400,
                    headers: { 'Content-Type': 'application/json' }
                });
            }
        }
        
        // Construire le contenu de l'email
        const emailContent = `
Nouvelle demande de démonstration MaintiFlow

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INFORMATIONS DU DEMANDEUR

Prénom: ${data.prenom}
Nom: ${data.nom}
Email: ${data.email}
Téléphone: ${data.telephone}
Entreprise: ${data.entreprise}
Fonction: ${data.fonction || 'Non renseigné'}
Taille de l'organisation: ${data.taille || 'Non renseigné'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MESSAGE

${data.message || 'Aucun message'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Date de la demande: ${new Date().toLocaleString('fr-TN', { timeZone: 'Africa/Tunis' })}
Source: Site MaintiFlow
        `;
        
        // Envoyer l'email via Resend ou MailChannels
        // Option 1: Si vous utilisez Resend
        if (env.RESEND_API_KEY) {
            const emailResponse = await fetch('https://api.resend.com/emails', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${env.RESEND_API_KEY}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    from: 'MaintiFlow <noreply@maintiflow.com>',
                    to: ['contact@maintiflow.com'],
                    subject: `[MaintiFlow] Nouvelle demande de démo - ${data.entreprise}`,
                    text: emailContent,
                    reply_to: data.email
                })
            });
            
            if (!emailResponse.ok) {
                throw new Error('Erreur envoi email Resend');
            }
        }
        // Option 2: MailChannels (gratuit avec Cloudflare Workers)
        else {
            const emailResponse = await fetch('https://api.mailchannels.net/tx/v1/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    personalizations: [{
                        to: [{ email: 'contact@maintiflow.com', name: 'MaintiFlow' }]
                    }],
                    from: { email: 'noreply@maintiflow.com', name: 'MaintiFlow' },
                    subject: `[MaintiFlow] Nouvelle demande de démo - ${data.entreprise}`,
                    content: [{
                        type: 'text/plain',
                        value: emailContent
                    }],
                    reply_to: { email: data.email, name: `${data.prenom} ${data.nom}` }
                })
            });
            
            if (!emailResponse.ok) {
                console.error('MailChannels error:', await emailResponse.text());
                // Continue anyway - store in KV as backup
            }
        }
        
        // Stocker la demande dans KV (backup)
        if (env.MAINTIFLOW_KV) {
            const key = `demo_${Date.now()}_${data.email.replace('@', '_at_')}`;
            await env.MAINTIFLOW_KV.put(key, JSON.stringify({
                ...data,
                timestamp: new Date().toISOString(),
                type: 'demo'
            }), { expirationTtl: 60 * 60 * 24 * 90 }); // 90 jours
        }
        
        return new Response(JSON.stringify({ 
            success: true,
            message: 'Demande envoyée avec succès'
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
