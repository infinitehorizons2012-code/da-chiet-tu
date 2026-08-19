export async function onRequest(context) {
  const { request } = context;
  const url = new URL(request.url);

  if (url.pathname.startsWith("/api/")) {
    return context.next();
  }

  const PASSWORD = "hanzi"; // M?t kh?u m?c d?nh

  const authHeader = request.headers.get("Authorization");

  if (!authHeader) {
    return new Response("Unauthorized", {
      status: 401,
      headers: {
        "WWW-Authenticate": 'Basic realm="Vui long nhap mat khau"',
      },
    });
  }

  const [scheme, encoded] = authHeader.split(" ");
  if (!encoded || scheme !== "Basic") {
    return new Response("Bad Request", { status: 400 });
  }

  const decoded = atob(encoded);
  const [username, password] = decoded.split(":");

  if (password !== PASSWORD) {
    return new Response("Unauthorized", {
      status: 401,
      headers: {
        "WWW-Authenticate": 'Basic realm="Mat khau sai, vui long nhap lai"',
      },
    });
  }

  return context.next();
}
