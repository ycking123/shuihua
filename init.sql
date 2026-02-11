-- MySQL dump 10.13  Distrib 9.6.0, for Linux (x86_64)
--
-- Host: localhost    Database: agent_db
-- ------------------------------------------------------
-- Server version	9.6.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'e31c7120-ffe7-11f0-a272-0242ac110002:1-391';

--
-- Table structure for table `gen_table`
--

DROP TABLE IF EXISTS `gen_table`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table` (
  `table_id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '表名称',
  `table_comment` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '表描述',
  `sub_table_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '子表关联的外键名',
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '实体类名称',
  `tpl_category` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'crud' COMMENT '使用的模板（crud单表操作 tree树表操作）',
  `tpl_web_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '前端模板类型（element-ui模版 element-plus模版）',
  `package_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '生成功能名',
  `function_author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '生成功能作者',
  `gen_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '生成代码方式（0zip压缩包 1自定义路径）',
  `gen_path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '/' COMMENT '生成路径（不填默认项目路径）',
  `options` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '其它生成选项',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`table_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='代码生成业务表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table`
--

LOCK TABLES `gen_table` WRITE;
/*!40000 ALTER TABLE `gen_table` DISABLE KEYS */;
INSERT INTO `gen_table` VALUES (1,'sys_device','',NULL,NULL,'SysDevice','crud','','com.xunmei.system','system','device',NULL,'ruoyi','0','/',NULL,'admin','2025-01-08 15:29:27','',NULL,NULL),(2,'vss_algorithm','VSS算法信息表',NULL,NULL,'VssAlgorithm','crud','','com.xm.common','system','algorithm','VSS算法信息表','ruoyi','0','/','{\"parentMenuId\":\"\"}','admin','2025-05-14 10:13:16','','2025-05-14 10:16:18',NULL),(5,'vss_channel','VSS视频信息表',NULL,NULL,'VssChannel','crud','','com.xm.common','system','channel','VSS视频信息','ruoyi','0','/','{\"parentMenuId\":\"\"}','admin','2025-05-14 10:17:25','','2025-05-14 10:17:50',NULL),(6,'vss_result_resource','VSS结果资源表',NULL,NULL,'VssResultResource','crud','','com.xm.common','system','resource','VSS结果资源','ruoyi','0','/','{\"parentMenuId\":\"\"}','admin','2025-05-14 10:17:25','','2025-05-14 10:18:14',NULL),(7,'cosmos_predict_history','Cosmos检测历史记录表',NULL,NULL,'CosmosPredictHistory','crud','','com.xm.common','common','history','vss','ruoyi','0','/','{\"parentMenuId\":\"\"}','admin','2025-07-08 16:12:45','','2025-07-08 16:14:51',NULL);
/*!40000 ALTER TABLE `gen_table` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gen_table_column`
--

DROP TABLE IF EXISTS `gen_table_column`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gen_table_column` (
  `column_id` bigint NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_id` bigint DEFAULT NULL COMMENT '归属表编号',
  `column_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '列名称',
  `column_comment` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '列类型',
  `java_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'JAVA类型',
  `java_field` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'JAVA字段名',
  `is_pk` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否主键（1是）',
  `is_increment` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否自增（1是）',
  `is_required` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否必填（1是）',
  `is_insert` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否为插入字段（1是）',
  `is_edit` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否编辑字段（1是）',
  `is_list` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否列表字段（1是）',
  `is_query` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否查询字段（1是）',
  `query_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'EQ' COMMENT '查询方式（等于、不等于、大于、小于、范围）',
  `html_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）',
  `dict_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典类型',
  `sort` int DEFAULT NULL COMMENT '排序',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`column_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='代码生成业务表字段';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gen_table_column`
--

LOCK TABLES `gen_table_column` WRITE;
/*!40000 ALTER TABLE `gen_table_column` DISABLE KEYS */;
INSERT INTO `gen_table_column` VALUES (1,1,'id',NULL,'bigint','Long','id','1','1','0','1',NULL,NULL,NULL,'EQ','input','',1,'admin','2025-01-08 15:29:27','',NULL),(2,1,'device_name',NULL,'varchar(255)','String','deviceName','0','0','1','1','1','1','1','LIKE','input','',2,'admin','2025-01-08 15:29:27','',NULL),(3,1,'product_model',NULL,'varchar(255)','String','productModel','0','0','0','1','1','1','1','EQ','input','',3,'admin','2025-01-08 15:29:27','',NULL),(4,1,'mac_address',NULL,'varchar(255)','String','macAddress','0','0','0','1','1','1','1','EQ','input','',4,'admin','2025-01-08 15:29:27','',NULL),(5,1,'resolution',NULL,'varchar(50)','String','resolution','0','0','0','1','1','1','1','EQ','input','',5,'admin','2025-01-08 15:29:27','',NULL),(6,1,'device_status',NULL,'varchar(50)','String','deviceStatus','0','0','0','1','1','1','1','EQ','radio','',6,'admin','2025-01-08 15:29:27','',NULL),(7,1,'created_time',NULL,'datetime','Date','createdTime','0','0','0','1','1','1','1','EQ','datetime','',7,'admin','2025-01-08 15:29:27','',NULL),(8,1,'update_time',NULL,'datetime','Date','updateTime','0','0','0','1','1',NULL,NULL,'EQ','datetime','',8,'admin','2025-01-08 15:29:27','',NULL),(9,2,'id','算法主键编号','int','Long','id','1','0','0','1',NULL,NULL,NULL,'EQ','input','',1,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(10,2,'name','算法名称','varchar(32)','String','name','0','0','0','1','1','1','1','LIKE','input','',2,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(11,2,'en_name','英文名称','varchar(32)','String','enName','0','0','0','1','1','1','1','LIKE','input','',3,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(12,2,'desc','算法描述','varchar(255)','String','desc','0','0','0','1','1','1','1','EQ','input','',4,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(13,2,'prompt','算法提示词','varchar(255)','String','prompt','0','0','0','1','1','1','1','EQ','input','',5,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(14,2,'alert_prompt','告警提示词','varchar(255)','String','alertPrompt','0','0','0','1','1','1','1','EQ','input','',6,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(15,2,'industry','算法所属行业','varchar(255)','String','industry','0','0','0','1','1','1','1','EQ','input','',7,'admin','2025-05-14 10:13:16','','2025-05-14 10:16:18'),(31,5,'id','视频文件编号','int','Long','id','1','1','0','1',NULL,NULL,NULL,'EQ','input','',1,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(32,5,'url','视频文件地址','varchar(255)','String','url','0','0','0','1','1','1','1','EQ','input','',2,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(33,5,'name','视频文件名称','varchar(255)','String','name','0','0','0','1','1','1','1','LIKE','input','',3,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(34,5,'origin_name','视频原名','varchar(255)','String','originName','0','0','0','1','1','1','1','LIKE','input','',4,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(35,5,'thumbnail','缩略图地址','varchar(255)','String','thumbnail','0','0','0','1','1','1','1','EQ','input','',5,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(36,5,'duration','视频文件长度','varchar(255)','String','duration','0','0','0','1','1','1','1','EQ','input','',6,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(37,5,'recordTime','视频时间','datetime','Date','recordTime','0','0','0','1','1','1','1','EQ','datetime','',7,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(38,5,'industry','上传视频所属行业','varchar(12)','String','industry','0','0','0','1','1','1','1','EQ','input','',8,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(39,5,'type','类型(1: 视频文件；2: 流地址）','tinyint(1)','Integer','type','0','0','0','1','1','1','1','EQ','select','',9,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(40,5,'algorithm_id','算法ID','int','Long','algorithmId','0','0','0','1','1','1','1','EQ','input','',10,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(41,5,'result','当前算法是否报警（0：是；1：否)','tinyint(1)','Integer','result','0','0','0','1','1','1','1','EQ','input','',11,'admin','2025-05-14 10:17:25','','2025-05-14 10:17:50'),(42,6,'id','主键编号','int','Long','id','1','0','0','1',NULL,NULL,NULL,'EQ','input','',1,'admin','2025-05-14 10:17:25','','2025-05-14 10:18:14'),(43,6,'channel_id','VSS视频源编号','int','Long','channelId','0','0','0','1','1','1','1','EQ','input','',2,'admin','2025-05-14 10:17:25','','2025-05-14 10:18:14'),(44,6,'url','检测结果资源地址','varchar(255)','String','url','0','0','0','1','1','1','1','EQ','input','',3,'admin','2025-05-14 10:17:25','','2025-05-14 10:18:14'),(45,6,'type','检测结果资源类别','tinyint','Integer','type','0','0','0','1','1','1','1','EQ','select','',4,'admin','2025-05-14 10:17:25','','2025-05-14 10:18:14'),(46,7,'id','主键，流水号','bigint','Long','id','1','1','0','1',NULL,NULL,NULL,'EQ','input','',1,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(47,7,'input_image_or_video_path','输入图片或视频地址','varchar(255)','String','inputImageOrVideoPath','0','0','0','1','1','1','1','EQ','input','',2,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(48,7,'type','模型类型','tinyint','Integer','type','0','0','0','1','1','1','1','EQ','select','',3,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(49,7,'prompt','提示词','varchar(255)','String','prompt','0','0','0','1','1','1','1','EQ','input','',4,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(50,7,'prompt_left','左侧视角提示词','varchar(1000)','String','promptLeft','0','0','0','1','1','1','1','EQ','textarea','',5,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(51,7,'prompt_right','右侧视角提示词','varchar(1000)','String','promptRight','0','0','0','1','1','1','1','EQ','textarea','',6,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(52,7,'prompt_back','后方视角提示词','varchar(1000)','String','promptBack','0','0','0','1','1','1','1','EQ','textarea','',7,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(53,7,'prompt_back_left','左后方视角提示词','varchar(1000)','String','promptBackLeft','0','0','0','1','1','1','1','EQ','textarea','',8,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(54,7,'prompt_back_right','右后方视角提示词','varchar(255)','String','promptBackRight','0','0','0','1','1','1','1','EQ','input','',9,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(55,7,'video_url','生成的视频地址','varchar(1000)','String','videoUrl','0','0','0','1','1','1','1','EQ','textarea','',10,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(56,7,'video_prompt','优化后的提示词','varchar(1000)','String','videoPrompt','0','0','0','1','1','1','1','EQ','textarea','',11,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51'),(57,7,'create_time','创建事件','datetime','Date','createTime','0','0','0','1',NULL,NULL,NULL,'EQ','datetime','',12,'admin','2025-07-08 16:12:45','','2025-07-08 16:14:51');
/*!40000 ALTER TABLE `gen_table_column` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_blob_triggers`
--

DROP TABLE IF EXISTS `qrtz_blob_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_blob_triggers` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `blob_data` blob COMMENT '存放持久化Trigger对象',
  PRIMARY KEY (`sched_name`,`trigger_name`,`trigger_group`),
  CONSTRAINT `qrtz_blob_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='Blob类型的触发器表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_blob_triggers`
--

LOCK TABLES `qrtz_blob_triggers` WRITE;
/*!40000 ALTER TABLE `qrtz_blob_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_blob_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_calendars`
--

DROP TABLE IF EXISTS `qrtz_calendars`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_calendars` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `calendar_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '日历名称',
  `calendar` blob NOT NULL COMMENT '存放持久化calendar对象',
  PRIMARY KEY (`sched_name`,`calendar_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='日历信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_calendars`
--

LOCK TABLES `qrtz_calendars` WRITE;
/*!40000 ALTER TABLE `qrtz_calendars` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_calendars` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_cron_triggers`
--

DROP TABLE IF EXISTS `qrtz_cron_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_cron_triggers` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `cron_expression` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'cron表达式',
  `time_zone_id` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '时区',
  PRIMARY KEY (`sched_name`,`trigger_name`,`trigger_group`),
  CONSTRAINT `qrtz_cron_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='Cron类型的触发器表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_cron_triggers`
--

LOCK TABLES `qrtz_cron_triggers` WRITE;
/*!40000 ALTER TABLE `qrtz_cron_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_cron_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_fired_triggers`
--

DROP TABLE IF EXISTS `qrtz_fired_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_fired_triggers` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `entry_id` varchar(95) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度器实例id',
  `trigger_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `instance_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度器实例名',
  `fired_time` bigint NOT NULL COMMENT '触发的时间',
  `sched_time` bigint NOT NULL COMMENT '定时器制定的时间',
  `priority` int NOT NULL COMMENT '优先级',
  `state` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '状态',
  `job_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '任务名称',
  `job_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '任务组名',
  `is_nonconcurrent` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否并发',
  `requests_recovery` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '是否接受恢复执行',
  PRIMARY KEY (`sched_name`,`entry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='已触发的触发器表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_fired_triggers`
--

LOCK TABLES `qrtz_fired_triggers` WRITE;
/*!40000 ALTER TABLE `qrtz_fired_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_fired_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_job_details`
--

DROP TABLE IF EXISTS `qrtz_job_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_job_details` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `job_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `job_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务组名',
  `description` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关介绍',
  `job_class_name` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '执行任务类名称',
  `is_durable` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '是否持久化',
  `is_nonconcurrent` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '是否并发',
  `is_update_data` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '是否更新数据',
  `requests_recovery` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '是否接受恢复执行',
  `job_data` blob COMMENT '存放持久化job对象',
  PRIMARY KEY (`sched_name`,`job_name`,`job_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='任务详细信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_job_details`
--

LOCK TABLES `qrtz_job_details` WRITE;
/*!40000 ALTER TABLE `qrtz_job_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_job_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_locks`
--

DROP TABLE IF EXISTS `qrtz_locks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_locks` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `lock_name` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '悲观锁名称',
  PRIMARY KEY (`sched_name`,`lock_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='存储的悲观锁信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_locks`
--

LOCK TABLES `qrtz_locks` WRITE;
/*!40000 ALTER TABLE `qrtz_locks` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_locks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_paused_trigger_grps`
--

DROP TABLE IF EXISTS `qrtz_paused_trigger_grps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_paused_trigger_grps` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  PRIMARY KEY (`sched_name`,`trigger_group`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='暂停的触发器表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_paused_trigger_grps`
--

LOCK TABLES `qrtz_paused_trigger_grps` WRITE;
/*!40000 ALTER TABLE `qrtz_paused_trigger_grps` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_paused_trigger_grps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_scheduler_state`
--

DROP TABLE IF EXISTS `qrtz_scheduler_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_scheduler_state` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `instance_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '实例名称',
  `last_checkin_time` bigint NOT NULL COMMENT '上次检查时间',
  `checkin_interval` bigint NOT NULL COMMENT '检查间隔时间',
  PRIMARY KEY (`sched_name`,`instance_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='调度器状态表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_scheduler_state`
--

LOCK TABLES `qrtz_scheduler_state` WRITE;
/*!40000 ALTER TABLE `qrtz_scheduler_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_scheduler_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_simple_triggers`
--

DROP TABLE IF EXISTS `qrtz_simple_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_simple_triggers` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `repeat_count` bigint NOT NULL COMMENT '重复的次数统计',
  `repeat_interval` bigint NOT NULL COMMENT '重复的间隔时间',
  `times_triggered` bigint NOT NULL COMMENT '已经触发的次数',
  PRIMARY KEY (`sched_name`,`trigger_name`,`trigger_group`),
  CONSTRAINT `qrtz_simple_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='简单触发器的信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_simple_triggers`
--

LOCK TABLES `qrtz_simple_triggers` WRITE;
/*!40000 ALTER TABLE `qrtz_simple_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_simple_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_simprop_triggers`
--

DROP TABLE IF EXISTS `qrtz_simprop_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_simprop_triggers` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_name的外键',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_triggers表trigger_group的外键',
  `str_prop_1` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'String类型的trigger的第一个参数',
  `str_prop_2` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'String类型的trigger的第二个参数',
  `str_prop_3` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'String类型的trigger的第三个参数',
  `int_prop_1` int DEFAULT NULL COMMENT 'int类型的trigger的第一个参数',
  `int_prop_2` int DEFAULT NULL COMMENT 'int类型的trigger的第二个参数',
  `long_prop_1` bigint DEFAULT NULL COMMENT 'long类型的trigger的第一个参数',
  `long_prop_2` bigint DEFAULT NULL COMMENT 'long类型的trigger的第二个参数',
  `dec_prop_1` decimal(13,4) DEFAULT NULL COMMENT 'decimal类型的trigger的第一个参数',
  `dec_prop_2` decimal(13,4) DEFAULT NULL COMMENT 'decimal类型的trigger的第二个参数',
  `bool_prop_1` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Boolean类型的trigger的第一个参数',
  `bool_prop_2` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'Boolean类型的trigger的第二个参数',
  PRIMARY KEY (`sched_name`,`trigger_name`,`trigger_group`),
  CONSTRAINT `qrtz_simprop_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `trigger_name`, `trigger_group`) REFERENCES `qrtz_triggers` (`sched_name`, `trigger_name`, `trigger_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='同步机制的行锁表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_simprop_triggers`
--

LOCK TABLES `qrtz_simprop_triggers` WRITE;
/*!40000 ALTER TABLE `qrtz_simprop_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_simprop_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `qrtz_triggers`
--

DROP TABLE IF EXISTS `qrtz_triggers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `qrtz_triggers` (
  `sched_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调度名称',
  `trigger_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '触发器的名字',
  `trigger_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '触发器所属组的名字',
  `job_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_job_details表job_name的外键',
  `job_group` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'qrtz_job_details表job_group的外键',
  `description` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '相关介绍',
  `next_fire_time` bigint DEFAULT NULL COMMENT '上一次触发时间（毫秒）',
  `prev_fire_time` bigint DEFAULT NULL COMMENT '下一次触发时间（默认为-1表示不触发）',
  `priority` int DEFAULT NULL COMMENT '优先级',
  `trigger_state` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '触发器状态',
  `trigger_type` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '触发器的类型',
  `start_time` bigint NOT NULL COMMENT '开始时间',
  `end_time` bigint DEFAULT NULL COMMENT '结束时间',
  `calendar_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '日程表名称',
  `misfire_instr` smallint DEFAULT NULL COMMENT '补偿执行的策略',
  `job_data` blob COMMENT '存放持久化job对象',
  PRIMARY KEY (`sched_name`,`trigger_name`,`trigger_group`),
  KEY `sched_name` (`sched_name`,`job_name`,`job_group`) USING BTREE,
  CONSTRAINT `qrtz_triggers_ibfk_1` FOREIGN KEY (`sched_name`, `job_name`, `job_group`) REFERENCES `qrtz_job_details` (`sched_name`, `job_name`, `job_group`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='触发器详细信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `qrtz_triggers`
--

LOCK TABLES `qrtz_triggers` WRITE;
/*!40000 ALTER TABLE `qrtz_triggers` DISABLE KEYS */;
/*!40000 ALTER TABLE `qrtz_triggers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_analysis_reports`
--

DROP TABLE IF EXISTS `shjl_analysis_reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_analysis_reports` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `source_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '来源类型',
  `source_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '来源ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '报告标题',
  `detailed_report` longtext COLLATE utf8mb4_unicode_ci COMMENT '详细报告内容',
  `conclusion_cards` json DEFAULT NULL COMMENT '结论卡片(JSON)',
  `mind_map_data` json DEFAULT NULL COMMENT '思维导图数据(JSON)',
  `raw_response` json DEFAULT NULL COMMENT '原始响应数据(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_analysis_source` (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='分析报告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_analysis_reports`
--

LOCK TABLES `shjl_analysis_reports` WRITE;
/*!40000 ALTER TABLE `shjl_analysis_reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_analysis_reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_audit_logs`
--

DROP TABLE IF EXISTS `shjl_audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_audit_logs` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户ID',
  `action` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '操作动作',
  `resource_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '资源类型',
  `resource_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '资源ID',
  `ip_address` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'IP地址',
  `user_agent` text COLLATE utf8mb4_unicode_ci COMMENT '用户代理',
  `details` json DEFAULT NULL COMMENT '详情(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_audit_user_action` (`user_id`,`action`),
  CONSTRAINT `shjl_audit_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `shjl_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_audit_logs`
--

LOCK TABLES `shjl_audit_logs` WRITE;
/*!40000 ALTER TABLE `shjl_audit_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_chat_messages`
--

DROP TABLE IF EXISTS `shjl_chat_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_chat_messages` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `session_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会话ID',
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色(user/assistant/system)',
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '消息内容',
  `message_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'text' COMMENT '消息类型',
  `meta_data` json DEFAULT NULL COMMENT '元数据(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_messages_session_created` (`session_id`,`created_at`),
  CONSTRAINT `shjl_chat_messages_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `shjl_chat_sessions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天消息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_chat_messages`
--

LOCK TABLES `shjl_chat_messages` WRITE;
/*!40000 ALTER TABLE `shjl_chat_messages` DISABLE KEYS */;
INSERT INTO `shjl_chat_messages` VALUES ('01934c54-c7a7-46a5-b4be-bbc1fc8a57e5','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧高事** (责任人: [\'小周\', \'小乐\', \'小皮蛋\'], 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 09:34:05'),('02d4b66b-3a5c-4b54-8758-519e6b60ed9d','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 08:06:16'),('039e5935-5f69-45f2-9d66-ab5afa68a82e','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:32:12'),('04172843-27bc-4204-bf6a-393da0a55a77','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧中事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级为紧急','text',NULL,'2026-02-03 09:20:42'),('045a6544-76a8-4329-a4bb-9d014dd3edef','23255a62-641a-41c4-a3eb-4b11d3876987','user','优先级：紧急','text',NULL,'2026-02-03 09:27:38'),('06c91f56-4cdd-4a52-bf79-4d9893b19d81','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n根据帝欧水华集团费用报销标准，以下是主要规定：\n\n**一、目的**\n规范集团各部门费用报销标准、明确报销要求，加强财务管理，根据国家法律法规及公司内控制度制定。\n\n**二、报销标准**\n- **副总裁、财务总监、董事会秘书、内审负责人**：实报实销\n- **主管级、科员级**：宴请标准为70元/人\n\n**三、特殊规定**\n1. 业务费因特殊情况超过标准，需总监级以上负责人书面同意\n2. 机票、汽车/高铁、住宿费超过标准需提前向直管领导申请同意\n3. 住宿费可在差旅期间合并计算，但需在单据上说明\n4. 网约车需提供发票及对应行程单\n5. 出差当天往返无补助\n\n**四、签批权限**\n- 董事长、副董事长、总裁由各自分别审批\n- 集团其他人员需对应直管领导审批\n\n**五、其他规定**\n- 办公用品实报实销，单价≥500元必须事前在EKP系统内填写《办公用品申购单》\n- 本制度由审计监察部监督执行，最终解释权归集团财务管理部所有\n\n该标准自发布之日起，《帝欧（集财）字【2025】第【001】号，帝欧集团费用报销标准》自动作废。','text',NULL,'2026-02-03 08:06:59'),('07c69132-c154-4b59-99fd-915092542e39','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n您好。请问有什么需要我协助您处理？','text',NULL,'2026-02-03 09:40:26'),('090a0b1a-871a-4e77-85af-1ac196ab8392','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午8点','text',NULL,'2026-02-03 09:05:29'),('09d92bc0-d01b-4ce1-bd05-5c22362cf5bc','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧中事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级为紧急','text',NULL,'2026-02-03 09:12:44'),('0a5cdf68-55d5-4386-8cc1-4e6a2b92c3b4','23255a62-641a-41c4-a3eb-4b11d3876987','user','你是谁','text',NULL,'2026-02-03 09:40:48'),('0b579e3a-175e-4974-9d14-4cb6363271b5','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n欧神诺瓷砖是高品质瓷砖品牌，具有以下特点：\n\n1. **产品质量权威认证**：荣获沸腾质量奖，产品经过专业机构检测认证，特别是超低吸水率和超低辐射特性得到权威背书。\n\n2. **生产工艺先进**：采用先进的生产工艺和设备，如高性能压机，确保瓷砖品质卓越。\n\n3. **健康安全特性**：瓷砖吸水率低，更加耐用，能有效避免潮湿环境中霉菌滋生，特别适合有老人和孩子的家庭，是对健康的重要保障。\n\n4. **防污性能优越**：通过高温烧制，釉面砖釉层致密，且涂覆长效防污剂，采用纳米涂层技术形成疏水、疏油层，增强防污性能。\n\n欧神诺佛山标准体现了对产品质量的严格把控，是值得信赖的高端瓷砖品牌。','text',NULL,'2026-02-03 08:06:26'),('0b838a4a-93d0-4e78-8b7b-dcdae04716af','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧中事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级是高','text',NULL,'2026-02-03 09:32:45'),('0b9e4400-2749-458a-9e8f-cb0c20a422c9','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n作为AI助手，我没有个人情感或偏好。我的目标是为您提供专业、简洁且有深度的服务，帮助您解决问题、制定策略或获取信息。无论您需要什么支持，我都会以最高效的方式协助您。','text',NULL,'2026-02-03 07:26:04'),('0be0073e-2bf4-4c99-bbbb-4276e73b4e6a','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:10:45'),('0ca1ff55-739d-4281-a5a3-48aa0796ad97','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','你好','text',NULL,'2026-02-04 06:16:49'),('0ed7b046-c21b-4d63-8ff8-67b051fcc4f4','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n您好。请问有什么需要我协助您处理？','text',NULL,'2026-02-03 09:26:33'),('0eee02d7-a41d-4ef6-a694-85caf185cc2a','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午我要开会','text',NULL,'2026-02-03 09:32:33'),('18f38700-97a3-45c5-bcb8-d38ec0777c64','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午和小周开会','text',NULL,'2026-02-03 08:00:36'),('1a4b82f1-c22d-463c-9f3f-2e07773729f5','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','您好。我是您的战略智僚助手，随时准备为您提供专业、简洁且有深度的分析与建议。请告诉我您需要什么帮助。','text',NULL,'2026-02-03 07:25:25'),('1c0598a5-1762-4935-8e8e-fd3519f7d34e','23255a62-641a-41c4-a3eb-4b11d3876987','user','你喜欢我吗','text',NULL,'2026-02-03 07:26:02'),('1ed615c2-e2a5-44a3-999e-2ef026da12ee','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到，明天上午开会已知晓。请补充会议主题以及紧急程度。','text',NULL,'2026-02-03 08:53:00'),('1f1f0c4d-8fc1-4d69-8527-88622c9219e3','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','您好！有什么我可以帮助您的吗？','text',NULL,'2026-02-04 09:37:36'),('1f6c6d78-f75a-408a-9b54-3a1a7354fab5','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 08:46:30'),('231e6415-7078-4af0-9764-9536c4886dce','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是 针对企业的数据化整形','text',NULL,'2026-02-03 08:32:45'),('2343c5e3-acbe-4756-9fae-97ece90d2261','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n我是您的战略智僚助手，专注于为您提供专业、简洁且有深度的分析与建议。','text',NULL,'2026-02-03 09:40:49'),('296561ad-21a4-4d53-bfdc-94a71a508b37','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','明天下午我要开会','text',NULL,'2026-02-04 06:52:44'),('2b96b989-ba28-4b45-8b23-0291da132527','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','会议主题：我的财富  具体时间：下午3点 参会人：乐乐 堃堃； 优先级：紧急','text',NULL,'2026-02-04 06:56:00'),('2c25ba1a-dd34-4b91-85a9-d1a5d0e0ea04','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','明天下午我有一场会议','text',NULL,'2026-02-04 08:34:58'),('2ff8f39f-3c00-4044-b9ec-ff0d03c98aca','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午3点，重要','text',NULL,'2026-02-03 08:39:21'),('31714a87-a749-409a-9686-acd335c479e9','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到[主题:帝欧中事, 时间:上午9点, 参会人:小周,小乐,小皮蛋]。请补充[优先级]','text',NULL,'2026-02-03 09:27:27'),('3192fb12-5d19-440d-9f8a-0ab3624a159f','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n您好。请问有什么需要我协助您处理？','text',NULL,'2026-02-03 09:31:02'),('391ac70c-cd69-4e28-9db5-fa71b5cbf486','23255a62-641a-41c4-a3eb-4b11d3876987','user','帮我介绍一下帝欧水华报销的内容','text',NULL,'2026-02-03 09:08:51'),('3c793606-f88e-49a9-a5f9-2605d6a3fa70','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:04:46'),('3d220c1a-6220-405f-8001-7de4ff5f7e3c','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到具体时间：明天上午。请补充主题、责任人和优先级。','text',NULL,'2026-02-03 09:04:48'),('3d44b95b-252f-40bf-be92-7c4881421b4e','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到[明天上午我要开会]。请补充[主题]、[具体时间（精确到点）]、[责任人/参会人]、[优先级]','text',NULL,'2026-02-03 09:26:39'),('3d4e64e8-9373-49f2-bb22-838b11a2012c','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题：国家大事 责任人：周周 优先级：重要','text',NULL,'2026-02-03 09:05:14'),('3dd3a086-df68-4cac-8932-1df123b8d84d','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','你好','text',NULL,'2026-02-04 06:26:29'),('4150c4af-4259-40ec-b1be-d4dc876348d3','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午我要开会','text',NULL,'2026-02-03 09:40:51'),('41c4284b-2d62-4864-8e58-c2f5ec7b1d32','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧战略** (责任人: [\'小周\', \'小刘\', \'小王\'], 截止: 2026-02-05 15:00)','text',NULL,'2026-02-04 08:35:26'),('46eef284-1528-4b7e-a5bb-aaa3ea851c0c','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','你好','text',NULL,'2026-02-04 06:20:07'),('4b9965aa-c28f-49be-b646-2f700747c02f','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','明天开始会议','text',NULL,'2026-02-04 09:43:49'),('4bb27f6f-6924-4162-9b81-550367e0cfe7','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','我是一个基于人工智能技术的虚拟助手，旨在通过自然语言处理和机器学习技术，为用户提供信息查询、任务协助、问题解答等服务。我可以处理各种类型的请求，包括日常咨询、数据分析、日程管理等。我的目标是提供高效、准确和便捷的用户体验。','text',NULL,'2026-02-04 08:29:46'),('4c1ad674-893a-4c95-91f2-f032fd2faf7d','d84aeb49-e3a6-432d-a94d-88758d3b025a','assistant','你好！有什么我可以帮助您的吗？','text',NULL,'2026-02-05 02:02:54'),('4fe63736-0120-4912-9f2c-fc5cf43bdc88','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午我要开会','text',NULL,'2026-02-04 09:12:13'),('5366f891-6669-4626-aff9-bce4bd30996a','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n根据帝欧水华集团费用报销标准，以下是主要报销内容和规定：\n\n**一、报销范围**\n- 业务费：特殊情况超过标准需总监级以上负责人书面同意\n- 办公用品：实报实销，单价≥500元必须事前在EKP系统内填写《办公用品申购单》\n- 差旅费：包括交通、住宿、餐饮等，需提供出差申请及打卡记录（董事、高管及特别顾问除外）\n\n**二、发票规范**\n1. 发票必须具备以下条件：\n   - 真实性\n   - 发票内容、类型与实际业务一致\n   - 公司名称、纳税人识别号准确\n   - 大小写金额一致\n2. 发票税率大于3%（除餐饮、烟酒茶、福利费外），必须开具增值税专用发票，否则税点损失由报销申请人承担\n\n**三、签批权限**\n- 董事长、副董事长、总裁由各自分别审批\n- 集团其他人员需对应直管领导审批\n\n**四、特殊规定**\n- 由公司安排的各种大型会议或外出培训，如果会议包含住宿和用餐，不得再报销差旅补助\n- 出差未规范打卡当日无补助\n\n该标准自发布之日起，《帝欧（集财）字【2025】第【001】号，帝欧集团费用报销标准》自动作废，由审计监察部监督执行，最终解释权归集团财务管理部所有。','text',NULL,'2026-02-03 09:09:02'),('54267755-57f1-4614-adc7-89132e462c68','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','明天下午我要开会','text',NULL,'2026-02-04 06:55:08'),('5479d5d1-d733-4e03-9076-aee3ecd89ca5','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n您好。请问有什么需要我协助您处理？','text',NULL,'2026-02-03 08:06:18'),('54937855-a7cd-4280-9863-eb931d92a416','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到会议时间：明天下午。请补充会议主题、参会人和优先级（高/中/低）。','text',NULL,'2026-02-03 09:32:35'),('57f0b8a4-0b34-47b5-9279-22bfa15a79fc','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到[明天上午我要开会]。请补充[主题]、[具体时间（精确到点）]、[责任人/参会人]、[优先级]','text',NULL,'2026-02-03 09:11:40'),('584f7a12-0d88-4467-a0e5-bc0faad09167','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','主题：帝欧战略 时间：下午3点 参会人：小周，小刘，小王 优先级：紧急','text',NULL,'2026-02-04 08:35:24'),('5857cac7-cc94-4ce8-bd58-a87c12dd88d2','9e67be86-5154-4865-a51c-b0c7efa26aa2','assistant','# 2024集团组织架构敏捷化调整预案通知执行路线图\n\n## 一、预案通知核心材料\n\n### 1.1 预案通知框架\n- **标题**：关于2024集团组织架构敏捷化调整的预案通知\n- **发文部门**：人力资源中心\n- **签发人**：严总\n- **编号**：HR-AGILE-2024-001\n- **密级**：重要战略文件\n- **分发范围**：集团高管、各事业部负责人、人力资源部全体\n\n### 1.2 通知正文要点\n1. **调整背景**：市场环境变化、数字化转型需求、提升组织响应速度\n2. **调整目标**：构建敏捷型组织、增强市场适应性、优化资源配置\n3. **调整原则**：业务驱动、小团队作战、快速迭代、持续优化\n4. **核心内容**：组织架构调整方向、关键岗位设置、权责划分\n5. **实施步骤**：分阶段推进、时间节点、里程碑事件\n6. **保障措施**：沟通机制、培训支持、绩效调整\n\n## 二、详细建议报告\n\n### 2.1 现状分析\n- 当前组织架构痛点：层级过多、决策链条长、跨部门协作低效\n- 行业标杆对比：领先企业敏捷组织模式借鉴\n- 员工调研数据：对现有架构的满意度与改进建议\n\n### 2.2 敏捷化调整方案\n- **组织模式**：采用\"平台+业务单元\"双轮驱动模式\n- **结构调整**：\n  - 设立战略决策委员会\n  - 组建跨职能敏捷小组\n  - 优化中后台支持体系\n- **权责划分**：明确决策权限下放机制与责任边界\n- **人才配置**：关键岗位胜任力模型与人才盘点\n\n### 2.3 实施路线图\n\n#### 第一阶段：准备与规划（1-2月）\n- 成立专项工作组（严总牵头）\n- 完成组织诊断与差距分析\n- 制定详细实施方案与沟通计划\n- 获得集团高管层审批\n\n#### 第二阶段：试点与调整（3-4月）\n- 选择1-2个业务单元进行试点\n- 组建敏捷团队并试运行\n- 收集反馈并进行方案优化\n- 完成人员调配与培训\n\n#### 第三阶段：全面推广（5-8月）\n- 分批次在各业务单元推广\n- 调整配套制度与流程\n- 开展全员培训与文化宣导\n- 建立敏捷组织运行机制\n\n#### 第四阶段：评估与优化（9-12月）\n- 组织效能评估\n- 问题诊断与持续改进\n- 2025年组织优化规划\n- 形成最佳实践案例库\n\n### 2.4 风险管控\n- **变革阻力**：建立多层级沟通机制，强化变革愿景\n- **人才流失**：关键人才保留计划，职业发展通道设计\n- **短期业绩**：设置过渡期绩效缓冲机制，平衡长期与短期目标\n- **文化冲突**：敏捷文化培育，价值观重塑\n\n### 2.5 资源需求\n- 人力资源：专项工作组编制、外部顾问支持\n- 财务资源：培训预算、系统改造投入、激励措施\n- 技术支持：协同工具升级、数据分析平台建设\n\n## 三、执行建议\n\n1. **高层共识**：先期与各业务负责人进行一对一沟通，确保理解一致\n2. **渐进推进**：避免\"一刀切\"，根据业务特性差异化实施\n3. **数据驱动**：建立组织效能监测指标，定期评估调整效果\n4. **敏捷迭代**：采用PDCA循环，持续优化组织设计\n5. **文化先行**：将敏捷文化融入人才发展体系，强化行为引导\n\n此执行路线图确保组织架构敏捷化调整有序推进，平衡变革力度与组织稳定性，为集团战略目标实现提供组织保障。','text',NULL,'2026-02-03 09:22:35'),('594e84e8-623e-4211-9546-427fb3c6404d','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','您好，我是一个人工智能助手，专门设计来提供信息和帮助解答问题的。我是由人工智能技术驱动的，旨在协助用户获取信息、解决问题和执行任务。有什么可以帮助您的吗？','text',NULL,'2026-02-04 08:29:38'),('5a37ee11-2a77-46a1-a257-741a22ad730e','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:37:33'),('5a6c5a52-0915-44d1-bd3c-c7eeb989b673','23255a62-641a-41c4-a3eb-4b11d3876987','user','针对企业的数据化整形','text',NULL,'2026-02-03 08:32:24'),('5b76fded-68c0-47d0-9868-811e62e0ecbe','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n已为您安排明天上午9点的会议\n\n已创建 1 个任务：\n- **帝欧中事** (责任人: 我, 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 09:32:14'),('5c2e2acf-8920-47e5-809b-76456e204a14','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:45:05'),('5dd464bf-1f13-40fd-96a1-5c76fd0ec128','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','你好！我是您的在线助手，随时准备回答您的问题或提供帮助。请问有什么可以为您服务的？','text',NULL,'2026-02-04 09:37:14'),('5fd4774c-ef99-40d8-8f15-639b0542e6cc','23255a62-641a-41c4-a3eb-4b11d3876987','user','周小牛，王大牛','text',NULL,'2026-02-03 08:39:07'),('60045af2-8f56-43a5-b68c-79feda423705','8a760c16-cb50-4154-a0d6-f0ef9fbd1560','assistant','\n公司战略是企业为实现长期目标而设计的整体行动方案，它明确了组织的使命、愿景和方向，并规划如何在竞争环境中获取可持续竞争优势。战略包含三个核心层次：公司层（业务组合与资源配置）、业务层（市场定位与竞争策略）和职能层（各职能部门如何支持整体战略）。有效的战略能够将组织资源与市场机会相匹配，建立差异化优势，并适应外部环境变化，最终实现价值创造和股东回报最大化。','text',NULL,'2026-02-03 09:53:35'),('63211375-833b-4d1f-837b-093c2c93bb2f','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧高事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级是紧急','text',NULL,'2026-02-03 09:34:03'),('64843e53-220a-4335-9d64-df45594f51b8','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','解释一下阿基米德原理','text',NULL,'2026-02-04 08:30:08'),('6592ba20-0cdc-4ab9-ad8e-a3e39ae53e36','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n已为您安排明天上午9点的会议\n\n已创建 1 个任务：\n- **帝欧中事** (责任人: 我, 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 09:12:50'),('68422bd7-3716-49c6-bdfe-40b0a82294b6','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午我要开会','text',NULL,'2026-02-03 09:40:29'),('68a03e4e-92c4-49a2-b053-9e9faeb39ae6','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午我要开会','text',NULL,'2026-02-03 09:33:54'),('691c0f9e-7002-4e1e-b7e8-122532240feb','23255a62-641a-41c4-a3eb-4b11d3876987','user','下午5点','text',NULL,'2026-02-03 08:00:43'),('6a96a37a-6e3c-46da-a372-459f325b25fc','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n我是您的战略智僚助手，专注于提供专业、简洁且有深度的分析与建议。','text',NULL,'2026-02-03 07:25:39'),('6b805e40-af81-4d46-b22a-c921e30df480','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请问会议的主题是什么？','text',NULL,'2026-02-03 08:32:05'),('6c03c18a-fcca-4ff0-b126-2bb6dd850042','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','收到明天下午有一场会议。请补充会议主题、具体时间（精确到点）、参会人、优先级（紧急/重要/一般/低）。','text',NULL,'2026-02-04 08:35:00'),('6fd1571b-9ef2-460a-b0a4-b6095feaa616','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧中事** (责任人: [\'小周\', \'小乐\', \'小皮蛋\'], 截止: 明天上午9点)','text',NULL,'2026-02-03 09:27:41'),('758f3a42-a708-428c-b3b3-99b8c532ef90','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:26:37'),('7a736261-6804-4e94-8320-ce6ed6094359','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排明天上午9点的会议\n\n已创建 1 个任务：\n- **针对企业的数据化整形** (责任人: 我, 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 08:32:47'),('7bcf7ef2-b73c-4d89-b740-539071e181c4','23255a62-641a-41c4-a3eb-4b11d3876987','user','你叫什么名字','text',NULL,'2026-02-03 07:25:37'),('7d450717-ef0e-4ac4-9c3c-a13035acb615','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题：企业内部的转型','text',NULL,'2026-02-03 08:53:13'),('7fd872dd-b9d1-4b66-9a6b-af12fcca79ce','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **国家大事** (责任人: 周周, 截止: 2026-02-04 08:00)','text',NULL,'2026-02-03 09:05:31'),('83bab4b7-18a4-48ad-93d6-c8c1b3c8148e','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请补充会议的参会人员和紧急程度。','text',NULL,'2026-02-03 08:38:50'),('854a797e-c07f-4421-bb02-ee7056487588','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排明天下午3点的会议\n\n已创建 1 个任务：\n- **和姚聪开会** (责任人: Sender, 截止: 2026-02-04 15:00)','text',NULL,'2026-02-03 08:00:15'),('86a65f20-d8b3-4044-ae97-2e22f14d66c2','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:20:20'),('872a6b12-e0c3-4cf2-86d9-2d06c3445b7e','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到会议时间：明天下午。请补充会议主题、参会人和优先级（高/中/低）。','text',NULL,'2026-02-03 09:33:56'),('8a09671d-b8cc-4f06-bfa8-f31e62ade74c','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','讲解一下帝欧水华费用报销原则','text',NULL,'2026-02-04 08:32:19'),('8a36a098-4bda-4066-a432-d5bca6fa24c0','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午9点开会','text',NULL,'2026-02-03 08:32:04'),('8a7a27df-707d-4567-9375-a672cb22fa8a','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧中事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级是紧急程度','text',NULL,'2026-02-03 09:27:25'),('8aa678d4-5b31-4f40-8108-5de4568e190e','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:37:50'),('8dddcf04-bba6-45f7-905b-9592d32e9622','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请问会议具体是在几点开始？','text',NULL,'2026-02-03 08:00:38'),('9290678c-65a9-480a-91fa-3ace2c6bcd6d','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','你好','text',NULL,'2026-02-05 02:02:50'),('93258cee-f9d3-448d-ad20-a208cd48a041','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 09:09:44'),('936ade84-9087-45a4-9ec2-8a7042625f10','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天下午我要和姚聪开会，3点，紧急','text',NULL,'2026-02-03 07:31:36'),('94860d70-8df2-4bf6-a1f3-5a94891668a5','8a760c16-cb50-4154-a0d6-f0ef9fbd1560','assistant','我能提供战略规划、商业分析、决策支持和问题解决等服务。具体包括市场趋势分析、竞争情报评估、风险管理策略制定、商业模式优化、组织效能提升等。我可以帮助您分析复杂问题、制定长期愿景、设计实施路径，并提供基于数据的洞察和建议。无论您面临商业挑战还是战略决策，我都能提供结构化思维和系统性解决方案。','text',NULL,'2026-02-03 09:53:05'),('9514e26e-73fe-475a-b8aa-ed4c34d85032','23255a62-641a-41c4-a3eb-4b11d3876987','user','时间：9点 紧急程度：重要','text',NULL,'2026-02-03 08:53:32'),('99c916e8-dbdd-47ec-9329-8c4a05316819','23255a62-641a-41c4-a3eb-4b11d3876987','user','介绍一下欧神诺瓷砖','text',NULL,'2026-02-03 08:06:22'),('9a234c1c-850c-4a7e-9688-f0e5f1c0ee28','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 09:40:25'),('9ee075c9-95bd-4f5b-99e9-4625d881ea1a','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','您好！我在这里，随时准备帮助您。有什么问题或者需要我协助的地方吗？','text',NULL,'2026-02-04 09:40:30'),('9f9ddd79-4ef0-414f-b1f9-d1e31e59c16f','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','你好！请问有什么我可以帮您的吗？','text',NULL,'2026-02-04 09:40:21'),('9fbb2790-e354-4ae5-9bb0-bb96873cff54','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:37:10'),('a0138659-ca43-4163-bf31-1d4050ffb7f0','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 09:26:32'),('a0c38f43-c94a-4e31-8a7a-92360423202f','8a760c16-cb50-4154-a0d6-f0ef9fbd1560','user','公司战略是什么？','text',NULL,'2026-02-03 09:53:33'),('a22abfd6-a147-4eae-aef8-876f26783076','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到[明天上午我要开会]。请补充[主题]、[具体时间（精确到点）]、[责任人/参会人]、[优先级]','text',NULL,'2026-02-03 09:12:38'),('a46aa6f1-5d37-4ca4-8a9d-8081068762f1','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n已为您安排明天下午的会议\n\n已创建 1 个任务：\n- **会议** (责任人: 我, 截止: 2026-02-04 下午)','text',NULL,'2026-02-03 09:40:39'),('a47bfc7f-c1e5-42ed-badc-cbd6e7bdb780','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','你好','text',NULL,'2026-02-04 06:16:57'),('a4e6e659-cf08-4e02-8680-759e43b09377','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 07:25:23'),('a5c2039c-a374-4dd9-948e-35fe036f68f3','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','根据您提供的参考信息，帝欧水华集团的费用报销原则可以概括如下：\n\n1. **目的**：制定该费用报销原则的目的是为了规范集团各部门的费用报销标准，明确报销要求，加强财务管理。\n\n2. **依据**：该原则依据国家法律、法规的有关规定以及公司相关内控制度，结合实际情况制定。\n\n3. **废止旧规**：自新制度发布之日起，《帝欧（集财）字【2025】第【001】号，帝欧集团费用报销标准》自动作废。\n\n4. **监督执行**：该制度由审计监察部监督执行，最终解释权归集团财务管理部所有。\n\n5. **日常费用报销规范**：\n   - **业务费**：因特殊情况超过标准的业务费，需总监级以上负责人书面同意。\n   - **办公用品**：实报实销，单价≥500元的办公用品，必须事前在EKP系统内填写《办公用品申购单》进行申购流程。\n\n6. **签批权限**：\n   - 董事长、副董事长、总裁由各自分别审批。\n   - 集团其他人员需对应直管领导审批。\n\n请注意，这些信息是基于您提供的文档标题和摘要。具体的费用报销细则可能包含更详细的条款和流程，建议查阅完整的文件以获取准确的信息。','text',NULL,'2026-02-04 08:32:36'),('a86cbdc1-6b44-43e5-aeef-200bdb2b55bb','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到会议主题“企业内部的转型”。请继续补充具体时间（几点？）和紧急程度。','text',NULL,'2026-02-03 08:53:15'),('a8a4c2b4-190a-40ae-b2e9-076503befae6','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n您好。请问有什么需要我协助您处理？','text',NULL,'2026-02-03 09:09:45'),('a98c6c34-75eb-44b7-98f5-219d54c64790','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','待办事项汇总\n\n已创建 1 个任务：\n- **和姚聪开会** (责任人: Sender, 截止: 2026-02-04 15:00)','text',NULL,'2026-02-03 07:31:39'),('a9dd874b-b346-43d6-b88e-d36bad0a5c85','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:11:38'),('abd959ed-51ea-4c4f-a7e3-fa6aa33caf10','d84aeb49-e3a6-432d-a94d-88758d3b025a','assistant','收到\'明天开始会议\'。请补充会议的主题、具体时间（精确到点）、责任人/参会人以及优先级。','text',NULL,'2026-02-04 09:43:54'),('ac68d0d8-80ee-43b6-8787-fe5ff0d1cb7d','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **我的财富** (责任人: [\'乐乐\', \'堃堃\'], 截止: 2026-02-05 15:00)','text',NULL,'2026-02-04 06:56:02'),('ad1a8a3a-4808-4a5a-81a0-ffc2ba18cf59','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧高事、时间下午9点、参会人有小周，小乐，小皮蛋、优先级是紧急','text',NULL,'2026-02-03 09:41:00'),('adeb62c6-162d-40b8-841a-a263bb21f0bc','9e67be86-5154-4865-a51c-b0c7efa26aa2','user','请帮我生成关于“关于 2024 集团组织架构敏捷化调整的预案通知”的相关所需材料和详细建议报告。这份任务是由 人力资源中心 - 严总 发起的，目前的状态是 重要战略关注。请给出具体的执行路线图。','text',NULL,'2026-02-03 09:22:13'),('b1b63d94-97f1-4bb8-bfdf-e6f0345bf5ed','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','大模型，明天上午9点，张小燕，高','text',NULL,'2026-02-04 09:44:42'),('b3ed2a13-8a6e-42ac-bff3-316aaa68896b','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:40:27'),('b4986f6f-0bb6-4a13-96b6-6dc5ad119a5e','23255a62-641a-41c4-a3eb-4b11d3876987','user','大概7点，重要','text',NULL,'2026-02-03 08:46:48'),('b81085fd-7cec-471d-a85a-a5877a6a2fb5','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-04 09:40:15'),('b8fc0eb0-d233-4aa1-ab90-4a5ea0cac892','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧高事、时间下午9点、参会人有小周，小乐，小皮蛋、优先级是紧急','text',NULL,'2026-02-04 09:12:20'),('b958b18b-237f-4abb-b24e-a73e88dc7dba','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','收到：明天下午开会。请补充会议主题、具体时间（精确到点）、参会人、优先级。','text',NULL,'2026-02-04 06:55:11'),('ba871f90-a258-4642-80fa-5b8bc3f7b646','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 09:31:00'),('bbf8fa84-330b-4a46-bb94-349268eb1c2f','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到[明天上午我要开会]。请补充[主题]、[具体时间（精确到点）]、[责任人/参会人]、[优先级]','text',NULL,'2026-02-03 09:20:22'),('bc25e38e-c7b9-431b-ab37-90c6d16bef0a','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请补充会议的具体时间（几点？）和紧急程度。','text',NULL,'2026-02-03 08:39:09'),('bdeecf05-908d-4f87-9f07-68f86ff39efd','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排明天上午7点的会议\n\n已创建 1 个任务：\n- **会议** (责任人: 我, 截止: 2026-02-04 07:00)','text',NULL,'2026-02-03 08:48:14'),('be1cefd1-ce3e-4c26-9a6d-da516d6c1f56','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 08:52:59'),('c0c3d2bf-1b86-4dc5-9616-b4be6168564d','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:27:13'),('c5bd988e-533c-4ea7-b664-f94a48879547','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到，明天上午开会已知晓。请继续补充会议的具体时间（几点？）以及紧急程度。','text',NULL,'2026-02-03 08:48:08'),('c5c52367-b5b7-4f2f-99e7-1945ab444463','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排明天上午9点的会议\n\n已创建 1 个任务：\n- **会议** (责任人: 我, 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 08:33:58'),('c6464ba6-dafd-4c97-a53b-ae4af5a6dd8a','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到您要明天下午开会的消息。请补充会议主题、具体时间（精确到点）、参会人以及优先级。','text',NULL,'2026-02-04 09:12:17'),('c66d87eb-1fcd-4296-a3a0-0e79fa18ef48','23255a62-641a-41c4-a3eb-4b11d3876987','user','介绍一下帝欧水华报销标准','text',NULL,'2026-02-03 08:06:55'),('c674f355-045c-401b-9771-055ed719ed04','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请补充会议的具体时间（几点？）和紧急程度。','text',NULL,'2026-02-03 08:39:37'),('c7ff83c5-4168-499b-bffa-019581697af6','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到，明天上午开会已知晓。请继续补充会议的具体时间（几点？）以及紧急程度。','text',NULL,'2026-02-03 08:46:32'),('c9c6be74-fdfe-42f3-889b-65e4d172e24f','8a760c16-cb50-4154-a0d6-f0ef9fbd1560','user','你能干那些事情？','text',NULL,'2026-02-03 09:53:03'),('c9dd0c63-f196-4518-a417-fc88f3c1ac46','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','你好 请问你是谁','text',NULL,'2026-02-04 08:29:34'),('ca288540-3e75-466f-ba75-fb2c3bdc95ec','c27b9352-4053-4ab4-8cd1-68b252eea92b','assistant','阿基米德原理是古希腊科学家阿基米德在公元前3世纪提出的一个物理学原理，它描述了浮力的本质。以下是阿基米德原理的详细解释：\n\n阿基米德原理指出：一个物体在流体（液体或气体）中所受的浮力，等于它排开流体体积的重量。\n\n具体来说，有以下几点：\n\n1. **浮力的定义**：当一个物体部分或全部浸入流体中时，它会受到一个向上的力，这个力就是浮力。\n\n2. **浮力的大小**：浮力的大小等于物体排开的流体体积的重量。换句话说，如果一个物体排开了一体积为V的流体，那么它所受的浮力就是该体积流体的重量。\n\n3. **流体密度**：浮力还与流体的密度ρ有关，因为重量是由流体密度和排开体积的乘积决定的，即浮力F = ρVg，其中g是重力加速度。\n\n4. **浮力的方向**：浮力的方向始终是垂直向上的，与物体的重量方向相反。\n\n阿基米德原理是流体力学和工程学中一个非常重要的概念，它被广泛应用于船舶设计、潜水艇操作、气象学等领域。','text',NULL,'2026-02-04 08:30:21'),('cae1d55c-d201-4223-9d64-9cae4dd834db','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排会议：明天上午9点，主题“企业内部的转型”，参会人我，高优先级\n\n已创建 1 个任务：\n- **企业内部的转型** (责任人: 我, 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 08:53:34'),('cba7016e-90eb-4e6b-9465-6f468fd3c68d','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请问会议具体是在几点开始？','text',NULL,'2026-02-03 08:33:51'),('d10d8ec1-6358-4127-a66a-ccae0804ea97','d84aeb49-e3a6-432d-a94d-88758d3b025a','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **大模型会议** (责任人: 张小燕, 截止: 2026-02-05 09:00:00)','text',NULL,'2026-02-04 09:44:46'),('d1a22ca0-047f-4a31-9624-382128ac3236','23255a62-641a-41c4-a3eb-4b11d3876987','user','上午9点','text',NULL,'2026-02-03 08:33:56'),('d2cdb2e6-20ec-4ee3-b1dc-29af174fbf77','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','您好！如果您有任何问题或需要帮助，请随时告诉我。','text',NULL,'2026-02-04 09:37:53'),('d359a1eb-2695-4cd0-afe6-433e6335e31d','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧大事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级为紧急','text',NULL,'2026-02-03 09:12:20'),('d4df6378-2122-4962-bbf4-32ec7daeae06','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到您要安排明天下午的会议。请补充会议主题、具体时间（精确到点）、参会人以及优先级。','text',NULL,'2026-02-03 09:40:52'),('d609639c-00d2-48fc-9bd9-09b3130d7257','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请补充任务主题、具体时间、责任人和优先级。','text',NULL,'2026-02-03 09:04:39'),('d7de78bf-50f2-4e12-9312-5d15208d536c','23255a62-641a-41c4-a3eb-4b11d3876987','user','主题是帝欧中事、时间上午9点、参会人有小周，小乐，小皮蛋、优先级为紧急','text',NULL,'2026-02-03 09:26:42'),('d84f94f9-98ad-4e0b-8f25-eaced3d4d2fa','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','你好！有什么我可以帮您的？','text',NULL,'2026-02-04 09:45:08'),('d8b6af66-0aa7-4fd8-87fd-2ba1bbf9f907','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到主题：国家大事，责任人：周周，优先级：重要。请补充具体时间（精确到分钟/小时）。','text',NULL,'2026-02-03 09:05:15'),('d905d81c-97bd-4222-a50c-66609db59503','23255a62-641a-41c4-a3eb-4b11d3876987','user','李二，王麻子','text',NULL,'2026-02-03 08:39:36'),('dbacd84c-0f61-401d-b516-bdd1b5405b59','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 08:48:07'),('e0bc81a5-060c-47cb-8b4a-a1be1a0ebd54','23255a62-641a-41c4-a3eb-4b11d3876987','user','你好','text',NULL,'2026-02-03 09:04:37'),('e0c88c16-23f3-48a1-a177-4ec3c6f1236a','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排明天下午5点的会议\n\n已创建 1 个任务：\n- **和小周开会** (责任人: Sender, 截止: 2026-02-04 17:00)','text',NULL,'2026-02-03 08:00:46'),('e1603953-2aa7-427f-8217-7309670229e6','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天开个会','text',NULL,'2026-02-03 08:33:50'),('e276d5b4-b1b3-471e-be7c-1de790cfc919','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','\n已为您安排明天上午9点的会议\n\n已创建 1 个任务：\n- **帝欧大事** (责任人: 我, 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 09:12:23'),('e315228b-26ae-480f-a485-7adf1f4faa47','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天我要和姚聪开会，请帮我生成待办，紧急','text',NULL,'2026-02-03 08:00:13'),('e3d7652a-c459-40e1-80a2-257fe030f34d','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧中事** (责任人: [\'小周\', \'小乐\', \'小皮蛋\'], 截止: 2026-02-04 09:00)','text',NULL,'2026-02-03 09:32:49'),('e86f0e0b-778e-44f3-987c-519eab9bfcb6','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您安排明天上午7点的会议\n\n已创建 1 个任务：\n- **会议** (责任人: 我, 截止: 2026-02-04 07:00)','text',NULL,'2026-02-03 08:46:50'),('ead82898-dceb-42ca-b775-f29c3c06c110','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧中事** (责任人: [\'小周\', \'小乐\', \'小皮蛋\'], 截止: 明天上午9点)','text',NULL,'2026-02-03 09:26:44'),('ec872207-821d-4777-817c-d501b8eedd25','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 09:12:36'),('eee6c3ec-d9b6-46ad-964f-8c879be2944e','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到[明天上午我要开会]。请补充[主题]、[具体时间（精确到点）]、[责任人/参会人]、[优先级]','text',NULL,'2026-02-03 09:27:16'),('ef76e092-7943-4d95-8d6c-add85db75eec','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','请问会议的主题是什么？','text',NULL,'2026-02-03 08:32:26'),('f0286f70-a15c-435e-b94d-9a9b5854db87','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧高事** (责任人: 小周，小乐，小皮蛋, 截止: 2026-02-05 21:00)','text',NULL,'2026-02-04 09:12:28'),('f0427356-1ce3-4fa3-84dc-f4e27ae15a9e','d84aeb49-e3a6-432d-a94d-88758d3b025a','assistant','您好，请问有什么可以帮助您的？','text',NULL,'2026-02-04 09:43:42'),('f24b00cd-3f55-4a14-9c2a-4c03781c64f6','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','您好！有什么可以帮助您的吗？','text',NULL,'2026-02-04 09:10:48'),('f6039f9e-cd20-4d91-809a-7853cbec8bf2','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','收到。请补充参会人员。','text',NULL,'2026-02-03 08:39:22'),('f7ec1f2d-f502-44f0-8747-766fbff54acb','d84aeb49-e3a6-432d-a94d-88758d3b025a','user','你好','text',NULL,'2026-02-04 09:43:38'),('f860e6f2-12ff-4021-abac-69b830dc9753','23255a62-641a-41c4-a3eb-4b11d3876987','user','大概7点，重要','text',NULL,'2026-02-03 08:48:13'),('f9b01ea9-a73e-4247-9515-be32c1286f8b','23255a62-641a-41c4-a3eb-4b11d3876987','user','明天上午我要开会','text',NULL,'2026-02-03 08:38:48'),('fe40d04b-243f-4084-80e2-7e9d7eb11801','c27b9352-4053-4ab4-8cd1-68b252eea92b','user','请你介绍一下自己','text',NULL,'2026-02-04 08:29:44'),('fe645fa0-efd9-41ca-a432-16a9f41b4f62','23255a62-641a-41c4-a3eb-4b11d3876987','assistant','已为您创建相关待办事项\n\n已创建 1 个任务：\n- **帝欧高事** (责任人: [\'小周\', \'小乐\', \'小皮蛋\'], 截止: 2026-02-04 21:00)','text',NULL,'2026-02-03 09:41:02');
/*!40000 ALTER TABLE `shjl_chat_messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_chat_sessions`
--

DROP TABLE IF EXISTS `shjl_chat_sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_chat_sessions` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `title` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '会话标题',
  `summary` text COLLATE utf8mb4_unicode_ci COMMENT '会话摘要',
  `is_pinned` tinyint(1) DEFAULT '0' COMMENT '是否置顶',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `shjl_chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `shjl_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='聊天会话表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_chat_sessions`
--

LOCK TABLES `shjl_chat_sessions` WRITE;
/*!40000 ALTER TABLE `shjl_chat_sessions` DISABLE KEYS */;
INSERT INTO `shjl_chat_sessions` VALUES ('23255a62-641a-41c4-a3eb-4b11d3876987','74df104d-169c-4305-8205-0c74d68ba556','新对话','默认会话',0,'2026-02-03 07:25:23','2026-02-03 07:25:23',0),('8a760c16-cb50-4154-a0d6-f0ef9fbd1560','0a4ff789-b489-4b9e-a9cd-fa9b9c36c799','新对话','默认会话',0,'2026-02-03 09:53:03','2026-02-03 09:53:03',0),('9e67be86-5154-4865-a51c-b0c7efa26aa2','859dcd40-6f88-4aa6-8a97-81c831e94682','新对话','默认会话',0,'2026-02-03 09:22:13','2026-02-03 09:22:13',0),('c27b9352-4053-4ab4-8cd1-68b252eea92b','bdda5fbd-e8e9-4145-ae43-1cf62daeab20','新对话','默认会话',0,'2026-02-04 06:52:44','2026-02-04 06:52:44',0),('d84aeb49-e3a6-432d-a94d-88758d3b025a','e295b86a-7a24-4745-af18-9c8ab4210861','新对话','默认会话',0,'2026-02-04 06:16:49','2026-02-04 06:16:49',0);
/*!40000 ALTER TABLE `shjl_chat_sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_knowledge_documents`
--

DROP TABLE IF EXISTS `shjl_knowledge_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_knowledge_documents` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文档标题',
  `content` longtext COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '文档内容',
  `source_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '来源URL',
  `file_type` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '文件类型',
  `created_by` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '创建人ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `shjl_knowledge_documents_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `shjl_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识库文档表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_knowledge_documents`
--

LOCK TABLES `shjl_knowledge_documents` WRITE;
/*!40000 ALTER TABLE `shjl_knowledge_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_knowledge_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_meeting_attendees`
--

DROP TABLE IF EXISTS `shjl_meeting_attendees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_meeting_attendees` (
  `meeting_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会议ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `external_email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外部邮箱',
  `external_name` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外部姓名',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT 'pending' COMMENT '状态',
  PRIMARY KEY (`meeting_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `shjl_meeting_attendees_ibfk_1` FOREIGN KEY (`meeting_id`) REFERENCES `shjl_meetings` (`id`),
  CONSTRAINT `shjl_meeting_attendees_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `shjl_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会议参会人表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_meeting_attendees`
--

LOCK TABLES `shjl_meeting_attendees` WRITE;
/*!40000 ALTER TABLE `shjl_meeting_attendees` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_meeting_attendees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_meetings`
--

DROP TABLE IF EXISTS `shjl_meetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_meetings` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `organizer_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '组织者ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '会议标题',
  `description` text COLLATE utf8mb4_unicode_ci COMMENT '会议描述',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `location` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '会议地点',
  `wecom_schedule_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '企业微信日程ID',
  `summary` text COLLATE utf8mb4_unicode_ci COMMENT '会议纪要/总结',
  `transcript` longtext COLLATE utf8mb4_unicode_ci COMMENT '会议转写记录',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `organizer_id` (`organizer_id`),
  CONSTRAINT `shjl_meetings_ibfk_1` FOREIGN KEY (`organizer_id`) REFERENCES `shjl_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会议表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_meetings`
--

LOCK TABLES `shjl_meetings` WRITE;
/*!40000 ALTER TABLE `shjl_meetings` DISABLE KEYS */;
INSERT INTO `shjl_meetings` VALUES ('3ee3e884-8265-4b2f-ab4a-682d43479210','0a4ff789-b489-4b9e-a9cd-fa9b9c36c799','会议纪要',NULL,'2026-02-04 19:40:51','2026-02-04 19:40:51','腾讯会议',NULL,'','','2026-02-04 19:40:51','2026-02-04 19:40:51');
/*!40000 ALTER TABLE `shjl_meetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_ontology_edges`
--

DROP TABLE IF EXISTS `shjl_ontology_edges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_ontology_edges` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `source_node_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '源节点ID',
  `target_node_id` char(36) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '目标节点ID',
  `relation_type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '关系类型',
  `weight` float DEFAULT '1' COMMENT '权重',
  `properties` json DEFAULT NULL COMMENT '属性(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_edges_source` (`source_node_id`),
  KEY `idx_edges_target` (`target_node_id`),
  CONSTRAINT `shjl_ontology_edges_ibfk_1` FOREIGN KEY (`source_node_id`) REFERENCES `shjl_ontology_nodes` (`id`),
  CONSTRAINT `shjl_ontology_edges_ibfk_2` FOREIGN KEY (`target_node_id`) REFERENCES `shjl_ontology_nodes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='本体关系边表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_ontology_edges`
--

LOCK TABLES `shjl_ontology_edges` WRITE;
/*!40000 ALTER TABLE `shjl_ontology_edges` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_ontology_edges` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_ontology_nodes`
--

DROP TABLE IF EXISTS `shjl_ontology_nodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_ontology_nodes` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标签/名称',
  `type` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '类型',
  `properties` json DEFAULT NULL COMMENT '属性(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='本体节点表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_ontology_nodes`
--

LOCK TABLES `shjl_ontology_nodes` WRITE;
/*!40000 ALTER TABLE `shjl_ontology_nodes` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_ontology_nodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_roles`
--

DROP TABLE IF EXISTS `shjl_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_roles` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '角色名称',
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '描述',
  `permissions` json DEFAULT NULL COMMENT '权限列表(JSON)',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_roles`
--

LOCK TABLES `shjl_roles` WRITE;
/*!40000 ALTER TABLE `shjl_roles` DISABLE KEYS */;
/*!40000 ALTER TABLE `shjl_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_todos`
--

DROP TABLE IF EXISTS `shjl_todos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_todos` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `user_id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户ID',
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '标题',
  `content` longtext COLLATE utf8mb4_unicode_ci COMMENT '内容',
  `type` enum('task','email','approval','meeting','chat_record') COLLATE utf8mb4_unicode_ci DEFAULT 'task' COMMENT '类型',
  `priority` enum('urgent','high','normal','low') COLLATE utf8mb4_unicode_ci DEFAULT 'normal' COMMENT '优先级',
  `status` enum('pending','in_progress','completed','archived') COLLATE utf8mb4_unicode_ci DEFAULT 'pending' COMMENT '状态',
  `sender` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '发送人',
  `source_origin` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '来源',
  `source_message_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '来源消息ID',
  `ai_summary` text COLLATE utf8mb4_unicode_ci COMMENT 'AI摘要',
  `ai_action` text COLLATE utf8mb4_unicode_ci COMMENT 'AI建议动作',
  `is_user_task` tinyint(1) DEFAULT '0' COMMENT '是否用户任务',
  `text_type` int DEFAULT '0' COMMENT '文本类型',
  `due_at` datetime DEFAULT NULL COMMENT '截止时间',
  `completed_at` datetime DEFAULT NULL COMMENT '完成时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  KEY `idx_todos_user_status` (`user_id`,`status`),
  KEY `idx_todos_created_at` (`created_at` DESC),
  CONSTRAINT `shjl_todos_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `shjl_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='待办事项表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_todos`
--

LOCK TABLES `shjl_todos` WRITE;
/*!40000 ALTER TABLE `shjl_todos` DISABLE KEYS */;
INSERT INTO `shjl_todos` VALUES ('1218d11f-f334-446d-9d49-fe1b0b977e76','74df104d-169c-4305-8205-0c74d68ba556','帝欧中事','\n责任人: 小周, 小乐, 小皮蛋\n截止时间: 2026-02-04 09:00','chat_record','high','pending','小周, 小乐, 小皮蛋',NULL,NULL,'【截止: 2026-02-04 09:00】 ',NULL,0,0,'2026-02-04 09:00:00',NULL,'2026-02-03 17:32:50','2026-02-03 17:32:50',0),('20fb81f5-0486-4684-838c-61e6d5bd2d3a','bdda5fbd-e8e9-4145-ae43-1cf62daeab20','帝欧战略','\n责任人: 小周, 小刘, 小王\n截止时间: 2026-02-05 15:00','chat_record','urgent','pending','小周, 小刘, 小王',NULL,NULL,'【截止: 2026-02-05 15:00】 ',NULL,0,0,'2026-02-05 15:00:00',NULL,'2026-02-04 16:35:26','2026-02-04 16:35:26',0),('292521e5-c1a9-429f-b77e-a8d960eb0813','74df104d-169c-4305-8205-0c74d68ba556','帝欧中事','\n责任人: 小周, 小乐, 小皮蛋\n截止时间: 明天上午9点','chat_record','high','pending','小周, 小乐, 小皮蛋',NULL,NULL,'【截止: 明天上午9点】 ',NULL,0,0,NULL,NULL,'2026-02-03 17:26:45','2026-02-03 17:26:45',0),('2a4ed0ad-d19b-4c98-bdb4-1cbc61d638c9','74df104d-169c-4305-8205-0c74d68ba556','和姚聪开会','明天下午和姚聪开会\n责任人: Sender\n截止时间: 2026-02-04 15:00','chat_record','urgent','pending','Sender',NULL,NULL,'【截止: 2026-02-04 15:00】 明天下午和姚聪开会',NULL,0,0,'2026-02-04 15:00:00',NULL,'2026-02-03 15:09:52','2026-02-03 15:09:52',0),('2c4a34a3-5151-422a-9f32-b0d476f2e02a','74df104d-169c-4305-8205-0c74d68ba556','会议','会议\n责任人: 我\n截止时间: 2026-02-04 09:00','chat_record','high','pending','我',NULL,NULL,'【截止: 2026-02-04 09:00】 会议',NULL,0,0,'2026-02-04 09:00:00',NULL,'2026-02-03 16:33:58','2026-02-03 16:33:58',0),('3b033dd2-7561-4469-8664-4400288d6440','e295b86a-7a24-4745-af18-9c8ab4210861','大模型会议','讨论大模型相关事宜\n责任人: 张小燕\n截止时间: 2026-02-05 09:00:00','meeting','high','pending','张小燕',NULL,NULL,'【截止: 2026-02-05 09:00:00】 讨论大模型相关事宜',NULL,0,0,NULL,NULL,'2026-02-04 17:44:47','2026-02-04 17:44:47',0),('3c490288-c30e-4b79-9903-0b2a4b1f1c86','74df104d-169c-4305-8205-0c74d68ba556','[研发 - 小柯] 开发运营后台临时查询接口','任务详情: 1. 今天18:00前完成；2. 接口需查询用户待办任务完成情况；3. 返回字段包含用户ID、任务名称、完成时间；4. 开发完成后同步给运营-小夏\n责任人: 研发 - 小柯\n截止时间: 2026-02-03 18:00','chat_record','urgent','pending','XiLe',NULL,NULL,'截止日期: 2026-02-03 18:00',NULL,0,1,NULL,NULL,'2026-02-03 09:50:43','2026-02-03 09:50:43',0),('3d07a40b-e257-4ff5-a7cb-febadd74181b','74df104d-169c-4305-8205-0c74d68ba556','针对企业的数据化整形','针对企业的数据化整形\n责任人: 我\n截止时间: 2026-02-04 09:00','chat_record','high','pending','我',NULL,NULL,'【截止: 2026-02-04 09:00】 针对企业的数据化整形',NULL,0,0,'2026-02-04 09:00:00',NULL,'2026-02-03 16:32:48','2026-02-03 16:32:48',0),('46edc891-804b-4d45-bb98-c01af31e6fab','74df104d-169c-4305-8205-0c74d68ba556','和小周开会','和小周开会\n责任人: Sender\n截止时间: 2026-02-04 17:00','chat_record','high','pending','Sender',NULL,NULL,'【截止: 2026-02-04 17:00】 和小周开会',NULL,0,0,'2026-02-04 17:00:00',NULL,'2026-02-03 16:00:47','2026-02-03 16:00:47',0),('530cef1d-f87c-4763-8fcc-0f4af86702dd','74df104d-169c-4305-8205-0c74d68ba556','与姚聪开会','明天下午3点与姚聪开会\n责任人: Sender（发送者）\n截止时间: 2026-02-04 15:00','chat_record','urgent','pending','Sender（发送者）',NULL,NULL,'【截止: 2026-02-04 15:00】 明天下午3点与姚聪开会',NULL,0,0,'2026-02-04 15:00:00',NULL,'2026-02-03 09:37:42','2026-02-03 09:37:42',0),('557aa781-b02f-4e78-9194-6c2d72cc6429','f8790cd0-6b74-441a-841f-f3e7879eb53b','与世界上最帅的小堃开会','明天下午3点开会\n责任人: Sender（发送者）\n截止时间: 2026-02-04 15:00','chat_record','urgent','pending','Sender（发送者）',NULL,NULL,'【截止: 2026-02-04 15:00】 明天下午3点开会',NULL,0,0,'2026-02-04 15:00:00',NULL,'2026-02-03 10:00:52','2026-02-03 10:00:52',0),('56cf6e57-fa95-41f8-8738-847d0d7f08b7','74df104d-169c-4305-8205-0c74d68ba556','会议','会议\n责任人: 我\n截止时间: 2026-02-04 07:00','chat_record','urgent','pending','我',NULL,NULL,'【截止: 2026-02-04 07:00】 会议',NULL,0,0,'2026-02-04 07:00:00',NULL,'2026-02-03 16:48:15','2026-02-03 16:48:15',0),('5a7af387-d7a2-4a24-b2c4-cfe525b51e37','74df104d-169c-4305-8205-0c74d68ba556','帝欧高事','明天下午9点开会\n责任人: 小周，小乐，小皮蛋\n截止时间: 2026-02-05 21:00','meeting','urgent','pending','小周，小乐，小皮蛋',NULL,NULL,'【截止: 2026-02-05 21:00】 明天下午9点开会',NULL,0,0,'2026-02-05 21:00:00',NULL,'2026-02-04 17:12:29','2026-02-04 17:12:29',0),('67bc4c20-b1a8-452c-925c-e9996b11162a','74df104d-169c-4305-8205-0c74d68ba556','企业内部的转型','参会人：我\n责任人: 我\n截止时间: 2026-02-04 09:00','chat_record','urgent','pending','我',NULL,NULL,'【截止: 2026-02-04 09:00】 参会人：我',NULL,0,0,'2026-02-04 09:00:00',NULL,'2026-02-03 16:53:34','2026-02-03 16:53:34',0),('6bf062ee-dcb5-4111-bde7-732544d62ccf','74df104d-169c-4305-8205-0c74d68ba556','你好','无具体任务内容\n责任人: Sender（发送者）\n截止时间: 2026-02-03 18:00','chat_record','high','pending','Sender（发送者）',NULL,NULL,'【截止: 2026-02-03 18:00】 无具体任务内容',NULL,0,0,'2026-02-03 18:00:00',NULL,'2026-02-03 15:04:11','2026-02-03 15:04:11',0),('7b592e08-ed64-4831-8cbc-f18ba9001a4c','74df104d-169c-4305-8205-0c74d68ba556','[研发 - 小柯] 修复运营后台任务导出功能','任务详情: 1. 周六12:00前完成；2. 修复Excel导出乱码问题；3. 增加按时间筛选功能；4. 修复完成后通知运营小夏测试，测试通过后上线\n责任人: 研发 - 小柯\n截止时间: 2026-02-08 12:00','chat_record','urgent','pending','XiLe',NULL,NULL,'截止日期: 2026-02-08 12:00',NULL,0,1,NULL,NULL,'2026-02-03 09:49:41','2026-02-03 09:49:41',0),('8ab12c92-0339-47ba-b32d-9b875b91fefb','74df104d-169c-4305-8205-0c74d68ba556','[研发 - 小柯] 修复运营后台任务导出功能','任务详情: 1. 周六12:00前完成；2. 修复Excel导出乱码问题；3. 增加按时间筛选功能；4. 修复完成后通知运营-小夏测试，测试通过后上线\n责任人: 研发 - 小柯\n截止时间: 2026-02-08 12:00','chat_record','urgent','pending','XiLe',NULL,NULL,'截止日期: 2026-02-08 12:00',NULL,0,1,NULL,NULL,'2026-02-03 09:50:44','2026-02-03 09:50:44',0),('934bba83-e9c0-4cf4-b921-e91a7c3b4d8b','74df104d-169c-4305-8205-0c74d68ba556','你好','无具体任务内容\n责任人: Sender（发送者）\n截止时间: 2026-02-03 18:00','chat_record','high','pending','Sender（发送者）',NULL,NULL,'【截止: 2026-02-03 18:00】 无具体任务内容',NULL,0,0,'2026-02-03 18:00:00',NULL,'2026-02-03 15:04:00','2026-02-03 15:04:00',0),('9771f5ad-9bb7-4f32-b687-48746f1c485a','74df104d-169c-4305-8205-0c74d68ba556','和姚聪开会','明天下午和姚聪开会\n责任人: Sender\n截止时间: 2026-02-04 15:00','chat_record','urgent','pending','Sender',NULL,NULL,'【截止: 2026-02-04 15:00】 明天下午和姚聪开会',NULL,0,0,'2026-02-04 15:00:00',NULL,'2026-02-03 15:31:39','2026-02-03 15:31:39',0),('ad33d42a-609f-44f7-92be-f8ba1357186c','74df104d-169c-4305-8205-0c74d68ba556','和姚聪开会','与姚聪的会议\n责任人: Sender\n截止时间: 2026-02-04 15:00','chat_record','urgent','pending','Sender',NULL,NULL,'【截止: 2026-02-04 15:00】 与姚聪的会议',NULL,0,0,'2026-02-04 15:00:00',NULL,'2026-02-03 16:00:16','2026-02-03 16:00:16',0),('afa83620-b5f5-498d-989b-47aa8a5f2f73','74df104d-169c-4305-8205-0c74d68ba556','国家大事','\n责任人: 周周\n截止时间: 2026-02-04 08:00','chat_record','high','pending','周周',NULL,NULL,'【截止: 2026-02-04 08:00】 ',NULL,0,0,'2026-02-04 08:00:00',NULL,'2026-02-03 17:05:32','2026-02-03 17:05:32',0),('befce2b3-bd31-4bf8-ab66-7b86f1897539','74df104d-169c-4305-8205-0c74d68ba556','帝欧高事','\n责任人: 小周, 小乐, 小皮蛋\n截止时间: 2026-02-04 21:00','chat_record','urgent','pending','小周, 小乐, 小皮蛋',NULL,NULL,'【截止: 2026-02-04 21:00】 ',NULL,0,0,'2026-02-04 21:00:00',NULL,'2026-02-03 17:41:03','2026-02-03 17:41:03',0),('c6bbc3df-d0da-48a4-a656-b04600a05fdc','74df104d-169c-4305-8205-0c74d68ba556','帝欧中事','\n责任人: 小周, 小乐, 小皮蛋\n截止时间: 明天上午9点','chat_record','high','pending','小周, 小乐, 小皮蛋',NULL,NULL,'【截止: 明天上午9点】 ',NULL,0,0,NULL,NULL,'2026-02-03 17:27:41','2026-02-03 17:27:41',0),('c9443bb8-390a-48b7-a478-c3cd23b80d3a','0a4ff789-b489-4b9e-a9cd-fa9b9c36c799','【会议】会议纪要','【会议纪要】\n...\n\n已提取待办: 0条','meeting','high','completed','会议助手','meeting_minutes','3ee3e884-8265-4b2f-ab4a-682d43479210',NULL,NULL,0,0,NULL,NULL,'2026-02-04 19:40:51','2026-02-04 19:40:51',0),('cbabd7b4-e487-48c4-aa4d-15351da7ef3f','74df104d-169c-4305-8205-0c74d68ba556','会议','明天上午7点的会议\n责任人: 我\n截止时间: 2026-02-04 07:00','chat_record','urgent','pending','我',NULL,NULL,'【截止: 2026-02-04 07:00】 明天上午7点的会议',NULL,0,0,'2026-02-04 07:00:00',NULL,'2026-02-03 16:46:50','2026-02-03 16:46:50',0),('e629cef7-63a0-43bb-9973-ecd315da9d66','74df104d-169c-4305-8205-0c74d68ba556','[研发 - 小柯] 开发运营后台临时查询接口','任务详情: 1. 今天18:00前完成；2. 接口需查询用户待办任务完成情况；3. 返回字段包含用户ID、任务名称、完成时间；4. 开发完成后同步给运营小夏\n责任人: 研发 - 小柯\n截止时间: 2026-02-03 18:00','chat_record','urgent','pending','XiLe',NULL,NULL,'截止日期: 2026-02-03 18:00',NULL,0,1,NULL,NULL,'2026-02-03 09:49:41','2026-02-03 09:49:41',0),('e970df8b-c7ff-4bfc-b109-a90ed2e9dbba','74df104d-169c-4305-8205-0c74d68ba556','与李逵开会','明天下午3点与李逵开会\n责任人: Sender（发送者）\n截止时间: 2026-02-04 15:00','chat_record','urgent','pending','Sender（发送者）',NULL,NULL,'【截止: 2026-02-04 15:00】 明天下午3点与李逵开会',NULL,0,0,'2026-02-04 15:00:00',NULL,'2026-02-03 09:54:15','2026-02-03 09:54:15',0),('ebdaf9c2-34d3-496e-a177-b9524857e678','bdda5fbd-e8e9-4145-ae43-1cf62daeab20','我的财富','\n责任人: 乐乐, 堃堃\n截止时间: 2026-02-05 15:00','chat_record','urgent','pending','乐乐, 堃堃',NULL,NULL,'【截止: 2026-02-05 15:00】 ',NULL,0,0,'2026-02-05 15:00:00',NULL,'2026-02-04 14:56:02','2026-02-04 14:56:02',0),('fdb5026e-5f49-4c28-8415-859b7e3d2e3e','74df104d-169c-4305-8205-0c74d68ba556','帝欧高事','\n责任人: 小周, 小乐, 小皮蛋\n截止时间: 2026-02-04 09:00','chat_record','high','pending','小周, 小乐, 小皮蛋',NULL,NULL,'【截止: 2026-02-04 09:00】 ',NULL,0,0,'2026-02-04 09:00:00',NULL,'2026-02-03 17:34:05','2026-02-03 17:34:05',0);
/*!40000 ALTER TABLE `shjl_todos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shjl_users`
--

DROP TABLE IF EXISTS `shjl_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shjl_users` (
  `id` char(36) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '主键ID',
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码哈希',
  `wecom_userid` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '企业微信UserID',
  `full_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '全名',
  `avatar_url` text COLLATE utf8mb4_unicode_ci COMMENT '头像URL',
  `role_id` int DEFAULT NULL COMMENT '角色ID',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否激活',
  `last_login_at` datetime DEFAULT NULL COMMENT '最后登录时间',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) DEFAULT '0' COMMENT '是否删除',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `wecom_userid` (`wecom_userid`),
  KEY `role_id` (`role_id`),
  KEY `idx_users_wecom_userid` (`wecom_userid`),
  KEY `idx_users_email` (`email`),
  CONSTRAINT `shjl_users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `shjl_roles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shjl_users`
--

LOCK TABLES `shjl_users` WRITE;
/*!40000 ALTER TABLE `shjl_users` DISABLE KEYS */;
INSERT INTO `shjl_users` VALUES ('0a4ff789-b489-4b9e-a9cd-fa9b9c36c799','xiejian',NULL,'$pbkdf2-sha256$29000$xDgHwHivNWbsHSNkjLHWOg$lMAGIbhqOuwEXGrvH/RbjaIIoye/UpKm7klWfcG2iA4',NULL,NULL,NULL,NULL,1,NULL,'2026-02-03 09:21:53','2026-02-03 09:21:53',0),('74df104d-169c-4305-8205-0c74d68ba556','admin',NULL,'$pbkdf2-sha256$29000$zDmHkNJaS2ntvbfWeg8h5A$fDJjbRAQJJVaKy2jB..YDtvBsSP4KVTIDn00Ioj0y2k',NULL,NULL,NULL,NULL,1,NULL,'2026-02-02 09:28:12','2026-02-02 09:28:12',0),('859dcd40-6f88-4aa6-8a97-81c831e94682','12345',NULL,'$pbkdf2-sha256$29000$AuD8HwNAiJFSSql1jnEOoQ$j5ixpMm5L1nLSOKD6aMWjHEc0orhetEs8wCB.nespPc',NULL,NULL,NULL,NULL,1,NULL,'2026-02-03 09:21:20','2026-02-03 09:21:20',0),('bdda5fbd-e8e9-4145-ae43-1cf62daeab20','zzk',NULL,'$pbkdf2-sha256$29000$aa2VkvL.X.s9R8gZg5Aypg$lbkeLnHjCelZCPHR68xmeHBI.9PCss01TqXCITw46Gc',NULL,NULL,NULL,NULL,1,NULL,'2026-02-03 01:50:23','2026-02-03 01:50:23',0),('e295b86a-7a24-4745-af18-9c8ab4210861','yc',NULL,'$pbkdf2-sha256$29000$5fyfk7LWmvPem5MyBqAUIg$UpalXoLrWYdhUle9sWo86Xuagk..vg7oBpPTkl.z4eo',NULL,NULL,NULL,NULL,1,NULL,'2026-02-04 06:16:30','2026-02-04 06:16:30',0),('f8790cd0-6b74-441a-841f-f3e7879eb53b','aaaa123',NULL,'$pbkdf2-sha256$29000$shYi5HwPwfhfKyUkBECIkQ$/afGn2/DnYRr4UzmaqYeWtEZa7ZdEbVfmclSLh9QcME',NULL,NULL,NULL,NULL,1,NULL,'2026-02-03 01:53:25','2026-02-03 01:53:25',0);
/*!40000 ALTER TABLE `shjl_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_bank`
--

DROP TABLE IF EXISTS `sys_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_bank` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '统一主键ID',
  `account_no` varchar(100) NOT NULL COMMENT '银行账号 (OSN:银行账号 / DW:Code)',
  `account_name` varchar(255) DEFAULT NULL COMMENT '账户名称/户名',
  `bank_name` varchar(255) DEFAULT NULL COMMENT '开户行名称',
  `cnaps_code` varchar(50) DEFAULT NULL COMMENT '联行号',
  `currency_code` varchar(20) DEFAULT 'CNY' COMMENT '币种',
  `current_balance` decimal(20,2) DEFAULT '0.00' COMMENT '当前余额 (需每日ETL更新)',
  `frozen_amount` decimal(20,2) DEFAULT '0.00' COMMENT '冻结金额',
  `balance_updated_at` datetime DEFAULT NULL COMMENT '余额最后同步时间',
  `owner_org_name` varchar(255) DEFAULT NULL COMMENT '归属组织名称',
  `account_type` varchar(50) DEFAULT NULL COMMENT '账户类型',
  `usage_type` varchar(50) DEFAULT NULL COMMENT '用途分类',
  `status` varchar(20) DEFAULT 'NORMAL' COMMENT '统一状态',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否有效',
  `open_date` date DEFAULT NULL COMMENT '开户日期',
  `close_date` date DEFAULT NULL COMMENT '销户日期',
  `source_system` varchar(20) NOT NULL COMMENT '来源系统: OSN / DW',
  `original_id` varchar(100) DEFAULT NULL COMMENT '原系统主键ID',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_source_acc` (`source_system`,`account_no`),
  KEY `idx_balance` (`current_balance`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='集团银行账户主表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_bank`
--

LOCK TABLES `sys_bank` WRITE;
/*!40000 ALTER TABLE `sys_bank` DISABLE KEYS */;
INSERT INTO `sys_bank` VALUES (1,'TEST-BANK-001','测试账户-北京分公司','中国农业银行',NULL,'CNY',1000.50,0.00,NULL,NULL,NULL,NULL,'NORMAL',1,NULL,NULL,'DW',NULL,'2026-02-04 11:42:12','2026-02-04 11:50:56',NULL),(2,'DW-BANK-001','帝王洁具股份有限公司','招商银行成都分行','308651000123','CNY',2500000.00,50000.00,NULL,'成都总部','基本户','主营业务','NORMAL',1,'2019-06-01',NULL,'DW',NULL,'2026-02-04 11:59:17','2026-02-04 12:30:03',NULL),(3,'6222021234567890123','广东欧神诺陶瓷有限公司','中国工商银行佛山分行','308651000123','CNY',2500000.00,0.00,NULL,'佛山基地','基本户','主营业务','NORMAL',1,'2019-06-01',NULL,'OSN',NULL,'2026-02-04 11:59:17','2026-02-04 12:30:04',NULL);
/*!40000 ALTER TABLE `sys_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_bank_ext_dw`
--

DROP TABLE IF EXISTS `sys_bank_ext_dw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_bank_ext_dw` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `master_id` bigint NOT NULL COMMENT '关联主表ID',
  `sys_version` varchar(50) DEFAULT NULL,
  `bank_ref_id` varchar(100) DEFAULT NULL,
  `org_ref_id` varchar(100) DEFAULT NULL,
  `customer_id` varchar(100) DEFAULT NULL,
  `supplier_id` varchar(100) DEFAULT NULL,
  `employee_id` varchar(100) DEFAULT NULL,
  `user_type` int DEFAULT NULL,
  `is_base_account` tinyint(1) DEFAULT NULL,
  `is_allow_sub` tinyint(1) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  `is_net_bank` tinyint(1) DEFAULT NULL,
  `is_reserved` tinyint(1) DEFAULT NULL,
  `is_private` tinyint(1) DEFAULT NULL,
  `is_elec_note` tinyint(1) DEFAULT NULL,
  `is_multi_curr` tinyint(1) DEFAULT NULL,
  `inc_exp_direction` int DEFAULT NULL,
  `ctrl_inc_exp_item` int DEFAULT NULL,
  `check_sign_flag` int DEFAULT NULL,
  `signature_code` varchar(255) DEFAULT NULL,
  `effective_start` datetime DEFAULT NULL,
  `effective_end` datetime DEFAULT NULL,
  `freeze_date` datetime DEFAULT NULL,
  `freeze_reason` varchar(255) DEFAULT NULL,
  `close_reason` varchar(255) DEFAULT NULL,
  `desc_flex_field_context_value` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_1` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_2` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_3` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_4` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_5` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_6` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_7` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_8` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_9` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_10` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_11` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_12` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_13` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_14` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_15` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_16` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_17` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_18` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_19` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_20` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_21` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_22` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_23` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_24` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_25` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_26` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_27` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_28` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_29` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_30` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_31` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_32` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_33` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_34` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_35` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_36` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_37` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_38` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_39` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_40` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_41` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_42` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_43` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_44` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_45` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_46` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_47` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_48` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_49` varchar(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_50` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_1` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_2` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_3` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_4` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_5` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_6` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_7` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_8` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_9` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_10` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_11` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_12` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_13` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_14` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_15` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_16` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_17` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_18` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_19` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_20` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_21` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_22` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_23` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_24` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_25` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_26` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_27` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_28` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_29` varchar(150) DEFAULT NULL,
  `desc_flex_field_private_seg_30` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_master_dw` (`master_id`),
  CONSTRAINT `fk_dw_master` FOREIGN KEY (`master_id`) REFERENCES `sys_bank` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='帝王银行账户扩展表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_bank_ext_dw`
--

LOCK TABLES `sys_bank_ext_dw` WRITE;
/*!40000 ALTER TABLE `sys_bank_ext_dw` DISABLE KEYS */;
INSERT INTO `sys_bank_ext_dw` VALUES (1,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,'1.0','BANK-REF-001','ORG-REF-001',NULL,NULL,NULL,1,1,0,1,1,0,0,1,0,0,0,1,'SIG-001','2019-06-01 00:00:00',NULL,NULL,NULL,NULL,'BankContext',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_bank_ext_dw` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_bank_ext_osn`
--

DROP TABLE IF EXISTS `sys_bank_ext_osn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_bank_ext_osn` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `master_id` bigint NOT NULL COMMENT '关联主表ID',
  `open_type` varchar(50) DEFAULT NULL COMMENT '开户类型',
  `settlement_center` varchar(100) DEFAULT NULL COMMENT '结算中心',
  `sub_org_name` varchar(100) DEFAULT NULL COMMENT '所属组织',
  `internal_code` varchar(100) DEFAULT NULL COMMENT '账户编码(内部)',
  `account_nature` varchar(100) DEFAULT NULL COMMENT '账户性质',
  `tax_reg_no` varchar(100) DEFAULT NULL COMMENT '纳税登记号',
  `raw_status` varchar(50) DEFAULT NULL COMMENT '原始状态',
  `raw_account_state` varchar(50) DEFAULT NULL COMMENT '原始账户状态',
  `remark` text COMMENT '备注',
  PRIMARY KEY (`id`),
  KEY `idx_master_osn` (`master_id`),
  CONSTRAINT `fk_osn_master` FOREIGN KEY (`master_id`) REFERENCES `sys_bank` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='欧神诺银行账户扩展表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_bank_ext_osn`
--

LOCK TABLES `sys_bank_ext_osn` WRITE;
/*!40000 ALTER TABLE `sys_bank_ext_osn` DISABLE KEYS */;
INSERT INTO `sys_bank_ext_osn` VALUES (1,3,'对公','佛山结算中心','佛山基地','OSN-ACCT-001','一般户','91440000MA...','正常','正常','测试账户');
/*!40000 ALTER TABLE `sys_bank_ext_osn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_config`
--

DROP TABLE IF EXISTS `sys_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_config` (
  `config_id` int NOT NULL AUTO_INCREMENT COMMENT '参数主键',
  `config_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '参数名称',
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '参数键名',
  `config_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '参数键值',
  `config_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N' COMMENT '系统内置（Y是 N否）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`config_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='参数配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_config`
--

LOCK TABLES `sys_config` WRITE;
/*!40000 ALTER TABLE `sys_config` DISABLE KEYS */;
INSERT INTO `sys_config` VALUES (1,'主框架页-默认皮肤样式名称','sys.index.skinName','skin-blue','Y','admin','2025-01-06 16:34:06','',NULL,'蓝色 skin-blue、绿色 skin-green、紫色 skin-purple、红色 skin-red、黄色 skin-yellow'),(2,'用户管理-账号初始密码','sys.user.initPassword','123456','Y','admin','2025-01-06 16:34:06','',NULL,'初始化密码 123456'),(3,'主框架页-侧边栏主题','sys.index.sideTheme','theme-dark','Y','admin','2025-01-06 16:34:06','',NULL,'深色主题theme-dark，浅色主题theme-light'),(4,'账号自助-验证码开关','sys.account.captchaEnabled','true','Y','admin','2025-01-06 16:34:06','',NULL,'是否开启验证码功能（true开启，false关闭）'),(5,'账号自助-是否开启用户注册功能','sys.account.registerUser','false','Y','admin','2025-01-06 16:34:06','',NULL,'是否开启注册用户功能（true开启，false关闭）'),(6,'用户登录-黑名单列表','sys.login.blackIPList','','Y','admin','2025-01-06 16:34:06','',NULL,'设置登录IP黑名单限制，多个匹配项以;分隔，支持匹配（*通配、网段）');
/*!40000 ALTER TABLE `sys_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dept`
--

DROP TABLE IF EXISTS `sys_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dept` (
  `dept_id` bigint NOT NULL AUTO_INCREMENT COMMENT '部门id',
  `parent_id` bigint DEFAULT '0' COMMENT '父部门id',
  `ancestors` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '祖级列表',
  `dept_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '部门名称',
  `order_num` int DEFAULT '0' COMMENT '显示顺序',
  `leader` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '负责人',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '联系电话',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '邮箱',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '部门状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`dept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dept`
--

LOCK TABLES `sys_dept` WRITE;
/*!40000 ALTER TABLE `sys_dept` DISABLE KEYS */;
INSERT INTO `sys_dept` VALUES (100,0,'0','中国民航大学',0,'','','','0','0','admin','2025-01-06 16:33:55','admin','2025-12-02 16:57:44'),(101,100,'0,100','南院',1,'','','','0','0','admin','2025-01-06 16:33:55','admin','2025-12-02 16:57:53'),(102,100,'0,100','长沙分公司',2,'若依','15888888888','ry@qq.com','0','2','admin','2025-01-06 16:33:55','',NULL),(103,101,'0,100,101','教学楼1',1,'','','','0','0','admin','2025-01-06 16:33:55','admin','2025-12-02 16:58:33'),(104,101,'0,100,101','教学楼2',2,'','','','0','0','admin','2025-01-06 16:33:55','admin','2025-12-02 16:58:41'),(105,101,'0,100,101','教学楼3',3,'','','','0','0','admin','2025-01-06 16:33:55','admin','2025-12-02 16:58:48'),(106,101,'0,100,101','教学楼4',4,'','','','0','0','admin','2025-01-06 16:33:56','admin','2025-12-02 16:58:54'),(107,101,'0,100,101','运维部门',5,'若依','15888888888','ry@qq.com','0','2','admin','2025-01-06 16:33:56','',NULL),(108,102,'0,100,102','市场部门',1,'若依','15888888888','ry@qq.com','0','2','admin','2025-01-06 16:33:56','',NULL),(109,102,'0,100,102','财务部门',2,'若依','15888888888','ry@qq.com','0','2','admin','2025-01-06 16:33:56','',NULL),(110,100,'0,100','北院',2,NULL,NULL,NULL,'0','0','admin','2025-12-02 16:58:01','admin','2025-12-02 16:58:19'),(111,103,'0,100,101,103','教室1',0,NULL,NULL,NULL,'0','0','admin','2025-12-02 16:59:01','',NULL),(112,103,'0,100,101,103','教室2',1,NULL,NULL,NULL,'0','0','admin','2025-12-02 16:59:10','',NULL),(113,110,'0,100,110','教学楼1',0,NULL,NULL,NULL,'0','0','admin','2025-12-02 16:59:18','',NULL),(114,110,'0,100,110','教学楼2',1,NULL,NULL,NULL,'0','0','admin','2025-12-02 16:59:26','',NULL),(115,110,'0,100,110','教学楼3',2,NULL,NULL,NULL,'0','0','admin','2025-12-02 16:59:37','',NULL);
/*!40000 ALTER TABLE `sys_dept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dict_data`
--

DROP TABLE IF EXISTS `sys_dict_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_data` (
  `dict_code` bigint NOT NULL AUTO_INCREMENT COMMENT '字典编码',
  `dict_sort` int DEFAULT '0' COMMENT '字典排序',
  `dict_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典标签',
  `dict_value` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典键值',
  `dict_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典类型',
  `css_class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '表格回显样式',
  `is_default` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT 'N' COMMENT '是否默认（Y是 N否）',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`dict_code`)
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_data`
--

LOCK TABLES `sys_dict_data` WRITE;
/*!40000 ALTER TABLE `sys_dict_data` DISABLE KEYS */;
INSERT INTO `sys_dict_data` VALUES (1,1,'男','0','sys_user_sex','','','Y','0','admin','2025-01-06 16:34:05','',NULL,'性别男'),(2,2,'女','1','sys_user_sex','','','N','0','admin','2025-01-06 16:34:05','',NULL,'性别女'),(3,3,'未知','2','sys_user_sex','','','N','0','admin','2025-01-06 16:34:05','',NULL,'性别未知'),(4,1,'显示','0','sys_show_hide','','primary','Y','0','admin','2025-01-06 16:34:05','',NULL,'显示菜单'),(5,2,'隐藏','1','sys_show_hide','','danger','N','0','admin','2025-01-06 16:34:05','',NULL,'隐藏菜单'),(6,1,'正常','0','sys_normal_disable','','primary','Y','0','admin','2025-01-06 16:34:05','',NULL,'正常状态'),(7,2,'停用','1','sys_normal_disable','','danger','N','0','admin','2025-01-06 16:34:05','',NULL,'停用状态'),(8,1,'正常','0','sys_job_status','','primary','Y','0','admin','2025-01-06 16:34:05','',NULL,'正常状态'),(9,2,'暂停','1','sys_job_status','','danger','N','0','admin','2025-01-06 16:34:05','',NULL,'停用状态'),(10,1,'默认','DEFAULT','sys_job_group','','','Y','0','admin','2025-01-06 16:34:05','',NULL,'默认分组'),(11,2,'系统','SYSTEM','sys_job_group','','','N','0','admin','2025-01-06 16:34:05','',NULL,'系统分组'),(12,1,'是','Y','sys_yes_no','','primary','Y','0','admin','2025-01-06 16:34:05','',NULL,'系统默认是'),(13,2,'否','N','sys_yes_no','','danger','N','0','admin','2025-01-06 16:34:05','',NULL,'系统默认否'),(14,1,'通知','1','sys_notice_type','','warning','Y','0','admin','2025-01-06 16:34:05','',NULL,'通知'),(15,2,'公告','2','sys_notice_type','','success','N','0','admin','2025-01-06 16:34:05','',NULL,'公告'),(16,1,'正常','0','sys_notice_status','','primary','Y','0','admin','2025-01-06 16:34:06','',NULL,'正常状态'),(17,2,'关闭','1','sys_notice_status','','danger','N','0','admin','2025-01-06 16:34:06','',NULL,'关闭状态'),(18,99,'其他','0','sys_oper_type','','info','N','0','admin','2025-01-06 16:34:06','',NULL,'其他操作'),(19,1,'新增','1','sys_oper_type','','info','N','0','admin','2025-01-06 16:34:06','',NULL,'新增操作'),(20,2,'修改','2','sys_oper_type','','info','N','0','admin','2025-01-06 16:34:06','',NULL,'修改操作'),(21,3,'删除','3','sys_oper_type','','danger','N','0','admin','2025-01-06 16:34:06','',NULL,'删除操作'),(22,4,'授权','4','sys_oper_type','','primary','N','0','admin','2025-01-06 16:34:06','',NULL,'授权操作'),(23,5,'导出','5','sys_oper_type','','warning','N','0','admin','2025-01-06 16:34:06','',NULL,'导出操作'),(24,6,'导入','6','sys_oper_type','','warning','N','0','admin','2025-01-06 16:34:06','',NULL,'导入操作'),(25,7,'强退','7','sys_oper_type','','danger','N','0','admin','2025-01-06 16:34:06','',NULL,'强退操作'),(26,8,'生成代码','8','sys_oper_type','','warning','N','0','admin','2025-01-06 16:34:06','',NULL,'生成操作'),(27,9,'清空数据','9','sys_oper_type','','danger','N','0','admin','2025-01-06 16:34:06','',NULL,'清空操作'),(28,1,'成功','0','sys_common_status','','primary','N','0','admin','2025-01-06 16:34:06','',NULL,'正常状态'),(29,2,'失败','1','sys_common_status','','danger','N','0','admin','2025-01-06 16:34:06','',NULL,'停用状态'),(108,0,'vmns_ip','10.87.20.129','sys_vmns',NULL,'default','N','0','admin','2025-02-08 17:22:12','admin','2025-02-13 14:46:26',NULL),(109,1,'vmns_port','81','sys_vmns',NULL,'default','N','0','admin','2025-02-08 17:22:22','admin','2025-03-27 14:19:48',NULL),(110,2,'vmns_appName','vipservereventengineG1','sys_vmns',NULL,'default','N','0','admin','2025-02-08 17:22:46','',NULL,NULL),(111,3,'vmns_token','6ff5e4c9-8899-4dd3-94ed-9f2d10a48be9','sys_vmns',NULL,'default','N','0','admin','2025-02-08 17:23:08','admin','2025-02-08 17:40:25',NULL),(112,4,'org_code','500105022160000001','sys_vmns',NULL,'default','N','0','admin','2025-02-08 18:21:46','admin','2025-02-17 14:30:02',NULL),(113,5,'org_name','五粮液天网','sys_vmns',NULL,'default','N','0','admin','2025-02-08 18:21:55','admin','2025-02-17 14:30:15',NULL),(114,6,'center_code','50010502','sys_vmns',NULL,'default','N','0','admin','2025-02-08 18:22:12','admin','2025-02-17 14:30:39',NULL),(115,7,'center_name','五粮液天网','sys_vmns',NULL,'default','N','0','admin','2025-02-08 18:22:23','admin','2025-02-17 14:30:51',NULL),(116,8,'img_ip','10.87.23.42','sys_vmns',NULL,'default','N','0','admin','2025-02-17 14:28:06','admin','2025-02-18 14:55:11',NULL),(117,9,'img_port','8088','sys_vmns',NULL,'default','N','0','admin','2025-02-17 14:29:00','',NULL,NULL);
/*!40000 ALTER TABLE `sys_dict_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_dict_type`
--

DROP TABLE IF EXISTS `sys_dict_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_dict_type` (
  `dict_id` bigint NOT NULL AUTO_INCREMENT COMMENT '字典主键',
  `dict_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典名称',
  `dict_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '字典类型',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`dict_id`),
  UNIQUE KEY `dict_type` (`dict_type`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_dict_type`
--

LOCK TABLES `sys_dict_type` WRITE;
/*!40000 ALTER TABLE `sys_dict_type` DISABLE KEYS */;
INSERT INTO `sys_dict_type` VALUES (1,'用户性别','sys_user_sex','0','admin','2025-01-06 16:34:05','',NULL,'用户性别列表'),(2,'菜单状态','sys_show_hide','0','admin','2025-01-06 16:34:05','',NULL,'菜单状态列表'),(3,'系统开关','sys_normal_disable','0','admin','2025-01-06 16:34:05','',NULL,'系统开关列表'),(4,'任务状态','sys_job_status','0','admin','2025-01-06 16:34:05','',NULL,'任务状态列表'),(5,'任务分组','sys_job_group','0','admin','2025-01-06 16:34:05','',NULL,'任务分组列表'),(6,'系统是否','sys_yes_no','0','admin','2025-01-06 16:34:05','',NULL,'系统是否列表'),(7,'通知类型','sys_notice_type','0','admin','2025-01-06 16:34:05','',NULL,'通知类型列表'),(8,'通知状态','sys_notice_status','0','admin','2025-01-06 16:34:05','',NULL,'通知状态列表'),(9,'操作类型','sys_oper_type','0','admin','2025-01-06 16:34:05','',NULL,'操作类型列表'),(10,'系统状态','sys_common_status','0','admin','2025-01-06 16:34:05','',NULL,'登录状态列表'),(101,'推送数据','sys_vmns','0','admin','2025-02-08 17:21:12','',NULL,NULL);
/*!40000 ALTER TABLE `sys_dict_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_enterprise`
--

DROP TABLE IF EXISTS `sys_enterprise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_enterprise` (
  `enterprise_id` bigint NOT NULL AUTO_INCREMENT COMMENT '企业ID',
  `enterprise_name` varchar(100) NOT NULL COMMENT '企业名称',
  `enterprise_code` varchar(50) NOT NULL COMMENT '企业编码',
  `contact_person` varchar(50) DEFAULT NULL COMMENT '联系人',
  `contact_phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `contact_email` varchar(100) DEFAULT NULL COMMENT '联系邮箱',
  `access_key` varchar(64) NOT NULL COMMENT 'Access Key',
  `secret_key` varchar(128) NOT NULL COMMENT 'Secret Key',
  `status` char(1) DEFAULT '0' COMMENT '状态（0正常 1停用）',
  `del_flag` char(1) DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`enterprise_id`),
  UNIQUE KEY `idx_enterprise_code` (`enterprise_code`),
  UNIQUE KEY `idx_access_key` (`access_key`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='企业信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_enterprise`
--

LOCK TABLES `sys_enterprise` WRITE;
/*!40000 ALTER TABLE `sys_enterprise` DISABLE KEYS */;
INSERT INTO `sys_enterprise` VALUES (1,'aaaa','0001',NULL,NULL,NULL,'AKE04641532BE70DC98DFC8A290527E4AC','SK546dd254967c0c7bb6f63b3e477cd91dd8d91addeda7900c4bcc67f317ffd877','0','0','admin',NULL,'',NULL,NULL),(2,'bbb','bbb',NULL,NULL,NULL,'AKC77DA40C937B68ED810324CF4CFDDBC7','SK0f1ddaf3718265564794f79eb3cbd35b245b15c635ca722a23a684f9c3f17406','0','2','admin',NULL,'',NULL,NULL);
/*!40000 ALTER TABLE `sys_enterprise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_job`
--

DROP TABLE IF EXISTS `sys_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_job` (
  `job_id` bigint NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `job_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT 'DEFAULT' COMMENT '任务组名',
  `invoke_target` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调用目标字符串',
  `cron_expression` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT 'cron执行表达式',
  `misfire_policy` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '3' COMMENT '计划执行错误策略（1立即执行 2执行一次 3放弃执行）',
  `concurrent` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '1' COMMENT '是否并发执行（0允许 1禁止）',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '状态（0正常 1暂停）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '备注信息',
  PRIMARY KEY (`job_id`,`job_name`,`job_group`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='定时任务调度表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_job`
--

LOCK TABLES `sys_job` WRITE;
/*!40000 ALTER TABLE `sys_job` DISABLE KEYS */;
INSERT INTO `sys_job` VALUES (1,'系统默认（无参）','DEFAULT','ryTask.ryNoParams','0/10 * * * * ?','3','1','1','admin','2025-01-06 16:34:07','',NULL,''),(2,'系统默认（有参）','DEFAULT','ryTask.ryParams(\'ry\')','0/15 * * * * ?','3','1','1','admin','2025-01-06 16:34:07','',NULL,''),(3,'系统默认（多参）','DEFAULT','ryTask.ryMultipleParams(\'ry\', true, 2000L, 316.50D, 100)','0/20 * * * * ?','3','1','1','admin','2025-01-06 16:34:07','',NULL,'');
/*!40000 ALTER TABLE `sys_job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_job_log`
--

DROP TABLE IF EXISTS `sys_job_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_job_log` (
  `job_log_id` bigint NOT NULL AUTO_INCREMENT COMMENT '任务日志ID',
  `job_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '任务组名',
  `invoke_target` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '调用目标字符串',
  `job_message` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '日志信息',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '执行状态（0正常 1失败）',
  `exception_info` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '异常信息',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`job_log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='定时任务调度日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_job_log`
--

LOCK TABLES `sys_job_log` WRITE;
/*!40000 ALTER TABLE `sys_job_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_job_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_logininfor`
--

DROP TABLE IF EXISTS `sys_logininfor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_logininfor` (
  `info_id` bigint NOT NULL AUTO_INCREMENT COMMENT '访问ID',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '用户账号',
  `ipaddr` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '登录IP地址',
  `login_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '登录地点',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '浏览器类型',
  `os` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '操作系统',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '登录状态（0成功 1失败）',
  `msg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '提示消息',
  `login_time` datetime DEFAULT NULL COMMENT '访问时间',
  PRIMARY KEY (`info_id`),
  KEY `idx_sys_logininfor_lt` (`login_time`) USING BTREE,
  KEY `idx_sys_logininfor_s` (`status`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=338 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='系统访问记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_logininfor`
--

LOCK TABLES `sys_logininfor` WRITE;
/*!40000 ALTER TABLE `sys_logininfor` DISABLE KEYS */;
INSERT INTO `sys_logininfor` VALUES (100,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-01-06 16:40:44'),(101,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-08 09:41:41'),(102,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-08 11:00:05'),(103,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-08 13:31:08'),(104,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-08 15:29:10'),(105,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','1','验证码错误','2025-01-09 09:11:36'),(106,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-09 09:11:41'),(107,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-09 09:53:52'),(108,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-09 10:50:40'),(109,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-09 15:52:45'),(110,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-09 17:05:39'),(111,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-10 08:18:30'),(112,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-10 09:16:25'),(113,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-10 11:03:15'),(114,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-10 13:23:49'),(115,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','1','验证码错误','2025-01-14 09:40:15'),(116,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-14 09:40:19'),(117,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-14 10:58:33'),(118,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-14 13:23:56'),(119,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-14 15:26:08'),(120,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-15 08:39:10'),(121,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','1','验证码已失效','2025-01-15 10:52:59'),(122,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-15 10:53:05'),(123,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-15 13:29:15'),(124,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-15 15:57:15'),(125,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-15 17:22:12'),(126,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-16 08:38:38'),(127,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-16 09:33:34'),(128,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-20 11:05:53'),(129,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','1','验证码错误','2025-01-20 13:49:31'),(130,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-20 13:49:34'),(131,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-20 14:56:59'),(132,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-20 17:59:20'),(133,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-21 15:08:56'),(134,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-22 09:27:24'),(135,'admin','10.87.11.221','内网IP','Chrome 12','Windows 10','0','登录成功','2025-01-23 10:32:52'),(136,'admin','127.0.0.1','内网IP','Chrome 13','Mac OS X','0','登录成功','2025-01-23 10:35:52'),(137,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-07 17:02:24'),(138,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-07 18:09:53'),(139,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 09:09:02'),(140,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-08 09:10:25'),(141,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 09:10:29'),(142,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-08 09:12:23'),(143,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 09:12:27'),(144,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-08 09:14:19'),(145,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 09:14:27'),(146,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-08 09:15:46'),(147,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 09:15:54'),(148,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-08 09:16:38'),(149,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 09:16:43'),(150,'admin','10.87.11.232','内网IP','Chrome 13','Windows 10','0','登录成功','2025-02-08 10:24:54'),(151,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','1','验证码错误','2025-02-08 11:02:30'),(152,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 11:02:34'),(153,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 13:51:05'),(154,'admin','10.87.11.6','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 15:53:18'),(155,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','1','验证码错误','2025-02-08 16:04:58'),(156,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 16:05:02'),(157,'admin','10.87.11.89','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 16:14:34'),(158,'admin','10.87.11.6','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 17:04:01'),(159,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 17:05:55'),(160,'admin','10.87.11.6','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 18:35:48'),(161,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-08 18:54:31'),(162,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','1','验证码已失效','2025-02-09 10:15:07'),(163,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','1','验证码已失效','2025-02-09 10:15:21'),(164,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 10:16:35'),(165,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-09 10:18:23'),(166,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 10:18:48'),(167,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-09 10:19:44'),(168,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 10:20:35'),(169,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-09 10:22:57'),(170,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 10:23:18'),(171,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-09 10:52:52'),(172,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 10:58:02'),(173,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','退出成功','2025-02-09 11:04:37'),(174,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 11:17:58'),(175,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 11:17:59'),(176,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 11:18:08'),(177,'admin','10.87.11.6','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 11:34:29'),(178,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 12:09:20'),(179,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 13:48:41'),(180,'admin','10.87.11.6','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 14:08:17'),(181,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','1','验证码错误','2025-02-09 14:39:19'),(182,'admin','127.0.0.1','内网IP','Chrome 12','Windows 10','0','登录成功','2025-02-09 14:39:23'),(183,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-27 14:17:47'),(184,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-27 16:20:31'),(185,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-27 17:01:23'),(186,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-27 17:36:08'),(187,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','退出成功','2025-03-27 18:01:40'),(188,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-27 18:01:43'),(189,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-28 09:25:16'),(190,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-28 10:16:16'),(191,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-03-28 14:08:05'),(192,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-14 17:17:09'),(193,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码错误','2025-04-15 10:27:33'),(194,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-15 10:27:39'),(195,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-15 13:22:00'),(196,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-15 13:29:58'),(197,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-15 14:41:41'),(198,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-15 17:19:16'),(199,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','退出成功','2025-04-15 17:28:38'),(200,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-15 17:28:47'),(201,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-16 09:15:16'),(202,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-16 13:39:28'),(203,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-17 17:32:54'),(204,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-18 09:35:54'),(205,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-18 13:39:04'),(206,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-18 14:14:30'),(207,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-18 15:46:04'),(208,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-18 17:54:41'),(209,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码错误','2025-04-28 16:33:46'),(210,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-04-28 16:33:53'),(211,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-07 14:47:07'),(212,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-12 16:37:54'),(213,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码错误','2025-05-13 09:51:11'),(214,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 09:51:15'),(215,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 10:15:13'),(216,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 11:03:47'),(217,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 14:27:03'),(218,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 14:45:06'),(219,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 15:13:18'),(220,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 16:07:19'),(221,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-13 17:22:55'),(222,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-14 09:40:29'),(223,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-14 13:24:35'),(224,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-14 16:23:13'),(225,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-15 11:07:32'),(226,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-15 13:18:59'),(227,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-15 13:43:02'),(228,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码已失效','2025-05-15 14:51:33'),(229,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-15 14:51:39'),(230,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-15 15:51:49'),(231,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-15 16:34:30'),(232,'admin','127.0.0.1','内网IP','Chrome Mobile','Android 1.x','0','登录成功','2025-05-16 08:49:53'),(233,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-16 08:57:02'),(234,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-16 09:14:12'),(235,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-16 09:23:05'),(236,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-16 10:53:16'),(237,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-16 15:51:55'),(238,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-16 17:41:25'),(239,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-19 09:38:52'),(240,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-19 10:36:00'),(241,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-19 17:08:22'),(242,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-20 13:42:42'),(243,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-20 15:23:02'),(244,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-21 15:01:08'),(245,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-22 10:10:18'),(246,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-22 17:06:35'),(247,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-23 14:54:43'),(248,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-23 16:05:58'),(249,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-23 16:26:54'),(250,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-05-23 17:20:04'),(251,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-03 13:52:13'),(252,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-06 16:28:37'),(253,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-09 08:54:57'),(254,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-09 11:37:39'),(255,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-11 10:12:21'),(256,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-11 11:22:29'),(257,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-06-11 13:17:12'),(258,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-04 10:51:40'),(259,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-07 09:57:36'),(260,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-07 11:14:54'),(261,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-07 13:45:55'),(262,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-07 16:10:07'),(263,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-08 09:35:09'),(264,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-08 10:10:17'),(265,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-08 13:18:50'),(266,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-08 14:09:40'),(267,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-08 16:10:38'),(268,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-08 16:55:58'),(269,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-10 09:42:30'),(270,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-10 10:37:01'),(271,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-10 13:40:01'),(272,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-11 12:46:22'),(273,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-14 10:41:18'),(274,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-14 13:23:06'),(275,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-15 10:11:30'),(276,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-15 15:44:44'),(277,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-16 16:55:59'),(278,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-17 10:29:07'),(279,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-17 14:03:52'),(280,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-21 13:33:59'),(281,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-28 14:20:01'),(282,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-28 16:22:35'),(283,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码错误','2025-07-29 09:33:02'),(284,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-29 09:33:06'),(285,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-07-29 15:28:41'),(286,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-08-21 10:19:21'),(287,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-08-21 13:27:23'),(288,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-08-21 15:31:25'),(289,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码已失效','2025-08-22 09:29:35'),(290,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','1','验证码错误','2025-08-22 09:29:45'),(291,'admin','127.0.0.1','内网IP','Chrome 13','Windows 10','0','登录成功','2025-08-22 09:29:54'),(292,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-09-22 16:21:42'),(293,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-01 17:59:26'),(294,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-01 18:01:36'),(295,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 09:23:54'),(296,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 09:24:00'),(297,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 10:08:41'),(298,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 10:19:44'),(299,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 10:19:56'),(300,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 11:07:36'),(301,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 11:07:48'),(302,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 11:44:10'),(303,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 11:44:16'),(304,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 12:20:36'),(305,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 13:17:02'),(306,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 13:18:51'),(307,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 13:18:55'),(308,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 13:46:30'),(309,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 13:46:34'),(310,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 13:50:35'),(311,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 13:50:38'),(312,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 13:53:59'),(313,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 13:54:03'),(314,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 14:51:27'),(315,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 14:59:38'),(316,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 14:59:42'),(317,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 15:25:44'),(318,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 15:25:48'),(319,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 16:44:34'),(320,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 16:44:43'),(321,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 16:44:54'),(322,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 16:45:00'),(323,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 16:56:51'),(324,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 16:56:54'),(325,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-02 16:56:56'),(326,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-02 16:56:58'),(327,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-15 10:13:04'),(328,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-15 10:17:33'),(329,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-15 10:21:31'),(330,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','退出成功','2025-12-15 10:25:10'),(331,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2025-12-15 10:25:16'),(332,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2026-02-03 06:27:57'),(333,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2026-02-03 06:36:08'),(334,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2026-02-03 07:28:09'),(335,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2026-02-03 07:28:09'),(336,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2026-02-03 07:28:11'),(337,'admin','127.0.0.1','内网IP','Chrome 14','Windows 10','0','登录成功','2026-02-04 05:34:48');
/*!40000 ALTER TABLE `sys_logininfor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_menu`
--

DROP TABLE IF EXISTS `sys_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_menu` (
  `menu_id` bigint NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `menu_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '菜单名称',
  `parent_id` bigint DEFAULT '0' COMMENT '父菜单ID',
  `order_num` int DEFAULT '0' COMMENT '显示顺序',
  `path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '路由地址',
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '组件路径',
  `query` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '路由参数',
  `route_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '路由名称',
  `is_frame` int DEFAULT '1' COMMENT '是否为外链（0是 1否）',
  `is_cache` int DEFAULT '0' COMMENT '是否缓存（0缓存 1不缓存）',
  `menu_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '菜单类型（M目录 C菜单 F按钮）',
  `visible` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '菜单状态（0显示 1隐藏）',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '菜单状态（0正常 1停用）',
  `perms` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '权限标识',
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '#' COMMENT '菜单图标',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '备注',
  PRIMARY KEY (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2027 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='菜单权限表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_menu`
--

LOCK TABLES `sys_menu` WRITE;
/*!40000 ALTER TABLE `sys_menu` DISABLE KEYS */;
INSERT INTO `sys_menu` VALUES (1,'系统管理',0,7,'system',NULL,'','',1,0,'M','0','0','','system','admin','2025-01-06 16:33:58','admin','2025-12-02 15:20:24','系统管理目录'),(2,'系统监控',0,10,'monitor',NULL,'','',1,0,'M','0','0','','monitor','admin','2025-01-06 16:33:58','admin','2025-12-02 14:07:40','系统监控目录'),(3,'系统工具',0,9,'tool',NULL,'','',1,0,'M','0','0','','tool','admin','2025-01-06 16:33:58','admin','2025-12-02 14:07:35','系统工具目录'),(100,'用户管理',1,1,'user','system/user/index','','',1,0,'C','0','0','system:user:list','user','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:01','用户管理菜单'),(101,'角色管理',1,2,'role','system/role/index','','',1,0,'C','0','0','system:role:list','peoples','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:09','角色管理菜单'),(102,'菜单管理',1,3,'menu','system/menu/index','','',1,0,'C','0','0','system:menu:list','tree-table','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:19','菜单管理菜单'),(103,'部门管理',1,4,'dept','system/dept/index','','',1,0,'C','0','0','system:dept:list','tree','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:26','部门管理菜单'),(104,'岗位管理',1,5,'post','system/post/index','','',1,0,'C','0','0','system:post:list','post','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:32','岗位管理菜单'),(105,'字典管理',1,6,'dict','system/dict/index','','',1,0,'C','0','0','system:dict:list','dict','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:39','字典管理菜单'),(106,'参数设置',1,7,'config','system/config/index','','',1,0,'C','0','0','system:config:list','edit','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:44','参数设置菜单'),(107,'通知公告',1,8,'notice','system/notice/index','','',1,0,'C','0','0','system:notice:list','message','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:52','通知公告菜单'),(108,'日志管理',1,9,'log','','','',1,0,'M','0','0','','log','admin','2025-01-06 16:33:59','admin','2025-12-15 10:23:58','日志管理菜单'),(109,'在线用户',2,1,'online','monitor/online/index','','',1,0,'C','0','0','monitor:online:list','online','admin','2025-01-06 16:33:59','',NULL,'在线用户菜单'),(110,'定时任务',2,2,'job','monitor/job/index','','',1,0,'C','0','0','monitor:job:list','job','admin','2025-01-06 16:33:59','',NULL,'定时任务菜单'),(111,'数据监控',2,3,'druid','monitor/druid/index','','',1,0,'C','0','0','monitor:druid:list','druid','admin','2025-01-06 16:33:59','',NULL,'数据监控菜单'),(112,'服务监控',2,4,'server','monitor/server/index','','',1,0,'C','0','0','monitor:server:list','server','admin','2025-01-06 16:33:59','admin','2025-04-15 11:11:11','服务监控菜单'),(113,'缓存监控',2,5,'cache','monitor/cache/index','','',1,0,'C','0','0','monitor:cache:list','redis','admin','2025-01-06 16:33:59','',NULL,'缓存监控菜单'),(114,'缓存列表',2,6,'cacheList','monitor/cache/list','','',1,0,'C','0','0','monitor:cache:list','redis-list','admin','2025-01-06 16:33:59','',NULL,'缓存列表菜单'),(116,'代码生成',3,2,'gen','tool/gen/index','','',1,0,'C','0','0','tool:gen:list','code','admin','2025-01-06 16:33:59','',NULL,'代码生成菜单'),(117,'系统接口',3,3,'swagger','tool/swagger/index','','',1,0,'C','0','0','tool:swagger:list','swagger','admin','2025-01-06 16:33:59','',NULL,'系统接口菜单'),(500,'操作日志',108,1,'operlog','monitor/operlog/index','','',1,0,'C','0','0','monitor:operlog:list','form','admin','2025-01-06 16:33:59','',NULL,'操作日志菜单'),(501,'登录日志',108,2,'logininfor','monitor/logininfor/index','','',1,0,'C','0','0','monitor:logininfor:list','logininfor','admin','2025-01-06 16:33:59','',NULL,'登录日志菜单'),(1000,'用户查询',100,1,'','','','',1,0,'F','0','0','system:user:query','#','admin','2025-01-06 16:33:59','',NULL,''),(1001,'用户新增',100,2,'','','','',1,0,'F','0','0','system:user:add','#','admin','2025-01-06 16:33:59','',NULL,''),(1002,'用户修改',100,3,'','','','',1,0,'F','0','0','system:user:edit','#','admin','2025-01-06 16:33:59','',NULL,''),(1003,'用户删除',100,4,'','','','',1,0,'F','0','0','system:user:remove','#','admin','2025-01-06 16:33:59','',NULL,''),(1004,'用户导出',100,5,'','','','',1,0,'F','0','0','system:user:export','#','admin','2025-01-06 16:33:59','',NULL,''),(1005,'用户导入',100,6,'','','','',1,0,'F','0','0','system:user:import','#','admin','2025-01-06 16:33:59','',NULL,''),(1006,'重置密码',100,7,'','','','',1,0,'F','0','0','system:user:resetPwd','#','admin','2025-01-06 16:33:59','',NULL,''),(1007,'角色查询',101,1,'','','','',1,0,'F','0','0','system:role:query','#','admin','2025-01-06 16:33:59','',NULL,''),(1008,'角色新增',101,2,'','','','',1,0,'F','0','0','system:role:add','#','admin','2025-01-06 16:33:59','',NULL,''),(1009,'角色修改',101,3,'','','','',1,0,'F','0','0','system:role:edit','#','admin','2025-01-06 16:33:59','',NULL,''),(1010,'角色删除',101,4,'','','','',1,0,'F','0','0','system:role:remove','#','admin','2025-01-06 16:33:59','',NULL,''),(1011,'角色导出',101,5,'','','','',1,0,'F','0','0','system:role:export','#','admin','2025-01-06 16:33:59','',NULL,''),(1012,'菜单查询',102,1,'','','','',1,0,'F','0','0','system:menu:query','#','admin','2025-01-06 16:33:59','',NULL,''),(1013,'菜单新增',102,2,'','','','',1,0,'F','0','0','system:menu:add','#','admin','2025-01-06 16:33:59','',NULL,''),(1014,'菜单修改',102,3,'','','','',1,0,'F','0','0','system:menu:edit','#','admin','2025-01-06 16:33:59','',NULL,''),(1015,'菜单删除',102,4,'','','','',1,0,'F','0','0','system:menu:remove','#','admin','2025-01-06 16:33:59','',NULL,''),(1016,'部门查询',103,1,'','','','',1,0,'F','0','0','system:dept:query','#','admin','2025-01-06 16:33:59','',NULL,''),(1017,'部门新增',103,2,'','','','',1,0,'F','0','0','system:dept:add','#','admin','2025-01-06 16:33:59','',NULL,''),(1018,'部门修改',103,3,'','','','',1,0,'F','0','0','system:dept:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1019,'部门删除',103,4,'','','','',1,0,'F','0','0','system:dept:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1020,'岗位查询',104,1,'','','','',1,0,'F','0','0','system:post:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1021,'岗位新增',104,2,'','','','',1,0,'F','0','0','system:post:add','#','admin','2025-01-06 16:34:00','',NULL,''),(1022,'岗位修改',104,3,'','','','',1,0,'F','0','0','system:post:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1023,'岗位删除',104,4,'','','','',1,0,'F','0','0','system:post:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1024,'岗位导出',104,5,'','','','',1,0,'F','0','0','system:post:export','#','admin','2025-01-06 16:34:00','',NULL,''),(1025,'字典查询',105,1,'#','','','',1,0,'F','0','0','system:dict:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1026,'字典新增',105,2,'#','','','',1,0,'F','0','0','system:dict:add','#','admin','2025-01-06 16:34:00','',NULL,''),(1027,'字典修改',105,3,'#','','','',1,0,'F','0','0','system:dict:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1028,'字典删除',105,4,'#','','','',1,0,'F','0','0','system:dict:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1029,'字典导出',105,5,'#','','','',1,0,'F','0','0','system:dict:export','#','admin','2025-01-06 16:34:00','',NULL,''),(1030,'参数查询',106,1,'#','','','',1,0,'F','0','0','system:config:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1031,'参数新增',106,2,'#','','','',1,0,'F','0','0','system:config:add','#','admin','2025-01-06 16:34:00','',NULL,''),(1032,'参数修改',106,3,'#','','','',1,0,'F','0','0','system:config:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1033,'参数删除',106,4,'#','','','',1,0,'F','0','0','system:config:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1034,'参数导出',106,5,'#','','','',1,0,'F','0','0','system:config:export','#','admin','2025-01-06 16:34:00','',NULL,''),(1035,'公告查询',107,1,'#','','','',1,0,'F','0','0','system:notice:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1036,'公告新增',107,2,'#','','','',1,0,'F','0','0','system:notice:add','#','admin','2025-01-06 16:34:00','',NULL,''),(1037,'公告修改',107,3,'#','','','',1,0,'F','0','0','system:notice:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1038,'公告删除',107,4,'#','','','',1,0,'F','0','0','system:notice:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1039,'操作查询',500,1,'#','','','',1,0,'F','0','0','monitor:operlog:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1040,'操作删除',500,2,'#','','','',1,0,'F','0','0','monitor:operlog:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1041,'日志导出',500,3,'#','','','',1,0,'F','0','0','monitor:operlog:export','#','admin','2025-01-06 16:34:00','',NULL,''),(1042,'登录查询',501,1,'#','','','',1,0,'F','0','0','monitor:logininfor:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1043,'登录删除',501,2,'#','','','',1,0,'F','0','0','monitor:logininfor:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1044,'日志导出',501,3,'#','','','',1,0,'F','0','0','monitor:logininfor:export','#','admin','2025-01-06 16:34:00','',NULL,''),(1045,'账户解锁',501,4,'#','','','',1,0,'F','0','0','monitor:logininfor:unlock','#','admin','2025-01-06 16:34:00','',NULL,''),(1046,'在线查询',109,1,'#','','','',1,0,'F','0','0','monitor:online:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1047,'批量强退',109,2,'#','','','',1,0,'F','0','0','monitor:online:batchLogout','#','admin','2025-01-06 16:34:00','',NULL,''),(1048,'单条强退',109,3,'#','','','',1,0,'F','0','0','monitor:online:forceLogout','#','admin','2025-01-06 16:34:00','',NULL,''),(1049,'任务查询',110,1,'#','','','',1,0,'F','0','0','monitor:job:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1050,'任务新增',110,2,'#','','','',1,0,'F','0','0','monitor:job:add','#','admin','2025-01-06 16:34:00','',NULL,''),(1051,'任务修改',110,3,'#','','','',1,0,'F','0','0','monitor:job:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1052,'任务删除',110,4,'#','','','',1,0,'F','0','0','monitor:job:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1053,'状态修改',110,5,'#','','','',1,0,'F','0','0','monitor:job:changeStatus','#','admin','2025-01-06 16:34:00','',NULL,''),(1054,'任务导出',110,6,'#','','','',1,0,'F','0','0','monitor:job:export','#','admin','2025-01-06 16:34:00','',NULL,''),(1055,'生成查询',116,1,'#','','','',1,0,'F','0','0','tool:gen:query','#','admin','2025-01-06 16:34:00','',NULL,''),(1056,'生成修改',116,2,'#','','','',1,0,'F','0','0','tool:gen:edit','#','admin','2025-01-06 16:34:00','',NULL,''),(1057,'生成删除',116,3,'#','','','',1,0,'F','0','0','tool:gen:remove','#','admin','2025-01-06 16:34:00','',NULL,''),(1058,'导入代码',116,4,'#','','','',1,0,'F','0','0','tool:gen:import','#','admin','2025-01-06 16:34:00','',NULL,''),(1059,'预览代码',116,5,'#','','','',1,0,'F','0','0','tool:gen:preview','#','admin','2025-01-06 16:34:00','',NULL,''),(1060,'生成代码',116,6,'#','','','',1,0,'F','0','0','tool:gen:code','#','admin','2025-01-06 16:34:00','',NULL,''),(2008,'首页',0,0,'index','index',NULL,'',1,0,'C','0','0','index','guide','admin','2025-12-02 12:24:28','admin','2025-12-02 17:08:55',''),(2009,'基本信息',0,8,'user/profile',NULL,NULL,'',1,0,'M','0','0','','user','admin','2025-12-02 13:22:26','admin','2025-12-02 13:22:45',''),(2019,'退出登录',0,11,'__logout__',NULL,NULL,'',1,0,'M','0','0',NULL,'link','admin','2025-12-02 16:54:31','',NULL,''),(2020,'企业管理',1,10,'enterprise','system/enterprise/index',NULL,'',1,0,'C','0','0','system:enterprise:list','peoples','admin','2026-02-03 06:07:32','',NULL,'企业管理菜单'),(2021,'企业查询',2020,1,'',NULL,NULL,'',1,0,'F','0','0','system:enterprise:query','#','admin','2026-02-03 06:07:32','',NULL,''),(2022,'企业新增',2020,2,'',NULL,NULL,'',1,0,'F','0','0','system:enterprise:add','#','admin','2026-02-03 06:07:32','',NULL,''),(2023,'企业修改',2020,3,'',NULL,NULL,'',1,0,'F','0','0','system:enterprise:edit','#','admin','2026-02-03 06:07:32','',NULL,''),(2024,'企业删除',2020,4,'',NULL,NULL,'',1,0,'F','0','0','system:enterprise:remove','#','admin','2026-02-03 06:07:32','',NULL,''),(2025,'企业导出',2020,5,'',NULL,NULL,'',1,0,'F','0','0','system:enterprise:export','#','admin','2026-02-03 06:07:32','',NULL,''),(2026,'重置AK/SK',2020,6,'',NULL,NULL,'',1,0,'F','0','0','system:enterprise:resetAkSk','#','admin','2026-02-03 06:07:32','',NULL,'');
/*!40000 ALTER TABLE `sys_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_notice`
--

DROP TABLE IF EXISTS `sys_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_notice` (
  `notice_id` int NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `notice_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告标题',
  `notice_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '公告类型（1通知 2公告）',
  `notice_content` longblob COMMENT '公告内容',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '公告状态（0正常 1关闭）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`notice_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='通知公告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_notice`
--

LOCK TABLES `sys_notice` WRITE;
/*!40000 ALTER TABLE `sys_notice` DISABLE KEYS */;
INSERT INTO `sys_notice` VALUES (10,'123','1',_binary '<p><img src=\"/dev-api/profile/upload/2025/01/15/0694f9b9-8f0d-44e6-bd65-40aad669c9d3_20250115155735A001.jpg\"></p>','0','admin','2025-01-15 15:57:49','',NULL,NULL);
/*!40000 ALTER TABLE `sys_notice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_oper_log`
--

DROP TABLE IF EXISTS `sys_oper_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_oper_log` (
  `oper_id` bigint NOT NULL AUTO_INCREMENT COMMENT '日志主键',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '模块标题',
  `business_type` int DEFAULT '0' COMMENT '业务类型（0其它 1新增 2修改 3删除）',
  `method` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '方法名称',
  `request_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '请求方式',
  `operator_type` int DEFAULT '0' COMMENT '操作类别（0其它 1后台用户 2手机端用户）',
  `oper_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '操作人员',
  `dept_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '部门名称',
  `oper_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '请求URL',
  `oper_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '主机地址',
  `oper_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '操作地点',
  `oper_param` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '请求参数',
  `json_result` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '返回参数',
  `status` int DEFAULT '0' COMMENT '操作状态（0正常 1异常）',
  `error_msg` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '错误消息',
  `oper_time` datetime DEFAULT NULL COMMENT '操作时间',
  `cost_time` bigint DEFAULT '0' COMMENT '消耗时间',
  PRIMARY KEY (`oper_id`),
  KEY `idx_sys_oper_log_bt` (`business_type`) USING BTREE,
  KEY `idx_sys_oper_log_ot` (`oper_time`) USING BTREE,
  KEY `idx_sys_oper_log_s` (`status`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=347 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='操作日志记录';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_oper_log`
--

LOCK TABLES `sys_oper_log` WRITE;
/*!40000 ALTER TABLE `sys_oper_log` DISABLE KEYS */;
INSERT INTO `sys_oper_log` VALUES (100,'部门管理',3,'com.xunmei.web.controller.system.SysDeptController.remove()','DELETE',1,'admin','研发部门','/system/dept/109','127.0.0.1','内网IP','109','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:44:51',98),(101,'部门管理',3,'com.xunmei.web.controller.system.SysDeptController.remove()','DELETE',1,'admin','研发部门','/system/dept/108','127.0.0.1','内网IP','108','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:44:54',100),(102,'部门管理',3,'com.xunmei.web.controller.system.SysDeptController.remove()','DELETE',1,'admin','研发部门','/system/dept/102','127.0.0.1','内网IP','102','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:44:56',83),(103,'部门管理',3,'com.xunmei.web.controller.system.SysDeptController.remove()','DELETE',1,'admin','研发部门','/system/dept/107','127.0.0.1','内网IP','107','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:44:58',55),(104,'部门管理',2,'com.xunmei.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0\",\"children\":[],\"deptId\":100,\"deptName\":\"四川交投\",\"email\":\"\",\"leader\":\"\",\"orderNum\":0,\"params\":{},\"parentId\":0,\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:45:17',61),(105,'部门管理',2,'com.xunmei.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100\",\"children\":[],\"deptId\":101,\"deptName\":\"成都总公司\",\"email\":\"\",\"leader\":\"\",\"orderNum\":1,\"params\":{},\"parentId\":100,\"parentName\":\"四川交投\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:45:31',136),(106,'部门管理',2,'com.xunmei.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":103,\"deptName\":\"研发部门\",\"email\":\"\",\"leader\":\"\",\"orderNum\":1,\"params\":{},\"parentId\":101,\"parentName\":\"成都总公司\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:45:40',83),(107,'部门管理',2,'com.xunmei.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":104,\"deptName\":\"市场部门\",\"email\":\"\",\"leader\":\"\",\"orderNum\":2,\"params\":{},\"parentId\":101,\"parentName\":\"成都总公司\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:45:48',87),(108,'部门管理',2,'com.xunmei.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":105,\"deptName\":\"测试部门\",\"email\":\"\",\"leader\":\"\",\"orderNum\":3,\"params\":{},\"parentId\":101,\"parentName\":\"成都总公司\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:45:59',84),(109,'部门管理',2,'com.xunmei.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":106,\"deptName\":\"财务部门\",\"email\":\"\",\"leader\":\"\",\"orderNum\":4,\"params\":{},\"parentId\":101,\"parentName\":\"成都总公司\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:46:06',71),(110,'通知公告',3,'com.xunmei.web.controller.system.SysNoticeController.remove()','DELETE',1,'admin','研发部门','/system/notice/1','127.0.0.1','内网IP','[1]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:46:56',54),(111,'通知公告',3,'com.xunmei.web.controller.system.SysNoticeController.remove()','DELETE',1,'admin','研发部门','/system/notice/2','127.0.0.1','内网IP','[2]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 09:46:58',38),(112,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createBy\":\"admin\",\"icon\":\"monitor\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"车辆监测\",\"menuType\":\"M\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"car\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 11:12:51',67),(113,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/car/device/index\",\"createBy\":\"admin\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"设备列表\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2000,\"path\":\"/car/device\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 11:16:09',58),(114,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/device/index\",\"createTime\":\"2025-01-08 11:16:09\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2001,\"menuName\":\"设备列表\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2000,\"path\":\"/car/device\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 11:17:50',52),(115,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/device/index\",\"createTime\":\"2025-01-08 11:16:09\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2001,\"menuName\":\"设备列表\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2000,\"path\":\"car/device\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 11:25:01',56),(116,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/device/index\",\"createTime\":\"2025-01-08 11:16:09\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2001,\"menuName\":\"设备列表\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2000,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 11:25:56',55),(117,'角色管理',5,'com.xunmei.web.controller.system.SysRoleController.export()','POST',1,'admin','研发部门','/system/role/export','127.0.0.1','内网IP','{\"pageSize\":\"10\",\"pageNum\":\"1\"}',NULL,0,NULL,'2025-01-08 13:33:23',1308),(118,'代码生成',6,'com.xunmei.generator.controller.GenController.importTableSave()','POST',1,'admin','研发部门','/tool/gen/importTable','127.0.0.1','内网IP','{\"tables\":\"sys_device\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-08 15:29:27',743),(119,'代码生成',8,'com.xunmei.generator.controller.GenController.batchGenCode()','GET',1,'admin','研发部门','/tool/gen/batchGenCode','127.0.0.1','内网IP','{\"tables\":\"sys_device\"}',NULL,0,NULL,'2025-01-08 15:29:31',366),(120,'用户管理',3,'com.xunmei.web.controller.system.SysUserController.remove()','DELETE',1,'admin','研发部门','/system/user/2','127.0.0.1','内网IP','[2]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 09:23:43',199),(121,'用户管理',2,'com.xunmei.web.controller.system.SysUserController.edit()','PUT',1,'admin','研发部门','/system/user','127.0.0.1','内网IP','{\"admin\":true,\"avatar\":\"\",\"createBy\":\"admin\",\"createTime\":\"2025-01-06 16:33:56\",\"delFlag\":\"0\",\"dept\":{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":103,\"deptName\":\"研发部门\",\"leader\":\"\",\"orderNum\":1,\"params\":{},\"parentId\":101,\"status\":\"0\"},\"deptId\":103,\"email\":\"\",\"loginDate\":\"2025-01-10 09:16:15\",\"loginIp\":\"127.0.0.1\",\"nickName\":\"管理员\",\"params\":{},\"phonenumber\":\"15888888888\",\"postIds\":[1],\"remark\":\"管理员\",\"roleIds\":[1],\"roles\":[{\"admin\":true,\"dataScope\":\"1\",\"deptCheckStrictly\":false,\"flag\":false,\"menuCheckStrictly\":false,\"params\":{},\"roleId\":1,\"roleKey\":\"admin\",\"roleName\":\"超级管理员\",\"roleSort\":1,\"status\":\"0\"}],\"sex\":\"1\",\"status\":\"0\",\"userId\":1,\"userName\":\"admin\"}',NULL,1,'不允许操作超级管理员用户','2025-01-10 09:24:29',65),(122,'角色管理',2,'com.xunmei.web.controller.system.SysRoleController.edit()','PUT',1,'admin','研发部门','/system/role','127.0.0.1','内网IP','{\"admin\":false,\"createTime\":\"2025-01-06 16:33:58\",\"dataScope\":\"2\",\"delFlag\":\"0\",\"deptCheckStrictly\":true,\"flag\":false,\"menuCheckStrictly\":true,\"menuIds\":[2000,2001],\"params\":{},\"remark\":\"普通角色\",\"roleId\":2,\"roleKey\":\"common\",\"roleName\":\"普通角色\",\"roleSort\":2,\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 09:28:43',175),(123,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"server/index\",\"createBy\":\"admin\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"服务器管理\",\"menuType\":\"C\",\"orderNum\":0,\"params\":{},\"parentId\":2000,\"path\":\"server\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 09:56:19',58),(124,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.23.55\",\"serverName\":\"验证新增\",\"serverPort\":8080}',NULL,1,'Invalid bound statement (not found): com.xunmei.core.mapper.SysServerMapper.selectCount','2025-01-10 11:40:45',40),(125,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.23.55\",\"serverName\":\"验证新增\",\"serverPort\":8080}',NULL,1,'Invalid bound statement (not found): com.xunmei.core.mapper.SysServerMapper.selectCount','2025-01-10 11:42:09',7910),(126,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.23.55\",\"serverName\":\"验证新增\",\"serverPort\":8080}',NULL,1,'Invalid bound statement (not found): com.xunmei.core.mapper.SysServerMapper.selectCount','2025-01-10 11:42:48',8137),(127,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.23.57\",\"serverName\":\"验证新增\",\"serverPort\":8080}',NULL,1,'Invalid bound statement (not found): com.xunmei.core.mapper.SysServerMapper.selectCount','2025-01-10 13:24:49',6326),(128,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.23.57\",\"serverName\":\"验证新增\",\"serverPort\":8080}',NULL,1,'ip重复','2025-01-10 13:33:19',3986),(129,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.22.22\",\"serverName\":\"验证新增\",\"serverPort\":8080}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:34:06',236),(130,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":14,\"serverIp\":\"10.87.22.22\",\"serverName\":\"验证新增1\",\"serverPort\":8080}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:35:44',627),(131,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/1','127.0.0.1','内网IP','[1]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:40:54',77),(132,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/2','127.0.0.1','内网IP','[2]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:40:57',39),(133,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/3','127.0.0.1','内网IP','[3]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:40:58',44),(134,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/4','127.0.0.1','内网IP','[4]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:41:47',66),(135,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/5','127.0.0.1','内网IP','[5]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:41:49',76),(136,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/6','127.0.0.1','内网IP','[6]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:41:52',61),(137,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/7','127.0.0.1','内网IP','[7]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:41:54',58),(138,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/8','127.0.0.1','内网IP','[8]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:41:56',54),(139,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/9','127.0.0.1','内网IP','[9]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:41:58',57),(140,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/10','127.0.0.1','内网IP','[10]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:42:01',41),(141,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/11','127.0.0.1','内网IP','[11]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:42:03',67),(142,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/12','127.0.0.1','内网IP','[12]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:42:05',47),(143,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/13','127.0.0.1','内网IP','[13]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 13:42:07',43),(144,'用户管理',1,'com.xunmei.web.controller.system.SysUserController.add()','POST',1,'admin','研发部门','/system/user','127.0.0.1','内网IP','{\"admin\":false,\"createBy\":\"admin\",\"deptId\":103,\"nickName\":\"张三\",\"params\":{},\"postIds\":[4],\"roleIds\":[2],\"status\":\"0\",\"userId\":100,\"userName\":\"zhangsan\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 14:14:38',757),(145,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":14,\"serverIp\":\"222.74.153.59\",\"serverName\":\"验证新增1\",\"serverPort\":11192}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 14:23:24',89),(146,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":14,\"serverIp\":\"222.74.153.59\",\"serverName\":\"验证新增1\",\"serverPort\":11192}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 14:27:15',85),(147,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":14,\"serverIp\":\"222.74.153.59\",\"serverName\":\"验证新增1\",\"serverPort\":11192}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 14:29:50',183),(148,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":14,\"serverIp\":\"222.74.153.59\",\"serverName\":\"验证新增1\",\"serverPort\":11192}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-10 14:32:30',86),(149,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/alarm/index\",\"createBy\":\"admin\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"预警中心\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2000,\"path\":\"alarm\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-14 09:43:19',62),(150,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":14,\"serverIp\":\"222.74.153.59\",\"serverName\":\"演示环境\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-14 10:58:53',118),(151,'角色管理',5,'com.xunmei.web.controller.system.SysRoleController.export()','POST',1,'admin','研发部门','/system/role/export','127.0.0.1','内网IP','{\"pageSize\":\"10\",\"pageNum\":\"1\",\"serverId\":\"14\"}',NULL,0,NULL,'2025-01-14 13:27:43',976),(152,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createBy\":\"admin\",\"icon\":\"druid\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"车流监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2000,\"path\":\"report\",\"query\":\"car/report/index\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-14 15:27:47',62),(153,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/report/index\",\"createTime\":\"2025-01-14 15:27:47\",\"icon\":\"druid\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2004,\"menuName\":\"车流监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2000,\"path\":\"report\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-14 15:29:59',64),(154,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/alarm/index\",\"createTime\":\"2025-01-14 09:43:19\",\"icon\":\"form\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2003,\"menuName\":\"预警中心\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2000,\"path\":\"alarm\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-15 10:53:54',61),(155,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/task/index\",\"createBy\":\"admin\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"任务列表\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":2000,\"path\":\"task\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-15 10:54:25',56),(156,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/task/index\",\"createTime\":\"2025-01-15 10:54:25\",\"icon\":\"excel\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2005,\"menuName\":\"任务列表\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":2000,\"path\":\"task\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-15 15:10:07',70),(157,'通知公告',1,'com.xunmei.web.controller.system.SysNoticeController.add()','POST',1,'admin','研发部门','/system/notice','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"noticeContent\":\"<p><img src=\\\"/dev-api/profile/upload/2025/01/15/0694f9b9-8f0d-44e6-bd65-40aad669c9d3_20250115155735A001.jpg\\\"></p>\",\"noticeTitle\":\"123\",\"noticeType\":\"1\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-15 15:57:49',59),(158,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"内网\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:30:18',87),(159,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"id\":15,\"serverIp\":\"10.87.10.145\",\"serverName\":\"内网\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:34:11',739),(160,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/15','127.0.0.1','内网IP','[15]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:34:30',72),(161,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"10.87.10.145\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:34:43',58),(162,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/16','127.0.0.1','内网IP','[16]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:37:50',94),(163,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"10.87.10.145\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:38:00',67),(164,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/17','127.0.0.1','内网IP','[17]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:38:25',40),(165,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"10.87.10.145\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:38:50',16095),(166,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"10.87.10.145\",\"serverPort\":11192,\"username\":\"admin\"}',NULL,1,'ip重复','2025-01-20 11:40:28',52),(167,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/18','127.0.0.1','内网IP','[18]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:40:38',40),(168,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"本地环境\",\"serverPort\":11192,\"username\":\"admin\"}',NULL,1,'Target must not be null','2025-01-20 11:40:56',3597),(169,'服务器维护',1,'com.xunmei.core.controller.SysServerController.edit()','POST',1,'admin','研发部门','/server','127.0.0.1','内网IP','{\"serverIp\":\"10.87.10.145\",\"serverName\":\"本地环境\",\"serverPort\":11192,\"username\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 11:42:27',94),(170,'菜单管理',1,'com.xunmei.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/subscribe/index\",\"createBy\":\"admin\",\"icon\":\"documentation\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"预警订阅\",\"menuType\":\"C\",\"orderNum\":5,\"params\":{},\"parentId\":2000,\"path\":\"subscribe\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-01-20 13:50:15',69),(171,'服务器删除',3,'com.xunmei.core.controller.SysServerController.remove()','DELETE',1,'admin','研发部门','/server/14','127.0.0.1','内网IP','[14]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-07 17:38:37',67),(172,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-08 11:12:51\",\"icon\":\"monitor\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2000,\"menuName\":\"预警管理\",\"menuType\":\"M\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}',NULL,1,'\r\n### Error updating database.  Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\r\n### The error may exist in file [D:\\workspace\\manager-api\\scjt-system\\target\\classes\\mapper\\system\\SysMenuMapper.xml]\r\n### The error may involve com.xunmei.system.mapper.SysMenuMapper.updateMenu-Inline\r\n### The error occurred while setting parameters\r\n### SQL: update sys_menu    SET menu_name = ?,    parent_id = ?,    order_num = ?,    path = ?,            route_name = ?,    is_frame = ?,    is_cache = ?,    menu_type = ?,    visible = ?,    status = ?,    perms = ?,    icon = ?,        update_by = ?,    update_time = sysdate()    where menu_id = ?\r\n### Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\n; Lock wait timeout exceeded; try restarting transaction; nested exception is com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction','2025-02-08 09:11:57',50270),(173,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-08 11:12:51\",\"icon\":\"monitor\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2000,\"menuName\":\"预警管理\",\"menuType\":\"M\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}',NULL,1,'\r\n### Error updating database.  Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\r\n### The error may exist in file [D:\\workspace\\manager-api\\scjt-system\\target\\classes\\mapper\\system\\SysMenuMapper.xml]\r\n### The error may involve com.xunmei.system.mapper.SysMenuMapper.updateMenu-Inline\r\n### The error occurred while setting parameters\r\n### SQL: update sys_menu    SET menu_name = ?,    parent_id = ?,    order_num = ?,    path = ?,            route_name = ?,    is_frame = ?,    is_cache = ?,    menu_type = ?,    visible = ?,    status = ?,    perms = ?,    icon = ?,        update_by = ?,    update_time = sysdate()    where menu_id = ?\r\n### Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\n; Lock wait timeout exceeded; try restarting transaction; nested exception is com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction','2025-02-08 09:12:14',50319),(174,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-08 11:12:51\",\"icon\":\"monitor\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2000,\"menuName\":\"预警管理\",\"menuType\":\"M\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}',NULL,1,'\r\n### Error updating database.  Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\r\n### The error may exist in file [D:\\workspace\\manager-api\\scjt-system\\target\\classes\\mapper\\system\\SysMenuMapper.xml]\r\n### The error may involve com.xunmei.system.mapper.SysMenuMapper.updateMenu-Inline\r\n### The error occurred while setting parameters\r\n### SQL: update sys_menu    SET menu_name = ?,    parent_id = ?,    order_num = ?,    path = ?,            route_name = ?,    is_frame = ?,    is_cache = ?,    menu_type = ?,    visible = ?,    status = ?,    perms = ?,    icon = ?,        update_by = ?,    update_time = sysdate()    where menu_id = ?\r\n### Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\n; Lock wait timeout exceeded; try restarting transaction; nested exception is com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction','2025-02-08 09:12:38',50799),(175,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-08 11:12:51\",\"icon\":\"monitor\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2000,\"menuName\":\"预警管理\",\"menuType\":\"M\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}',NULL,1,'\r\n### Error updating database.  Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\r\n### The error may exist in file [D:\\workspace\\manager-api\\scjt-system\\target\\classes\\mapper\\system\\SysMenuMapper.xml]\r\n### The error may involve com.xunmei.system.mapper.SysMenuMapper.updateMenu-Inline\r\n### The error occurred while setting parameters\r\n### SQL: update sys_menu    SET menu_name = ?,    parent_id = ?,    order_num = ?,    path = ?,            route_name = ?,    is_frame = ?,    is_cache = ?,    menu_type = ?,    visible = ?,    status = ?,    perms = ?,    icon = ?,        update_by = ?,    update_time = sysdate()    where menu_id = ?\r\n### Cause: com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction\n; Lock wait timeout exceeded; try restarting transaction; nested exception is com.mysql.cj.jdbc.exceptions.MySQLTransactionRollbackException: Lock wait timeout exceeded; try restarting transaction','2025-02-08 09:14:25',50360),(176,'字典类型',1,'com.xm.web.controller.system.SysDictTypeController.add()','POST',1,'admin','研发部门','/system/dict/type','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"dictName\":\"推送数据\",\"dictType\":\"sys_vmns\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:21:12',37),(177,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"vmns_ip\",\"dictSort\":0,\"dictType\":\"sys_vmns\",\"dictValue\":\"10.87.20.129\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:22:12',13),(178,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"vmns_port\",\"dictSort\":0,\"dictType\":\"sys_vmns\",\"dictValue\":\"81\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:22:22',8),(179,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"vmns_appName\",\"dictSort\":2,\"dictType\":\"sys_vmns\",\"dictValue\":\"vipservereventengineG1\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:22:46',21),(180,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 17:22:22\",\"default\":false,\"dictCode\":101,\"dictLabel\":\"vmns_port\",\"dictSort\":1,\"dictType\":\"sys_vmns\",\"dictValue\":\"81\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:22:50',22),(181,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"vmns_token\",\"dictSort\":3,\"dictType\":\"sys_vmns\",\"dictValue\":\"bcf7b93d-41ac-4298-bb1c-18e57b0cfd63\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:23:08',8),(182,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','10.87.11.6','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 17:22:22\",\"default\":false,\"dictCode\":101,\"dictLabel\":\"vmns_port\",\"dictSort\":1,\"dictType\":\"sys_vmns\",\"dictValue\":\"33050\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:40:01',30),(183,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','10.87.11.6','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 17:23:08\",\"default\":false,\"dictCode\":103,\"dictLabel\":\"vmns_token\",\"dictSort\":3,\"dictType\":\"sys_vmns\",\"dictValue\":\"6ff5e4c9-8899-4dd3-94ed-9f2d10a48be9\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 17:40:25',11),(184,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"org_code\",\"dictSort\":4,\"dictType\":\"sys_vmns\",\"dictValue\":\"11\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:21:46',48),(185,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"org_name\",\"dictSort\":0,\"dictType\":\"sys_vmns\",\"dictValue\":\"11\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:21:55',11),(186,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:21:55\",\"default\":false,\"dictCode\":105,\"dictLabel\":\"org_name\",\"dictSort\":5,\"dictType\":\"sys_vmns\",\"dictValue\":\"11\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:22:01',26),(187,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"center_code\",\"dictSort\":6,\"dictType\":\"sys_vmns\",\"dictValue\":\"11\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:22:13',10),(188,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"center_name\",\"dictSort\":7,\"dictType\":\"sys_vmns\",\"dictValue\":\"33\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:22:23',9),(189,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:21:55\",\"default\":false,\"dictCode\":105,\"dictLabel\":\"org_name\",\"dictSort\":5,\"dictType\":\"sys_vmns\",\"dictValue\":\"江北区支行\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:23:43',55),(190,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:21:46\",\"default\":false,\"dictCode\":104,\"dictLabel\":\"org_code\",\"dictSort\":4,\"dictType\":\"sys_vmns\",\"dictValue\":\"500105022160000001\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:24:51',15),(191,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','10.87.11.6','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:22:12\",\"default\":false,\"dictCode\":106,\"dictLabel\":\"center_code\",\"dictSort\":6,\"dictType\":\"sys_vmns\",\"dictValue\":\"50010502\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:39:03',15),(192,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','10.87.11.6','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:22:23\",\"default\":false,\"dictCode\":107,\"dictLabel\":\"center_name\",\"dictSort\":7,\"dictType\":\"sys_vmns\",\"dictValue\":\"江北区支行\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-08 18:39:14',11),(193,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 17:22:12\",\"default\":false,\"dictCode\":100,\"dictLabel\":\"vmns_ip\",\"dictSort\":0,\"dictType\":\"sys_vmns\",\"dictValue\":\"10.87.23.200\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-09 14:06:20',41),(194,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:21:46\",\"default\":false,\"dictCode\":104,\"dictLabel\":\"org_code\",\"dictSort\":4,\"dictType\":\"sys_vmns\",\"dictValue\":\"511502012160000001\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-09 14:06:42',21),(195,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:21:55\",\"default\":false,\"dictCode\":105,\"dictLabel\":\"org_name\",\"dictSort\":5,\"dictType\":\"sys_vmns\",\"dictValue\":\"演示机构\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-09 14:06:51',23),(196,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:22:23\",\"default\":false,\"dictCode\":107,\"dictLabel\":\"center_name\",\"dictSort\":7,\"dictType\":\"sys_vmns\",\"dictValue\":\"演示机构\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-09 14:07:00',18),(197,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 18:22:12\",\"default\":false,\"dictCode\":106,\"dictLabel\":\"center_code\",\"dictSort\":6,\"dictType\":\"sys_vmns\",\"dictValue\":\"51150201\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-02-09 14:07:19',24),(198,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 17:22:22\",\"default\":false,\"dictCode\":109,\"dictLabel\":\"vmns_port\",\"dictSort\":1,\"dictType\":\"sys_vmns\",\"dictValue\":\"80\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-03-27 14:19:20',89),(199,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-02-08 17:22:22\",\"default\":false,\"dictCode\":109,\"dictLabel\":\"vmns_port\",\"dictSort\":1,\"dictType\":\"sys_vmns\",\"dictValue\":\"81\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-03-27 14:19:48',89),(200,'菜单管理',2,'com.xunmei.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"monitor/server/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":112,\"menuName\":\"服务监控\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":2,\"path\":\"server\",\"perms\":\"monitor:server:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-04-15 11:11:11',33),(201,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"demo/index\",\"createBy\":\"admin\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"视频大模型\",\"menuType\":\"C\",\"orderNum\":7,\"params\":{},\"parentId\":2000,\"path\":\"demo/index\",\"perms\":\"demo:index\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-12 16:39:51',32),(202,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/demo/index\",\"createTime\":\"2025-05-12 16:39:51\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2007,\"menuName\":\"视频大模型\",\"menuType\":\"C\",\"orderNum\":7,\"params\":{},\"parentId\":2000,\"path\":\"car/demo/index\",\"perms\":\"demo:index\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-12 16:40:08',30),(203,'字典类型',1,'com.xm.web.controller.system.SysDictTypeController.add()','POST',1,'admin','研发部门','/system/dict/type','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"dictName\":\"VSS检测行业\",\"dictType\":\"vss_industry\",\"params\":{},\"remark\":\"VSS检测的行业类型\",\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 09:55:06',41),(204,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"交通监控\",\"dictSort\":0,\"dictType\":\"vss_industry\",\"dictValue\":\"traffic\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 09:55:57',21),(205,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"工业园区\",\"dictSort\":1,\"dictType\":\"vss_industry\",\"dictValue\":\"commercial\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 09:57:21',23),(206,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"银行金融\",\"dictSort\":2,\"dictType\":\"vss_industry\",\"dictValue\":\"finance\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 09:58:12',19),(207,'代码生成',6,'com.xm.generator.controller.GenController.importTableSave()','POST',1,'admin','研发部门','/tool/gen/importTable','127.0.0.1','内网IP','{\"tables\":\"vss_result_resource,vss_channel,vss_algorithm\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:13:17',297),(208,'代码生成',2,'com.xm.generator.controller.GenController.editSave()','PUT',1,'admin','研发部门','/tool/gen','127.0.0.1','内网IP','{\"businessName\":\"algorithm\",\"className\":\"VssAlgorithm\",\"columns\":[{\"capJavaField\":\"Id\",\"columnComment\":\"算法主键编号\",\"columnId\":9,\"columnName\":\"id\",\"columnType\":\"int\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:13:16\",\"dictType\":\"\",\"edit\":false,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isPk\":\"1\",\"isRequired\":\"0\",\"javaField\":\"id\",\"javaType\":\"Long\",\"list\":false,\"params\":{},\"pk\":true,\"query\":false,\"queryType\":\"EQ\",\"required\":false,\"sort\":1,\"superColumn\":false,\"tableId\":2,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Name\",\"columnComment\":\"算法名称\",\"columnId\":10,\"columnName\":\"name\",\"columnType\":\"varchar(32)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:13:16\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"name\",\"javaType\":\"String\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"LIKE\",\"required\":false,\"sort\":2,\"superColumn\":false,\"tableId\":2,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"EnName\",\"columnComment\":\"英文名称\",\"columnId\":11,\"columnName\":\"en_name\",\"columnType\":\"varchar(32)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:13:16\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"enName\",\"javaType\":\"String\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"LIKE\",\"required\":false,\"sort\":3,\"superColumn\":false,\"tableId\":2,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Desc\",\"columnComment\":\"算法描述\",\"columnId\":12,\"columnName\":\"desc\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:13:16\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"desc\",\"javaT','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:16:18',104),(209,'代码生成',3,'com.xm.generator.controller.GenController.remove()','DELETE',1,'admin','研发部门','/tool/gen/3','127.0.0.1','内网IP','[3]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:17:16',185),(210,'代码生成',3,'com.xm.generator.controller.GenController.remove()','DELETE',1,'admin','研发部门','/tool/gen/4','127.0.0.1','内网IP','[4]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:17:18',43),(211,'代码生成',6,'com.xm.generator.controller.GenController.importTableSave()','POST',1,'admin','研发部门','/tool/gen/importTable','127.0.0.1','内网IP','{\"tables\":\"vss_result_resource,vss_channel\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:17:25',110),(212,'代码生成',2,'com.xm.generator.controller.GenController.editSave()','PUT',1,'admin','研发部门','/tool/gen','127.0.0.1','内网IP','{\"businessName\":\"channel\",\"className\":\"VssChannel\",\"columns\":[{\"capJavaField\":\"Id\",\"columnComment\":\"视频文件编号\",\"columnId\":31,\"columnName\":\"id\",\"columnType\":\"int\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":false,\"htmlType\":\"input\",\"increment\":true,\"insert\":true,\"isIncrement\":\"1\",\"isInsert\":\"1\",\"isPk\":\"1\",\"isRequired\":\"0\",\"javaField\":\"id\",\"javaType\":\"Long\",\"list\":false,\"params\":{},\"pk\":true,\"query\":false,\"queryType\":\"EQ\",\"required\":false,\"sort\":1,\"superColumn\":false,\"tableId\":5,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Url\",\"columnComment\":\"视频文件地址\",\"columnId\":32,\"columnName\":\"url\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"url\",\"javaType\":\"String\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"EQ\",\"required\":false,\"sort\":2,\"superColumn\":false,\"tableId\":5,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Name\",\"columnComment\":\"视频文件名称\",\"columnId\":33,\"columnName\":\"name\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"name\",\"javaType\":\"String\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"LIKE\",\"required\":false,\"sort\":3,\"superColumn\":false,\"tableId\":5,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"OriginName\",\"columnComment\":\"视频原名\",\"columnId\":34,\"columnName\":\"origin_name\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"originNam','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:17:50',72),(213,'代码生成',2,'com.xm.generator.controller.GenController.editSave()','PUT',1,'admin','研发部门','/tool/gen','127.0.0.1','内网IP','{\"businessName\":\"resource\",\"className\":\"VssResultResource\",\"columns\":[{\"capJavaField\":\"Id\",\"columnComment\":\"主键编号\",\"columnId\":42,\"columnName\":\"id\",\"columnType\":\"int\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":false,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isPk\":\"1\",\"isRequired\":\"0\",\"javaField\":\"id\",\"javaType\":\"Long\",\"list\":false,\"params\":{},\"pk\":true,\"query\":false,\"queryType\":\"EQ\",\"required\":false,\"sort\":1,\"superColumn\":false,\"tableId\":6,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"ChannelId\",\"columnComment\":\"VSS视频源编号\",\"columnId\":43,\"columnName\":\"channel_id\",\"columnType\":\"int\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"channelId\",\"javaType\":\"Long\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"EQ\",\"required\":false,\"sort\":2,\"superColumn\":false,\"tableId\":6,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Url\",\"columnComment\":\"检测结果资源地址\",\"columnId\":44,\"columnName\":\"url\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"url\",\"javaType\":\"String\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"EQ\",\"required\":false,\"sort\":3,\"superColumn\":false,\"tableId\":6,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Type\",\"columnComment\":\"检测结果资源类别\",\"columnId\":45,\"columnName\":\"type\",\"columnType\":\"tinyint\",\"createBy\":\"admin\",\"createTime\":\"2025-05-14 10:17:25\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"select\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"type\",\"j','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 10:18:14',71),(214,'字典数据',1,'com.xm.web.controller.system.SysDictDataController.add()','POST',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"default\":false,\"dictLabel\":\"测试\",\"dictSort\":0,\"dictType\":\"vss_industry\",\"dictValue\":\"test\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 11:02:31',81),(215,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-05-14 11:02:31\",\"default\":false,\"dictCode\":121,\"dictLabel\":\"测试\",\"dictSort\":3,\"dictType\":\"vss_industry\",\"dictValue\":\"test\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 11:02:40',40),(216,'字典数据',2,'com.xm.web.controller.system.SysDictDataController.edit()','PUT',1,'admin','研发部门','/system/dict/data','127.0.0.1','内网IP','{\"createBy\":\"admin\",\"createTime\":\"2025-05-14 09:57:21\",\"default\":false,\"dictCode\":119,\"dictLabel\":\"酒厂园区\",\"dictSort\":1,\"dictType\":\"vss_industry\",\"dictValue\":\"commercial\",\"isDefault\":\"N\",\"listClass\":\"default\",\"params\":{},\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 13:25:03',36),(217,'字典类型',3,'com.xm.web.controller.system.SysDictDataController.remove()','DELETE',1,'admin','研发部门','/system/dict/data/121','127.0.0.1','内网IP','[121]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-05-14 13:25:06',84),(218,'代码生成',6,'com.xm.generator.controller.GenController.importTableSave()','POST',1,'admin','研发部门','/tool/gen/importTable','127.0.0.1','内网IP','{\"tables\":\"cosmos_predict_history\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-07-08 16:12:45',144),(219,'代码生成',2,'com.xm.generator.controller.GenController.editSave()','PUT',1,'admin','研发部门','/tool/gen','127.0.0.1','内网IP','{\"businessName\":\"history\",\"className\":\"CosmosPredictHistory\",\"columns\":[{\"capJavaField\":\"Id\",\"columnComment\":\"主键，流水号\",\"columnId\":46,\"columnName\":\"id\",\"columnType\":\"bigint\",\"createBy\":\"admin\",\"createTime\":\"2025-07-08 16:12:45\",\"dictType\":\"\",\"edit\":false,\"htmlType\":\"input\",\"increment\":true,\"insert\":true,\"isIncrement\":\"1\",\"isInsert\":\"1\",\"isPk\":\"1\",\"isRequired\":\"0\",\"javaField\":\"id\",\"javaType\":\"Long\",\"list\":false,\"params\":{},\"pk\":true,\"query\":false,\"queryType\":\"EQ\",\"required\":false,\"sort\":1,\"superColumn\":false,\"tableId\":7,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"InputImageOrVideoPath\",\"columnComment\":\"输入图片或视频地址\",\"columnId\":47,\"columnName\":\"input_image_or_video_path\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-07-08 16:12:45\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"inputImageOrVideoPath\",\"javaType\":\"String\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"EQ\",\"required\":false,\"sort\":2,\"superColumn\":false,\"tableId\":7,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Type\",\"columnComment\":\"模型类型\",\"columnId\":48,\"columnName\":\"type\",\"columnType\":\"tinyint\",\"createBy\":\"admin\",\"createTime\":\"2025-07-08 16:12:45\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"select\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":\"0\",\"isQuery\":\"1\",\"isRequired\":\"0\",\"javaField\":\"type\",\"javaType\":\"Integer\",\"list\":true,\"params\":{},\"pk\":false,\"query\":true,\"queryType\":\"EQ\",\"required\":false,\"sort\":3,\"superColumn\":false,\"tableId\":7,\"updateBy\":\"\",\"usableColumn\":false},{\"capJavaField\":\"Prompt\",\"columnComment\":\"提示词\",\"columnId\":49,\"columnName\":\"prompt\",\"columnType\":\"varchar(255)\",\"createBy\":\"admin\",\"createTime\":\"2025-07-08 16:12:45\",\"dictType\":\"\",\"edit\":true,\"htmlType\":\"input\",\"increment\":false,\"insert\":true,\"isEdit\":\"1\",\"isIncrement\":\"0\",\"isInsert\":\"1\",\"isList\":\"1\",\"isPk\":','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-07-08 16:14:51',108),(220,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"index\",\"createBy\":\"admin\",\"icon\":\"tab\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"首页\",\"menuType\":\"C\",\"orderNum\":0,\"params\":{},\"parentId\":0,\"path\":\"/index\",\"perms\":\"index\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 12:24:28',43),(221,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"index\",\"createTime\":\"2025-12-02 12:24:28\",\"icon\":\"tab\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2008,\"menuName\":\"首页\",\"menuType\":\"C\",\"orderNum\":0,\"params\":{},\"parentId\":0,\"path\":\"index\",\"perms\":\"index\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 12:24:45',19),(222,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createBy\":\"admin\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"基本信息\",\"menuType\":\"M\",\"orderNum\":8,\"params\":{},\"parentId\":0,\"path\":\"/user/profile\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 13:22:26',14),(223,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-12-02 13:22:26\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2009,\"menuName\":\"基本信息\",\"menuType\":\"M\",\"orderNum\":8,\"params\":{},\"parentId\":0,\"path\":\"user/profile\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 13:22:45',11),(224,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-06 16:33:58\",\"icon\":\"system\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":1,\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":7,\"params\":{},\"parentId\":0,\"path\":\"system\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 13:54:42',48),(225,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"user/profile/resetPwd\",\"createBy\":\"admin\",\"icon\":\"lock\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"修改密码\",\"menuType\":\"C\",\"orderNum\":9,\"params\":{},\"parentId\":0,\"path\":\"user/profile/resetPwd\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 13:58:06',13),(226,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/2010','127.0.0.1','内网IP','2010','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 13:59:36',69),(227,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"server/index\",\"createTime\":\"2025-01-10 09:56:19\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2002,\"menuName\":\"服务器管理\",\"menuType\":\"C\",\"orderNum\":0,\"params\":{},\"parentId\":2000,\"path\":\"server\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:01:33',14),(228,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createBy\":\"admin\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":2,\"params\":{},\"parentId\":1,\"path\":\"system/user/index\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:03:06',14),(229,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/user/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":100,\"menuName\":\"用户管理\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2011,\"path\":\"user\",\"perms\":\"system:user:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:03:18',10),(230,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/role/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"peoples\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":101,\"menuName\":\"角色管理\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2011,\"path\":\"role\",\"perms\":\"system:role:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:03:31',15),(231,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/menu/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":102,\"menuName\":\"菜单管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2011,\"path\":\"menu\",\"perms\":\"system:menu:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:03:42',18),(232,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/dept/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"tree\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":103,\"menuName\":\"部门管理\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":2011,\"path\":\"dept\",\"perms\":\"system:dept:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:03:52',14),(233,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/post/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"post\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":104,\"menuName\":\"岗位管理\",\"menuType\":\"C\",\"orderNum\":5,\"params\":{},\"parentId\":2011,\"path\":\"post\",\"perms\":\"system:post:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:04:05',15),(234,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/dict/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"dict\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":105,\"menuName\":\"字典管理\",\"menuType\":\"C\",\"orderNum\":6,\"params\":{},\"parentId\":2011,\"path\":\"dict\",\"perms\":\"system:dict:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:04:13',10),(235,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/config/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"edit\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":106,\"menuName\":\"参数设置\",\"menuType\":\"C\",\"orderNum\":7,\"params\":{},\"parentId\":2011,\"path\":\"config\",\"perms\":\"system:config:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:04:21',14),(236,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/notice/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"message\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":107,\"menuName\":\"通知公告\",\"menuType\":\"C\",\"orderNum\":8,\"params\":{},\"parentId\":2011,\"path\":\"notice\",\"perms\":\"system:notice:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:04:30',23),(237,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":108,\"menuName\":\"日志管理\",\"menuType\":\"M\",\"orderNum\":9,\"params\":{},\"parentId\":2011,\"path\":\"log\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:04:37',14),(238,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-08 11:12:51\",\"icon\":\"job\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2000,\"menuName\":\"训推管理\",\"menuType\":\"M\",\"orderNum\":4,\"params\":{},\"parentId\":1,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:05:33',16),(239,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-08 11:12:51\",\"icon\":\"job\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2000,\"menuName\":\"训推管理\",\"menuType\":\"M\",\"orderNum\":1,\"params\":{},\"parentId\":1,\"path\":\"car\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:06:02',18),(240,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-12-02 14:03:06\",\"icon\":\"system\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2011,\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":2,\"params\":{},\"parentId\":1,\"path\":\"system/user/index\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:06:49',14),(241,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-06 16:33:58\",\"icon\":\"tool\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":3,\"menuName\":\"系统工具\",\"menuType\":\"M\",\"orderNum\":9,\"params\":{},\"parentId\":0,\"path\":\"tool\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:07:35',14),(242,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-06 16:33:58\",\"icon\":\"monitor\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2,\"menuName\":\"系统监控\",\"menuType\":\"M\",\"orderNum\":10,\"params\":{},\"parentId\":0,\"path\":\"monitor\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:07:40',10),(243,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createBy\":\"admin\",\"icon\":\"skill\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"视频审批\",\"menuType\":\"M\",\"orderNum\":2,\"params\":{},\"parentId\":0,\"path\":\"media/approval\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:09:49',13),(244,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/mine\",\"createBy\":\"admin\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2012,\"path\":\"video/approval/mine\",\"perms\":\"video/approval/mine\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:11:08',16),(245,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/mine\",\"createTime\":\"2025-12-02 14:11:08\",\"icon\":\"#\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2013,\"menuName\":\"我的审批\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2012,\"path\":\"video/approval/mine\",\"perms\":\"video/approval/mine\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:11:20',9),(246,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/apply\",\"createBy\":\"admin\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2013,\"path\":\"video/approval/apply\",\"perms\":\"video:approval:apply\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:12:26',39),(247,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/apply\",\"createTime\":\"2025-12-02 14:12:26\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2014,\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2012,\"path\":\"video/approval/apply\",\"perms\":\"video:approval:apply\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:12:53',15),(248,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/mine\",\"createTime\":\"2025-12-02 14:11:08\",\"icon\":\"button\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2013,\"menuName\":\"我的审批\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2012,\"path\":\"video/approval/mine\",\"perms\":\"video/approval/mine\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:13:10',14),(249,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/all\",\"createBy\":\"admin\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"全部审批\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2012,\"path\":\"video/approval/all\",\"perms\":\"video:approval:all\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:14:23',8),(250,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/play\",\"createBy\":\"admin\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"视频流管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"video/list\",\"perms\":\"video:list\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:17:12',13),(251,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/monitor\",\"createBy\":\"admin\",\"icon\":\"build\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"video/monitor\",\"perms\":\"video:monitor\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:17:56',14),(252,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/monitor\",\"createTime\":\"2025-12-02 14:17:56\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2017,\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"video/monitor\",\"perms\":\"video:monitor\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:18:28',16),(253,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/dashboard\",\"createBy\":\"admin\",\"icon\":\"dashboard\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"行为预警\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"video/dashboard\",\"perms\":\"video:dashboard\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 14:19:13',6),(254,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-06 16:33:58\",\"icon\":\"system\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":1,\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":7,\"params\":{},\"parentId\":0,\"path\":\"system/user/index\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:15:43',11),(255,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-06 16:33:58\",\"icon\":\"system\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":1,\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":7,\"params\":{},\"parentId\":0,\"path\":\"system/user/index\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:16:35',9),(256,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/system/user/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":100,\"menuName\":\"用户管理\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2011,\"path\":\"user\",\"perms\":\"system:user:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:17:26',9),(257,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-12-02 14:03:06\",\"icon\":\"system\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2011,\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":2,\"params\":{},\"parentId\":1,\"path\":\"system\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:19:40',20),(258,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/system/user/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":100,\"menuName\":\"用户管理\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2011,\"path\":\"user\",\"perms\":\"system:user:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:19:50',11),(259,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-01-06 16:33:58\",\"icon\":\"system\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":1,\"menuName\":\"系统管理\",\"menuType\":\"M\",\"orderNum\":7,\"params\":{},\"parentId\":0,\"path\":\"system\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:20:24',15),(260,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/user/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":100,\"menuName\":\"用户管理\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2011,\"path\":\"user\",\"perms\":\"system:user:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:21:48',13),(261,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"car/device/index\",\"createTime\":\"2025-01-08 11:16:09\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2001,\"menuName\":\"设备列表\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2000,\"path\":\"device\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:27:58',14),(262,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/2007','127.0.0.1','内网IP','2007','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:28:49',10),(263,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/2001','127.0.0.1','内网IP','2001','{\"msg\":\"菜单已分配,不允许删除\",\"code\":601}',0,NULL,'2025-12-02 15:29:33',3),(264,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/2001','127.0.0.1','内网IP','2001','{\"msg\":\"菜单已分配,不允许删除\",\"code\":601}',0,NULL,'2025-12-02 15:29:41',4),(265,'角色管理',3,'com.xm.web.controller.system.SysRoleController.remove()','DELETE',1,'admin','研发部门','/system/role/2','127.0.0.1','内网IP','[2]',NULL,1,'普通角色已分配,不能删除','2025-12-02 15:29:54',88),(266,'用户管理',3,'com.xm.web.controller.system.SysUserController.remove()','DELETE',1,'admin','研发部门','/system/user/100','127.0.0.1','内网IP','[100]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:30:07',31),(267,'角色管理',3,'com.xm.web.controller.system.SysRoleController.remove()','DELETE',1,'admin','研发部门','/system/role/2','127.0.0.1','内网IP','[2]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:30:13',19),(268,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/2001','127.0.0.1','内网IP','2001','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:30:42',13),(269,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"server/index\",\"createTime\":\"2025-01-10 09:56:19\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2002,\"menuName\":\"一体机管理\",\"menuType\":\"C\",\"orderNum\":0,\"params\":{},\"parentId\":2000,\"path\":\"server\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:30:56',16),(270,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/apply\",\"createTime\":\"2025-12-02 14:12:26\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2014,\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2012,\"path\":\"apply\",\"perms\":\"video:approval:apply\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:40:11',58),(271,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"video/approval/apply\",\"createTime\":\"2025-12-02 14:12:26\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2014,\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2012,\"path\":\"apply\",\"perms\":\"video:approval:apply\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:40:16',20),(272,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"video/approval/mine\",\"createTime\":\"2025-12-02 14:11:08\",\"icon\":\"button\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2013,\"menuName\":\"我的审批\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2012,\"path\":\"mine\",\"perms\":\"video/approval/mine\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:40:24',26),(273,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"video/approval/mine\",\"createTime\":\"2025-12-02 14:11:08\",\"icon\":\"button\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2013,\"menuName\":\"我的审批\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2012,\"path\":\"mine\",\"perms\":\"video:approval:mine\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:40:57',18),(274,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/monitor\",\"createTime\":\"2025-12-02 14:17:56\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2017,\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"monitor\",\"perms\":\"video:monitor\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:07',34),(275,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"/video/approval/all\",\"createTime\":\"2025-12-02 14:14:23\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2015,\"menuName\":\"全部审批\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2012,\"path\":\"all\",\"perms\":\"video:approval:all\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:14',11),(276,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"video/approval/all\",\"createTime\":\"2025-12-02 14:14:23\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2015,\"menuName\":\"全部审批\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2012,\"path\":\"all\",\"perms\":\"video:approval:all\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:19',17),(277,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-12-02 14:09:49\",\"icon\":\"skill\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2012,\"menuName\":\"视频审批\",\"menuType\":\"M\",\"orderNum\":2,\"params\":{},\"parentId\":0,\"path\":\"media/approval\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:27',14),(278,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/approval/apply\",\"createTime\":\"2025-12-02 14:12:26\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2014,\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2012,\"path\":\"apply\",\"perms\":\"media:approval:apply\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:39',80),(279,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/approval/mine\",\"createTime\":\"2025-12-02 14:11:08\",\"icon\":\"button\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2013,\"menuName\":\"我的审批\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":2012,\"path\":\"mine\",\"perms\":\"media:approval:mine\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:45',14),(280,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/approval/all\",\"createTime\":\"2025-12-02 14:14:23\",\"icon\":\"list\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2015,\"menuName\":\"全部审批\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":2012,\"path\":\"all\",\"perms\":\"media:approval:all\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:50',10),(281,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/monitor\",\"createTime\":\"2025-12-02 14:17:56\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2017,\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"monitor\",\"perms\":\"media:monitor\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:41:58',17),(282,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/play\",\"createTime\":\"2025-12-02 14:17:12\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2016,\"menuName\":\"视频流管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"list\",\"perms\":\"media:list\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:42:10',19),(283,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/media\",\"createTime\":\"2025-12-02 14:17:12\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2016,\"menuName\":\"视频流管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"list\",\"perms\":\"media:list\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:42:18',15),(284,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/list\",\"createTime\":\"2025-12-02 14:17:12\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2016,\"menuName\":\"视频流管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"list\",\"perms\":\"media:list\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:42:24',16),(285,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/dashboard\",\"createTime\":\"2025-12-02 14:19:13\",\"icon\":\"dashboard\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2018,\"menuName\":\"行为预警\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"dashboard\",\"perms\":\"media:dashboard\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:42:37',16),(286,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/list/index\",\"createTime\":\"2025-12-02 14:17:12\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2016,\"menuName\":\"视频流管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"list\",\"perms\":\"media:list\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:57:56',18),(287,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/monitor/index\",\"createTime\":\"2025-12-02 14:17:56\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2017,\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"monitor\",\"perms\":\"media:monitor\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:58:02',16),(288,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/dashboard/index\",\"createTime\":\"2025-12-02 14:19:13\",\"icon\":\"dashboard\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2018,\"menuName\":\"行为预警\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"dashboard\",\"perms\":\"media:dashboard\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:58:08',17),(289,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/monitor/index\",\"createTime\":\"2025-12-02 14:17:56\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2017,\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":0,\"path\":\"mediaMonitor\",\"perms\":\"media:monitor\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 15:59:06',12),(290,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/115','127.0.0.1','内网IP','115','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:11:52',13),(291,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createTime\":\"2025-12-02 14:09:49\",\"icon\":\"skill\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2012,\"menuName\":\"视频审批\",\"menuType\":\"M\",\"orderNum\":2,\"params\":{},\"parentId\":0,\"path\":\"mediaApproval\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:21:45',14),(292,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/approval/apply\",\"createTime\":\"2025-12-02 14:12:26\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2014,\"menuName\":\"我的申请\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":2012,\"path\":\"apply\",\"perms\":\"media:approval:apply\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:21:54',14),(293,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/dashboard/index\",\"createTime\":\"2025-12-02 14:19:13\",\"icon\":\"dashboard\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2018,\"menuName\":\"行为预警\",\"menuType\":\"C\",\"orderNum\":5,\"params\":{},\"parentId\":0,\"path\":\"dashboard\",\"perms\":\"media:dashboard\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:35:53',103),(294,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"media/monitor/index\",\"createTime\":\"2025-12-02 14:17:56\",\"icon\":\"server\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2017,\"menuName\":\"视频监控\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":0,\"path\":\"mediaMonitor\",\"perms\":\"media:monitor\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:36:00',12),(295,'字典类型',3,'com.xm.web.controller.system.SysDictTypeController.remove()','DELETE',1,'admin','研发部门','/system/dict/type/102','127.0.0.1','内网IP','[102]',NULL,1,'VSS检测行业已分配,不能删除','2025-12-02 16:43:17',10),(296,'字典类型',3,'com.xm.web.controller.system.SysDictTypeController.remove()','DELETE',1,'admin','研发部门','/system/dict/type/102','127.0.0.1','内网IP','[102]',NULL,1,'VSS检测行业已分配,不能删除','2025-12-02 16:43:24',6),(297,'字典类型',3,'com.xm.web.controller.system.SysDictDataController.remove()','DELETE',1,'admin','研发部门','/system/dict/data/118','127.0.0.1','内网IP','[118]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:43:31',30),(298,'字典类型',3,'com.xm.web.controller.system.SysDictDataController.remove()','DELETE',1,'admin','研发部门','/system/dict/data/119','127.0.0.1','内网IP','[119]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:43:33',16),(299,'字典类型',3,'com.xm.web.controller.system.SysDictDataController.remove()','DELETE',1,'admin','研发部门','/system/dict/data/120','127.0.0.1','内网IP','[120]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:43:35',175),(300,'字典类型',3,'com.xm.web.controller.system.SysDictTypeController.remove()','DELETE',1,'admin','研发部门','/system/dict/type/102','127.0.0.1','内网IP','[102]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:43:47',26),(301,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"createBy\":\"admin\",\"icon\":\"link\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"退出登录\",\"menuType\":\"M\",\"orderNum\":11,\"params\":{},\"parentId\":0,\"path\":\"__logout__\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:54:31',18),(302,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0\",\"children\":[],\"deptId\":100,\"deptName\":\"中国民航大学\",\"email\":\"\",\"leader\":\"\",\"orderNum\":0,\"params\":{},\"parentId\":0,\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:57:44',39),(303,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100\",\"children\":[],\"deptId\":101,\"deptName\":\"南院\",\"email\":\"\",\"leader\":\"\",\"orderNum\":1,\"params\":{},\"parentId\":100,\"parentName\":\"中国民航大学\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:57:53',72),(304,'部门管理',1,'com.xm.web.controller.system.SysDeptController.add()','POST',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100\",\"children\":[],\"createBy\":\"admin\",\"deptName\":\"北院\",\"orderNum\":0,\"params\":{},\"parentId\":100,\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:58:01',16),(305,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100\",\"children\":[],\"deptId\":110,\"deptName\":\"北院\",\"orderNum\":2,\"params\":{},\"parentId\":100,\"parentName\":\"中国民航大学\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:58:19',25),(306,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":103,\"deptName\":\"教学楼1\",\"email\":\"\",\"leader\":\"\",\"orderNum\":1,\"params\":{},\"parentId\":101,\"parentName\":\"南院\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:58:33',28),(307,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":104,\"deptName\":\"教学楼2\",\"email\":\"\",\"leader\":\"\",\"orderNum\":2,\"params\":{},\"parentId\":101,\"parentName\":\"南院\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:58:41',25),(308,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":105,\"deptName\":\"教学楼3\",\"email\":\"\",\"leader\":\"\",\"orderNum\":3,\"params\":{},\"parentId\":101,\"parentName\":\"南院\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:58:48',39),(309,'部门管理',2,'com.xm.web.controller.system.SysDeptController.edit()','PUT',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101\",\"children\":[],\"deptId\":106,\"deptName\":\"教学楼4\",\"email\":\"\",\"leader\":\"\",\"orderNum\":4,\"params\":{},\"parentId\":101,\"parentName\":\"南院\",\"phone\":\"\",\"status\":\"0\",\"updateBy\":\"admin\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:58:54',25),(310,'部门管理',1,'com.xm.web.controller.system.SysDeptController.add()','POST',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101,103\",\"children\":[],\"createBy\":\"admin\",\"deptName\":\"教室1\",\"orderNum\":0,\"params\":{},\"parentId\":103,\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:59:01',16),(311,'部门管理',1,'com.xm.web.controller.system.SysDeptController.add()','POST',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,101,103\",\"children\":[],\"createBy\":\"admin\",\"deptName\":\"教室2\",\"orderNum\":1,\"params\":{},\"parentId\":103,\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:59:10',16),(312,'部门管理',1,'com.xm.web.controller.system.SysDeptController.add()','POST',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,110\",\"children\":[],\"createBy\":\"admin\",\"deptName\":\"教学楼1\",\"orderNum\":0,\"params\":{},\"parentId\":110,\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:59:18',9),(313,'部门管理',1,'com.xm.web.controller.system.SysDeptController.add()','POST',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,110\",\"children\":[],\"createBy\":\"admin\",\"deptName\":\"教学楼2\",\"orderNum\":1,\"params\":{},\"parentId\":110,\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:59:26',34),(314,'部门管理',1,'com.xm.web.controller.system.SysDeptController.add()','POST',1,'admin','研发部门','/system/dept','127.0.0.1','内网IP','{\"ancestors\":\"0,100,110\",\"children\":[],\"createBy\":\"admin\",\"deptName\":\"教学楼3\",\"orderNum\":2,\"params\":{},\"parentId\":110,\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 16:59:37',15),(315,'菜单管理',1,'com.xm.web.controller.system.SysMenuController.add()','POST',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/dict/data\",\"createBy\":\"admin\",\"icon\":\"dict\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuName\":\"字典数据\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":105,\"path\":\"dict-data\",\"status\":\"0\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 17:06:13',14),(316,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/dict/data\",\"createTime\":\"2025-12-02 17:06:13\",\"icon\":\"dict\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2020,\"menuName\":\"字典数据\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":105,\"path\":\"dict-data\",\"perms\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 17:07:16',26),(317,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','研发部门','/system/menu/2020','127.0.0.1','内网IP','2020','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 17:08:18',16),(318,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','研发部门','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"index\",\"createTime\":\"2025-12-02 12:24:28\",\"icon\":\"guide\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":2008,\"menuName\":\"首页\",\"menuType\":\"C\",\"orderNum\":0,\"params\":{},\"parentId\":0,\"path\":\"index\",\"perms\":\"index\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-02 17:08:55',16),(319,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2011','127.0.0.1','内网IP','2011','{\"msg\":\"存在子菜单,不允许删除\",\"code\":601}',0,NULL,'2025-12-15 10:22:00',15),(320,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2015','127.0.0.1','内网IP','2015','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:17',55),(321,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2013','127.0.0.1','内网IP','2013','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:19',11),(322,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2014','127.0.0.1','内网IP','2014','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:21',15),(323,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2012','127.0.0.1','内网IP','2012','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:24',41),(324,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2016','127.0.0.1','内网IP','2016','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:27',19),(325,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2017','127.0.0.1','内网IP','2017','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:30',44),(326,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2018','127.0.0.1','内网IP','2018','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:33',12),(327,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2002','127.0.0.1','内网IP','2002','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:36',17),(328,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2003','127.0.0.1','内网IP','2003','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:39',19),(329,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2004','127.0.0.1','内网IP','2004','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:41',28),(330,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2005','127.0.0.1','内网IP','2005','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:44',16),(331,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2006','127.0.0.1','内网IP','2006','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:47',16),(332,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2000','127.0.0.1','内网IP','2000','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:22:50',15),(333,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/user/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"user\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":100,\"menuName\":\"用户管理\",\"menuType\":\"C\",\"orderNum\":1,\"params\":{},\"parentId\":1,\"path\":\"user\",\"perms\":\"system:user:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:01',33),(334,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/role/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"peoples\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":101,\"menuName\":\"角色管理\",\"menuType\":\"C\",\"orderNum\":2,\"params\":{},\"parentId\":1,\"path\":\"role\",\"perms\":\"system:role:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:09',17),(335,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/menu/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"tree-table\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":102,\"menuName\":\"菜单管理\",\"menuType\":\"C\",\"orderNum\":3,\"params\":{},\"parentId\":1,\"path\":\"menu\",\"perms\":\"system:menu:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:19',16),(336,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/dept/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"tree\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":103,\"menuName\":\"部门管理\",\"menuType\":\"C\",\"orderNum\":4,\"params\":{},\"parentId\":1,\"path\":\"dept\",\"perms\":\"system:dept:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:26',16),(337,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/post/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"post\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":104,\"menuName\":\"岗位管理\",\"menuType\":\"C\",\"orderNum\":5,\"params\":{},\"parentId\":1,\"path\":\"post\",\"perms\":\"system:post:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:33',26),(338,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/dict/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"dict\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":105,\"menuName\":\"字典管理\",\"menuType\":\"C\",\"orderNum\":6,\"params\":{},\"parentId\":1,\"path\":\"dict\",\"perms\":\"system:dict:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:39',15),(339,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/config/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"edit\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":106,\"menuName\":\"参数设置\",\"menuType\":\"C\",\"orderNum\":7,\"params\":{},\"parentId\":1,\"path\":\"config\",\"perms\":\"system:config:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:44',17),(340,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"system/notice/index\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"message\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":107,\"menuName\":\"通知公告\",\"menuType\":\"C\",\"orderNum\":8,\"params\":{},\"parentId\":1,\"path\":\"notice\",\"perms\":\"system:notice:list\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:52',23),(341,'菜单管理',2,'com.xm.web.controller.system.SysMenuController.edit()','PUT',1,'admin','教学楼1','/system/menu','127.0.0.1','内网IP','{\"children\":[],\"component\":\"\",\"createTime\":\"2025-01-06 16:33:59\",\"icon\":\"log\",\"isCache\":\"0\",\"isFrame\":\"1\",\"menuId\":108,\"menuName\":\"日志管理\",\"menuType\":\"M\",\"orderNum\":9,\"params\":{},\"parentId\":1,\"path\":\"log\",\"perms\":\"\",\"query\":\"\",\"routeName\":\"\",\"status\":\"0\",\"updateBy\":\"admin\",\"visible\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:23:58',16),(342,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/2011','127.0.0.1','内网IP','2011','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2025-12-15 10:24:02',18),(343,'菜单管理',3,'com.xm.web.controller.system.SysMenuController.remove()','DELETE',1,'admin','教学楼1','/system/menu/116','127.0.0.1','内网IP','116','{\"msg\":\"存在子菜单,不允许删除\",\"code\":601}',0,NULL,'2025-12-15 10:24:19',3),(344,'企业管理',1,'com.xm.web.controller.system.SysEnterpriseController.add()','POST',1,'admin','教学楼1','/system/enterprise','127.0.0.1','内网IP','{\"accessKey\":\"AKE04641532BE70DC98DFC8A290527E4AC\",\"createBy\":\"admin\",\"delFlag\":\"0\",\"enterpriseCode\":\"0001\",\"enterpriseId\":1,\"enterpriseName\":\"aaaa\",\"params\":{},\"secretKey\":\"SK546dd254967c0c7bb6f63b3e477cd91dd8d91addeda7900c4bcc67f317ffd877\",\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200,\"data\":{\"accessKey\":\"AKE04641532BE70DC98DFC8A290527E4AC\",\"enterpriseCode\":\"0001\",\"enterpriseId\":1,\"enterpriseName\":\"aaaa\",\"params\":{},\"secretKey\":\"SK546dd254967c0c7bb6f63b3e477cd91dd8d91addeda7900c4bcc67f317ffd877\"}}',0,NULL,'2026-02-03 06:34:14',168),(345,'企业管理',1,'com.xm.web.controller.system.SysEnterpriseController.add()','POST',1,'admin','教学楼1','/system/enterprise','127.0.0.1','内网IP','{\"accessKey\":\"AKC77DA40C937B68ED810324CF4CFDDBC7\",\"createBy\":\"admin\",\"delFlag\":\"0\",\"enterpriseCode\":\"bbb\",\"enterpriseId\":2,\"enterpriseName\":\"bbb\",\"params\":{},\"secretKey\":\"SK0f1ddaf3718265564794f79eb3cbd35b245b15c635ca722a23a684f9c3f17406\",\"status\":\"0\"}','{\"msg\":\"操作成功\",\"code\":200,\"data\":{\"accessKey\":\"AKC77DA40C937B68ED810324CF4CFDDBC7\",\"enterpriseCode\":\"bbb\",\"enterpriseId\":2,\"enterpriseName\":\"bbb\",\"params\":{},\"secretKey\":\"SK0f1ddaf3718265564794f79eb3cbd35b245b15c635ca722a23a684f9c3f17406\"}}',0,NULL,'2026-02-04 05:36:11',28),(346,'企业管理',3,'com.xm.web.controller.system.SysEnterpriseController.remove()','DELETE',1,'admin','教学楼1','/system/enterprise/2','127.0.0.1','内网IP','[2]','{\"msg\":\"操作成功\",\"code\":200}',0,NULL,'2026-02-04 05:36:23',80);
/*!40000 ALTER TABLE `sys_oper_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_org`
--

DROP TABLE IF EXISTS `sys_org`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_org` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ç»Ÿä¸€ä¸»é”®ID',
  `org_code` varchar(100) NOT NULL COMMENT 'ç»„ç»‡ç¼–ç  (ä¸šåŠ¡ä¸»é”®)',
  `org_name` varchar(255) NOT NULL COMMENT 'ç»„ç»‡åç§°',
  `short_name` varchar(100) DEFAULT NULL COMMENT 'ç»„ç»‡ç®€ç§°',
  `parent_code` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§ç»„ç»‡ç¼–ç  (ç”¨äºŽæž„å»ºæ ‘)',
  `org_type` varchar(50) DEFAULT NULL COMMENT 'ç±»åž‹æ˜ å°„: COMPANY/DEPT/PLANT',
  `is_active` tinyint(1) DEFAULT '1' COMMENT 'æ˜¯å¦æœ‰æ•ˆ (1=æ˜¯, 0=å¦)',
  `source_system` varchar(20) NOT NULL COMMENT 'æ¥æºç³»ç»Ÿ: OSN(æ¬§ç¥žè¯º) / DW(å¸çŽ‹)',
  `original_id` varchar(100) DEFAULT NULL COMMENT 'åŽŸç³»ç»Ÿçš„ä¸»é”®ID',
  `created_at` datetime DEFAULT NULL COMMENT 'åˆ›å»ºæ—¶é—´',
  `updated_at` datetime DEFAULT NULL COMMENT 'æœ€åŽä¿®æ”¹æ—¶é—´',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_source_code` (`source_system`,`org_code`),
  KEY `idx_parent` (`parent_code`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='é›†å›¢ç»Ÿä¸€ç»„ç»‡ä¸»è¡¨';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_org`
--

LOCK TABLES `sys_org` WRITE;
/*!40000 ALTER TABLE `sys_org` DISABLE KEYS */;
INSERT INTO `sys_org` VALUES (1,'3000','欧神诺经营分析',NULL,NULL,'OTHER',1,'OSN','3000','2026-02-03 16:09:07','2026-02-04 11:38:51'),(2,'2000','欧神诺财务报表',NULL,NULL,'OTHER',1,'OSN','2000','2026-02-03 16:09:07','2026-02-04 11:38:51'),(3,'1000','佛山欧神诺陶瓷有限公司','三水生产基地',NULL,'COMPANY',1,'OSN','1000','2026-02-03 16:09:07','2026-02-04 11:38:51'),(4,'1060','杭州欧神诺云商科技有限公司',NULL,'佛山欧神诺陶瓷有限公司','COMPANY',1,'OSN','1060','2026-02-03 16:09:07','2026-02-04 11:38:51'),(5,'1030','佛山欧神诺云商科技有限公司',NULL,'佛山欧神诺陶瓷有限公司','COMPANY',1,'OSN','1030','2026-02-03 16:09:07','2026-02-04 11:38:51'),(6,'1020','广西欧神诺陶瓷有限公司','广西生产基地','佛山欧神诺陶瓷有限公司','COMPANY',1,'OSN','1020','2026-02-03 16:09:07','2026-02-04 11:38:51'),(7,'1010','景德镇欧神诺陶瓷有限公司','景德镇生产基地','佛山欧神诺陶瓷有限公司','COMPANY',1,'OSN','1010','2026-02-03 16:09:07','2026-02-04 11:38:51'),(8,'DW_CODE_001','帝王集团总部',NULL,NULL,'1',1,'DW','DW_CODE_001','2026-02-03 16:09:07','2026-02-04 11:38:51'),(9,'DW_CODE_002','财务中心',NULL,NULL,'1',1,'DW','DW_CODE_002','2026-02-03 16:09:07','2026-02-04 11:38:51'),(10,'DW_CODE_003','人力资源中心',NULL,NULL,'1',1,'DW','DW_CODE_003','2026-02-03 16:09:07','2026-02-04 11:38:51'),(11,'DW_CODE_004','华北销售大区',NULL,NULL,'1',1,'DW','DW_CODE_004','2026-02-03 16:09:07','2026-02-04 11:38:51'),(12,'DW_CODE_005','深圳生产基地',NULL,NULL,'1',1,'DW','DW_CODE_005','2026-02-03 16:09:07','2026-02-04 11:38:51'),(13,'DW_CODE_006','海外事业部',NULL,NULL,'1',1,'DW','DW_CODE_006','2026-02-03 16:09:07','2026-02-04 11:38:51'),(15,'DEPT_001','研发中心','R&D',NULL,'DEPT',1,'DW','DEPT_001','2026-02-04 11:41:47','2026-02-04 11:50:56');
/*!40000 ALTER TABLE `sys_org` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_org_ext_dw`
--

DROP TABLE IF EXISTS `sys_org_ext_dw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_org_ext_dw` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `master_id` bigint NOT NULL COMMENT 'å…³è”ä¸»è¡¨ID',
  `org_classify` varchar(50) DEFAULT NULL COMMENT 'ç»„ç»‡åˆ†ç±»',
  `is_hr_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦äººåŠ›èµ„æºç»„ç»‡',
  `is_legacy_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦é—ç•™ç»„ç»‡',
  `is_operating_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦è¿è¥ç»„ç»‡',
  `is_inventory_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦åº“å­˜ç»„ç»‡',
  `is_plant_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦å·¥åŽ‚ç»„ç»‡',
  `is_asset_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦èµ„äº§ç»„ç»‡',
  `is_audit_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦å®¡è®¡ç»„ç»‡',
  `is_service_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦æœåŠ¡ç»„ç»‡',
  `is_settlement_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦ç»“ç®—ç»„ç»‡',
  `is_budget_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦é¢„ç®—ç»„ç»‡',
  `is_portal_org` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦é—¨æˆ·ç»„ç»‡',
  `is_profit_center` tinyint(1) DEFAULT NULL COMMENT 'æ˜¯å¦åˆ©æ¶¦ä¸­å¿ƒ',
  `sys_version` varchar(50) DEFAULT NULL COMMENT 'ç³»ç»Ÿç‰ˆæœ¬å·',
  `time_zone_info` varchar(100) DEFAULT NULL COMMENT 'æ—¶åŒºä¿¡æ¯',
  `default_language` varchar(50) DEFAULT NULL COMMENT 'é»˜è®¤è¯­è¨€',
  `default_theme` varchar(50) DEFAULT NULL COMMENT 'é»˜è®¤ä¸»é¢˜',
  `manage_type` varchar(50) DEFAULT NULL COMMENT 'ç®¡ç†ç±»åž‹',
  `bom_ref_org` varchar(100) DEFAULT NULL COMMENT 'BOMå¼•ç”¨ç»„ç»‡',
  `date_format` varchar(50) DEFAULT NULL COMMENT 'æ—¥æœŸæ ¼å¼',
  `time_format` varchar(50) DEFAULT NULL COMMENT 'æ—¶é—´æ ¼å¼',
  `number_format` varchar(50) DEFAULT NULL COMMENT 'æ•°å­—æ ¼å¼',
  `currency_format` varchar(50) DEFAULT NULL COMMENT 'è´§å¸æ ¼å¼',
  `location` varchar(200) DEFAULT NULL COMMENT 'æ‰€åœ¨åœ°ç‚¹',
  `register_address` varchar(200) DEFAULT NULL COMMENT 'æ³¨å†Œåœ°å€',
  `master_site` varchar(100) DEFAULT NULL COMMENT 'ä¸»ç«™ç‚¹',
  `company_type` varchar(50) DEFAULT NULL COMMENT 'å…¬å¸ç±»åž‹',
  `contact` varchar(100) DEFAULT NULL COMMENT 'è”ç³»äºº',
  `work_calendar` varchar(100) DEFAULT NULL COMMENT 'å·¥ä½œæ—¥åŽ†',
  `effective_start_date` datetime DEFAULT NULL COMMENT 'ç”Ÿæ•ˆæ—¥æœŸ',
  `effective_disable_date` datetime DEFAULT NULL COMMENT 'å¤±æ•ˆæ—¥æœŸ',
  `created_by` varchar(100) DEFAULT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_id` (`master_id`),
  CONSTRAINT `sys_org_ext_dw_ibfk_1` FOREIGN KEY (`master_id`) REFERENCES `sys_org` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='U9æ•°æ®æ‰©å±•è¡¨';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_org_ext_dw`
--

LOCK TABLES `sys_org_ext_dw` WRITE;
/*!40000 ALTER TABLE `sys_org_ext_dw` DISABLE KEYS */;
INSERT INTO `sys_org_ext_dw` VALUES (1,8,'1',0,0,0,0,0,0,0,0,0,0,0,0,'VPOrg','80083',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,9,'1',0,0,0,0,0,0,0,0,0,0,0,0,'VPOrg','80083',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'张三丰',NULL,NULL,NULL,NULL,NULL),(3,10,'1',1,0,0,0,0,0,0,0,0,0,0,0,NULL,'80083',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'李四',NULL,NULL,NULL,NULL,NULL),(4,11,'1',0,0,1,0,0,0,0,0,0,0,0,0,NULL,'80083',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'王五',NULL,NULL,NULL,NULL,NULL),(5,12,'1',0,0,0,0,1,0,0,0,0,0,0,0,NULL,'80083',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'赵六',NULL,NULL,NULL,NULL,NULL),(6,13,'1',0,0,0,0,0,0,0,0,0,0,0,0,NULL,'80083','En_US',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,15,'DEPT',0,0,1,0,0,0,0,0,0,0,0,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_org_ext_dw` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_org_ext_osn`
--

DROP TABLE IF EXISTS `sys_org_ext_osn`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_org_ext_osn` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `master_id` bigint NOT NULL COMMENT 'å…³è”ä¸»è¡¨ID',
  `org_form` varchar(50) DEFAULT NULL COMMENT 'ç»„ç»‡å½¢æ€',
  `admin_org` varchar(100) DEFAULT NULL COMMENT 'æ‰€å±žè¡Œæ”¿ç»„ç»‡',
  `is_dept` char(1) DEFAULT NULL COMMENT 'æ˜¯å¦éƒ¨é—¨',
  `dept_nature` varchar(100) DEFAULT NULL COMMENT 'éƒ¨é—¨æ€§è´¨',
  `principal_name` varchar(100) DEFAULT NULL COMMENT 'è´Ÿè´£äºº',
  `vp_leader` varchar(100) DEFAULT NULL COMMENT 'åˆ†ç®¡é¢†å¯¼',
  `contact_person` varchar(100) DEFAULT NULL COMMENT 'è”ç³»äºº',
  `phone` varchar(50) DEFAULT NULL COMMENT 'å…¬å¸ç”µè¯',
  `other_principal` varchar(100) DEFAULT NULL COMMENT 'å…¶ä»–è´Ÿè´£äºº',
  `resp_post` varchar(100) DEFAULT NULL COMMENT 'è´Ÿè´£å²—',
  `taxpayer_id` varchar(100) DEFAULT NULL COMMENT 'çº³ç¨Žäººè¯†åˆ«å·',
  `taxpayer_name` varchar(255) DEFAULT NULL COMMENT 'çº³ç¨Žäººåç§°',
  `old_taxpayer_id` varchar(100) DEFAULT NULL COMMENT 'æ›¾ç”¨çº³ç¨Žäººè¯†åˆ«å·',
  `old_taxpayer_name` varchar(255) DEFAULT NULL COMMENT 'æ›¾ç”¨çº³ç¨Žäººåç§°',
  `taxpayer_type` varchar(50) DEFAULT NULL COMMENT 'çº³ç¨Žäººç±»åž‹',
  `social_credit_code` varchar(100) DEFAULT NULL COMMENT 'ç¤¾ä¼šç»Ÿä¸€ä¿¡ç”¨ä»£ç ',
  `address` varchar(500) DEFAULT NULL COMMENT 'å…¬å¸åœ°å€',
  `currency` varchar(20) DEFAULT NULL COMMENT 'å¸ç§',
  `exchange_rate_type` varchar(50) DEFAULT NULL COMMENT 'æ±‡çŽ‡ç±»åž‹',
  `period_scheme` varchar(100) DEFAULT NULL COMMENT 'æœŸé—´æ–¹æ¡ˆ',
  `internal_acct_entity` varchar(100) DEFAULT NULL COMMENT 'å¯¹å†…æ ¸ç®—',
  `external_acct_entity` varchar(100) DEFAULT NULL COMMENT 'å¯¹å¤–æ ¸ç®—',
  `upper_internal_acct` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§å¯¹å†…ä¼šè®¡ä¸»ä½“',
  `upper_acct_entity` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§ä¼šè®¡ä¸»ä½“',
  `related_acct_entity_1` varchar(100) DEFAULT NULL COMMENT 'å…³è”ä¼šè®¡ä¸»ä½“1',
  `related_acct_entity_2` varchar(100) DEFAULT NULL COMMENT 'å…³è”ä¼šè®¡ä¸»ä½“2',
  `related_acct_entity_3` varchar(100) DEFAULT NULL COMMENT 'å…³è”ä¼šè®¡ä¸»ä½“3',
  `sales_org_upper` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§é”€å”®ç»„ç»‡',
  `fund_org_upper` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§èµ„é‡‘ç»„ç»‡',
  `tax_entity_upper` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§çº³ç¨Žä¸»ä½“',
  `contract_entity` varchar(100) DEFAULT NULL COMMENT 'åˆåŒç­¾è®¢ä¸»ä½“',
  `production_area` varchar(100) DEFAULT NULL COMMENT 'å½’å±žäº§åŒº',
  `factory_location` varchar(100) DEFAULT NULL COMMENT 'åŽ‚å®¶åœ°ç‚¹',
  `logistics_type` varchar(50) DEFAULT NULL COMMENT 'ç‰©æµç»„ç»‡ç±»åž‹',
  `country` varchar(50) DEFAULT NULL COMMENT 'å›½å®¶/åœ°åŒº',
  `province` varchar(50) DEFAULT NULL COMMENT 'çœ/è‡ªæ²»å·ž',
  `city_1` varchar(50) DEFAULT NULL COMMENT 'åŸŽå¸‚1',
  `city_2` varchar(50) DEFAULT NULL COMMENT 'åŸŽå¸‚2',
  `district` varchar(50) DEFAULT NULL COMMENT 'åŒº/åŽ¿',
  `admin_org_upper_name` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§è¡Œæ”¿ç»„ç»‡åç§°',
  `admin_org_upper_code` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§è¡Œæ”¿ç»„ç»‡',
  `hr_biz_org_upper` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§äººåŠ›ä¸šåŠ¡ç»„ç»‡',
  `equity_upper` varchar(100) DEFAULT NULL COMMENT 'äº§æƒéš¶å±žä¸Šçº§',
  `finance_shared_upper` varchar(100) DEFAULT NULL COMMENT 'ä¸Šçº§è´¢åŠ¡å…±äº«',
  `approval_unit` varchar(100) DEFAULT NULL COMMENT 'æ‰¹æ–‡å•ä½',
  `approval_code` varchar(100) DEFAULT NULL COMMENT 'æ‰¹æ–‡ç¼–ç ',
  `org_level` varchar(50) DEFAULT NULL COMMENT 'ç»„ç»‡å±‚çº§',
  `unit_level` varchar(50) DEFAULT NULL COMMENT 'å•ä½çº§åˆ«',
  `headcount` int DEFAULT NULL COMMENT 'ç¼–åˆ¶',
  `industry` varchar(100) DEFAULT NULL COMMENT 'æ‰€å±žè¡Œä¸š',
  `economic_type` varchar(100) DEFAULT NULL COMMENT 'ç»æµŽç±»åž‹',
  `scale` varchar(100) DEFAULT NULL COMMENT 'ä¼ä¸šè§„æ¨¡',
  `biz_sector` varchar(100) DEFAULT NULL COMMENT 'ä¸šåŠ¡æ¿å—',
  `listing_type` varchar(50) DEFAULT NULL COMMENT 'ä¸Šå¸‚ç±»åž‹',
  `description` text COMMENT 'æè¿°',
  `language` varchar(20) DEFAULT NULL COMMENT 'è¯­è¨€',
  `sort_code` int DEFAULT NULL COMMENT 'æŽ’åºç ',
  `setup_date` date DEFAULT NULL COMMENT 'è®¾ç«‹æ—¥æœŸ',
  `timestamp_1` datetime DEFAULT NULL COMMENT 'æ—¶é—´æˆ³1',
  `timestamp_2` datetime DEFAULT NULL COMMENT 'æ—¶é—´æˆ³2',
  `logic_delete_1` int DEFAULT NULL COMMENT 'é€»è¾‘åˆ é™¤æ ‡å¿—ä½1',
  `logic_delete_2` int DEFAULT NULL COMMENT 'é€»è¾‘åˆ é™¤æ ‡å¿—ä½2',
  `status_1` varchar(50) DEFAULT NULL COMMENT 'çŠ¶æ€1',
  `status_2` varchar(50) DEFAULT NULL COMMENT 'çŠ¶æ€2',
  `status_3` varchar(50) DEFAULT NULL COMMENT 'çŠ¶æ€3',
  `fax` varchar(50) DEFAULT NULL COMMENT 'ä¼ çœŸ',
  `created_by` varchar(100) DEFAULT NULL,
  `modified_by` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `master_id` (`master_id`),
  CONSTRAINT `sys_org_ext_osn_ibfk_1` FOREIGN KEY (`master_id`) REFERENCES `sys_org` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='æ¬§ç¥žè¯ºæ•°æ®æ‰©å±•è¡¨';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_org_ext_osn`
--

LOCK TABLES `sys_org_ext_osn` WRITE;
/*!40000 ALTER TABLE `sys_org_ext_osn` DISABLE KEYS */;
INSERT INTO `sys_org_ext_osn` VALUES (1,1,'其他组织',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Y','N',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(2,2,'其他组织',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Y','N',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(3,3,'公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'N','Y',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'三水基地','广东',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(4,4,'公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'N','Y',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,5,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(5,5,'公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'N','Y',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,4,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,6,'公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'N','Y',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'广西基地','广西',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,3,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(7,7,'公司',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'N','Y',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'景德镇基地','江西省景德镇',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,NULL,NULL,2,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `sys_org_ext_osn` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_post`
--

DROP TABLE IF EXISTS `sys_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_post` (
  `post_id` bigint NOT NULL AUTO_INCREMENT COMMENT '岗位ID',
  `post_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '岗位编码',
  `post_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '岗位名称',
  `post_sort` int NOT NULL COMMENT '显示顺序',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`post_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='岗位信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_post`
--

LOCK TABLES `sys_post` WRITE;
/*!40000 ALTER TABLE `sys_post` DISABLE KEYS */;
INSERT INTO `sys_post` VALUES (1,'ceo','董事长',1,'0','admin','2025-01-06 16:33:57','',NULL,''),(2,'se','项目经理',2,'0','admin','2025-01-06 16:33:57','',NULL,''),(3,'hr','人力资源',3,'0','admin','2025-01-06 16:33:57','',NULL,''),(4,'user','普通员工',4,'0','admin','2025-01-06 16:33:57','',NULL,'');
/*!40000 ALTER TABLE `sys_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role`
--

DROP TABLE IF EXISTS `sys_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role` (
  `role_id` bigint NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色名称',
  `role_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色权限字符串',
  `role_sort` int NOT NULL COMMENT '显示顺序',
  `data_scope` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '1' COMMENT '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）',
  `menu_check_strictly` tinyint(1) DEFAULT '1' COMMENT '菜单树选择项是否关联显示',
  `dept_check_strictly` tinyint(1) DEFAULT '1' COMMENT '部门树选择项是否关联显示',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='角色信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role`
--

LOCK TABLES `sys_role` WRITE;
/*!40000 ALTER TABLE `sys_role` DISABLE KEYS */;
INSERT INTO `sys_role` VALUES (1,'超级管理员','admin',1,'1',1,1,'0','0','admin','2025-01-06 16:33:58','',NULL,'超级管理员'),(2,'普通角色','common',2,'2',1,1,'0','2','admin','2025-01-06 16:33:58','admin','2025-01-10 09:28:43','普通角色');
/*!40000 ALTER TABLE `sys_role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role_dept`
--

DROP TABLE IF EXISTS `sys_role_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_dept` (
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `dept_id` bigint NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`,`dept_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='角色和部门关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_dept`
--

LOCK TABLES `sys_role_dept` WRITE;
/*!40000 ALTER TABLE `sys_role_dept` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_dept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_role_menu`
--

DROP TABLE IF EXISTS `sys_role_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_role_menu` (
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `menu_id` bigint NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`,`menu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='角色和菜单关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_role_menu`
--

LOCK TABLES `sys_role_menu` WRITE;
/*!40000 ALTER TABLE `sys_role_menu` DISABLE KEYS */;
/*!40000 ALTER TABLE `sys_role_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `user_id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `dept_id` bigint DEFAULT NULL COMMENT '部门ID',
  `user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户账号',
  `nick_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '用户昵称',
  `user_type` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '00' COMMENT '用户类型（00系统用户）',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '用户邮箱',
  `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '手机号码',
  `sex` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '用户性别（0男 1女 2未知）',
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '头像地址',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '密码',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '帐号状态（0正常 1停用）',
  `del_flag` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '0' COMMENT '删除标志（0代表存在 2代表删除）',
  `login_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '最后登录IP',
  `login_date` datetime DEFAULT NULL COMMENT '最后登录时间',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '创建者',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT '' COMMENT '更新者',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='用户信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,103,'admin','管理员','00','','15888888888','1','','$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2','0','0','127.0.0.1','2026-02-04 13:34:48','admin','2025-01-06 16:33:56','','2026-02-04 05:34:48','管理员'),(2,105,'ry','若依','00','ry@qq.com','15666666666','1','','$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2','0','2','127.0.0.1','2025-01-06 16:33:56','admin','2025-01-06 16:33:56','',NULL,'测试员'),(100,103,'zhangsan','张三','00','','','0','','$2a$10$FWNPIfMn3PnjyYGcGarDyuM3qImhIFJ.W7o/AJrGrRHkOJfRl0Lu.','0','2','',NULL,'admin','2025-01-10 14:14:38','',NULL,NULL);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_post`
--

DROP TABLE IF EXISTS `sys_user_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_post` (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `post_id` bigint NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`,`post_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='用户与岗位关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_post`
--

LOCK TABLES `sys_user_post` WRITE;
/*!40000 ALTER TABLE `sys_user_post` DISABLE KEYS */;
INSERT INTO `sys_user_post` VALUES (1,1);
/*!40000 ALTER TABLE `sys_user_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user_role`
--

DROP TABLE IF EXISTS `sys_user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user_role` (
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`,`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC COMMENT='用户和角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user_role`
--

LOCK TABLES `sys_user_role` WRITE;
/*!40000 ALTER TABLE `sys_user_role` DISABLE KEYS */;
INSERT INTO `sys_user_role` VALUES (1,1);
/*!40000 ALTER TABLE `sys_user_role` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-05  2:20:00
