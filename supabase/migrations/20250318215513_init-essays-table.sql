-- 1. Enable vector extension
create extension vector;

-- 2. Create table structure
create table essays (
    id bigint primary key generated always as identity,
    title text not null,
    url text not null,
    content text not null,
    embedding vector(384),  -- Store 384-dimensional vectors
    scraped_at timestamp with time zone
);

-- 3. Similarity search function
create or replace function match_essays (
    query_embedding vector(384),
    match_threshold float,
    match_count int
)
returns table (
    id bigint,
    title text,
    url text,
    content text,
    similarity float
)
language plpgsql
as $$
begin
    return query
    select
        essays.id,
        essays.title,
        essays.url,
        essays.content,
        1 - (essays.embedding <=> query_embedding) as similarity  -- Cosine distance
    from essays
    where 1 - (essays.embedding <=> query_embedding) > match_threshold
    order by essays.embedding <=> query_embedding  -- Order by similarity
    limit match_count;
end;
$$; 