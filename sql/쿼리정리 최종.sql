CREATE DATABASE view_dbb;

select * from TOWNY_RESIDENTS;
select * from plugin_lighteconomy.BankTable;

### 1.player_info_view(유저 정보 view) = moneytable + banktable + ls_players
CREATE VIEW player_info_view AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.money as usermoney , m.isPlayer , v.total_games , v.number_victory , v.number_little_victory,  v.number_loss ,
SUBSTRING(FROM_UNIXTIME(pr.registered / 1000),1,19) as registered , SUBSTRING(FROM_UNIXTIME(pr.lastOnline / 1000),1,19) as lastOnline
FROM plugin_lighteconomy.MoneyTable as m
LEFT JOIN plugin_lighteconomy.BankTable as b ON m.name = b.name
LEFT join plugin_towny.TOWNY_RESIDENTS as pr ON b.name = pr.name
LEFT join plugin_vegas.VEGAS_STATISTIC as v ON pr.uuid = v.uuid;
-- where m.isPlayer =1;-- 


### 1.player_info_view(유저 정보 view) = moneytable + banktable + ls_players
CREATE VIEW player_info_view AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.money as usermoney , m.isPlayer , 
SUBSTRING(FROM_UNIXTIME(pr.registered / 1000),1,10) as '등록날짜' , SUBSTRING(FROM_UNIXTIME(pr.lastOnline / 1000),1,10) as '마지막 로그인',
v.total_games '전체 게임수', v.number_victory '승리횟수', v.number_little_victory '작은 승리횟수' , v.number_loss as '패배횟수'
FROM plugin_towny.TOWNY_RESIDENTS as pr
LEFT join plugin_lighteconomy.MoneyTable as m ON pr.uuid = m.uuid
LEFT JOIN plugin_lighteconomy.BankTable as b ON pr.uuid = b.uuid
LEFT join plugin_vegas.VEGAS_STATISTIC as v ON pr.uuid = v.uuid
where m.isPlayer =1;


CREATE VIEW player_info_view2 AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.money as usermoney , m.isPlayer , 
SUBSTRING(FROM_UNIXTIME(pr.registered / 1000),1,10) as '등록날짜' , SUBSTRING(FROM_UNIXTIME(pr.lastOnline / 1000),1,10) as '마지막 로그인',
v.total_games '전체 게임수', v.number_victory '승리횟수', v.number_little_victory '작은 승리횟수' , v.number_loss as '패배횟수'
FROM plugin_towny.TOWNY_RESIDENTS as pr
LEFT join plugin_lighteconomy.MoneyTable as m ON pr.uuid = m.uuid
LEFT JOIN plugin_lighteconomy.BankTable as b ON pr.uuid = b.uuid
LEFT join plugin_vegas.VEGAS_STATISTIC as v ON pr.uuid = v.uuid
where m.isPlayer =0;

select * from player_info_view2;


select * from test;
drop view test;

CREATE VIEW player_info_view_vegas as
select v.total_games '전체 게임수', v.number_victory '승리횟수', v.number_little_victory '작은 승리횟수' , v.number_loss as '패배횟수' from player_info_view as p 
LEFT join plugin_vegas.VEGAS_STATISTIC as v ON p.uuid = v.uuid;
-- v.total_games '전체 게임수', v.number_victory '승리횟수', v.number_little_victory '작은 승리횟수' , v.number_loss as '패배횟수',

select * from player_info_view;
drop view player_info_view;
select * from player_info_view_vegas;
select * from plugin_vegas.VEGAS_STATISTIC;

select * from plugin_lighteconomy.BankTable; # uuid , name , money(은행돈) , level(은행레벨)
select * from plugin_lighteconomy.MoneyTable; # uuid , name , money , isplayer(플레이어 여부)
select * from plugin_vegas.VEGAS_STATISTIC; # uuid , total_games , number_victory , number_little_victory , number_loss 
select  * from plugin_towny.TOWNY_RESIDENTS; # uuid , name , town , lastOnline , registered , 

