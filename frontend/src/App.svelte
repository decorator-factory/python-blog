<script>
    import PostCard from './PostCard.svelte';

    const API_ROOT = '';

    const getPosts = () =>
        fetch(`${API_ROOT}/posts`)
        .then(r => r.json())
    ;

    const post = {
        uid: 42,
        title: 'Hello, world!',
        content: 'Content!!!'
    };
</script>

<header>
    <h1 class="main-title">Welcome to my blog!</h1>
</header>
<main>
    <div class="posts">
        {#await getPosts()}
            Loading posts...
        {:then posts}
            {#each posts as post}
                <PostCard {post}/>
            {/each}
        {/await}
    </div>
</main>

<style>
    header {
        width: 100%;
        min-height: 8em;
        background: #98e675;
    }

    .main-title {
        font-size: 36pt;
        margin: 0;
        padding-top: 0.5em;
        text-align: center;
    }

    main {
        width: 60%;
        max-height: 80%;
        background: #f2f2f7;
        margin: auto;
        overflow-y: scroll;
    }

    main>.posts {
        height: 100%;
        margin: auto;
        width: 100%;
    }
</style>