import sqlite3

create_view = """
CREATE VIEW policy_lifecycle as
with dates as (select distinct(year_month) from calendar),
    users as (select distinct(user_id) from policy),
    users_active as (select u.user_id, date(policy_start_date) active_date from users u left join policy p on u.user_id = p.user_id
                     UNION
                     select u.user_id, date(policy_end_date) active_date from users u left join policy p on u.user_id = p.user_id),
    users_active_month as (select users_active.*, calendar.year_month active_date_month
                           from users_active left join calendar on users_active.active_date = calendar.date),
    base_dates_table as (select *,
                         case WHEN ua.active_date_month = d.year_month THEN 1 else 0 end current,
                         MIN(active_date_month) OVER (PARTITION BY ua.user_id) as start_month
                         from dates d left join users_active_month ua on d.year_month >= ua.active_date_month),
    dates_table_filter as (select *, ROW_NUMBER () over ( partition by user_id, year_month order by current desc, active_date desc) row_num from base_dates_table),
    dates_table_filtered as (select * from dates_table_filter where row_num = 1)
    select year_month, user_id, start_month active_from_month
        ,case
            when active_date_month = year_month AND start_month = year_month
                then 'new'
            when active_date_month = year_month AND start_month <> year_month
                then 'active'
            when cast(round(
                            (julianday(date(year_month || '-01')) - julianday(date(active_date_month || '-01')) ) / 30) as integer) = 1
                then 'churned'
            when cast( round( (julianday(date(year_month || '-01')) - julianday(date(active_date_month || '-01')) ) / 30) as integer) > 1
                then 'lapsed'
            end user_lifecycle_status
        ,case
            when cast( round( (julianday(date(year_month || '-01')) - julianday(date(active_date_month || '-01')) ) / 30) as integer) = 0
                then NULL
            when cast( round( (julianday(date(year_month || '-01')) - julianday(date(active_date_month || '-01')) ) / 30) as integer) > 0
                then cast( round( (julianday(date(year_month || '-01')) - julianday(date(active_date_month || '-01')) ) / 30) as integer) - 1
            end lapsed_months
        from dates_table_filtered order by year_month, user_id;"""

conn = sqlite3.connect("sqlite.db")
cur = conn.cursor()
cur.execute(create_view)
conn.close()
