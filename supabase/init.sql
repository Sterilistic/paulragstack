-- Enable the pgvector extension
create extension vector;

-- Create the essays table
create table essays (
    id bigint primary key generated always as identity,
    title text not null,
    url text not null,
    content text not null,
    embedding vector(384),
    scraped_at timestamp with time zone
);

-- Create a function for similarity search
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
        1 - (essays.embedding <=> query_embedding) as similarity
    from essays
    where 1 - (essays.embedding <=> query_embedding) > match_threshold
    order by essays.embedding <=> query_embedding
    limit match_count;
end;
$$; 