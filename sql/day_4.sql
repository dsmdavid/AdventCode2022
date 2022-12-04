-- create or replace table TEST_DB.AOC2022.INPUT_2022_04 as 
-- select  
--     t.$1 as input,
--     metadata$filename as fn,
--     metadata$file_row_number as rn
-- from @stage_aoc
-- (pattern => '.*2022__4.txt.gz')
-- as t;
create view test_db.aoc2022.solved_day_4 as 
with source as (
    select *
    from TEST_DB.AOC2022.INPUT_2022_04
),
temp as (
    select 
        regexp_substr_all(input, '[[:digit:]]+') as vals,
        vals[0]::int as a1,
        vals[1]::int as a2,
        vals[2]::int as b1,
        vals[3]::int as b2,
        -- regexp_substr(input,'(\\d+)-(\\d+),(\\d+)-(\\d+)',1,1,'e',1)::int as a1,
        -- regexp_substr(input,'(\\d+)-(\\d+),(\\d+)-(\\d+)',1,1,'e',2)::int as a2,
        -- regexp_substr(input,'(\\d+)-(\\d+),(\\d+)-(\\d+)',1,1,'e',3)::int as b1,
        -- regexp_substr(input,'(\\d+)-(\\d+),(\\d+)-(\\d+)',1,1,'e',4)::int as b2,
        least(a1, a2) as min_a,
        greatest(a1, a2) as max_a,
        least(b1, b2) as min_b,
        greatest(b1, b2) as max_b,
        case
            when min_a >= min_b and max_a <= max_b then true
            when min_b >= min_a and max_b <= max_a then true
            else false
        end as is_contained,
        case
            when min_a <= min_b and max_a >= min_b then true
            when min_a > min_b and max_a < max_b then true
            when min_b <= min_a and max_b >= min_a then true
            when min_b > min_a and max_b < max_a then true
            else false
        end as has_overlap,
        input
    from source
)
select sum(is_contained::number) as part1,
    sum(has_overlap::number) as part2
from temp