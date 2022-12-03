-- create or replace table TEST_DB.AOC2022.INPUT_2022_03 as 
-- select  
--     t.$1 as input,
--     metadata$filename as fn,
--     metadata$file_row_number as rn
-- from @stage_aoc
-- (pattern => '.*2022__3.txt.gz')
-- as t;
create view test_db.aoc2022.solved_day_3 as 
with source as (
    select *
    from TEST_DB.AOC2022.INPUT_2022_03
),
sample_input as (
    select v.$1 as input,
        row_number() over (
            order by null
        ) as rn
    from
    values ('vJrwpWtwJgWrhcsFMMfFFhFp'),
        ('jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL'),
        ('PmmdzqPrVvPwwTWBwg'),
        ('wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn'),
        ('ttgJtRGJQctTZtZT'),
        ('CrZsJsPPZsGzwwsLwLmpwMDw') 
        as v
),
input as (
    select input,
        rn
    from --sample_input 
        source
),
priorities as (
    select substr(input, 1, length(input) / 2) as container_first,
        substr(input, length(input) / 2 + 1) as container_second,
        substr(
            regexp_replace(
                container_first,
                concat('[^', container_second, ']'),
                ''
            ),
            1,
            1
        ) as common,
        ascii(common) as ascii_val,
        case
            when ascii_val >= 97 then ascii_val - 96
            else ascii_val - 64 + 26
        end as priority,
        ceil(div0(rn, 3)) as groups,
        lead(input) over (
            partition by groups
            order by rn
        ) as l_input,
        lead(input, 2) over (
            partition by groups
            order by rn
        ) as l_input_b,
        substr(
            regexp_replace(
                regexp_replace(
                    input,
                    concat('[^', l_input, ']'),
                    ''
                ),
                concat('[^', l_input_b, ']'),
                ''
            ),
            1,
            1
        ) as common_group,
        ascii(common_group) as ascii_val_group,
        case
            when ascii_val_group >= 97 then ascii_val_group - 96
            else ascii_val_group - 64 + 26
        end as priority_group,
        *
    from input
)
select sum(priority) as part1,
    sum(priority_group) as part2
from priorities