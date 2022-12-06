create or replace table TEST_DB.AOC2022.INPUT_2022_06 as
select t.$1 as input,
    metadata $filename as fn,
    metadata $file_row_number as rn
from @stage_aoc (pattern => '.*2022__6.txt.gz') as t;

-- create a long table with one character per row
-- "LETTER","RN","NEXT","PREV"
-- "c",1,2,0
-- "d",2,3,1
-- ...
create or replace table test_db.aoc2022.temp_base_06 as with source as (
        select *
        from TEST_DB.AOC2022.INPUT_2022_06
    ),
    -- create positions as long as the input 
    -- select max(length(input)) from source --> needed rowcount
    positions as (
        select row_number() over (
                order by null
            ) as rn
        from table(generator(ROWCOUNT => 4095))
    ),
    -- extracts one character per row
    prepare as (
        select substr(s.input, p.rn, 1) as letter,
            p.rn,
            p.rn + 1 as next
        from source as s
            cross join positions as p
    )
select *
from prepare
order by rn;

create or replace view test_db.aoc2022.solved_day_6 as 
with recursive signal (letter, rn, next, level) as (
    select letter,
        rn,
        next,
        1 as level
    from temp_base_06
    union allß
    select b.letter || n.letter,
        n.rn,
        n.next,
        b.level + 1 as level
    from signal as b
        left join temp_base_06 as n on b.next = n.rn
    where level <= 14
        -- letter does not exist in previous string
        and charindex(n.letter,b.letter) = 0
),
part_1 as (
    select 'part1' as part,
        min(rn) as answer
    from signal
    where level = 4
),
part_2 as (
    select 'part1' as part,
        min(rn) as answer
    from signal
    where level = 14
)
select *
from part_1
union all
select *
from part_2;

select * from test_db.aoc2022.solved_day_6;