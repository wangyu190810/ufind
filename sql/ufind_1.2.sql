ALTER TABLE user ADD source INTEGER DEFAULT 1;
ALTER TABLE user ADD active INTEGER DEFAULT 1;
ALTER TABLE user ADD coupon VARCHAR(255);
ALTER TABLE user ADD mobile_user INTEGER DEFAULT 0;

ALTER TABLE offer ADD offer_status INTEGER DEFAULT 1;
