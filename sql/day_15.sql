create or replace table TEST_DB.AOC2022.INPUT_2022_15 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__15.txt.gz') as t;

select * from TEST_DB.AOC2022.INPUT_2022_15;
/* so far, solves the part1 on the sample_input */
with sample_input_raw as (
    select $$Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3$$ as input
),
sample_input as (
select r.value::varchar as input, 'sample_input' as fn, r.index as rn from sample_input_raw as s,
lateral flatten(input => split(s.input, '\n')) as r),
source as (
    select *
    from 
        -- sample_input
        TEST_DB.AOC2022.INPUT_2022_15
),
parse_loc as (
select 
    input,
    regexp_substr_all(input, '\\-?\\d+') as all_numbers,
    all_numbers[0]::int as s_x,
    all_numbers[1]::int as s_y,
    all_numbers[2]::int as b_x,
    all_numbers[3]::int as b_y,
    abs(s_x - b_x) + abs(s_y - b_y) as distance
from source
),
boundaries as (
    select 
        min(least(s_x, b_x, s_x - distance))::int as min_x,
        max(greatest(s_x, b_x, s_x + distance))::int as max_x,
        min(least(s_y, b_y, s_y - distance))::int as min_y,
        max(greatest(s_y, b_y, s_y + distance)) as max_y 

    from parse_loc
),
grid_x as (
    select min_x + row_number() over (order by null) -1 as p_x
    from boundaries, 
    table(generator(rowcount => 10000000))
    qualify p_x <= max_x
    -- where p_x <= max_x

),
grid_y as (
    select min_y + row_number() over (order by null) -1 as p_y
    from boundaries, 
    table(generator(rowcount => 10000000))
    qualify p_y <= max_y 
        -- and p_y = 10
    --    and p_y = 2000000
    -- where p_x <= max_x

),
sensors as (
    select distinct s_x, s_y, b_x, b_y, distance from parse_loc
),
selected_sensor as (
    select * from sensors
--    where s_y = 7 and s_x = 8
),
beacons as (
    select distinct b_x, b_y from parse_loc
),
target_row as (
    select 
        p_x,
        p_y,
        case when 
        -- this also caters for occupied
            abs(s.s_x - p_x) + abs(s.s_y - p_y) <= s.distance
            then -1 else 
            1 end as is_available
    
    from grid_x
    cross join grid_y
    cross join selected_sensor as s

),
points_available as (
select 
    p_x,
    p_y,
    min(is_available) as is_available
    from target_row
group by 1,2),
part_1_prep as (
select 
    p_x,
    p_y,
    case when b_x is not null then 0 else is_available end as is_available

from points_available
left join beacons
    on p_x = b_x
    and p_y = b_y
order by p_x),
filled as (
select 
    p.*,
    case 
         when s.s_x is not null then 'S'
         when p.is_available = 0 then 'B'
         when p.is_available < 1 then '#' 
    else 'o' end as point_
from part_1_prep as p 
left join sensors as s
    on s.s_x = p.p_x
    and s.s_y = p.p_y
order by p_y, p_x)
-- select p_y,
-- listagg(point_, '') within group (order by p_x) as string_
-- from filled
-- group by 1
-- order by p_y;
,
part1_ans as (
select p_y,
    count(*) as total_
from filled 
where point_ in ('#') --,'S', 'B')
group by 1
order by 1),
perimeters as (
    -- the single available point must be adjacent to the perimeter of at least 2
    -- sensors (otherwise they'd be more than 1 single point)

    -- how can we calculate the perimeter?

select 
    --s.s_x, s.s_y, s.distance, 
    p_x, p_y
from selected_sensor as s
left join grid_x as x
    on p_x <= s_x + distance + 1
    and p_x >= s_x - distance - 1
left join grid_y as y 
    on p_y <= s_y + distance + 1
    and p_y >= s_y - distance - 1
where 1 = 1
    and x.p_x >= 0 and x.p_x <= 4000000 --20
    and y.p_y >= 0 and y.p_y <= 4000000 --20
    and abs(s.s_x - x.p_x) + abs(s.s_y - y.p_y) = distance + 1

),
test_perimeter as (
select 
    p.p_x,
    p.p_y,
    case when abs(s.s_x - p.p_x) + abs(s.s_y - p.p_y) <= distance then -1 else 1 end as is_available
from perimeters as p 
cross join selected_sensor as s 
),
part2 as (
select 
    p_x,
    p_y,
    4000000 * p_x + p_y as tuning,
    min(is_available) as is_available
from test_perimeter

group by 1,2
having min(is_available) >0

order by 1,2)
select * from part2


;
select * from part1_ans;







/* 


,
outer_polygon as (
select st_makepolygon(
--   to_geography('LINESTRING(0.0 0.0, 0.000002 0.000002, 0.000002 0.000002, 0.0 0.000002, 0.0 0.0)')  
  to_geography('LINESTRING(0.0 0.0, 4 0.0, 4 4, 0.0 4, 0.0 0.0)')
  ) as polygon_
  ),
scaled_sensors as (
    select s_x / 1000000 as s_x,
    s_y / 1000000 as s_y,
    distance / 1000000 as distance 
from selected_sensor
),
sensor_polygons as (
select 
st_makepolygon(to_geography('LINESTRING(' || (s_x)::varchar|| ' ' || (s_y - distance)::varchar || ', ' 
              || (s_x - distance)::varchar || ' ' || (s_y)::varchar || ', ' 
              || (s_x)::varchar || ' ' || (s_y + distance)::varchar|| ', '
              || (s_x + distance)::varchar || ' ' || (s_y )::varchar|| ', '
              || (s_x)::varchar || ' ' || (s_y - distance)::varchar|| ')')) as polygon_sensor,
              row_number() over (order by null) as polygon_rn
from scaled_sensors
),
combined as (
    select st_collect(polygon_sensor) as all_sensors
    from sensor_polygons
),
free_ as (
select c.polygon_sensor,
    o.polygon_,
ST_DIFFERENCE(o.polygon_, c.polygon_sensor) as free_,
row_number() over (order by null) as rn
from sensor_polygons as c
cross join outer_polygon as o
),
-- test_rec as (
--     select rn, free_
--     from free_
--     where rn = 1

--     union all 
--     select f.rn, st_intersection(t.free_, f.free_)
--     from test_rec as t
--     left join free_ as f
--         on t.rn + 1 = f.rn 

--     where f.rn is not null and t.free_ is not null
-- )
-- test_rec as (
--     select 0 as rn, o.polygon_ as remaining_polygon, o.polygon_ as original_polygon
--     from outer_polygon as o

--     union all 
--     select f.polygon_rn, ST_DIFFERENCE(t.remaining_polygon, f.polygon_sensor), f.polygon_sensor
--     from test_rec as t
--     left join sensor_polygons as f
--         on t.rn + 1 = f.polygon_rn 

--     where f.polygon_rn is not null and t.remaining_polygon is not null
-- )
-- select * from sensor_polygons;
test_rec as (
    select polygon_rn as rn, polygon_sensor
    from sensor_polygons
    where rn = 1

    union all 
    select f.polygon_rn as rn, st_union(t.polygon_sensor, f.polygon_sensor)
    from test_rec as t
    left join sensor_polygons as f
        on t.rn + 1 = f.polygon_rn

    where f.polygon_rn is not null and t.polygon_sensor is not null
)
select * from test_rec
order by rn desc
limit 1
;

select polygon_ from outer_polygon;
select * from filled 
select p_x, p_y

    --, listagg(point_) within group (order by p_x)
    from filled
    where p_x >= 0 and p_x <= 20
    and p_y >= 0 and p_y <= 20
    and point_ = 'o'
        -- group by 1 
        -- order by 1

;

from points_available
;
where is_available = -1;
select * from grid_x
limit 100;

-- 7814712000000 too low
-- 7814715039646 too low
-- 6763814000009


/***/