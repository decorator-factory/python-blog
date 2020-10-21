<script>
    import PostCard from './PostCard.svelte';

    const API_ROOT = '';

    let selectedTag = '';
    let posts = [];

    const filterPosts = (posts, tag) => {
        tag = tag.toLowerCase();

        if (tag === "")
            return posts;

        if (tag.startsWith("^"))
            return posts.filter(p => p.title.toLowerCase().startsWith(tag.slice(1)));

        if (tag.startsWith("~"))
            return posts.filter(p => p.title.toLowerCase().includes(tag.slice(1)));

        if (tag.endsWith("*"))
            return posts.filter(p => p.tags.some(t => t.startsWith(tag.slice(0, -1))));

         return posts.filter(p => p.tags.includes(tag))
    };


    $: displayedPosts = filterPosts(posts, selectedTag);



    const getPosts = () =>
        fetch(`${API_ROOT}/posts`)
        .then(r => r.json().then(j => { posts = j; }))
    ;

    const getPostContent = uid =>
        fetch(`${API_ROOT}/posts/${uid}/content`)
        .then(r => r.json()) // it's actually a JSON-encoded string, so it's fine
    ;

    const selectTag = ({detail: {tag}}) => {
        if (selectedTag === tag)
            selectedTag = "";
        else
            selectedTag = tag;
    };
</script>

<header>
    <h1 class="main-title">Welcome to my blog!</h1>
</header>
<main>
    <div class="search">
        Filter: <input type="text" bind:value={selectedTag}/><br/>
        <ul>
            <li>'python' searches for all posts tagged with 'python'</li>
            <li>'python*' searches for all posts tagged with 'python', 'python-short', 'pythons' etc.</li>
            <li>'^python' searches for all posts whose title starts with 'python'</li>
            <li>'~python' searches for all posts whose title contains 'python'</li>
        </ul>
    </div>
    <div class="posts">
        {#await getPosts()}
            Loading posts...
        {:then _}
            {#each displayedPosts as post (post.uid)}
                <PostCard
                    {post}
                    {getPostContent}
                    currentTagFilter={selectedTag}
                    on:tag-selected={selectTag}
                />
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