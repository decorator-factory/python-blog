<script>
    export let post; // { uid: number, title: string, content: string }

    let show = false;
    const toggleVisibility = () => { show = !show; };
</script>

<style>
    .post {
        display: grid;
        grid-template-rows: minmax(1.5em, 1fr) minmax(3em, auto);
        grid-template-columns: 1fr 10fr 1fr;

        grid-template-areas:
            "title title uid"
            "body body body"
        ;

        border: 4px solid black;

        max-width: 40em;
        margin-bottom: 7mm;
    }

    .post .uid {
        grid-area: "uid";
        padding: 0.5em;
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
    }

    .post div {
        border: 1px solid black;
    }
</style>

<div class="post">
    <div class="uid"><span class="centered">{post.uid}</span></div>
    <div class="title">{post.title}</div>
    <div class="content">
        <button on:click={toggleVisibility}>{show ? 'Hide' : 'Show'}</button>
        {#if show}
            <div>
            {@html post.content}
            </div>
        {/if}
    </div>
</div>