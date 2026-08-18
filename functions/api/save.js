export async function onRequestPost(context) {
  try {
    const body = await context.request.json();
    const { char, comps, username } = body;
    
    if (!char || !comps || !username) {
      return new Response(JSON.stringify({ success: false, error: 'Missing char, comps, or username' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }

    const db = context.env.hanzi_db;

    // Tách riêng srs và các trường khác
    const { srs, ...otherComps } = comps;

    // Lưu SRS vào user_progress
    if (srs) {
       await db.prepare('INSERT INTO user_progress (username, char, srs_data, updated_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT(username, char) DO UPDATE SET srs_data = excluded.srs_data, updated_at = CURRENT_TIMESTAMP').bind(username, char, JSON.stringify(srs)).run();
    }

    // Nếu là admin và có sửa các trường khác (như quiz_mapping)
    if (username === 'admin' && Object.keys(otherComps).length > 0) {
       const existing = await db.prepare('SELECT data FROM user_edits WHERE char = ?').bind(char).first();
       let newData = otherComps;
       if (existing && existing.data) {
         const oldData = JSON.parse(existing.data);
         // Không được ghi đè mất srs cũ nếu admin từng có srs trong user_edits (để tương thích ngược)
         newData = { ...oldData, ...otherComps };
       }
       await db.prepare('INSERT INTO user_edits (char, data, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP) ON CONFLICT(char) DO UPDATE SET data = excluded.data, updated_at = CURRENT_TIMESTAMP').bind(char, JSON.stringify(newData)).run();
    }

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
