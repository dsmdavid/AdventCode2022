-- create base file
-- create or replace table TEST_DB.AOC2022.INPUT_2022_08 as
-- select t.$1 as input,
--     metadata$filename as fn,
--     metadata$file_row_number as rn
-- from @stage_aoc (pattern => '.*2022__8.txt.gz') as t;
-- select * from TEST_DB.AOC2022.INPUT_2022_08;

create or replace table TEST_DB.AOC2022.solved_day_8 as with sample_values as (
                    select '30373' as input, 1 as rn
        union all   select '25512', 2
        union all   select '65332', 3
        union all   select '33549', 4
        union all   select '35390', 5
    ),
    source as (
        select *
        from input_2022_08 
            -- sample_values
    ),
    narrow as (
        -- split(regexp_replace(i.input, '.', ',\\0', 2), ',') as split_input,
        -- used for flattenning
        select i.rn,
            f.value::number as height,
            f.index + 1 as cn
        from source as i,
            lateral flatten(
                input => split(regexp_replace(i.input, '.', ',\\0', 2), ',')
            ) as f
    ),
    directions as (
                  select 'up' as dir
        union all select 'down'
        union all select 'left'
        union all select 'right'
    ),
    sample_ as (
        select narrow.*,
            directions.dir
        from narrow
            cross join directions 
            --where rn= 2 and cn =4
    ),
    rec as (
        select sample_.rn,
            sample_.cn,
            sample_.height,
            0 as ct,
            sample_.dir,
            sample_.rn as n_rn,
            sample_.cn as n_cn,
            1 as continue,
            0 as n_height
        from sample_
        union all
        select rec.rn,
            rec.cn,
            rec.height,
            rec.ct + 1 as ct,
            rec.dir,
            n.rn as n_rn,
            n.cn as n_cn,
            case
                when rec.height <= n.height then 0
                else 1
            end,
            n.height as n_height
        from rec
            inner join narrow as n on (
                case
                    when rec.dir = 'up' then rec.cn = n.cn and rec.n_rn - 1 = n.rn
                    when rec.dir = 'down' then rec.cn = n.c and rec.n_rn + 1 = n.rn
                    when rec.dir = 'left' then rec.n_cn - 1 = n.cn and rec.rn = n.rn
                    when rec.dir = 'right' then rec.n_cn + 1 = n.cn and rec.rn = n.rn
                end
            )
        where 1 = 1 
            and rec.continue = 1
    ),
    seen_by as (
        select n.rn,
            n.cn,
            n.height,
            min( case when rec.dir = 'up'       then rec.n_rn   end) as ups,
            max( case when rec.dir = 'down'     then rec.n_rn   end) as downs,
            min( case when rec.dir = 'left'     then rec.n_cn   end) as lefts,
            max( case when rec.dir = 'right'    then rec.n_cn   end) as rights,
            case
                when ups = 1 then 1
                when downs = (select max(rn)cfrom narrow) then 1
                when lefts = 1 then 1
                when rights = (select max(cn) from narrow) then 1
                else 0
            end as is_visible
        from sample_ as n
            left join rec on n.rn = rec.rn
            and n.cn = rec.cn
        where rec.continue = 1
        group by 1, 2, 3
    ),
    all_visibility as (
        select n.rn,
            n.cn,
            n.height,
            max(case when rec.dir = 'up'    then rec.ct end) as ups,
            max(case when rec.dir = 'down'  then rec.ct end) as downs,
            max(case when rec.dir = 'left'  then rec.ct end) as lefts,
            max(case when rec.dir = 'right' then rec.ct end) as rights,
            ups * downs * lefts * rights as visibility
        from sample_ as n
            left join rec on n.rn = rec.rn
            and n.cn = rec.cn
        group by 1, 2, 3
    )
select 'part1' as part,
    count(*) as answer
from seen_by
where is_visible = 1
union all
select 'part2' as part,
    max(visibility) as answer
from all_visibility;

select * from solved_day_8;
