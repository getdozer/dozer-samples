<script lang="ts">
	import { onMount } from 'svelte';
	import { ApiClient } from '@dozerjs/dozer';
	import { RecordMapper } from '@dozerjs/dozer/lib/cjs/helper';
	import { OperationType } from '@dozerjs/dozer/lib/cjs/generated/protos/types_pb.js';
	import NewUserCard from '$lib/components/NewUserCard.svelte';
	import { className } from '$lib/utils/utils';
	import NewOrderCard from '$lib/components/NewOrderCard.svelte';
	import NewCartCard from '$lib/components/NewCartCard.svelte';
	import Stats from '$lib/components/Stats.svelte';
	import EmptyState from '$lib/components/EmptyState.svelte';

	let state: any = {
		records: [],
		fields: []
	};

	let userState: any = {
		records: [],
		fields: []
	};

	let cartState: any = {
		records: [],
		fields: []
	};

	let wishlistState: any = {
		records: [],
		fields: []
	};

	let ordersState: any = {
		records: [],
		fields: []
	};

	let cartCountState: any = {
		records: [],
		fields: []
	};

	let orderCountState: any = {
		records: [],
		fields: []
	};

	let activeTab = 'analytics';

	const menu = [
		{
			name: 'Analytics'
		},
		{
			name: 'Users'
		},
		{
			name: 'Cart'
		},
		{
			name: 'Orders'
		}
	];

	// cart
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

			console.info('fields', fields);
			console.info('primary index keys', primaryIndexKeys);
			console.log('primary index list', primaryIndexList);
			console.info('mapper', mapper);

			let stream = client.onEvent();
			stream.on('data', (response) => {
				if (response.getTyp() === OperationType.UPDATE) {
					let oldValue = mapper.mapRecord(response?.getOld()?.getValuesList()!);
					let records = state.records;
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
						state.records = records;
					}
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					console.log('inserting', record);
					state.records = [record, ...state.records];
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);

					let records = state.records;

					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					console.log('deleting', record);
					console.log('existingIndex', existingIndex);

					if (existingIndex > -1) {
						console.log('deleting');
						records.splice(existingIndex, 1);
						state.records = records;
					}

					console.log('deleted', record);
				}
			});
		});
	});

	// profile
	onMount(async () => {
		// init dozer client
		const client = new ApiClient('profile');
		client.query().then(([fields, records]) => {
			console.log('fields', JSON.stringify(fields, null, 2));
			console.log('records', JSON.stringify(records, null, 2));

			userState.records = records;
			userState.fields = fields;
		});

		client.getFields().then((fieldsResponse) => {
			let fields = fieldsResponse.getFieldsList();
			let mapper = new RecordMapper(fieldsResponse.getFieldsList());
			let primaryIndexList = fieldsResponse.getPrimaryIndexList();
			let primaryIndexKeys = primaryIndexList.map((index) => fields[index].getName());

			console.info('fields', fields);
			console.info('primary index keys', primaryIndexKeys);
			console.log('primary index list', primaryIndexList);
			console.info('mapper', mapper);

			let stream = client.onEvent();
			stream.on('data', (response) => {
				if (response.getTyp() === OperationType.UPDATE) {
					let oldValue = mapper.mapRecord(response?.getOld()?.getValuesList()!);
					let records = userState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					if (existingIndex > -1) {
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						userState.records = records;
					}
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					userState.records = [record, ...userState.records];
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					let records = userState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					if (existingIndex > -1) {
						records.splice(existingIndex, 1);
						userState.records = records;
					}
				}
			});
		});
	});

	// order
	onMount(async () => {
		// init dozer client
		const client = new ApiClient('order');
		client.query().then(([fields, records]) => {
			console.log('fields', JSON.stringify(fields, null, 2));
			console.log('records', JSON.stringify(records, null, 2));

			ordersState.records = records;
			ordersState.fields = fields;
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
					let records = ordersState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					if (existingIndex > -1) {
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						ordersState.records = records;
					}
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					ordersState.records = [record, ...ordersState.records];
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					let records = ordersState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					if (existingIndex > -1) {
						records.splice(existingIndex, 1);
						ordersState.records = records;
					}
				}
			});
		});
	});

	// cart count
	onMount(async () => {
		// init dozer client
		const client = new ApiClient('cart_count');
		client.query().then(([fields, records]) => {
			console.log('fields', JSON.stringify(fields, null, 2));
			console.log('records', JSON.stringify(records, null, 2));

			cartCountState.records = records;
			cartCountState.fields = fields;
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
					let records = cartCountState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					if (existingIndex > -1) {
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						cartCountState.records = records;
					}
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					cartCountState.records = [record, ...cartCountState.records];
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					let records = cartCountState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					if (existingIndex > -1) {
						records.splice(existingIndex, 1);
						cartCountState.records = records;
					}
				}
			});
		});
	});

	// order count
	onMount(async () => {
		// init dozer client
		const client = new ApiClient('order_count');
		client.query().then(([fields, records]) => {
			console.log('fields', JSON.stringify(fields, null, 2));
			console.log('records', JSON.stringify(records, null, 2));

			orderCountState.records = records;
			orderCountState.fields = fields;
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
					let records = orderCountState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === oldValue[k])
					);

					if (existingIndex > -1) {
						records[existingIndex] = mapper.mapRecord(response?.getNew()?.getValuesList()!);
						orderCountState.records = records;
					}

					console.log('update', JSON.stringify(response, null, 2));
				}

				// insert event
				if (response.getTyp() === OperationType.INSERT) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					orderCountState.records = [record, ...orderCountState.records];

					console.log('insert', JSON.stringify(response, null, 2));
				}

				// delete event
				if (response.getTyp() === OperationType.DELETE) {
					let record = mapper.mapRecord(response?.getNew()?.getValuesList()!);
					let records = orderCountState.records;
					let existingIndex = records.findIndex((v: { [x: string]: any }) =>
						primaryIndexKeys.every((k) => v[k] === record[k])
					);

					if (existingIndex > -1) {
						records.splice(existingIndex, 1);
						orderCountState.records = records;
					}

					console.log('delete', JSON.stringify(response, null, 2));
				}
			});
		});
	});
