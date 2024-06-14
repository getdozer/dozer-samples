<script lang="ts">
	import EmptyState from '$lib/components/EmptyState.svelte';
	import ProductCard from '$lib/components/ProductCard.svelte';
	import { ApiClient } from '@dozerjs/dozer';
	import { RecordMapper } from '@dozerjs/dozer/lib/cjs/helper';
	import { OperationType } from '@dozerjs/dozer/lib/esm/generated/protos/types_pb.js';
	import { onMount } from 'svelte';
	import toast from 'svelte-french-toast';

	let productState: any = {
		records: [],
		fields: []
	};

	onMount(async () => {
		// init dozer client
		const dozer = new ApiClient('product');
		dozer
			.query({
				limit: 1000
			})
			.then(([fields, records]) => {
				productState.records = records;
				productState.fields = fields;
			});

		// init dozer client
		dozer.getFields().then((fieldsResponse) => {
			let fields = fieldsResponse.getFieldsList();
			let mapper = new RecordMapper(fieldsResponse.getFieldsList());
			let primaryIndexList = fieldsResponse.getPrimaryIndexList();
			let primaryIndexKeys = primaryIndexList.map((index) => fields[index].getName());

			let stream = dozer.onEvent();
			stream.on('data', (response) => {
				if (response.getTyp() === OperationType.UPDATE) {
					let oldValue = mapper.mapRecord(response?.getOld()?.getValuesList()!);
					let records = productState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					if (existingIndex > -1) {
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						productState.records = records;
					}
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					productState.records = [record, ...productState.records];
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					let records = productState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					if (existingIndex > -1) {
						records.splice(existingIndex, 1);
						productState.records = records;
					}
				}
			});
		});
	});

	async function handleAddToCart(productId: string, quantity: number) {
		const response = await fetch('/api/cart/add', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				productId,
				quantity
			})
		});

		const results = await response.json();

		if (results.error) {
			toast.error(results.error);
		} else {
			toast.success('Added to cart');
		}
	}

	export let data;
</script>

<div class="w-full items-start justify-center flex flex-col min-h-screen">
	<h1 class="text-2xl font-bold text-gray-900 w-full text-start">
		Welcome back, {data.currentUser.name}
	</h1>

	<h2 class="text-xl font-bold text-gray-900 py-3 w-full text-start">Recommeded Products</h2>

	{#if productState.records.length}
		<div class="mt-8 grid grid-cols-1 gap-y-12 sm:grid-cols-2 sm:gap-x-6 lg:grid-cols-4 xl:gap-x-8">
			{#each productState.records as item}
				<ProductCard
					title={item.name}
					description={item.description}
					price={item.price}
					image={item.image}
					type="product"
					quantity={1}
				>
					<form id="add-to-cart-form">
						<input hidden type="text" name="productId" value={item.id} />
						<input hidden type="text" name="quantity" value="1" />
						<button
							on:click={() => {
								handleAddToCart(item.id, 1);
							}}
							class="relative flex items-center justify-center rounded-md border border-transparent bg-gray-100 px-8 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200"
							>Add to bag
						</button>
					</form>
				</ProductCard>
			{/each}
		</div>
	{:else}
		<EmptyState title="No products found" description="Try adding some products to your store" />
	{/if}
</div>
