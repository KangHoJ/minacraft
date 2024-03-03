-- CREATE VIEW uesrs AS 
CREATE VIEW player_info_view AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.money as usermoney , ls.registration_date as registrate , last_login , date_format(last_login,'%Y-%m-%d') as login_d
FROM plugin_lighteconomy.MoneyTable as m
LEFT JOIN plugin_lighteconomy.BankTable as b ON m.name = b.name
LEFT join plugin_loginsecurity.ls_players as ls ON b.name = ls.last_name
where isPlayer =1;

drop view player_info_view;
drop view town_info_view;

CREATE VIEW town_info_view AS 
SELECT m.uuid,m.name, m.money as usermoney
FROM plugin_lighteconomy.MoneyTable as m
LEFT JOIN plugin_lighteconomy.BankTable as b ON m.name = b.name
LEFT join plugin_loginsecurity.ls_players as ls ON b.name = ls.last_name
where isPlayer =0;


select * from player_info_view;
select * from town_info_view;
select * from Tiles;


CREATE VIEW uesrs AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.isPlayer , m.money as usermoney , ls.registration_date as registrate , ls.formatted_last_login as lastest_login
FROM plugin_loginsecurity.ls_players as ls
LEFT JOIN plugin_lighteconomy.MoneyTable as m ON ls.last_name = m.name
LEFT JOIN plugin_lighteconomy.BankTable as b ON ls.last_name = b.name;

select * from plugin_loginsecurity.ls_players;
select * from plugin_lighteconomy.MoneyTable;
select * from plugin_lighteconomy.BankTable;
select * from plugin_towny.TOWNY_TOWNS;

select * from plugin_loginsecurity.ls_players;

ALTER TABLE plugin_loginsecurity.ls_players
ADD COLUMN formatted_last_login VARCHAR(10);
UPDATE plugin_loginsecurity.ls_players
SET formatted_last_login = DATE_FORMAT(last_login, '%Y-%m-%d');
select * from plugin_loginsecurity.ls_players;

-- CREATE VIEW sumuser AS 
SELECT registrate AS dates, 'registrate' AS event_type FROM player_info_view
    UNION ALL
SELECT login_d, 'last_login' FROM player_info_view;
drop view sumuser;


SELECT dates, event_type, COUNT(*) AS count
FROM sumuser
GROUP BY dates,event_type;

select * from player_info_view;
select * from plugin_loginsecurity.ls_players;
select * from sumuser;




SELECT dates, event_type, COUNT(*) AS count
    FROM sumuser
    GROUP BY dates, event_type;



CREATE TABLE daily_stats2 (
    dates DATE PRIMARY KEY,
    registrate_count INT,
    last_login_count INT
);

-- 이벤트 생성 (1분 간격으로 변경)
DELIMITER //
CREATE EVENT update_daily_stats2
ON SCHEDULE EVERY 30 MINUTE
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT INTO daily_stats (dates, registrate_count, last_login_count)
    SELECT
    dates,
    SUM(IF(event_type = 'registrate', 1, 0)) AS registrate_count,
    SUM(IF(event_type = 'last_login', 1, 0)) AS last_login_count
	FROM sumuser
GROUP BY
    dates;
END;
//
DELIMITER ;

DROP EVENT IF EXISTS update_daily_stats; # 이벤트 삭제
show events;
select * from daily_stats2;




select * from daily_stats;
SELECT dates, event_type, COUNT(*) AS count
    FROM sumuser
    GROUP BY dates, event_type;
    
select * from sumuser;

SELECT
    dates,
    SUM(IF(event_type = 'registrate', 1, 0)) AS registrate_count,
    SUM(IF(event_type = 'last_login', 1, 0)) AS last_login_count
FROM
    sumuser
GROUP BY
    dates;