</script>

<div class="flex flex-col items-center justify-center w-full">
	<h1 class="text-2xl font-bold text-gray-900 text-start w-full">Realtime Activities</h1>
	<div class="flex flex-col items-start justify-start w-full overflow-auto">
		<div
			class="flex flex-row w-auto mt-3 items-start justify-start gap-3 py-2 bg-gray-50 px-3 rounded-lg"
		>
			{#each menu as item}
				<!-- svelte-ignore a11y-click-events-have-key-events -->
				<div
					on:click={() => (activeTab = item.name.toLowerCase())}
					class={className(
						'px-3 w-fit text-sm text-center py-1 rounded-md hover:cursor-pointer hover:bg-white hover:shadow-sm',
						activeTab === item.name.toLowerCase() ? 'bg-white shadow-sm' : 'bg-gray-50 shadow-none'
					)}
				>
					{item.name}
				</div>
			{/each}
		</div>

		{#if activeTab === 'cart'}
			{#if state.records.length === 0}
				<EmptyState title="No cart record found" description="Add new cart to see the activities" />
			{:else}
				<div class="mt-6 w-full flex flex-col gap-3">
					{#each state.records as item}
						<NewCartCard
							cartId={item.id}
							productId={item.productId}
							quantity={item.quantity}
							orderedBy={item.userId}
							timestamp={item.createdAt}
						/>
					{/each}
				</div>
			{/if}
		{:else if activeTab === 'users'}
			{#if userState.records.length === 0}
				<EmptyState title="No user record found" description="Add new user to see the activities" />
			{:else}
				<div class="mt-6 w-full flex">
					{#each userState.records as item}
						<NewUserCard
							username={item.name}
							email={item.email}
							userId={item.id}
							image={item.image}
						/>
					{/each}
				</div>
			{/if}
		{:else if activeTab === 'orders'}
			{#if ordersState.records.length === 0}
				<EmptyState
					title="No order record found"
					description="Add new order to see the activities"
				/>
			{:else}
				<div class="mt-6 w-full flex flex-col gap-3">
					{#each ordersState.records as item}
						<NewOrderCard
							orderId={item.id}
							orderDate={item.createdAt}
							orderTotal={item.totalPrice}
							orderQuantity={item.quantity}
							orderedBy={item.userId}
						/>
					{/each}
				</div>
			{/if}
		{:else if activeTab === 'analytics'}
			<div class="mt-6 w-full flex flex-col gap-6">
				{#if orderCountState.records.length}
					<div id="order-stats" class="space-y-3">
						<h2 class="text-xl font-bold text-gray-900 py-3">Order stats</h2>

						<div class="grid grid-cols-5 w-full gap-3">
							{#each orderCountState.records as item}
								<div class="col-span-5 sm:col-span-3">
									<Stats
										title="Total Orders value"
										value={`$${item.total_price.toFixed(2)}`}
										stats={`$${(item.total_price / item.unique_users_count).toFixed(
											2
										)} avg order per user`}
									/>
								</div>

								<div class="col-span-5 sm:col-span-2">
									<Stats
										title="Total Orders"
										value={`${item.total_quantity.toFixed(2)}`}
										stats={`${item.avg_order_per_user.toFixed(2)} avg order per user`}
									/>
								</div>

								<div class="col-span-5 sm:col-span-5">
									<Stats
										title="Cancellations"
										value={`${item.total_quantity.toFixed(2)}`}
										stats={`${item.avg_order_per_user.toFixed(2)} avg order per user`}
									/>
								</div>
							{/each}
						</div>
					</div>
				{/if}

				{#if cartCountState.records.length}
					<div id="cart-stats" class="space-y-3">
						<h2 class="text-xl font-bold text-gray-900 py-3">Cart stats</h2>
						<div class="grid grid-cols-5 w-full gap-3">
							{#each cartCountState.records as item}
								<div class="col-span-5 sm:col-span-3">
									<Stats
										title="Total Cart value"
										value={`$${item.total_cart_value.toFixed(2)}`}
										stats="without tax and shipping"
									/>
								</div>

								<div class="col-span-5 sm:col-span-2">
									<Stats
										title="Total Cart items"
										value={`${item.total_items.toFixed(2)}`}
										stats="across all users"
									/>
								</div>

								<div class="col-span-5 sm:col-span-2">
									<Stats
										title="Total Shipping fee"
										value={`${item.total_shipping.toFixed(2)}`}
										stats="$5.32 per user cart"
									/>
								</div>

								<div class="col-span-5 sm:col-span-2">
									<Stats
										title="Total Tax fee"
										value={`${item.total_tax.toFixed(2)}`}
										stats="$9.45 per user cart"
									/>
								</div>
							{/each}
						</div>
					</div>
				{/if}

				{#if orderCountState.records.length}
					<div id="user-stats" class="space-y-3">
						<h2 class="text-xl font-bold text-gray-900 py-3">User stats</h2>
						{#each orderCountState.records as item}
							<Stats
								title="Total Users"
								value={`${item.unique_users_count.toFixed(2)}`}
								stats={`${item.avg_order_per_user.toFixed(2)} avg order per user`}
							/>

							<Stats
								title="Avg Users"
								value={`${item.unique_users_count.toFixed(2)}`}
								stats={`${item.avg_order_per_user.toFixed(2)} avg order per user`}
							/>
						{/each}
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
