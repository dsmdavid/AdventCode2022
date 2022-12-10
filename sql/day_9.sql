create or replace table TEST_DB.AOC2022.INPUT_2022_09 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__9.txt.gz') as t;
select * from TEST_DB.AOC2022.INPUT_2022_09;

/* parts i & ii with stored procedures */


create or replace procedure solver_aoc9()
returns table (part varchar, answer number)
language SQL 
as 
declare
    res resultset;
    query_output varchar default 'with source as (select * from temp_head_09),
    outputs as (
    select knot_id, count(distinct ktx,kty) as ct from source group by 1)
    select
        case when knot_id = 1 then \'part1\'
            when knot_id = 9 then \'part2\' 
            end as part,
            ct as answer
    from outputs where knot_id = 1 or knot_id = 9';
begin
    drop table if exists temp_head_09;
    call create_head_table_aoc9();
    call iterator_aoc9_part();
    res := (execute immediate :query_output);
    return table(res);
end;

create or replace procedure create_head_table_aoc9()
returns table (status varchar)
language SQL 
as 
declare
    res resultset;
    query varchar default $$ create or replace table temp_head_09 as 
with sample_input as (
    select 'R 4' as input, 1 as rn
    union all select 'U 4',2
    union all select 'L 3',3
    union all select 'D 1',4
    union all select 'R 4',5
    union all select 'D 1',6
    union all select 'L 5',7
    union all select 'R 2',8
),    
    source as (
    select * from 
        --  sample_input
         input_2022_09
),
helper_table as (
select row_number() over (order by null) as movement_step 
    from table(generator(ROWCOUNT => 20))
),
dirs as (
select 
    input::varchar(10) as input,
    split(input,' ')[0]::varchar as dir,
    split(input,' ')[1]::number as distance,
    rn
from source),
prep_instructions as (
select dirs.*, h.*, row_number() over (order by dirs.rn, h.movement_step) as single_step
from dirs
cross join helper_table as h 
where h.movement_step <= dirs.distance
),
dummy_last_instruction as (
    select 'last 0' as input, 'x' as dir, 0 as distance, 0 as rn, 0 as movement_step, (select max(single_step) from prep_instructions) +1 as single_step
),
instructions as (
    select * from prep_instructions
    union all 
    select * from dummy_last_instruction
),
knots_obj as (    
select row_number() over (order by null) as rn, object_construct('x',0,'y',0) as obj
from table(generator(rowcount =>10))),
knots as (
select object_agg(rn::varchar, obj) as knots_obj from knots_obj),
-- move the head first for simplicity (no diagonals)
head as (
    select 
        'null'::varchar(10) as input,
        'null' as dir,
        0::number as distance,
        0::number as single_step, 
        0::number as ktx, 
        0::number as kty, 
        0::number as knot_id
    union all 
    select 
        i.input,
        i.dir,
        i.distance,
        i.single_step,
        case when i.dir = 'R' then h.ktx + 1
             when i.dir = 'L' then h.ktx - 1
        else h.ktx end as ktx,
        case when i.dir = 'U' then h.kty + 1
             when i.dir = 'D' then h.kty -1
        else h.kty end as kty,
        h.knot_id
    from head as h
    left join instructions as i
        on h.single_step + 1 = i.single_step
    where i.input is not null
)
select * from head $$;
begin
    res := (execute immediate :query);
    return table(res);
end;

create or replace procedure iterator_aoc9_part()
returns varchar
language SQL
as
declare
    iteration integer default 0;
    total_iterations integer default 9;
    query varchar default $$
        insert into temp_head_09  
        with head as (
        select * from temp_head_09
        where knot_id = (select max(knot_id) from temp_head_09)),
        tail as (
            select
                null::varchar as input,
                null::varchar as dir,
                null::number as distance,
                -1::number as single_step,
                0::number as parent_ktx,
                0::number as parent_kty,
                (select max(knot_id) from head) as parent_knot_id,
                False as need_moving,
                0::number as ktx,
                0::number as kty,
                (select max(knot_id) from head) + 1 as knot_id
            
            union all 
            select 
                h.input,
                h.dir,
                h.distance,
                h.single_step,
                h.ktx as parent_ktx,
                h.kty as parent_kty,
                h.knot_id as parent_knot_id,
                case when power(h.ktx - t.ktx,2) + power(h.kty - t.kty,2) <= 2 then
                    false else true end as need_moving,
                case when (power(h.ktx - t.ktx,2) + power(h.kty - t.kty,2)) <= 2 then t.ktx 
                else 
                    case 
                        when h.ktx > t.ktx then t.ktx + 1
                        when h.ktx < t.ktx then t.ktx - 1
                        else t.ktx
                    end 
                end as ktx,
                case when (power(h.ktx - t.ktx,2) + power(h.kty - t.kty,2)) <= 2 then t.kty
                else
                    case 
                        when h.kty > t.kty then t.kty + 1
                        when h.kty < t.kty then t.kty - 1
                        else t.kty
                    end 
                end as kty,
                t.knot_id
            from tail as t
            left join head as h
                on t.single_step + 1 = h.single_step
                and t.parent_knot_id = h.knot_id
            where t.knot_id is not null and h.knot_id is not null
        )
        select input, dir, distance, single_step, ktx, kty, knot_id
        from tail $$;
    res resultset;
    
begin
    for i in 1 to total_iterations do
        iteration := iteration + 1;
        execute immediate :query;
  end for;
return 'End iteration run';
end;

call solver_aoc9();
