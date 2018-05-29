/* 
Syntax is assumed to be postgres 9.6



Loading some example data 
*/
create table event_log(EVENT_DATE timestamp,
 DEVICE_ID char(256),
 EVENT_ID integer,
 EVENT_VALUE float 
                       );

insert into event_log (EVENT_DATE, DEVICE_ID, EVENT_ID,EVENT_VALUE) values (now(), 'a', 1, 12.5);
insert into event_log (EVENT_DATE, DEVICE_ID, EVENT_ID,EVENT_VALUE) values (now(), 'b', 1, 12.5);
insert into event_log (EVENT_DATE, DEVICE_ID, EVENT_ID,EVENT_VALUE) values (now(), 'a', 1, 12.5);




/*challenge 2.1 get top 5% spenders*/


/*Assumption: Number of top five unique users is equal to 5% of users */
with spenders as ( SELECT DEVICE_ID as spending /*Get unique users*/
FROM event_log where EVENT_ID=2 group by DEVICE_ID)
select  ceil(  count(*)* 0.05) from spenders /* Get 5 % of users*/


/*challenge 2.2 Average amount of purchases in TPU*/


with spenders as 
( SELECT DEVICE_ID, sum(EVENT_VALUE) as spending, count(EVENT_ID) as purchases /* Get users, their amount of spending and their number of purchases*/
FROM event_log where EVENT_ID=2 group by DEVICE_ID),
 tpu as ( /* Get the tpu*/
select * from spenders
order by spending desc 
limit ceil( (select count(*)* 0.05 from spenders)))

select avg(purchases) from tpu /*Select the average*/
; 


/*Challenge 2.3 select average transaction delay*/

with spenders as 
( SELECT DEVICE_ID, sum(EVENT_VALUE) as spending, count(EVENT_ID) as purchases /* Get users, their amount of spending and their number of purchases*/
FROM event_log where EVENT_ID=2 group by DEVICE_ID),

tpu as ( /* Get the tpu*/
select * from spenders
order by spending desc 
limit ceil( (select count(*)* 0.05 from spenders))),

tpu_events as
(select el.EVENT_DATE, el.DEVICE_ID, rank() over (partition by el.DEVICE_ID ORDER BY el.EVENT_DATE) from event_log as el, tpu where el.DEVICE_ID = tpu.DEVICE_ID), /* Select tpu_users and give their transaction a rank ordered by the timestamp*/

/* Join the tpu events with the next event and calculate the difference*/
transaction_time_diffs as 
(
select (a.EVENT_DATE - b.EVENT_DATE) as TIME_DIFFERENCE, a.DEVICE_ID
from tpu_events as a , tpu_events as b where a.rank = b.rank+1 and a.DEVICE_ID=b.DEVICE_ID 
)

/* Finally calculate teh average grouped by user */
select DEVICE_ID, avg(TIME_DIFFERENCE) from transaction_time_diffs group by DEVICE_ID;
