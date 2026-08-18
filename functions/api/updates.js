export async function onRequestGet(context) {
  try {
    const db = context.env.hanzi_db;
    const url = new URL(context.request.url);
    const username = url.searchParams.get('username');

    // Lấy data chung của admin
    const { results: globalResults } = await db.prepare('SELECT char, data FROM user_edits').all();

    const updates = {};
    for (const row of globalResults) {
      if (row.char && row.data) {
        updates[row.char] = JSON.parse(row.data);
        // Xóa srs rác từ thời chưa có user_progress nếu có
        if (updates[row.char].srs) {
           delete updates[row.char].srs;
        }
      }
    }

    // Nếu có username, lấy tiến trình học của user này đắp vào
    if (username) {
       const { results: userResults } = await db.prepare('SELECT char, srs_data FROM user_progress WHERE username = ?').bind(username).all();
       for (const row of userResults) {
         if (row.char && row.srs_data) {
           if (!updates[row.char]) updates[row.char] = {};
           updates[row.char].srs = JSON.parse(row.srs_data);
         }
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
