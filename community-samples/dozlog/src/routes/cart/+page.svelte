<script lang="ts">
	import { onMount } from 'svelte';
	import { ApiClient } from '@dozerjs/dozer';
	import { RecordMapper } from '@dozerjs/dozer/lib/cjs/helper';
	import { OperationType } from '@dozerjs/dozer/lib/cjs/generated/protos/types_pb.js';
	import ProductCard from '$lib/components/ProductCard.svelte';
	import { enhance } from '$app/forms';
	import EmptyState from '$lib/components/EmptyState.svelte';
	import toast from 'svelte-french-toast';

	let results: any = null;
	let records: any = [];
	let fields: any = [];
	let state: any = {
		records: [],
		fields: []
	};

	let productState: any = {
		records: [],
		fields: []
	};

	let allCartItems: any = [];
	let totalCartItems = 0;
	let subtotalPrice = 0;
	let shippingPrice = 5;
	let taxPrice = 8.32;

	$: allCartItems = state.records.map((cartItem: any) => {
		let product = productState.records.find((product: any) => product.id === cartItem.productId);
		return {
			...product,
			quantity: cartItem.quantity,
			cartId: cartItem.id
		};
	});

	// get all product ids
	$: productIds = allCartItems.map((cartItem: any) => cartItem.id);

	$: totalCartItems = state.records.reduce((acc: any, curr: any) => {
		return acc + curr.quantity;
	}, 0);

	$: subtotalPrice = allCartItems.reduce((acc: any, curr: any) => {
		return acc + curr.price * curr.quantity;
	}, 0);

	$: finalPrice = subtotalPrice + shippingPrice + taxPrice;

	onMount(async () => {
		// init dozer client
		const client = new ApiClient('cart');
		client.query().then(([fields, records]) => {
			console.log('fields', JSON.stringify(fields, null, 2));
			console.log('records', JSON.stringify(records, null, 2));

			state.records = records;
			state.fields = fields;
		});

		client.getFields().then((fieldsResponse) => {
			let fields = fieldsResponse.getFieldsList();
			let mapper = new RecordMapper(fieldsResponse.getFieldsList());
			let primaryIndexList = fieldsResponse.getPrimaryIndexList();
			let primaryIndexKeys = primaryIndexList.map((index) => fields[index].getName());

			let stream = client.onEvent();
			stream.on('data', (response) => {
				if (response.getTyp() === OperationType.UPDATE) {
					let oldValue = mapper.mapRecord(response?.getOld()?.getValuesList()!);
					let records = state.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					if (existingIndex > -1) {
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						state.records = records;
					}

					console.log('updated', oldValue, mapper.mapRecord(response?.getNew()?.getValuesList()!));
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					state.records = [record, ...state.records];
					console.log('inserted', record);
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					let records = state.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					if (existingIndex > -1) {
						records.splice(existingIndex, 1);
						state.records = records;
					}

					console.log('deleted', record);
				}
			});
		});
	});

	onMount(async () => {
		const productClient = new ApiClient('product');
		productClient.query().then(([fields, records]) => {
			console.log('fields', JSON.stringify(fields, null, 2));
			console.log('records', JSON.stringify(records, null, 2));

			productState.records = records;
			productState.fields = fields;
		});

		// init dozer client
		productClient.getFields().then((fieldsResponse) => {
			let fields = fieldsResponse.getFieldsList();
			let mapper = new RecordMapper(fieldsResponse.getFieldsList());
			let primaryIndexList = fieldsResponse.getPrimaryIndexList();
			let primaryIndexKeys = primaryIndexList.map((index) => fields[index].getName());

			console.info('fields', fields);
			console.info('primary index keys', primaryIndexKeys);
			console.log('primary index list', primaryIndexList);
			console.info('mapper', mapper);

			let stream = productClient.onEvent();
			stream.on('data', (response) => {
				if (response.getTyp() === OperationType.UPDATE) {
					let oldValue = mapper.mapRecord(response?.getOld()?.getValuesList()!);
					let records = productState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					console.log('old', oldValue);
					console.log('new', mapper.mapRecord(response?.getNew()?.getValuesList()!));
					console.log('existingIndex', existingIndex);

					if (existingIndex > -1) {
						console.log('updating');
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						console.log('updated', records[existingIndex]);
						productState.records = records;
					}

					console.log('product updated', response?.getNew()?.getValuesList()!);
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					console.log('inserting', record);
					productState.records = [record, ...productState.records];
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);

					let records = productState.records;

					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					console.log('deleting', record);
					console.log('existingIndex', existingIndex);

					if (existingIndex > -1) {
						console.log('deleting');
						records.splice(existingIndex, 1);
						productState.records = records;
					}

					console.log('deleted', record);
				}
			});
		});
	});

	async function handleCheckout() {
		await fetch('/api/cart/checkout', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				quantity: totalCartItems,
				totalPrice: finalPrice,
				productIDs: productIds
			})
		})
			.then((res) => res.json())
			.then((res) => {
				return res;
			})
			.catch((err) => {
				return err;
			});

		handleDeleteAllCartItems();
	}

	// delete all cart items after checkout
	async function handleDeleteAllCartItems() {
		console.log('Deleting all cart items');
		await fetch('/api/cart/delete', {
			method: 'DELETE'
		})
			.then((res) => res.json())
			.then((res) => {
				return res;
			})
			.catch((err) => {
				return err;
			});

		toast.success('Checkout successful');
	}
