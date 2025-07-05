// @ts-ignore
import { serve } from "https://deno.land/std@1.0.0/http/server.ts"; // <-- Actualizado a 1.0.0, verifica que es la versión que funciona
// @ts-ignore
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Define la interfaz para el payload de la solicitud entrante
interface RequestPayload {
  post_id: string; // Asegúrate de que coincida con el tipo de ID de tu columna 'id' en la tabla 'posts'
}

console.info('Increment Post View Function Started');

// Deno.serve es la función principal que maneja las solicitudes HTTP
serve(async (req) => {
  // Solo permite solicitudes POST para incrementar el contador
  if (req.method !== 'POST') {
    return new Response(JSON.stringify({ error: "Method Not Allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Intenta parsear el cuerpo de la solicitud como JSON
  let payload: RequestPayload;
  try {
    payload = await req.json();
  } catch (e) {
    return new Response(JSON.stringify({ error: "Invalid JSON payload" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const { post_id } = payload;

  // Valida que 'post_id' esté presente en el payload
  if (!post_id) {
    return new Response(JSON.stringify({ error: "post_id is required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // --- ¡CAMBIOS CRUCIALES AQUÍ! ---
  // 1. Usa Deno.env.get("CLIENT_URL") para la URL de Supabase.
  // 2. Usa Deno.env.get("SERVICE_ROLE_KEY") para la clave de Supabase.
  //    Esta clave tiene permisos de administrador y puede bypassear RLS.
  //    Asegúrate de que estas variables de entorno están configuradas en el panel de Supabase
  //    bajo Edge Functions -> Environment Variables.
  
  // @ts-ignore
  const supabaseUrl = Deno.env.get("CLIENT_URL"); // Usar el nombre de tu variable
  // @ts-ignore
  const serviceRoleKey = Deno.env.get("SERVICE_ROLE_KEY"); // Usar el nombre de tu Service Role Key

  if (!supabaseUrl || !serviceRoleKey) {
    console.error("Missing CLIENT_URL or SERVICE_ROLE_KEY environment variables in Edge Function.");
    return new Response(JSON.stringify({ error: "Server configuration error: Missing Supabase credentials" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }

  const supabase = createClient(supabaseUrl, serviceRoleKey);

  try {
    // Incrementa el contador de visualizaciones de forma atómica y segura.
    // Usamos el nombre de columna 'views_count'.
    const { data: updatedPost, error: updateError } = await supabase
      .from("posts")
      .update({ views_count: (db_post) => db_post.views_count + 1 }) // <-- Cambio de 'views' a 'views_count' y uso de incremento atómico
      .eq("id", post_id)
      .select('id, views_count') // <-- Selecciona el ID y el nuevo conteo
      .single(); // Esperamos solo un resultado

    if (updateError) {
      console.error("Supabase error updating views:", updateError.message);
      return new Response(JSON.stringify({ error: updateError.message }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }

    if (!updatedPost) { // Si single() no encontró nada, updatedPost sería null
      return new Response(JSON.stringify({ error: "Post not found or not updated" }), {
        status: 404,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Devuelve el nuevo conteo de visualizaciones
    return new Response(JSON.stringify({ views_count: updatedPost.views_count }), { // <-- Cambio a 'views_count'
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });

  } catch (error) {
    console.error("Unhandled error in Edge Function:", error);
    return new Response(JSON.stringify({ error: "Internal server error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
});