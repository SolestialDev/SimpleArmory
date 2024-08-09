<script>
    import { onMount } from 'svelte'
    import { region, realm, character } from '$stores/user'
    import { getTransmogSets } from '$api/transmogsets'
    import { percent, percentFormat, getTitle } from '$util/utils'
    import ProgressBar from '$components/ProgressBar.svelte';
    import Loading from '$components/Loading.svelte';
    import Category from '$components/Category/Category.svelte';

    let sets
    $: promise = getTransmogSets($region, $realm, $character).then(_ => {
        init(_);
    })

    function init(_) {
        if (!_) return;
        sets = _;
    }

    onMount(async () => {
        window.ga('send', 'pageview', 'TransmogSets');
    });
</script>

<svelte:head>
	<title>{getTitle($character, 'TransmogSets')}</title>
</svelte:head>

<div class="container">
<div class="page-header">
    <h2>
        Transmog Sets
        <ProgressBar 
                rightSide={true}
                width={sets ? percent(sets.collected, sets.possible) : 0} 
                percentage={sets ? percentFormat(sets.collected, sets.possible) : ""}/>
    </h2>
</div>

{#await promise}
    <Loading/>
{:then value}
  <div>
    {#if sets}
    {#each sets.categories as category}
        <Category {category} superCat="Transmog Sets"></Category>
    {/each}
    {/if}
  </div>
{/await}

</div>
