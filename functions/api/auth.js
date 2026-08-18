export async function onRequestPost(context) {
  try {
    const db = context.env.hanzi_db;
    const url = new URL(context.request.url);
    const action = url.searchParams.get('action');
    const body = await context.request.json();
    const { username, password } = body;

    if (!username || !password) {
      return new Response(JSON.stringify({ success: false, error: 'Thiếu username hoặc password' }), { status: 400 });
    }

    // Luôn hardcode admin nếu chưa có
    if (username === 'admin') {
      const adminUser = await db.prepare('SELECT password FROM users WHERE username = ?').bind('admin').first();
      if (!adminUser) {
        await db.prepare('INSERT INTO users (username, password) VALUES (?, ?)').bind('admin', 'admin').run();
      }
    }

    if (action === 'register') {
      const existing = await db.prepare('SELECT username FROM users WHERE username = ?').bind(username).first();
      if (existing) {
        return new Response(JSON.stringify({ success: false, error: 'Username đã tồn tại' }), { status: 400 });
      }
      await db.prepare('INSERT INTO users (username, password) VALUES (?, ?)').bind(username, password).run();
      return new Response(JSON.stringify({ success: true }));
    } 
    
    if (action === 'login') {
      const user = await db.prepare('SELECT password FROM users WHERE username = ?').bind(username).first();
      if (!user) {
        return new Response(JSON.stringify({ success: false, error: 'Tài khoản không tồn tại' }), { status: 400 });
      }
      if (user.password !== password) {
        return new Response(JSON.stringify({ success: false, error: 'Sai mật khẩu' }), { status: 400 });
      }
      return new Response(JSON.stringify({ success: true, username }));
    }

    if (action === 'delete') {
      if (username === 'admin') {
        return new Response(JSON.stringify({ success: false, error: 'Không thể xóa tài khoản admin' }), { status: 400 });
      }
      const user = await db.prepare('SELECT password FROM users WHERE username = ?').bind(username).first();
      if (!user || user.password !== password) {
        return new Response(JSON.stringify({ success: false, error: 'Tài khoản không tồn tại hoặc sai mật khẩu' }), { status: 400 });
      }
      await db.prepare('DELETE FROM user_progress WHERE username = ?').bind(username).run();
      await db.prepare('DELETE FROM users WHERE username = ?').bind(username).run();
      return new Response(JSON.stringify({ success: true }));
    }

    return new Response(JSON.stringify({ success: false, error: 'Invalid action' }), { status: 400 });

  } catch (error) {
    return new Response(JSON.stringify({ success: false, error: error.message }), { status: 500 });
  }
}