select name , SUBSTRING(FROM_UNIXTIME(registered / 1000),1,19) as '등록날짜' from plugin_towny.TOWNY_RESIDENTS;
select SUBSTRING(FROM_UNIXTIME(lastOnline / 1000),1,19) as '마지막 로그인' from plugin_towny.TOWNY_RESIDENTS;




### 2.towny_info_view(유저 외 정보 view) = moneytable + banktable + ls_players + 추가예정
-- CREATE VIEW town_info_view AS 
-- SELECT m.uuid,m.name, m.money as usermoney
-- FROM plugin_lighteconomy.MoneyTable as m
-- LEFT JOIN plugin_lighteconomy.BankTable as b ON m.name = b.name
-- LEFT join plugin_loginsecurity.ls_players as ls ON b.name = ls.last_name
-- where isPlayer =0;
select * from town_info_view; # 조회

### last_login 포맷 변경 (형식을 str으로 바꾸기 위해)### 
ALTER TABLE plugin_loginsecurity.ls_players
ADD COLUMN formatted_last_login VARCHAR(10);
UPDATE plugin_loginsecurity.ls_players
SET login_d = DATE_FORMAT(last_login, '%Y-%m-%d');
select * from plugin_loginsecurity.ls_players;

### 3. sumuser 
CREATE VIEW sumuser AS 
SELECT registrate AS dates, 'registrate' AS event_type FROM player_info_view
    UNION ALL
SELECT login_d, 'last_login' FROM player_info_view;

drop view sumuser;
select * from sumuser;

-- 데이터 불러갈떄 query
SELECT dates, event_type, COUNT(*) AS count
    FROM sumuser
    GROUP BY dates, event_type;

############################트리거 부분###############################
DROP EVENT IF EXISTS update_daily_stats; # 이벤트 삭제
show events; # 이벤트 보기
SET GLOBAL event_scheduler = ON; # 스케쥴러 활성화

-- 테이블 생성
CREATE TABLE tri_table (
    dates DATE PRIMARY KEY,
    registrate_count INT,
    last_login_count INT
);

select * from tri_table;
select * from player_info_view;
select * from sumuser;

-- 이벤트 생성 (1분 간격으로 변경) # 추가해도 이전 모든 데이터가 덮어쓰이기 떄문 원하는 결과가 안나옴
DELIMITER //
CREATE EVENT update_daily_stats
ON SCHEDULE EVERY 30 MINUTE
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT INTO tri_table (dates, registrate_count, last_login_count)
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



-- 이벤트 다시 생성
DELIMITER //
CREATE EVENT update_daily_stats3
ON SCHEDULE EVERY 30 MINUTE
STARTS CURRENT_TIMESTAMP
DO
BEGIN
    INSERT INTO tri_table (dates, registrate_count, last_login_count)
    SELECT
        dates,
        SUM(IF(event_type = 'registrate', 1, 0)) AS registrate_count,
        SUM(IF(event_type = 'last_login', 1, 0)) AS last_login_count
    FROM sumuser
    WHERE dates > (NOW() - INTERVAL 30 MINUTE)
    GROUP BY dates
    ON DUPLICATE KEY UPDATE
        registrate_count = registrate_count + VALUES(registrate_count),
        last_login_count = last_login_count + VALUES(last_login_count);
END;
//
DELIMITER ;


select * from sumuser;
select registrate_count from tri_table;
show events;
SELECT event_name , last_executed , status FROM information_schema.EVENTS; 
# 이벤트 실행시간 확인(실행중인지 , 마지막 언제인지 , 이벤트명)


SHOW VARIABLES LIKE 'event_scheduler'; # 활성화인지 확인 
SET GLOBAL event_scheduler = ON; # 이벤트 스케쥴러 활성화


DROP EVENT update_daily_stats3;



select * from messages2;
select * from MoneyTable;

select * from player_info_view;
