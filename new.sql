/*
 * 集团组织与银行账户合并数据库脚本
 * 版本: V3.1 (顺序优化版)
 * 说明: 已调整表创建顺序，确保外键引用正确。
 */

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0; -- 暂时关闭外键检查，防止由于顺序或循环引用导致的创建失败

-- =================================================================
-- 1. 核心主表：sys_org
-- 作用：构建统一的组织树，必须最先创建，因为扩展表依赖它
-- =================================================================
DROP TABLE IF EXISTS `sys_org`;
CREATE TABLE `sys_org` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '统一主键ID',
    `org_code` VARCHAR(100) NOT NULL COMMENT '组织编码 (业务主键)',
    `org_name` VARCHAR(255) NOT NULL COMMENT '组织名称',
    `short_name` VARCHAR(100) COMMENT '组织简称',
    `parent_code` VARCHAR(100) COMMENT '上级组织编码',
    `org_type` VARCHAR(50) COMMENT '类型映射: COMPANY/DEPT/PLANT',
    `is_active` TINYINT(1) DEFAULT 1 COMMENT '是否有效 (1=是, 0=否)',
    `source_system` VARCHAR(20) NOT NULL COMMENT '来源系统: OSN / DW',
    `original_id` VARCHAR(100) COMMENT '原系统的主键ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY `uk_source_code` (`source_system`, `org_code`),
    INDEX `idx_parent` (`parent_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='集团统一组织主表';

-- =================================================================
-- 2. 欧神诺组织扩展表：sys_org_ext_osn
-- =================================================================
DROP TABLE IF EXISTS `sys_org_ext_osn`;
CREATE TABLE `sys_org_ext_osn` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `master_id` BIGINT NOT NULL COMMENT '关联主表ID',
    `org_form` VARCHAR(50) COMMENT '组织形态',
    `admin_org` VARCHAR(100) COMMENT '所属行政组织',
    `is_dept` CHAR(1) COMMENT '是否部门',
    `dept_nature` VARCHAR(100) COMMENT '部门性质',
    `principal_name` VARCHAR(100) COMMENT '负责人',
    `vp_leader` VARCHAR(100) COMMENT '分管领导',
    `contact_person` VARCHAR(100) COMMENT '联系人',
    `phone` VARCHAR(50) COMMENT '公司电话',
    `taxpayer_id` VARCHAR(100) COMMENT '纳税人识别号',
    `taxpayer_name` VARCHAR(255) COMMENT '纳税人名称',
    `social_credit_code` VARCHAR(100) COMMENT '社会统一信用代码',
    `address` VARCHAR(500) COMMENT '公司地址',
    `currency` VARCHAR(20) COMMENT '币种',
    `internal_acct_entity` VARCHAR(100) COMMENT '对内核算',
    `external_acct_entity` VARCHAR(100) COMMENT '对外核算',
    `production_area` VARCHAR(100) COMMENT '归属产区',
    `description` TEXT COMMENT '描述',
    `setup_date` DATE COMMENT '设立日期',
    `status_1` VARCHAR(50) COMMENT '状态1',
    `created_by` VARCHAR(100),
    `modified_by` VARCHAR(100),
    CONSTRAINT `fk_osn_org_master` FOREIGN KEY (`master_id`) REFERENCES `sys_org` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='欧神诺组织数据扩展表';

-- =================================================================
-- 3. 帝王组织扩展表：sys_org_ext_dw
-- =================================================================
DROP TABLE IF EXISTS `sys_org_ext_dw`;
CREATE TABLE `sys_org_ext_dw` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `master_id` BIGINT NOT NULL COMMENT '关联主表ID',
    `org_classify` VARCHAR(50) COMMENT '组织分类',
    `is_hr_org` TINYINT(1) COMMENT '是否人力资源组织',
    `is_operating_org` TINYINT(1) COMMENT '是否运营组织',
    `is_inventory_org` TINYINT(1) COMMENT '是否库存组织',
    `sys_version` VARCHAR(50) COMMENT '系统版本号',
    `time_zone_info` VARCHAR(100) COMMENT '时区信息',
    `location` VARCHAR(200) COMMENT '所在地点',
    `effective_start_date` DATETIME COMMENT '生效日期',
    `effective_disable_date` DATETIME COMMENT '失效日期',
    `created_by` VARCHAR(100),
    `modified_by` VARCHAR(100),
    CONSTRAINT `fk_dw_org_master` FOREIGN KEY (`master_id`) REFERENCES `sys_org` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帝王(U9)组织数据扩展表';

-- =================================================================
-- 4. 集团银行账户主表：sys_bank
-- =================================================================
DROP TABLE IF EXISTS `sys_bank`;
CREATE TABLE `sys_bank` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `account_no` VARCHAR(100) NOT NULL COMMENT '银行账号',
  `account_name` VARCHAR(255) DEFAULT NULL COMMENT '账户名称',
  `bank_name` VARCHAR(255) DEFAULT NULL COMMENT '开户行名称',
  `cnaps_code` VARCHAR(50) DEFAULT NULL COMMENT '联行号',
  `currency_code` VARCHAR(20) DEFAULT 'CNY' COMMENT '币种',
  `current_balance` DECIMAL(20,2) DEFAULT 0.00,
  `source_system` VARCHAR(20) NOT NULL COMMENT '来源系统: OSN / DW',
  `status` VARCHAR(20) DEFAULT 'NORMAL',
  `is_active` TINYINT(1) DEFAULT 1,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `uk_source_acc` (`source_system`, `account_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='集团银行账户主表';

-- =================================================================
-- 5. 欧神诺银行扩展表：sys_bank_ext_osn
-- =================================================================
DROP TABLE IF EXISTS `sys_bank_ext_osn`;
CREATE TABLE `sys_bank_ext_osn` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `master_id` BIGINT(20) NOT NULL COMMENT '关联主表ID',
  `open_type` VARCHAR(50) DEFAULT NULL,
  `settlement_center` VARCHAR(100) DEFAULT NULL,
  `account_nature` VARCHAR(100) DEFAULT NULL,
  `remark` TEXT,
  CONSTRAINT `fk_osn_bank_master` FOREIGN KEY (`master_id`) REFERENCES `sys_bank` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='欧神诺银行账户扩展表';

-- =================================================================
-- 6. 帝王银行扩展表：sys_bank_ext_dw
-- =================================================================
DROP TABLE IF EXISTS `sys_bank_ext_dw`;
CREATE TABLE `sys_bank_ext_dw` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `master_id` BIGINT(20) NOT NULL COMMENT '关联主表ID',
  `is_base_account` TINYINT(1) DEFAULT NULL,
  `is_default` TINYINT(1) DEFAULT NULL,
  `desc_flex_field_pub_seg_1` VARCHAR(150) DEFAULT NULL,
  `desc_flex_field_pub_seg_2` VARCHAR(150) DEFAULT NULL,
  -- ... (此处根据需要继续添加弹性域字段)
  CONSTRAINT `fk_dw_bank_master` FOREIGN KEY (`master_id`) REFERENCES `sys_bank` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帝王银行账户扩展表';

SET FOREIGN_KEY_CHECKS = 1; -- 恢复外键检查
