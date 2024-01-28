import { SvelteKitAuth } from '@auth/sveltekit';
import GitHub from '@auth/core/providers/github';
import { GITHUB_ID, GITHUB_SECRET, AUTH_SECRET } from '$env/static/private';
import type { Handle } from '@sveltejs/kit';
import { KyselyAdapter } from '$lib/adapter/KyselyAdapter';
import { db } from '$lib/db/db';

export const handle = SvelteKitAuth({
	trustHost: true,
	adapter: KyselyAdapter(db),
	secret: AUTH_SECRET,
	providers: [GitHub({ clientId: GITHUB_ID, clientSecret: GITHUB_SECRET })] as any,
	session: {
		// Choose how you want to save the user session.
		// The default is `"jwt"`, an encrypted JWT (JWE) stored in the session cookie.
		// If you use an `adapter` however, we default it to `"database"` instead.
		// You can still force a JWT session by explicitly defining `"jwt"`.
		// When using `"database"`, the session cookie will only contain a `sessionToken` value,
		// which is used to look up the session in the database.
		strategy: 'database',

		// Seconds - How long until an idle session expires and is no longer valid.
		// maxAge: 30 * 24 * 60 * 60, // 30 days

		// Seconds - Throttle how frequently to write to database to extend a session.
		// Use it to limit write operations. Set to 0 to always update the database.
		// Note: This option is ignored if using JSON Web Tokens
		// updateAge: 24 * 60 * 60, // 24 hours

		// The session token is usually either a random UUID or string, however if you
		// need a more customized session token string, you can define your own generate function.
		generateSessionToken: () => {
			return crypto.randomUUID();
		}
	},
	events: {
		signIn: async () => {
			console.log('✅ Successfully signed in');
		},
		createUser: async (message) => {
			console.log('✅ Successfully created user in database', message);
			console.log('👮‍♂️ User', message.user.name);
			console.log('💌 Email', message.user.email);
		},
		linkAccount: async (message) => {
			console.log('✅ Successfully linked account', message);
		},
		session(message) {
			console.log('👮‍♂️ User', message);
		}
	}
}) satisfies Handle;
