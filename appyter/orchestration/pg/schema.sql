create extension if not exists "uuid-ossp";
create schema if not exists pgq;
create table if not exists pgq.task (
  id uuid default uuid_generate_v4(),
  channel varchar,
  job jsonb,
  queued timestamp default now(),
  started timestamp,
  completed timestamp
);
create view pgq.queue as
with
  queue as (
    select *
    from pgq.task
    where started is null
  ),
  pqueue as (
    select queue.*, row_number() over (
      partition by channel
      order by created asc
    ) as position
    from queue
  )
select *
from pqueue
order by position asc, created asc;

create function pgq.task_position(id uuid) returns number
as $$
  select queue.position
  from pgq.queue
  where queue.id = task_position.id;
$$ language sql strict immutable;
create function pgq.put(channel varchar, job jsonb) returns row (
  id uuid,
  position bigint
) as $$
  with current_task as (
    insert into pgq.task (channel, job)
    values (put.channel, put.job)
    returning *
  ), task_notify as (
    select pg_notify('pgq', current_task.channel || ' ' || current_task.id::text || ' ' || 'put')
    from current_task
  ) select current_task.id, pgq.task_position(current_task.id) as position
  from current_task;
$$ language sql strict;
create function pgq.take(id uuid) returns row (
  id uuid,
  job jsonb
) as $$
  with current_task as (
    select *
    from pgq.task
    where task.id = take.id
  ), task_update as (
    update pgq.task
    set started = now()
    where task.id = take.id
  ), notify as (
    select pg_notify('pgq', current_task.channel || ' ' current_task.id::text || ' ' || 'pop')
    from current_task
  ) select current_task.id, current_task.job
  from current_task;
$$ language sql;
create function pgq.pop() returns row (
  id uuid,
  job jsonb
) as $$
  select pgq.take(select id from pgq.queue limit 1);
$$ language sql;
create function pgq.task_done(id uuid) returns void
as $$
  with current_task as (
    select *
    from pgq.task
    where task.id = task_done.id
  ), update as (
    update pgq.task
    set completed = now()
    where task.id = task_done.id
  ), notify as (
    select pg_notify('pgq', current_task.channel || ' ' || current_task.id::text || ' task_done')
    from current_task
  ) select null;
$$ language sql strict;
create function pgq.requeue(id uuid) returns void
as $$
  with current_task as (
    select *
    from pgq.task
    where task.id = requeue.id
  ), update as (
    update pgq.task
    set started = null, completed = null
    where task.id = requeue.id
  ), notify as (
    select pg_notify('pgq', current_task.channel || ' ' requeue.id::text || ' put')
    from current_task
  ) select null;
$$ language sql strict;