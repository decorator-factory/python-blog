<script>
    import { slide } from 'svelte/transition';
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();

    export let currentTagFilter;
    export let getPostContent;
    export let post; // { uid: number, title: string, content: string? }

    let show = false;
    const toggleVisibility = () => {
        show = !show;
        if (show)
            getPostContent(post.uid).then(s => { content = s; });
    };

    let content = "Loading...";


    const getMatchedTags = (myTags, tagFilter) =>
        tagFilter.endsWith("*")
            ? myTags.filter(t => t.startsWith(tagFilter.slice(0, -1)))
            : myTags.filter(t => t === tagFilter);
    $: matchedTags = getMatchedTags(post.tags, currentTagFilter);

    const selectTag = tag => {
        dispatch('tag-selected', { tag });
    };
</script>

<style>
    .post {
        width: 90%;
        display: grid;
        grid-template-rows: minmax(1.5em, 1fr) 1.5em minmax(3em, auto);
        grid-template-columns: 1fr 10fr 1fr;

        grid-template-areas:
            "title title uid"
            "tags tags tags"
            "body body body"
        ;

        border: 4px solid black;

        max-width: 40em;
        /* margin-bottom: 7mm; */

        transition: 0.2s;
    }

    .post .uid {
        grid-area: "uid";
        padding: 5mm;
        background: #ddddff;
        font-size: 20pt;
    }

    .centered {
        margin-left: auto;
        margin-right: auto;
    }

    .post .title {
        grid-area: title;
        padding: 0.5em;
        font-size: 150%;
        font-weight: 800;
    }

    .post .content {
        grid-area: body;
        padding: 0.5em;
        background: white;
    }

    .large {
        max-width: 100em;
    }

    .tags {
        border-top: 1px solid #cccccc;
        grid-area: tags;
    }

    .tag {
        color: #737373;
        margin: 4px;
        padding: 2mm 1mm;
        cursor: pointer;
        transition: 0.1s;
    }

    .tag:hover {
        color: #000000;
    }

    .selected-tag {
        color: red;
    }
</style>

<div class="post" class:large={show} transition:slide={{duration: 150}}>
    <div class="uid"><span class="centered">{post.uid}</span></div>
    <div class="title">{post.title}</div>
    <div class="tags">
        {#each post.tags as tag}
            <span
                class="tag"
                class:selected-tag={matchedTags.includes(tag)}
                on:click={selectTag(tag)}
            >{tag} </span>
        {/each}
    </div>
    <div class="content">
        <button on:click={toggleVisibility}>{show ? 'Hide' : 'Show'}</button>
        {#if show}
            <div>
            {@html content}
            </div>
        {/if}
    </div>
</div>