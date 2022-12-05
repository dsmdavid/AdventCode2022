-- create or replace table TEST_DB.AOC2022.INPUT_2022_05 as 
-- select  
--     t.$1 as input,
--     metadata$filename as fn,
--     metadata$file_row_number as rn
-- from @stage_aoc
-- (pattern => '.*2022__5.txt.gz')
-- as t;
-- select * from  TEST_DB.AOC2022.INPUT_2022_05;
--create view test_db.aoc2022.solved_day_5 as 
create view test_db.AOC2022.temp_instructions_25 as 
with source as (
    select *
    from TEST_DB.AOC2022.INPUT_2022_05
),
instructions as (
    select
        regexp_substr_all(input, '[[:digit:]]+') as vals,
        vals[0]::int as quantity,
        vals[1]::int as from_,
        vals[2]::int as to_,
        row_number() over (order by null) as step
    from source where rn >= 11
)
select 
    step,
    quantity,
    from_,
    to_
from instructions;

create or replace view test_db.AOC2022.temp_starting_25 as 
with source as (
    select *
    from TEST_DB.AOC2022.INPUT_2022_05
),
matrix as (
    select input
    from source where rn < 9
),
basic_columns as (
    select 
        regexp_substr_all(input, '....') as vals,
        replace(replace(replace(vals[0], ' ',''),']',''),'[','') as c1,
        replace(replace(replace(vals[1], ' ',''),']',''),'[','') as c2,
        replace(replace(replace(vals[2], ' ',''),']',''),'[','') as c3,
        replace(replace(replace(vals[3], ' ',''),']',''),'[','') as c4,
        replace(replace(replace(vals[4], ' ',''),']',''),'[','') as c5,
        replace(replace(replace(vals[5], ' ',''),']',''),'[','') as c6,
        replace(replace(replace(vals[6], ' ',''),']',''),'[','') as c7,
        replace(replace(replace(vals[7], ' ',''),']',''),'[','') as c8,
        replace(replace(replace(input, array_to_string(vals, ''), ''),']',''),'[','') as c9,
        input
from matrix
),
columns as (
select 
    listagg(c1,'') as c1,
    listagg(c2,'') as c2,
    listagg(c3,'') as c3,
    listagg(c4,'') as c4,
    listagg(c5,'') as c5,
    listagg(c6,'') as c6,
    listagg(c7,'') as c7,
    listagg(c8,'') as c8,
    listagg(c9,'') as c9

from basic_columns),
starting_columns as (
    select 
        row_number() over (order by null) as col_,
        replace(reverse(input),' ','') as input
    from columns
         unpivot(input for col in (c1,c2,c3,c4,c5,c6,c7,c8,c9))
)
-- select * from starting_columns

select * from starting_columns;

create or replace procedure solver_aoc5_part(PART integer)
returns table (solution varchar)
language SQL
as
declare
    iteration integer default 0;
    total_iterations integer;
    query varchar default 'update temp_iteration_25 as t
    set input = m.input
    from (
    with instructions as (
select * from temp_instructions_25
where step = ?),
starting as (
select 
    col_,
    input as input
from temp_iteration_25),
from_ as (
    select 
        col_,
        length(input) as lin,
        substring(s.input, length(input) - i.quantity + 1, i.quantity) as           transit,
        substring(s.input,1, length(input) - i.quantity ) as input
    from starting as s
    left join instructions as i
        on s.col_ = i.from_
    where i.step is not null 
),
to_ as (
    select
        t.lin,
        i.quantity,
        t.transit,
        s.col_,
        s.input || case when ?=2 then t.transit else reverse(t.transit) end as input
    from starting as s
    left join instructions as i
        on s.col_ = i.to_
    left join from_ as t
        on t.col_ = i.from_
    where i.step is not null 
)
select col_, input from from_
union all 
select col_, input from to_) as m
where t.col_ = m.col_';
--    log_query varchar default 'create or replace table temp_log_25 as select * from temp_instructions_25 where step = ?';
    solution_query varchar default $$with solution_ as (
select input, right(input,1) as letter
from temp_iteration_25
    order by col_
)
select listagg(letter, '') as solution from solution_$$;
    res resultset;
    
begin
    execute immediate 'create or replace table temp_iteration_25 as select * from temp_starting_25';
    select max(step) into :total_iterations from temp_instructions_25;
    for i in 1 to total_iterations do
        iteration := iteration + 1;
        execute immediate :query using (iteration, PART);
        execute immediate :log_query using (iteration);

  end for;
res := (execute immediate :solution_query);
return table(res);
end;