</script>

<div class="h-screen w-full">
	<h2 class="text-xl font-bold text-gray-900 py-3">My Cart</h2>

	{#if allCartItems.length === 0}
		<EmptyState
			title="Your cart is empty"
			description="Must add some products to cart first before you can checkout"
		/>
	{:else}
		<div class="w-full grid grid-cols-2 gap-x-6 items-start justify-center">
			<div
				id="cart-items"
				class="flex flex-col col-span-2 sm:col-span-1 w-full items-center justify-center gap-3 max-w-2xl"
			>
				{#each allCartItems as item}
					<ProductCard
						title={item.name}
						description={item.description}
						price={item.price}
						image={item.image}
						type="cart"
						quantity={item.quantity}
					>
						<form id="remove-product-from-cart" method="POST" use:enhance>
							<input hidden type="text" name="id" value={item.cartId} />
							<button
								type="submit"
								formaction="?/removeFromCart"
								class="text-gray-900 text-sm hover:text-red-500"
								>Remove
							</button>
						</form>
					</ProductCard>
				{/each}
			</div>

			{#if subtotalPrice > 0}
				<div id="card-value" class="col-span-2 sm:col-span-1 bg-gray-50 h-auto">
					<section
						aria-labelledby="summary-heading"
						class="mt-16 rounded-lg bg-gray-50 px-4 py-6 sm:p-6 lg:col-span-5 lg:mt-0 lg:p-8"
					>
						<h2 id="summary-heading" class="text-lg font-medium text-gray-900">Order summary</h2>

						<dl class="mt-6 space-y-4">
							<div class="flex items-center justify-between">
								<dt class="text-sm text-gray-600">Subtotal</dt>
								<dd class="text-sm font-medium text-gray-900">${subtotalPrice}</dd>
							</div>
							<div class="flex items-center justify-between border-t border-gray-200 pt-4">
								<dt class="flex items-center text-sm text-gray-600">
									<span>Shipping estimate</span>
									<a href="#" class="ml-2 flex-shrink-0 text-gray-400 hover:text-gray-500">
										<span class="sr-only">Learn more about how shipping is calculated</span>
										<svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
											<path
												fill-rule="evenodd"
												d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM8.94 6.94a.75.75 0 11-1.061-1.061 3 3 0 112.871 5.026v.345a.75.75 0 01-1.5 0v-.5c0-.72.57-1.172 1.081-1.287A1.5 1.5 0 108.94 6.94zM10 15a1 1 0 100-2 1 1 0 000 2z"
												clip-rule="evenodd"
											/>
										</svg>
									</a>
								</dt>
								<dd class="text-sm font-medium text-gray-900">$5.00</dd>
							</div>
							<div class="flex items-center justify-between border-t border-gray-200 pt-4">
								<dt class="flex text-sm text-gray-600">
									<span>Tax estimate</span>
									<a href="#" class="ml-2 flex-shrink-0 text-gray-400 hover:text-gray-500">
										<span class="sr-only">Learn more about how tax is calculated</span>
										<svg class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
											<path
												fill-rule="evenodd"
												d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM8.94 6.94a.75.75 0 11-1.061-1.061 3 3 0 112.871 5.026v.345a.75.75 0 01-1.5 0v-.5c0-.72.57-1.172 1.081-1.287A1.5 1.5 0 108.94 6.94zM10 15a1 1 0 100-2 1 1 0 000 2z"
												clip-rule="evenodd"
											/>
										</svg>
									</a>
								</dt>
								<dd class="text-sm font-medium text-gray-900">$8.32</dd>
							</div>
							<div class="flex items-center justify-between border-t border-gray-200 pt-4">
								<dt class="text-base font-medium text-gray-900">Order total</dt>
								<dd class="text-base font-medium text-gray-900">${finalPrice}</dd>
							</div>
						</dl>

						<div class="mt-6">
							<button
								type="button"
								on:click={handleCheckout}
								class="w-full rounded-md border border-transparent bg-pink-500 px-4 py-3 text-base font-medium text-white shadow-sm hover:bg-pink-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-50"
								>Checkout</button
							>
						</div>
					</section>
				</div>
			{/if}
		</div>
	{/if}
</div>
