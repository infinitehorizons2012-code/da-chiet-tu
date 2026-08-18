export async function onRequestGet(context) {
  try {
    const db = context.env.hanzi_db;
    const { results } = await db.prepare('SELECT char, data FROM user_edits').all();

    const updates = {};
    for (const row of results) {
      if (row.char && row.data) {
        updates[row.char] = JSON.parse(row.data);
      }
    }

    return new Response(JSON.stringify({ success: true, updates }), {
      headers: { 'Content-Type': 'application/json' }
    });
  } catch (error) {
    return new Response(JSON.stringify({ success: false, error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
