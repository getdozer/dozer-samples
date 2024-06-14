<script lang="ts">
	import { signIn } from '@auth/sveltekit/client';

	export let data;
</script>

<h1>Welcome to SvelteKit</h1>
<button on:click={signIn}>Sign in</button>
