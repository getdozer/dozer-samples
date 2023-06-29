import { db, type Cart } from '$lib/db/db';
import { fail, redirect } from '@sveltejs/kit';
import { nanoid } from 'nanoid';

export const load = async ({ locals }) => {
	const session = await locals.getSession();

	if (!session) {
		throw redirect(303, '/auth/signin');
	}
	const user = await db
		.selectFrom('profile')
		.selectAll()
		.where('email', '=', session.user?.email as string)
		.executeTakeFirstOrThrow();

	if (!user) {
		throw redirect(303, '/auth/signin?csrf=true');
	}

	const products = await db.selectFrom('product').selectAll().execute();

	return {
		currentUser: user,
		products: products
	};
};

// export const actions = {
// 	addToCart: async ({ request, locals, url }) => {
// 		const session = await locals.getSession();
// 		const formData = await request.formData();
// 		const productId = formData.get('productId') as string;
// 		const quantity = formData.get('quantity') as string;

// 		if (!session) {
// 			throw redirect(303, '/auth/signin?csrf=true');
// 		}

// 		const user = await db
// 			.selectFrom('profile')
// 			.selectAll()
// 			.where('email', '=', session.user?.email as string)
// 			.executeTakeFirstOrThrow();

// 		// Convenient validation check:
// 		if (!productId) {
// 			// Again, always return { form } and things will just work.
// 			return fail(400, { message: 'Missing productId' });
// 		}

// 		if (!quantity) {
// 			// Again, always return { form } and things will just work.
// 			return fail(400, { message: 'Missing quantity' });
// 		}

// 		console.log('server form', productId, quantity, user.id);

// 		// add item to cart
// 		const data = await db
// 			.insertInto('cart')
// 			.values({
// 				productId: productId,
// 				quantity: parseInt(quantity),
// 				userId: user.id,
// 				createdAt: new Date().toDateString(),
// 				updatedAt: new Date().toDateString(),
// 				id: nanoid(12)
// 			})
// 			.returning('id')
// 			.executeTakeFirstOrThrow();

// 		console.log('server form', data);

// 		return {
// 			status: 201,
// 			message: 'Added to cart'
// 		};
// 	}
// };
