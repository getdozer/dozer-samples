import { db } from '$lib/db/db.js';
import { fail } from '@sveltejs/kit';

export const DELETE = async ({ locals }) => {
	const session = await locals.getSession();

	if (!session) {
		throw fail(303, {
			message: 'You must be logged in to checkout'
		});
	}

	const user = await db
		.selectFrom('profile')
		.selectAll()
		.where('email', '=', session.user?.email as string)
		.executeTakeFirstOrThrow();

	// delete all items from cart
	await db.deleteFrom('cart').where('cart.userId', '=', user.id).execute();

	return new Response(JSON.stringify('All items deleted successfully!'), {
		headers: {
			'Content-Type': 'application/json'
		}
	});
};
