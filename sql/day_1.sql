with source as (
    select *
    from TEST_DB.AOC2022.INPUT_2022_01
),
-- create elve_id:
groups as (
    select cal,
        filename,
        file_row_number,
        row_number() over (
            order by file_row_number
        ) as elve_id
    from source
    where cal is null
),
-- assign elve_id:
carrying as (
    select i.cal,
        i.file_row_number,
        min(groups.elve_id) as elf
    from source as i
        left join groups on i.file_row_number < groups.file_row_number
    where i.cal is not null
    group by 1,
        2
    order by i.file_row_number asc
),
-- compute
top_3 as (
    select sum(cal::number) as total_calories
    from carrying
    group by elf
    order by total_calories desc
    limit 3
)
select sum(total_calories) as answer,
    'part_2' as part
from top_3
union all
select max(total_calories) as answer,
    'part_1' as part
from top_3