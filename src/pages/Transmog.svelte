<script>
    import { onMount } from 'svelte'
    import { region, realm, character } from '$stores/user'
    import { getTransmogItems } from '$api/transmogitems'
    import { percent, percentFormat, getTitle } from '$util/utils'
    import ProgressBar from '$components/ProgressBar.svelte';
    import Loading from '$components/Loading.svelte';
    import Category from '$components/Category/Category.svelte';

    export let transmogType = 0;

    const types = {
        0: "Head",
        1: "Shoulder",
        2: "Shirt",
        3: "Chest",
        4: "Waist",
        5: "Legs",
        6: "Boots",
        7: "Wrists",
        8: "Hands",
        9: "Back",
        10: "Tabard",
        11: "Two-Hand Weapon",
        12: "Ranged Weapon",
        13: "Shield",
        15: "One-Hand Weapon" 
    }


    let items
    $: promise = getTransmogItems($region, $realm, $character, transmogType).then(_ => {
        init(_);
    })

    function init(_) {
        if (!_) return;
        items = _;
    }

    onMount(async () => {
        window.ga('send', 'pageview', '{types[transmogType]} Appearances');
    });
</script>

<svelte:head>
	<title>{getTitle($character, '{types[transmogType]}')}</title>
</svelte:head>

<div class="container">
<div class="page-header">
    <h2>
        {types[transmogType]} Appearances
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
        <Category {category} superCat="Head Appearances"></Category>
    {/each}
    {/if}
  </div>
{/await}

</div>
