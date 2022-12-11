create or replace table TEST_DB.AOC2022.INPUT_2022_10 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__10.txt.gz') as t;

create or replace table TEST_DB.AOC2022.solved_2022_10 as with source as (
        select 'noop' as input, 0 as rn
        union all
        select input, rn from INPUT_2022_10
    ),
    helper_step as (
        select row_number() over (
                order by null
            ) as intra_step
        from table(generator(rowcount => 3))
    ),
    length_instruction as (
        select 'addx' as instruction, 2 as turns
        union all
        select 'noop' as instruction, 1 as turns
    ),
    instructions as (
        select split_part(input, ' ', 1) as instruction,
            try_to_number(split_part(input, ' ', 2)) as val,
            input,
            rn
        from source
    ),
    steps as (
        select i.input,
            i.instruction,
            i.val,
            i.rn,
            li.turns,
            h.intra_step,
            row_number() over (
                order by i.rn,
                    h.intra_step
            ) - 1 as single_step
        from instructions as i
            left join length_instruction as li on i.instruction = li.instruction
            left join helper_step as h on h.intra_step <= li.turns
    ),
    moves as (
        select *,
            case
                when single_step = 0 then 1
                when intra_step = turns then coalesce(val, 0)
                else 0
            end new_val,
            sum(new_val) over (
                order by single_step rows between unbounded preceding and current row
            ) as cum_sum
        from steps
    ),
    cycle_value as (
        select *,
            lag(cum_sum) over (
                order by single_step
            ) as signal_during_cycle,
            signal_during_cycle * single_step as strength,
            -- During cycle  1: CRT draws pixel in position 0
            mod(single_step - 1, 40) as pixel_position,
            case
                when (pixel_position - 1 <= signal_during_cycle)
                    and (signal_during_cycle <= pixel_position + 1) then '#'
                else '.'
            end as pixel,
            ceil(single_step / 40) as row_
        from moves
    ),
    partii as (
        select row_,
            listagg(pixel) as row_string
        from cycle_value
        where single_step != 0
        group by 1
        order by row_ asc
    )
select sum(strength)::varchar as answer,
    'part1' as part
from cycle_value
where single_step in (20, 60, 100, 140, 180, 220)
union all
select row_string as answer,
    'part2' as part
from partii;
select *
from solved_2022_10;
-- "ANSWER","PART"
-- "12880","part1"
-- "####..##....##..##..###....##.###..####.","part2"
-- "#....#..#....#.#..#.#..#....#.#..#.#....","part2"
-- "###..#.......#.#..#.#..#....#.#..#.###..","part2"
-- "#....#.......#.####.###.....#.###..#....","part2"
-- "#....#..#.#..#.#..#.#....#..#.#.#..#....","part2"
-- "#.....##...##..#..#.#.....##..#..#.####.","part2"