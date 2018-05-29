/* 
Syntax is assumed to be postgres 9.6



Loading some example data 
*/
create table event_log(EVENT_DATE date,
 DEVICE_ID char(256),
 EVENT_ID integer,
 EVENT_VALUE float 
                       );

insert into event_log (EVENT_DATE, DEVICE_ID, EVENT_ID,EVENT_VALUE) values (now(), 'a', 1, 12.5);
insert into event_log (EVENT_DATE, DEVICE_ID, EVENT_ID,EVENT_VALUE) values (now(), 'b', 1, 12.5);
insert into event_log (EVENT_DATE, DEVICE_ID, EVENT_ID,EVENT_VALUE) values (now(), 'a', 1, 12.5);



/*challenge 2.1 get top 5% spenders*/

with spenders as ( SELECT DEVICE_ID, sum(EVENT_VALUE) as spending
FROM event_log where EVENT_ID=2 group by DEVICE_ID)
select * from spenders
order by spending desc 
limit (select count(*) * 0.05 from spenders) 
+1; /* add one to always get at least one spender*/



with distinct_events as ( SELECT DISTINCT DEVICE_ID
FROM event_log)
select count(DEVICE_ID) from distinct_events;
