create view test_db.aoc2022.solved_day_2 as 
with source as (
    select *
    from TEST_DB.AOC2022.INPUT_2022_02
),
shapes as (
    select val.$1 as input_,
        val.$2 as shape
    from (
            values ('A', 'rock'),
                ('B', 'paper'),
                ('C', 'scissors'),
                ('X', 'rock'),
                ('Y', 'paper'),
                ('Z', 'scissors')
        ) as val
),
shape_scores as (
    select val.$1 as shape,
        val.$2 as score
    from (
            values ('rock', 1),
                ('paper', 2),
                ('scissors', 3)
        ) as val
),
event_score as (
    select val.$1 as event,
        val.$2 as score
    from (
            values ('win', 6),
                ('tie', 3),
                ('lose', 0)
        ) as val
),
winners as (
    select val.$1 as win,
        val.$2 as lose
    from (
            values ('rock', 'scissors'),
                ('paper', 'rock'),
                ('scissors', 'paper')
        ) as val
),
decoded as (
    select *,
        split(input, ' ') [0]::varchar as player1,
        split(input, ' ') [1]::varchar as player2
    from source
),
outcomes as (
    select d.*,
        s1.shape as p1_shape,
        s2.shape as p2_shape,
        ss1.score as p1_ss_score,
        ss2.score as p2_ss_score,
        case
            when p1_shape = p2_shape then 'tie'
            when w1.win is null then 'lose'
            else 'win'
        end as outcome_p1,
        case
            when p1_shape = p2_shape then 'tie'
            when w2.win is null then 'lose'
            else 'win'
        end as outcome_p2 -- ,
        -- se1.score as p1_se_score,
        -- se2.score as p2_se_score
    from decoded as d
        left join shapes as s1 on player1 = s1.input_
        left join shapes as s2 on player2 = s2.input_
        left join shape_scores as ss1 on s1.shape = ss1.shape
        left join shape_scores as ss2 on s2.shape = ss2.shape
        left join winners as w1 on s1.shape = w1.win
        and s2.shape = w1.lose
        left join winners as w2 on s2.shape = w2.win
        and s1.shape = w2.lose
),
scores as (
    select o.*,
        se1.score as p1_se_score,
        se2.score as p2_se_score,
        p1_ss_score + p1_se_score as p1_total_score,
        p2_ss_score + p2_se_score as p2_total_score
    from outcomes as o
        left join event_score as se1 on o.outcome_p1 = se1.event
        left join event_score as se2 on o.outcome_p2 = se2.event
),
part1 as (
    select sum(p1_total_score),
        sum(p2_total_score)
    from scores
),
final as (
    select *
    from part1
)
select *
from final