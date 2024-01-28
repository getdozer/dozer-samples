import { db, type Order } from '$lib/db/db.js';
import { fail } from '@sveltejs/kit';
import { nanoid } from 'nanoid';

export const POST = async ({ request, locals }) => {
	const session = await locals.getSession();

	if (!session) {
		throw fail(303, {
			message: 'You must be logged in to checkout'
		});
	}

	const { productIDs, quantity, totalPrice } = await request.json();

	if (!productIDs || !quantity || !totalPrice) {
		throw fail(400, {
			message: 'Missing required fields'
		});
	}

	const user = await db
		.selectFrom('profile')
		.selectAll()
		.where('email', '=', session.user?.email as string)
		.executeTakeFirstOrThrow();

	// add to orders
	const data = await db
		.insertInto('order')
		.values({
			userId: user.id,
			productId: JSON.stringify(productIDs),
			quantity: quantity,
			totalPrice: parseInt(totalPrice),
			createdAt: new Date().toDateString(),
			updatedAt: new Date().toDateString(),
			id: nanoid(12)
		})
		.returning('id')
		.executeTakeFirstOrThrow();

	return new Response(JSON.stringify(data), {
		status: 200,
		headers: {
			'Content-Type': 'application/json'
		}
	});
};
