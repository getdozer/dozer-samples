import { db } from '$lib/db/db';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ request }) => {
	const { ids } = await request.json();

	const response = await db.selectFrom('product').where('id', 'in', ids).selectAll().execute();

	return new Response(JSON.stringify(response), {
		headers: { 'content-type': 'application/json' }
	});
};
