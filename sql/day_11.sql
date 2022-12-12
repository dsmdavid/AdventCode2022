create or replace table TEST_DB.AOC2022.INPUT_2022_11 as
select t.$1 as input,
    metadata$filename as fn,
    metadata$file_row_number as rn
from @stage_aoc (pattern => '.*2022__11.txt.gz') as t;

/* close, but no bananas */ 
-- the below code is WIP and not working

create or replace table temp_initial_items_11 as
with source as (
    select input, rn from INPUT_2022_11
    union all
    select null, (select max(rn) from INPUT_2022_11) + 1
),
parsed as (
select *, 
    regexp_substr_all(input, '\\d+') as vals,
    case when input ilike 'monkey%' then vals[0]::number end as monkey,
    case when input ilike '%starting%' then vals end as items,
    case when input ilike '%operation%' then regexp_substr(input, '\\*|\\+') end as operator,
    case when input ilike '%operation%' then vals[0] end as operation,
    case when input ilike '%test%' then vals[0]::number end as divisible_by,
    case when input ilike '%if true%' then vals[0]::number end as monkey_if_true,
    case when input ilike '%if false%' then vals[0]::number end as monkey_if_false
from source),
monkey_def as (
select rn - 7 as group_monkey from source
where input is null
),
monkey_ass as (
    select
    source.rn,
    max(md.group_monkey) as group_monkey
from source
    left join monkey_def as md
    on md.group_monkey <= source.rn   
    group by 1
)
-- select * from monkey_ass
-- order by rn;
,
tabular as (
select
    ma.group_monkey,
    min(monkey) as monkey,
    array_agg(items)[0] as items,
    min(operator) as operator,
    case when min(operation) is null then 'old' else min(operation) end as operation_value,
    min(divisible_by) as divisible_by,
    min(monkey_if_true) as monkey_if_true,
    min(monkey_if_false) as monkey_if_false
from parsed
left join monkey_ass as ma
    on ma.rn = parsed.rn
group by ma.group_monkey
order by monkey),
stats as (
    select count(*) as n_monkeys,
        pow(10,sum(log(10,divisible_by)))::int as lcm
    from tabular
),
items as (
    select 
        t.monkey as current_monkey,
        it.value::number(38,0) as item,
        0 as current_round
    from tabular as t,lateral flatten(input => t.items) as it
),
cross_joined as (
    select * exclude (items, group_monkey) from tabular
    cross join stats
)
-- select * from items;
-- select * from temp_initial_items_11;
,
rec_round as (
    select 
        item::number(38,0) as item,
        current_monkey,
        0 as next_monkey,
        1 as next_round
    from items

    UNION ALL
    
    select 
        case when rr.current_monkey = rr.next_monkey then 
            (case 
                when cj.operation_value = 'old' then rr.item * rr.item
                when cj.operator = '*' then rr.item * cj.operation_value
                when cj.operator = '+' then rr.item + cj.operation_value
            end) % cj.lcm 
            else rr.item end
            as 
            mod_item,
        case when rr.current_monkey != rr.next_monkey then rr.current_monkey
            else 
                case when mod_item % cj.divisible_by = 0 then cj.monkey_if_true
                else cj.monkey_if_false end
            end as        current_monkey,
        ((rr.next_monkey +1) % cj.n_monkeys) as mod_next_monkey,
        case when mod_next_monkey = 0 then rr.next_round + 1 else rr.next_round end as next_round
    
    from rec_round as rr
    left join cross_joined as cj 
        on rr.current_monkey = cj.monkey
    where rr.next_round <=10001
    
)

, summary as (
    select next_monkey, count(*) as inspected
    from rec_round
    where next_monkey = current_monkey and next_round <= 10001
    group by 1
)
select *
from monkey_business
order by inspected desc;
-- select (120024 * 120022)::number(38,0); 
-- 14399759920
-- 18085004878 -- true
-- 14405520528
