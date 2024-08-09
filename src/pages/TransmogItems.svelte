<script>
    import { onMount } from 'svelte'
    import { region, realm, character } from '$stores/user'
    import { getTransmogItems } from '$api/transmogitems'
    import { percent, percentFormat, getTitle } from '$util/utils'
    import ProgressBar from '$components/ProgressBar.svelte';
    import Loading from '$components/Loading.svelte';
    import Category from '$components/Category/Category.svelte';

    let items
    $: promise = getTransmogItems($region, $realm, $character).then(_ => {
        init(_);
    })

    function init(_) {
        if (!_) return;
        items = _;
    }

    onMount(async () => {
        window.ga('send', 'pageview', 'TransmogItems');
    });
</script>

<svelte:head>
	<title>{getTitle($character, 'TransmogItems')}</title>
</svelte:head>

<div class="container">
<div class="page-header">
    <h2>
        Transmog Sets
        <ProgressBar 
                rightSide={true}
                width={items ? percent(items.collected, items.possible) : 0} 
                percentage={items ? percentFormat(items.collected, items.possible) : ""}/>
    </h2>
</div>

{#await promise}
    <Loading/>
{:then value}
  <div>
    {#if items}
    {#each items.categories as category}
        <Category {category} superCat="Transmog Items"></Category>
    {/each}
    {/if}
  </div>
{/await}

</div>
