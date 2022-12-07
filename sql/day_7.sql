-- create base file
create or replace table TEST_DB.AOC2022.INPUT_2022_07 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__7.txt.gz') as t;

-- create the instructions and step assignment as separate tables to remove
-- a bit of clutter from the main solution
create or replace table test_db.aoc2022.temp_instructions_07 as with paths as (
        select *,
            case
                when substring(input, 1, 4) = '$ cd' then substring(input, 6, len(input))
                else null
            end as path
        from test_db.aoc2022.input_2022_07
    ),
    instructions as (
        select *,
            row_number() over (
                order by rn
            ) as step,
            step + 1 as next_step
        from paths
        where path is not null
    )
select *
from instructions
order by step;

create or replace table temp_instructions_assigned_07 as with temp as (
        select t.input,
            t.rn,
            case
                when substr(t.input, 1, 3) != 'dir' then regexp_replace(t.input, '([\\d\\s]+)')
                else ''
            end as filename,
            try_to_number(regexp_replace(t.input, '(\\D+)')) as size,
            min(i.step) as step
        from input_2022_07 as t
            left join temp_instructions_07 as i on t.rn = i.rn -- where substr(t.input,1,1) != '$'
        group by 1,
            2
    )
select t.input,
    t.rn,
    t.filename,
    t.size,
    coalesce(
        lag(t.step) ignore nulls over (
            order by t.rn
        ),
        t.step
    ) as step
from temp as t;

-- have fun with the main solution...
create or replace view test_db.aoc2022.solved_day_7 as with recursive current_path (
        path,
        rn,
        step,
        next_step,
        level,
        cur_path,
        cur_path_string,
        visited
    ) as (
        select ''::varchar(1000) as path,
            0::number(38, 0) as rn,
            0::number(38, 0) as step,
            1::number(38, 0) as next_step,
            0::number(38, 0) as level,
            ''::varchar(1000) as cur_path,
            ''::varchar(1000) as cur_path_string,
            1::number(38, 0) as visited
        union all
        select t.path,
            t.rn,
            t.step,
            t.next_step,
            case
                when t.path = '..' then c.level - 1
                else c.level + 1
            end as level,
            case
                when t.path = '..' then regexp_replace(c.cur_path, '^(.*)\\|[^\\|]*$', '\\1')
                else c.cur_path || '|' || c.level::string
            end as cur_path,
            case
                when t.path = '..' then regexp_replace(c.cur_path_string, '^(.*)\\|[^\\|]*$', '\\1')
                else c.cur_path_string || '|' || t.path
            end as cur_path,
            1 as visited
        from temp_instructions_07 as t
            inner join current_path as c on t.step = c.next_step
        where 1 = 1 -- c.visited != 1 
            and t.step <= 365
    ),
    occur_levels as (
        select c.*,
            row_number() over (
                partition by c.level
                order by c.rn
            ) as level_ocurrence
        from current_path as c 
        order by rn
    ),
    file_assigned as (
        select ol.path::varchar(1000) as path,
            ol.rn::number(38, 0) as rn,
            ol.step::number(38, 0) as step,
            ol.level::number(38, 0) as level,
            ol.cur_path,
            ol.cur_path_string,
            ol.level_ocurrence::number(38, 0) as level_ocurrence,
            sum(try_to_number(ia.size)::int) as size
        from input_2022_07 as inp
            left join temp_instructions_assigned_07 as ia on ia.rn = inp.rn
            left join occur_levels as ol --;
            on ol.step::number = ia.step::number
        group by 1,
            2,
            3,
            4,
            5,
            6,
            7
        order by rn
    ),
    -- create the paths as objects for flattening.
    -- should have thought of this a lot earlier
    paths as (
        select *,
            regexp_substr_all(cur_path, '(\\d+)') as numeric_path,
            regexp_substr_all(cur_path_string, '[a-z]+') as string_path
        from file_assigned
    ),
    -- flatten, and extract the path_level, ready for pivot
    path_level as (
        select paths.*,
            f.value::number as path_value,
            string_path [f.value::number-1]::varchar as path_level_str
        from paths,
            lateral flatten(input => numeric_path) as f
    ),
    -- go wide! 
    -- luckily, only 10 level-deep paths were found!
    pivoted as (
        select *
        from path_level pivot(
                min(path_level_str) for path_value in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
            )
        order by rn
    ),
    -- loving the group by rollup
    sizes as (
        select "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            sum(size) as size,
            min(rn) as initial_rn
        from pivoted
        group by rollup ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
        order by initial_rn
    ),
    final as (
        select "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            max(size) as size
        from sizes
        group by 1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11
    ),
    part1_prep as (
        select sum(size) as total_size_in_use,
            70000000 as total_space,
            30000000 as space_needed,
            total_space - total_size_in_use as free_space,
            space_needed - free_space as diff_needed
        from final
        where "1" is null
    )
select min(t.size) as answer,
    'part2' as part
from final as t
    cross join part1_prep
where t.size > diff_needed
union all
select sum(t.size) as answer,
    'part1' as part
from final as t
where t.size <= 100000;
select *
from solved_day_7;