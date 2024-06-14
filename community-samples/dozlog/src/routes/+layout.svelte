<script lang="ts">
	import { networkStore } from 'svelte-legos';
	import '$lib/app.css';
	import OfflineBanner from '$lib/components/OfflineBanner.svelte';
	import { Toaster } from 'svelte-french-toast';
	import { page } from '$app/stores';
	import { className } from '$lib/utils/utils';

	const networkState = networkStore();

	const menu = [
		{
			name: 'Products',
			href: '/'
		},
		{
			name: 'Cart',
			href: '/cart'
		},
		{
			name: 'Admin',
			href: '/admin'
		}
	];

	$: path = $page.url.pathname;
</script>

<div class="mx-auto px-3 sm:px-6 lg:px-8 flex flex-col space-y-6 max-w-5xl">
	<Toaster />
	{#if !$networkState.isOnline}
		<OfflineBanner />
	{/if}

	<nav class="flex flex-row w-full items-center justify-between">
		<div>
			<a href="/" class="text-2xl font-bold tracking-tight text-gray-900">Dozlog</a>
		</div>

		<ul class="flex justify-between flex-row gap-6">
			{#each menu as item}
				<a
					href={item.href}
					class={className(
						'text-gray-900 text-sm hover:text-pink-500',
						path === item.href
							? 'underline text-pink-500'
							: 'transition-all duration-150 ease-in-out'
					)}>{item.name}</a
				>
			{/each}
		</ul>
	</nav>

	<slot />
</div>
