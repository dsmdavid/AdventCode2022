create or replace table TEST_DB.AOC2022.INPUT_2022_09 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__9.txt.gz') as t;
select * from TEST_DB.AOC2022.INPUT_2022_09;



/* part 1 */
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
       -- sample_input
        input_2022_09
),
helper_table as (
select row_number() over (order by null) as movement_step 
    from table(generator(ROWCOUNT => 20))
),
dirs as (
select 
    input,
    split(input,' ')[0]::varchar as dir,
    split(input,' ')[1]::number as distance,
    rn
from source),
instructions as (
select dirs.*, h.*, row_number() over (order by dirs.rn, h.movement_step) as single_step
from dirs
cross join helper_table as h 
where h.movement_step <= dirs.distance

),
knots as (
select row_number() over (order by null) as knot_id,
    0::number as ktx,
    0::number as kty,
    knot_id + 1 as next_knot_id
from table(generator(rowcount => 2))),
-- select * from instructions
-- where input = 'L 2';
-- move the head first for simplicity (no diagonals)
head as (
    select 
        'null' as input,
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
),
all_head as (
select * from head),
tail as (
    select
        'null'::varchar as dir,
        null::number as distance,
        -1::number as single_step,
        0::number as parent_ktx,
        0::number as parent_kty,
        0::number as parent_knot_id,
        False as need_moving,
        0::number as ktx,
        0::number as kty,
        1::number as knot_id
    
    union all 
    select 
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
    left join all_head as h
        on t.single_step + 1 = h.single_step
        and t.parent_knot_id = h.knot_id
    where t.knot_id is not null and h.knot_id is not null
)
select count(*), count(distinct ktx, kty) from tail; 