<script>
    import PostCard from './PostCard.svelte';

    const API_ROOT = '';

    let selectedTag = '';
    let posts = [];

    const filterPosts = (posts, tag) =>
        tag === ""
            ? posts
            : tag.endsWith("*")
                ? posts.filter(p => p.tags.some(t => t.startsWith(tag.slice(0, -1))))
                : posts.filter(p => p.tags.includes(tag));


    $: displayedPosts = filterPosts(posts, selectedTag);



    const getPosts = () =>
        fetch(`${API_ROOT}/posts`)
        .then(r => r.json().then(j => { posts = j; }))
    ;

    const getPostContent = uid =>
        fetch(`${API_ROOT}/posts/${uid}/content`)
        .then(r => r.json()) // it's actually a JSON-encoded string, so it's fine
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
    <div class="search">
        Tag filter: <input type="text" bind:value={selectedTag}/><br/>
        <ul>
            <li>Simple tag search like 'python' works as expected</li>
            <li>Putting a '*' at the end will match any tag that starts with 'python'</li>
        </ul>
    </div>
    <div class="posts">
        {#await getPosts()}
            Loading posts...
        {:then _}
            {#each displayedPosts as post}
                <PostCard {post} {getPostContent}/>
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
        min-height: 50%;
        max-height: 80%;
        background: #f2f2f7;
        margin: auto;
        overflow-y: scroll;

        display: grid;
        grid-template-areas:
            "posts search"
            "posts .     ";
        grid-template-columns: 20fr 1fr;
        grid-template-rows: 2em auto;
    }

    .posts {
        height: 100%;
        margin: auto;
        width: 100%;
        grid-area: posts;
    }

    .search {
        grid-area: search;
    }
</style>