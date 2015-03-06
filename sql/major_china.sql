﻿# Host: 127.0.0.1  (Version: 5.6.22-log)
# Date: 2015-03-06 17:31:06
# Generator: MySQL-Front 5.3  (Build 4.13)

/*!40101 SET NAMES utf8 */;

#
# Source for table "major_china"
#

DROP TABLE IF EXISTS `major_china`;
CREATE TABLE `major_china` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `faculty_id` int(11) DEFAULT NULL,
  `faculty_name` varchar(255) DEFAULT NULL,
  `major_id` varchar(11) DEFAULT NULL,
  `major_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=506 DEFAULT CHARSET=utf8;

#
# Data for table "major_china"
#

INSERT INTO `major_china` VALUES (1,1,'哲学','10102','逻辑学'),(2,1,'哲学','010103K','宗教学'),(3,2,'经济学','20101','经济学'),(4,2,'经济学','20102','经济统计学'),(5,2,'经济学','020201K','财政学'),(6,2,'经济学','20202','税收学'),(7,2,'经济学','020301K','金融学'),(8,2,'经济学','20302','金融工程'),(9,2,'经济学','20303','保险学'),(10,2,'经济学','20304','投资学'),(11,2,'经济学','20401','国际经济与贸易'),(12,2,'经济学','20402','贸易经济'),(13,3,'法学','030101K','法学'),(14,3,'法学','30201','政治学与行政学'),(15,3,'法学','30202','国际政治'),(16,3,'法学','30203','外交学'),(17,3,'法学','30301','社会学'),(18,3,'法学','30302','社会工作'),(19,3,'法学','30401','民族学'),(20,3,'法学','30501','科学社会主义'),(21,3,'法学','30502','中国共产党历史'),(22,3,'法学','30503','思想政治教育'),(23,3,'法学','030601K','治安学'),(24,3,'法学','030602K','侦查学'),(25,3,'法学','030603K','边防管理'),(26,4,'教育学','40101','教育学'),(27,4,'教育学','40102','科学教育'),(28,4,'教育学','40103','人文教育'),(29,4,'教育学','40104','教育技术学'),(30,4,'教育学','40105','艺术教育'),(31,4,'教育学','40106','学前教育'),(32,4,'教育学','40107','小学教育'),(33,4,'教育学','40108','特殊教育'),(34,4,'教育学','40201','体育教育'),(35,4,'教育学','040202K','运动训练'),(36,4,'教育学','40203','社会体育指导与管理'),(37,4,'教育学','040204K','武术与民族传统体育'),(38,4,'教育学','40205','运动人体科学'),(39,5,'文学','50101','汉语言文学'),(40,5,'文学','50102','汉语言'),(41,5,'文学','50103','汉语国际教育'),(42,5,'文学','50104','中国少数民族语言文学'),(43,5,'文学','50105','古典文献学'),(44,5,'文学','50201','英语'),(45,5,'文学','50202','俄语'),(46,5,'文学','50203','德语'),(47,5,'文学','50204','法语'),(48,5,'文学','50205','西班牙语'),(49,5,'文学','50206','阿拉伯语'),(50,5,'文学','50207','日语'),(51,5,'文学','50208','波斯语'),(52,5,'文学','50209','朝鲜语'),(53,5,'文学','50210','菲律宾语'),(54,5,'文学','50211','梵语巴利语'),(55,5,'文学','50212','印度尼西亚语'),(56,5,'文学','50213','印地语'),(57,5,'文学','50214','柬埔寨语'),(58,5,'文学','50215','老挝语'),(59,5,'文学','50216','缅甸语'),(60,5,'文学','50217','马来语'),(61,5,'文学','50218','蒙古语'),(62,5,'文学','50219','僧伽罗语'),(63,5,'文学','50220','泰语'),(64,5,'文学','50221','乌尔都语'),(65,5,'文学','50222','希伯来语'),(66,5,'文学','50223','越南语'),(67,5,'文学','50224','豪萨语'),(68,5,'文学','50225','斯瓦希里语'),(69,5,'文学','50226','阿尔巴尼亚语'),(70,5,'文学','50227','保加利亚语'),(71,5,'文学','50228','波兰语'),(72,5,'文学','50229','捷克语'),(73,5,'文学','50230','斯洛伐克语'),(74,5,'文学','50231','罗马尼亚语'),(75,5,'文学','50232','葡萄牙语'),(76,5,'文学','50233','瑞典语'),(77,5,'文学','50234','塞尔维亚语'),(78,5,'文学','50235','土耳其语'),(79,5,'文学','50236','希腊语'),(80,5,'文学','50237','匈牙利语'),(81,5,'文学','50238','意大利语'),(82,5,'文学','50239','泰米尔语'),(83,5,'文学','50240','普什图语'),(84,5,'文学','50241','世界语'),(85,5,'文学','50242','孟加拉语'),(86,5,'文学','50243','尼泊尔语'),(87,5,'文学','50244','克罗地亚语'),(88,5,'文学','50245','荷兰语'),(89,5,'文学','50246','芬兰语'),(90,5,'文学','50247','乌克兰语'),(91,5,'文学','50248','挪威语'),(92,5,'文学','50249','丹麦语'),(93,5,'文学','50250','冰岛语'),(94,5,'文学','50251','爱尔兰语'),(95,5,'文学','50252','拉脱维亚语'),(96,5,'文学','50253','立陶宛语'),(97,5,'文学','50254','斯洛文尼亚语'),(98,5,'文学','50255','爱沙尼亚语'),(99,5,'文学','50256','马耳他语'),(100,5,'文学','50257','哈萨克语'),(101,5,'文学','50258','乌兹别克语'),(102,5,'文学','50259','祖鲁语'),(103,5,'文学','50260','拉丁语'),(104,5,'文学','50261','翻译'),(105,5,'文学','50262','商务英语'),(106,5,'文学','50301','新闻学'),(107,5,'文学','50302','广播电视学'),(108,5,'文学','50303','广告学'),(109,5,'文学','50304','传播学'),(110,5,'文学','50305','编辑出版学'),(111,6,'历史学','60101','历史学'),(112,6,'历史学','60102','世界史'),(113,6,'历史学','60103','考古学'),(114,6,'历史学','60104','文物与博物馆学'),(115,7,'理学','70101','数学与应用数学'),(116,7,'理学','70102','信息与计算科学'),(117,7,'理学','70201','物理学'),(118,7,'理学','70202','应用物理学'),(119,7,'理学','70203','核物理'),(120,7,'理学','70301','化学'),(121,7,'理学','70302','应用化学'),(122,7,'理学','70401','天文学'),(123,7,'理学','70501','地理科学'),(124,7,'理学','70502','自然地理与资源环境'),(125,7,'理学','70503','人文地理与城乡规划'),(126,7,'理学','70504','地理信息科学'),(127,7,'理学','70601','大气科学'),(128,7,'理学','70602','应用气象学'),(129,7,'理学','70701','海洋科学'),(130,7,'理学','70702','海洋技术(注：可授理学或工学学士学位)'),(131,7,'理学','70801','地球物理学'),(132,7,'理学','70802','空间科学与技术'),(133,7,'理学','70901','地质学'),(134,7,'理学','70902','地球化学'),(135,7,'理学','71001','生物科学'),(136,7,'理学','71002','生物技术'),(137,7,'理学','71003','生物信息学'),(138,7,'理学','71004','生态学'),(139,7,'理学','71101','心理学'),(140,7,'理学','71102','应用心理学'),(141,7,'理学','71201','统计学'),(142,7,'理学','71202','应用统计学'),(143,8,'工学','80101','理论与应用力学'),(144,8,'工学','80102','工程力学'),(145,8,'工学','80201','机械工程'),(146,8,'工学','80202','机械设计制造及其自动化'),(147,8,'工学','80203','材料成型及控制工程'),(148,8,'工学','80204','机械电子工程'),(149,8,'工学','80205','工业设计'),(150,8,'工学','80206','过程装备与控制工程'),(151,8,'工学','80207','车辆工程'),(152,8,'工学','80208','汽车服务工程'),(153,8,'工学','80301','测控技术与仪器'),(154,8,'工学','80401','材料科学与工程'),(155,8,'工学','80402','材料物理'),(156,8,'工学','80403','材料化学'),(157,8,'工学','80404','冶金工程'),(158,8,'工学','80405','金属材料工程'),(159,8,'工学','80406','无机非金属材料工程'),(160,8,'工学','80407','高分子材料与工程'),(161,8,'工学','80408','复合材料与工程'),(162,8,'工学','80501','能源与动力工程'),(163,8,'工学','80601','电气工程及其自动化'),(164,8,'工学','80701','电子信息工程'),(165,8,'工学','80702','电子科学与技术'),(166,8,'工学','80703','通信工程'),(167,8,'工学','80704','微电子科学与工程'),(168,8,'工学','80705','光电信息科学与工程'),(169,8,'工学','80706','信息工程'),(170,8,'工学','80801','自动化'),(171,8,'工学','80901','计算机科学与技术'),(172,8,'工学','80902','软件工程'),(173,8,'工学','80903','网络工程'),(174,8,'工学','080904K','信息安全'),(175,8,'工学','80905','物联网工程'),(176,8,'工学','80906','数字媒体技术'),(177,8,'工学','81001','土木工程'),(178,8,'工学','81002','建筑环境与能源应用工程'),(179,8,'工学','81003','给排水科学与工程'),(180,8,'工学','81004','建筑电气与智能化'),(181,8,'工学','81101','水利水电工程'),(182,8,'工学','81102','水文与水资源工程'),(183,8,'工学','81103','港口航道与海岸工程'),(184,8,'工学','81201','测绘工程'),(185,8,'工学','81202','遥感科学与技术'),(186,8,'工学','81301','化学工程与工艺'),(187,8,'工学','81302','制药工程'),(188,8,'工学','81401','地质工程'),(189,8,'工学','81402','勘查技术与工程'),(190,8,'工学','81403','资源勘查工程'),(191,8,'工学','81501','采矿工程'),(192,8,'工学','81502','石油工程'),(193,8,'工学','81503','矿物加工工程'),(194,8,'工学','81504','油气储运工程'),(195,8,'工学','81601','纺织工程'),(196,8,'工学','81602','服装设计与工程'),(197,8,'工学','81701','轻化工程'),(198,8,'工学','81702','包装工程'),(199,8,'工学','81703','印刷工程'),(200,8,'工学','81801','交通运输'),(201,8,'工学','81802','交通工程'),(202,8,'工学','081803K','航海技术'),(203,8,'工学','081804K','轮机工程'),(204,8,'工学','081805K','飞行技术'),(205,8,'工学','81901','船舶与海洋工程'),(206,8,'工学','82001','航空航天工程'),(207,8,'工学','82002','飞行器设计与工程'),(208,8,'工学','82003','飞行器制造工程'),(209,8,'工学','82004','飞行器动力工程'),(210,8,'工学','82005','飞行器环境与生命保障工程'),(211,8,'工学','82101','武器系统与工程'),(212,8,'工学','82102','武器发射工程'),(213,8,'工学','82103','探测制导与控制技术'),(214,8,'工学','82104','弹药工程与爆炸技术'),(215,8,'工学','82105','特种能源技术与工程'),(216,8,'工学','82106','装甲车辆工程'),(217,8,'工学','82107','信息对抗技术'),(218,8,'工学','82201','核工程与核技术'),(219,8,'工学','82202','辐射防护与核安全'),(220,8,'工学','82203','工程物理'),(221,8,'工学','82204','核化工与核燃料工程'),(222,8,'工学','82301','农业工程'),(223,8,'工学','82302','农业机械化及其自动化'),(224,8,'工学','82303','农业电气化'),(225,8,'工学','82304','农业建筑环境与能源工程'),(226,8,'工学','82305','农业水利工程'),(227,8,'工学','82401','森林工程'),(228,8,'工学','82402','木材科学与工程'),(229,8,'工学','82403','林产化工'),(230,8,'工学','82501','环境科学与工程'),(231,8,'工学','82502','环境工程'),(232,8,'工学','82503','环境科学'),(233,8,'工学','82504','环境生态工程'),(234,8,'工学','82601','生物医学工程'),(235,8,'工学','82701','食品科学与工程'),(236,8,'工学','82702','食品质量与安全'),(237,8,'工学','82703','粮食工程'),(238,8,'工学','82704','乳品工程'),(239,8,'工学','82705','酿酒工程'),(240,8,'工学','82801','建筑学'),(241,8,'工学','82802','城乡规划'),(242,8,'工学','82803','风景园林'),(243,8,'工学','82901','安全工程'),(244,8,'工学','83001','生物工程'),(245,8,'工学','083101K','刑事科学技术'),(246,8,'工学','083102K','消防工程'),(247,9,'农学','90101','农学'),(248,9,'农学','90102','园艺'),(249,9,'农学','90103','植物保护'),(250,9,'农学','90104','植物科学与技术'),(251,9,'农学','90105','种子科学与工程'),(252,9,'农学','90106','设施农业科学与工程'),(253,9,'农学','90201','农业资源与环境'),(254,9,'农学','90202','野生动物与自然保护区管理'),(255,9,'农学','90203','水土保持与荒漠化防治'),(256,9,'农学','90301','动物科学'),(257,9,'农学','90401','动物医学'),(258,9,'农学','90402','动物药学'),(259,9,'农学','90501','林学'),(260,9,'农学','90502','园林'),(261,9,'农学','90503','森林保护'),(262,9,'农学','90601','水产养殖学'),(263,9,'农学','90602','海洋渔业科学与技术'),(264,9,'农学','90701','草业科学'),(265,10,'医学','100101K','基础医学'),(266,10,'医学','100201K','临床医学'),(267,10,'医学','100301K','口腔医学'),(268,10,'医学','100401K','预防医学'),(269,10,'医学','100402','食品卫生与营养学'),(270,10,'医学','100501K','中医学'),(271,10,'医学','100502K','针灸推拿学'),(272,10,'医学','100503K','藏医学'),(273,10,'医学','100504K','蒙医学'),(274,10,'医学','100505K','维医学'),(275,10,'医学','100506K','壮医学'),(276,10,'医学','100507K','哈医学'),(277,10,'医学','100601K','中西医临床医学'),(278,10,'医学','100701','药学'),(279,10,'医学','100702','药物制剂'),(280,10,'医学','100801','中药学'),(281,10,'医学','100802','中药资源与开发'),(282,10,'医学','100901K','法医学'),(283,10,'医学','101001','医学检验技术'),(284,10,'医学','101002','医学实验技术'),(285,10,'医学','101003','医学影像技术'),(286,10,'医学','101004','眼视光学'),(287,10,'医学','101005','康复治疗学'),(288,10,'医学','101006','口腔医学技术'),(289,10,'医学','101007','卫生检验与检疫'),(290,10,'医学','101101','护理学'),(291,12,'管理学','120101','管理科学'),(292,12,'管理学','120102','信息管理与信息系统'),(293,12,'管理学','120103','工程管理'),(294,12,'管理学','120104','房地产开发与管理'),(295,12,'管理学','120105','工程造价'),(296,12,'管理学','120201K','工商管理'),(297,12,'管理学','120202','市场营销'),(298,12,'管理学','120203K','会计学'),(299,12,'管理学','120204','财务管理'),(300,12,'管理学','120205','国际商务'),(301,12,'管理学','120206','人力资源管理'),(302,12,'管理学','120207','审计学'),(303,12,'管理学','120208','资产评估'),(304,12,'管理学','120209','物业管理'),(305,12,'管理学','120210','文化产业管理'),(306,12,'管理学','120301','农林经济管理'),(307,12,'管理学','120302','农村区域发展'),(308,12,'管理学','120401','公共事业管理'),(309,12,'管理学','120402','行政管理'),(310,12,'管理学','120403','劳动与社会保障'),(311,12,'管理学','120404','土地资源管理'),(312,12,'管理学','120405','城市管理'),(313,12,'管理学','120501','图书馆学'),(314,12,'管理学','120502','档案学'),(315,12,'管理学','120503','信息资源管理'),(316,12,'管理学','120601','物流管理'),(317,12,'管理学','120602','物流工程'),(318,12,'管理学','120701','工业工程'),(319,12,'管理学','120801','电子商务'),(320,12,'管理学','120901K','旅游管理'),(321,12,'管理学','120902','酒店管理'),(322,12,'管理学','120903','会展经济与管理'),(323,13,'艺术学','130101','艺术史论'),(324,13,'艺术学','130201','音乐表演'),(325,13,'艺术学','130202','音乐学'),(326,13,'艺术学','130203','作曲与作曲技术理论'),(327,13,'艺术学','130204','舞蹈表演'),(328,13,'艺术学','130205','舞蹈学'),(329,13,'艺术学','130206','舞蹈编导'),(330,13,'艺术学','130301','表演'),(331,13,'艺术学','130302','戏剧学'),(332,13,'艺术学','130303','电影学'),(333,13,'艺术学','130304','戏剧影视文学'),(334,13,'艺术学','130305','广播电视编导'),(335,13,'艺术学','130306','戏剧影视导演'),(336,13,'艺术学','130307','戏剧影视美术设计'),(337,13,'艺术学','130308','录音艺术'),(338,13,'艺术学','130309','播音与主持艺术'),(339,13,'艺术学','130310','动画'),(340,13,'艺术学','130401','美术学'),(341,13,'艺术学','130402','绘画'),(342,13,'艺术学','130403','雕塑'),(343,13,'艺术学','130404','摄影'),(344,13,'艺术学','130501','艺术设计学'),(345,13,'艺术学','130502','视觉传达设计'),(346,13,'艺术学','130503','环境设计'),(347,13,'艺术学','130504','产品设计'),(348,13,'艺术学','130505','服装与服饰设计'),(349,13,'艺术学','130506','公共艺术'),(350,13,'艺术学','130507','工艺美术'),(351,13,'艺术学','130508','数字媒体艺术'),(352,1,'哲学','010104T','伦理学'),(353,2,'经济学','020103T','国民经济管理'),(354,2,'经济学','020104T','资源与环境经济学'),(355,2,'经济学','020105T','商务经济学'),(356,2,'经济学','020106T','能源经济'),(357,2,'经济学','020305T','金融数学'),(358,2,'经济学','020306T','信用管理'),(359,2,'经济学','020307T','经济与金融'),(360,3,'法学','030102T','知识产权'),(361,3,'法学','030103T','监狱学'),(362,3,'法学','030204T','国际事务与国际关系'),(363,3,'法学','030205T','政治学、经济学与哲学'),(364,3,'法学','030303T','人类学'),(365,3,'法学','030304T','女性学'),(366,3,'法学','030305T','家政学'),(367,3,'法学','030604TK','禁毒学'),(368,3,'法学','030605TK','警犬技术'),(369,3,'法学','030606TK','经济犯罪侦查'),(370,3,'法学','030607TK','边防指挥'),(371,3,'法学','030608TK','消防指挥'),(372,3,'法学','030609TK','警卫学'),(373,3,'法学','030610TK','公安情报学'),(374,3,'法学','030611TK','犯罪学'),(375,3,'法学','030612TK','公安管理学'),(376,3,'法学','030613TK','涉外警务'),(377,3,'法学','030614TK','国内安全保卫'),(378,3,'法学','030615TK','警务指挥与战术'),(379,4,'教育学','040109T','华文教育'),(380,4,'教育学','040206T','运动康复'),(381,4,'教育学','040207T','休闲体育'),(382,5,'文学','050106T','应用语言学'),(383,5,'文学','050107T','秘书学'),(384,5,'文学','050306T','网络与新媒体'),(385,5,'文学','050307T','数字出版'),(386,6,'历史学','060105T','文物保护技术'),(387,6,'历史学','060106T','外国语言与外国历史'),(388,7,'理学','070103T','数理基础科学'),(389,7,'理学','070204T','声学'),(390,7,'理学','070303T','化学生物学'),(391,7,'理学','070304T','分子科学与工程'),(392,7,'理学','070703T','海洋资源与环境'),(393,7,'理学','070704T','军事海洋学'),(394,7,'理学','070903T','地球信息科学与技术'),(395,7,'理学','070904T','古生物学'),(396,8,'工学','080209T','机械工艺技术'),(397,8,'工学','080210T','微机电系统工程'),(398,8,'工学','080211T','机电技术教育'),(399,8,'工学','080212T','汽车维修工程教育'),(400,8,'工学','080409T','粉体材料科学与工程'),(401,8,'工学','080410T','宝石及材料工艺学'),(402,8,'工学','080411T','焊接技术与工程'),(403,8,'工学','080412T','功能材料'),(404,8,'工学','080413T','纳米材料与技术'),(405,8,'工学','080414T','新能源材料与器件'),(406,8,'工学','080502T','能源与环境系统工程'),(407,8,'工学','080503T','新能源科学与工程'),(408,8,'工学','080602T','智能电网信息工程'),(409,8,'工学','080603T','光源与照明'),(410,8,'工学','080604T','电气工程与智能控制'),(411,8,'工学','080707T','广播电视工程'),(412,8,'工学','080708T','水声工程'),(413,8,'工学','080709T','电子封装技术'),(414,8,'工学','080710T','集成电路设计与集成系统'),(415,8,'工学','080711T','医学信息工程'),(416,8,'工学','080712T','电磁场与无线技术'),(417,8,'工学','080713T','电波传播与天线'),(418,8,'工学','080714T','电子信息科学与技术(注：可授工学或理学学士学位)'),(419,8,'工学','080715T','电信工程及管理'),(420,8,'工学','080716T','应用电子技术教育'),(421,8,'工学','080802T','轨道交通信号与控制'),(422,8,'工学','080907T','智能科学与技术'),(423,8,'工学','080908T','空间信息与数字技术'),(424,8,'工学','080909T','电子与计算机工程'),(425,8,'工学','081005T','城市地下空间工程'),(426,8,'工学','081006T','道路桥梁与渡河工程'),(427,8,'工学','081104T','水务工程'),(428,8,'工学','081203T','导航工程'),(429,8,'工学','081204T','地理国情监测'),(430,8,'工学','081303T','资源循环科学与工程'),(431,8,'工学','081304T','能源化学工程'),(432,8,'工学','081305T','化学工程与工业生物工程'),(433,8,'工学','081404T','地下水科学与工程'),(434,8,'工学','081505T','矿物资源工程'),(435,8,'工学','081506T','海洋油气工程'),(436,8,'工学','081603T','非织造材料与工程'),(437,8,'工学','081604T','服装设计与工艺教育'),(438,8,'工学','081806T','交通设备与控制工程'),(439,8,'工学','081807T','救助与打捞工程'),(440,8,'工学','081808TK','船舶电子电气工程'),(441,8,'工学','081902T','海洋工程与技术'),(442,8,'工学','081903T','海洋资源开发技术'),(443,8,'工学','082006T','飞行器质量与可靠性'),(444,8,'工学','082007T','飞行器适航技术'),(445,8,'工学','082505T','环保设备工程'),(446,8,'工学','082506T','资源环境科学'),(447,8,'工学','082507T','水质科学与技术'),(448,8,'工学','082602T','假肢矫形工程'),(449,8,'工学','082706T','葡萄与葡萄酒工程'),(450,8,'工学','082707T','食品营养与检验教育'),(451,8,'工学','082708T','烹饪与营养教育'),(452,8,'工学','082804T','历史建筑保护工程'),(453,8,'工学','083002T','生物制药'),(454,8,'工学','083103TK','交通管理工程'),(455,8,'工学','083104TK','安全防范工程'),(456,8,'工学','083105TK','公安视听技术'),(457,8,'工学','083106TK','抢险救援指挥与技术'),(458,8,'工学','083107TK','火灾勘查'),(459,8,'工学','083108TK','网络安全与执法'),(460,8,'工学','083109TK','核生化消防'),(461,9,'农学','090107T','茶学'),(462,9,'农学','090108T','烟草'),(463,9,'农学','090109T','应用生物科学'),(464,9,'农学','090110T','农艺教育'),(465,9,'农学','090111T','园艺教育'),(466,9,'农学','090302T','蚕学'),(467,9,'农学','090303T','蜂学'),(468,9,'农学','090403T','动植物检疫'),(469,9,'农学','090603T','水族科学与技术'),(470,10,'医学','100202TK','麻醉学'),(471,10,'医学','100203TK','医学影像学'),(472,10,'医学','100204TK','眼视光医学'),(473,10,'医学','100205TK','精神医学'),(474,10,'医学','100206TK','放射医学'),(475,10,'医学','100403TK','妇幼保健医学'),(476,10,'医学','100404TK','卫生监督'),(477,10,'医学','100405TK','全球健康学'),(478,10,'医学','100703TK','临床药学'),(479,10,'医学','100704T','药事管理'),(480,10,'医学','100705T','药物分析'),(481,10,'医学','100706T','药物化学'),(482,10,'医学','100707T','海洋药学'),(483,10,'医学','100803T','藏药学'),(484,10,'医学','100804T','蒙药学'),(485,10,'医学','100805T','中药制药'),(486,10,'医学','100806T','中草药栽培与鉴定'),(487,10,'医学','101008T','听力与言语康复学'),(488,12,'管理学','120106TK','保密管理'),(489,12,'管理学','120211T','劳动关系'),(490,12,'管理学','120212T','体育经济与管理'),(491,12,'管理学','120213T','财务会计教育'),(492,12,'管理学','120214T','市场营销教育'),(493,12,'管理学','120406TK','海关管理'),(494,12,'管理学','120407T','交通管理'),(495,12,'管理学','120408T','海事管理'),(496,12,'管理学','120409T','公共关系学'),(497,12,'管理学','120603T','采购管理'),(498,12,'管理学','120702T','标准化工程'),(499,12,'管理学','120703T','质量管理工程'),(500,12,'管理学','120802T','电子商务及法律'),(501,12,'管理学','120904T','旅游管理与服务教育'),(502,13,'艺术学','130311T','影视摄影与制作'),(503,13,'艺术学','130405T','书法学'),(504,13,'艺术学','130406T','中国画'),(505,13,'艺术学','130509T','艺术与科技');