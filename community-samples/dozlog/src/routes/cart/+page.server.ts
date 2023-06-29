import { fail, redirect } from '@sveltejs/kit';
import { db } from '$lib/db/db';

export const load = async () => {
	return {};
};

export const actions = {
	removeFromCart: async ({ request, locals, url }) => {
		const session = await locals.getSession();
		const formData = await request.formData();
		const id = formData.get('id') as string;

		if (!session) {
			throw redirect(303, '/auth/signin?csrf=true');
		}

		const user = await db
			.selectFrom('profile')
			.selectAll()
			.where('email', '=', session.user?.email as string)
			.executeTakeFirstOrThrow();

		if (!id) {
			return fail(400, { message: 'Missing cart id' });
		}

		// remove item from cart
		const data = await db
			.deleteFrom('cart')
			.where('userId', '=', user.id)
			.where('cart.id', '=', id)
			.execute();

		console.log('server form', data);

		return {
			status: 201,
			message: 'Removed from cart'
		};
	},
	orderCheckout: async ({ request, locals, url }) => {
		const session = await locals.getSession();
		const formData = await request.formData();
		const id = formData.get('id') as string;

		if (!session) {
			throw redirect(303, '/auth/signin?csrf=true');
		}

		const user = await db
			.selectFrom('profile')
			.selectAll()
			.where('email', '=', session.user?.email as string)
			.executeTakeFirstOrThrow();

		if (!id) {
			return fail(400, { message: 'Missing cart id' });
		}

		// remove item from cart
		const data = await db
			.deleteFrom('cart')
			.where('userId', '=', user.id)
			.where('cart.id', '=', id)
			.execute();

		console.log('server form', data);

		return {
			status: 201,
			message: 'Removed from cart'
		};
	}
};
