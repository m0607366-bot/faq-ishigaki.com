// www.faq-ishigaki.com/… → https://faq-ishigaki.com/…（パスと ?… はそのまま）
export default {
	fetch(request) {
		const u = new URL(request.url);
		u.protocol = "https:";
		u.hostname = "faq-ishigaki.com";
		u.port = "";
		return Response.redirect(u.toString(), 301);
	},
};
