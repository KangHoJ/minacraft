### 1.player_info_view(유저 정보 view) = moneytable + banktable + ls_players
CREATE VIEW player_info_view AS 
SELECT b.uuid,b.name,b.money as bankmoney,b.level as banklevel , m.money as usermoney , ls.registration_date as registrate , last_login , date_format(last_login,'%Y-%m-%d') as login_d
FROM plugin_lighteconomy.MoneyTable as m
LEFT JOIN plugin_lighteconomy.BankTable as b ON m.name = b.name
LEFT join plugin_loginsecurity.ls_players as ls ON b.name = ls.last_name
where isPlayer =1;

select * from player_info_view; # 조회

### 2.towny_info_view(유저 외 정보 view) = moneytable + banktable + ls_players + 추가예정
CREATE VIEW town_info_view AS 
SELECT m.uuid,m.name, m.money as usermoney
FROM plugin_lighteconomy.MoneyTable as m
LEFT JOIN plugin_lighteconomy.BankTable as b ON m.name = b.name
LEFT join plugin_loginsecurity.ls_players as ls ON b.name = ls.last_name
where isPlayer =0;

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


-- 이벤트 생성 (1분 간격으로 변경)
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








