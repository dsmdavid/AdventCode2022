create or replace table TEST_DB.AOC2022.INPUT_2022_13 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__13.txt.gz') as t;

select * from TEST_DB.AOC2022.INPUT_2022_13;
/* so far, solves the part1 on the sample_input */
with sample_input_raw as (
    select $$[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
$$ as input
),
sample_input as (
select r.value::varchar as input, 'sample_input' as fn, r.index as rn from sample_input_raw as s,
lateral flatten(input => split(s.input, '\n')) as r),
source as (
    select *
    from 
        sample_input
        -- TEST_DB.AOC2022.INPUT_2022_12
),
pairs as (
select 
    parse_json(input) as array_,
    ceil((rn+1)/3) as group_,
    row_number() over (partition by group_ order by rn) as intra_pair
 from sample_input
 where input is not null and input != ''),
 pivoted as (
 select group_, p.$2 as left_, p.$3 as right_ from pairs
    pivot(min(array_) for intra_pair in (1,2)) as p
), 
rec_search as (

select 
group_, 
left_ as original_left_, left_, typeof(left_) as type_left_, coalesce(type_left_ = 'INTEGER',FALSE) as is_number_left_, coalesce(type_left_ = 'ARRAY',FALSE) as is_array_left_, type_left_ is null as is_null_left_, '0' as depth_left,
right_ as original_right_, right_, typeof(right_) as type_right_, coalesce(type_right_ = 'INTEGER',FALSE) as is_number_right_, coalesce(type_right_ = 'ARRAY',FALSE) as is_array_right_, type_right_ is null as is_null_right_, '0' as depth_left, 
0 as decision
from pivoted
where group_ = 1

)
select * from rec_search

