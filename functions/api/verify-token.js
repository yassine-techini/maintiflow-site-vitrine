/**
 * API Verify Token - Vérifie si le token de téléchargement est valide
 */

export async function onRequestGet(context) {
    const { request, env } = context;
    
    try {
        const url = new URL(request.url);
        const token = url.searchParams.get('token');
        
        if (!token) {
            return new Response(JSON.stringify({ 
                valid: false,
                error: 'Token manquant'
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Vérifier le token dans KV
        if (env.MAINTIFLOW_KV) {
            const tokenData = await env.MAINTIFLOW_KV.get(`brochure_token_${token}`);
            
            if (!tokenData) {
                return new Response(JSON.stringify({ 
                    valid: false,
                    expired: false,
                    error: 'Token invalide'
                }), {
                    status: 404,
                    headers: { 'Content-Type': 'application/json' }
                });
            }
            
            const data = JSON.parse(tokenData);
            const expiresAt = new Date(data.expiresAt).getTime();
            
            if (Date.now() > expiresAt) {
                return new Response(JSON.stringify({ 
                    valid: false,
                    expired: true,
                    error: 'Token expiré'
                }), {
                    status: 410,
                    headers: { 'Content-Type': 'application/json' }
                });
            }
            
            // Token valide
            return new Response(JSON.stringify({ 
                valid: true,
                email: data.email
            }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Si KV n'est pas configuré, accepter tous les tokens
        return new Response(JSON.stringify({ 
            valid: true,
            warning: 'KV not configured'
        }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
        
    } catch (error) {
        console.error('Error:', error);
        return new Response(JSON.stringify({ 
            valid: false,
            error: 'Erreur serveur'
        }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}
