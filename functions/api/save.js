export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const { char, comps } = body;
    
    if (!char || !comps) {
      return new Response(JSON.stringify({ success: false, error: 'Missing char or comps' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const db = context.env.hanzi_db;
    const existing = await db.prepare('SELECT data FROM user_edits WHERE char = ?').bind(char).first();

    let newData = comps;
    if (existing && existing.data) {
      const oldData = JSON.parse(existing.data);
      newData = { ...oldData, ...comps };
    }

    await db.prepare('INSERT INTO user_edits (char, data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP) ON CONFLICT(char) DO UPDATE SET data = excluded.data, updated_at = CURRENT_TIMESTAMP').bind(char, JSON.stringify(newData)).run();

    return new Response(JSON.stringify({ success: true }), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ success: false, error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
