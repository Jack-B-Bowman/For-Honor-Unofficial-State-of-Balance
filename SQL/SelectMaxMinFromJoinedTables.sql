-- select name,
--        username,
--        UTCSeconds,
--        platform,
--        wins,
--        losses
-- from (
--   select name, 
--          username, 
--          UTCSeconds,
--          max(UTCSeconds) over (partition by username) as max_date,
--          min(UTCSeconds) over (partition by username) as min_date,
--          platform,
--          wins,
--          losses 
--   from (SELECT mode.name,mode.wins,mode.losses, stat.username, stat.platform, stat.UTCSeconds FROM mode INNER JOIN stat on mode.playerID = stat.playerID)
-- )
-- where UTCSeconds = max_date OR UTCSeconds = min_date;


SELECT newStats.name newStats.username, (newStats.wins - oldStats.wins) as wins, (newStats.losses - oldStats.losses) as losses from 
(SELECT * from (

select name,
       username,
       UTCSeconds,
       platform,
       wins,
       losses
from (
  select name, 
         username, 
         UTCSeconds,
         max(UTCSeconds) over (partition by username) as max_date,
         platform,
         wins,
         losses 
  from (SELECT mode.name,mode.wins,mode.losses, stat.username, stat.platform, stat.UTCSeconds FROM mode INNER JOIN stat on mode.playerID = stat.playerID)
) as maxValues
where UTCSeconds = max_date

) as maxTable
) newStats

INNER JOIN

(SELECT * from (

select name,
       username,
       UTCSeconds,
       platform,
       wins,
       losses
from (
  select name, 
         username, 
         UTCSeconds,
         min(UTCSeconds) over (partition by username) as min_date,
         platform,
         wins,
         losses 
  from (SELECT mode.name,mode.wins,mode.losses, stat.username, stat.platform, stat.UTCSeconds FROM mode INNER JOIN stat on mode.playerID = stat.playerID)
) as minValues
where UTCSeconds = min_date

) as maxTable
) oldStats

on oldStats.name=newStats.name and oldStats.username=newStats.username
