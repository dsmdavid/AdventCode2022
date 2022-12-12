create or replace table TEST_DB.AOC2022.INPUT_2022_12 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__12.txt.gz') as t;

select * from TEST_DB.AOC2022.INPUT_2022_12;
/* so far, solves the part1 on the sample_input */
with sample_input_raw as (
    select $$Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi$$ as input
),
sample_input as (
select r.value::varchar as input, 'sample_input' as fn, r.index as rn from sample_input_raw as s,
lateral flatten(input => split(s.input, '\n')) as r),
source as (
    select * from 
        sample_input
        -- TEST_DB.AOC2022.INPUT_2022_12
),
layout as (
select 
    s.rn as row_,
    l.index + 1 as col_,
    array_construct(row_, col_) as tuple,
    case when l.value = 'S' then True else False end as start_,
    case when l.value = 'E' then True else False end as end_,
    case when l.value = 'S' then 'a' 
         when l.value = 'E' then 'z' 
         else l.value end as val,
    ascii(val) as val_number,
    (array_agg(case when start_ then tuple end)  over ())[0] as start_tuple,
    (array_agg(case when end_ then tuple end)  over ())[0] as end_tuple 

from source as s, 
    lateral flatten(input => split(regexp_replace(s.input, '.', ',\\0', 2), ',') ) as l 
),
next_ as (
    select v.$1 as plus_row, v.$2 as plus_col
from (values (-1,0),
             (1,0),
             (0,-1),
             (0,1)
) as v
),
layout_next as (
    -- I had this inside the recursive, snowflake didn't like it
    select *
    from layout
    cross join next_
)
--select count(*) from layout_next;
,
solver as (
    select 
        row_,   col_,   tuple,  end_,   val,    val_number, end_tuple, array_construct(tuple) as path_, row_ + plus_row as next_row, col_+ plus_col as next_col
        from layout_next as l
        where l.start_
    union all 
    select 
        l.row_, l.col_, l.tuple, l.end_, l.val, l.val_number, l.end_tuple, array_append(s.path_, l.tuple) as path_, l.row_ + l.plus_row as next_row, l.col_+l.plus_col as next_col
    from solver as s 
    left join layout_next as l ON s.next_row = l.row_ and s.next_col = l.col_ 
    where 
        s.val_number + 1 >= l.val_number
    and l.val is not null 
    and not array_contains(l.tuple, s.path_)
    and not s.end_
    and array_size(s.path_) < 400
)
select min(array_size(path_) - 1) as answer, 'part1' as part from solver
where solver.end_
order by 1 asc
-- ;
-- Processing aborted due to error 300002:2328349570; incident 4029033.
-- Processing aborted due to error 300002:2328349570; incident 2727370.
