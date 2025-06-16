-- 觅乡记乡村旅游平台数据库表结构
SET FOREIGN_KEY_CHECKS = 0;

-- 创建数据库
CREATE DATABASE IF NOT EXISTS mixiangji CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mixiangji;

-- 自定义用户表 (替代Django内置用户表)
CREATE TABLE users_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME(6),
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    phone VARCHAR(20) NOT NULL DEFAULT '',
    avatar VARCHAR(200) NOT NULL DEFAULT '',
    bio LONGTEXT NOT NULL,
    user_type VARCHAR(10) NOT NULL DEFAULT 'tourist',
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- 用户资料表
CREATE TABLE users_userprofile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    real_name VARCHAR(50) NOT NULL DEFAULT '',
    id_card VARCHAR(50) NOT NULL DEFAULT '',
    gender VARCHAR(10) NOT NULL DEFAULT 'other',
    birthday DATE,
    address VARCHAR(255) NOT NULL DEFAULT '',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
);

-- 商户资料表
CREATE TABLE users_merchantprofile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    business_name VARCHAR(100) NOT NULL,
    business_license VARCHAR(200) NOT NULL,
    contact_person VARCHAR(50) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    description LONGTEXT NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
);

-- 收藏表
CREATE TABLE users_favorite (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target_type VARCHAR(20) NOT NULL,
    target_id INT NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, target_type, target_id)
);

-- 区域表
CREATE TABLE regions_region (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    level VARCHAR(10) NOT NULL,
    is_hot BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    parent_id INT,
    FOREIGN KEY (parent_id) REFERENCES regions_region(id) ON DELETE CASCADE,
    INDEX idx_code (code)
);

-- 乡村表
CREATE TABLE villages_village (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    intro LONGTEXT NOT NULL,
    description LONGTEXT NOT NULL,
    cover_image VARCHAR(200) NOT NULL,
    location VARCHAR(100) NOT NULL,
    features LONGTEXT NOT NULL,
    views INT NOT NULL DEFAULT 0,
    rating DECIMAL(2,1) NOT NULL DEFAULT 0.0,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    is_recommended BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    region_id INT NOT NULL,
    FOREIGN KEY (region_id) REFERENCES regions_region(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_region_id (region_id),
    INDEX idx_is_recommended (is_recommended)
);

-- 乡村图库表
CREATE TABLE villages_villagegallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT NOT NULL DEFAULT 0,
    village_id INT NOT NULL,
    FOREIGN KEY (village_id) REFERENCES villages_village(id) ON DELETE CASCADE
);

-- 景点表
CREATE TABLE villages_attraction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    intro LONGTEXT NOT NULL,
    description LONGTEXT NOT NULL,
    cover_image VARCHAR(200) NOT NULL,
    location VARCHAR(100) NOT NULL,
    opening_hours VARCHAR(255) NOT NULL,
    ticket_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    village_id INT NOT NULL,
    FOREIGN KEY (village_id) REFERENCES villages_village(id) ON DELETE CASCADE
);

-- 景点图库表
CREATE TABLE villages_attractiongallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT NOT NULL DEFAULT 0,
    attraction_id INT NOT NULL,
    FOREIGN KEY (attraction_id) REFERENCES villages_attraction(id) ON DELETE CASCADE
);

-- 产品类别表
CREATE TABLE products_productcategory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type VARCHAR(10) NOT NULL,
    icon VARCHAR(200) NOT NULL DEFAULT '',
    `order` INT NOT NULL DEFAULT 0,
    sort_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
);

-- 特产表
CREATE TABLE products_product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cover_image VARCHAR(200) NOT NULL,
    intro LONGTEXT NOT NULL,
    description LONGTEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    discount_price DECIMAL(10,2),
    stock INT NOT NULL DEFAULT 0,
    sales INT NOT NULL DEFAULT 0,
    rating DECIMAL(2,1) NOT NULL DEFAULT 0.0,
    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    specs LONGTEXT NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    views INT NOT NULL DEFAULT 0,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    category_id INT,
    merchant_id INT NOT NULL,
    village_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES products_productcategory(id) ON DELETE SET NULL,
    FOREIGN KEY (merchant_id) REFERENCES users_user(id) ON DELETE CASCADE,
    FOREIGN KEY (village_id) REFERENCES villages_village(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_village_id (village_id),
    INDEX idx_is_featured (is_featured)
);

-- 特产图库表
CREATE TABLE products_productgallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT NOT NULL DEFAULT 0,
    product_id INT NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products_product(id) ON DELETE CASCADE
);

-- 美食表 (修正：添加ingredients字段，移除is_available字段)
CREATE TABLE products_food (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cover_image VARCHAR(200) NOT NULL,
    intro LONGTEXT NOT NULL,
    description LONGTEXT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    discount_price DECIMAL(10,2),
    rating DECIMAL(2,1) NOT NULL DEFAULT 0.0,
    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    ingredients LONGTEXT NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    views INT NOT NULL DEFAULT 0,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    category_id INT,
    merchant_id INT NOT NULL,
    village_id INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES products_productcategory(id) ON DELETE SET NULL,
    FOREIGN KEY (merchant_id) REFERENCES users_user(id) ON DELETE CASCADE,
    FOREIGN KEY (village_id) REFERENCES villages_village(id) ON DELETE CASCADE
);

-- 美食图库表
CREATE TABLE products_foodgallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT NOT NULL DEFAULT 0,
    food_id INT NOT NULL,
    FOREIGN KEY (food_id) REFERENCES products_food(id) ON DELETE CASCADE
);

-- 民宿表
CREATE TABLE homestays_homestay (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    property_type VARCHAR(20) NOT NULL,
    address VARCHAR(255) NOT NULL,
    location VARCHAR(100) NOT NULL,
    intro LONGTEXT NOT NULL,
    description LONGTEXT NOT NULL,
    cover_image VARCHAR(200) NOT NULL,
    views INT NOT NULL DEFAULT 0,
    rating DECIMAL(2,1) NOT NULL DEFAULT 0.0,
    orders_count INT NOT NULL DEFAULT 0,
    lowest_price DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    features LONGTEXT NOT NULL,
    check_in_time VARCHAR(50) NOT NULL DEFAULT '14:00',
    check_out_time VARCHAR(50) NOT NULL DEFAULT '12:00',
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    merchant_id INT NOT NULL,
    village_id INT NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES users_user(id) ON DELETE CASCADE,
    FOREIGN KEY (village_id) REFERENCES villages_village(id) ON DELETE CASCADE,
    INDEX idx_name (name),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_village_id (village_id),
    INDEX idx_is_featured (is_featured)
);

-- 民宿图库表
CREATE TABLE homestays_homestaygallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT NOT NULL DEFAULT 0,
    homestay_id INT NOT NULL,
    FOREIGN KEY (homestay_id) REFERENCES homestays_homestay(id) ON DELETE CASCADE
);

-- 房型表 (修正：字段名调整，添加缺失字段)
CREATE TABLE homestays_roomtype (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cover_image VARCHAR(200) NOT NULL,
    area INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    discount_price DECIMAL(10,2),
    bed_type VARCHAR(20) NOT NULL,
    max_guests INT NOT NULL,
    room_count INT NOT NULL,
    description LONGTEXT NOT NULL,
    facilities LONGTEXT NOT NULL,
    breakfast BOOLEAN NOT NULL DEFAULT FALSE,
    cancellation VARCHAR(255) NOT NULL DEFAULT '',
    status VARCHAR(10) NOT NULL DEFAULT 'active',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    homestay_id INT NOT NULL,
    FOREIGN KEY (homestay_id) REFERENCES homestays_homestay(id) ON DELETE CASCADE
);

-- 房型图库表
CREATE TABLE homestays_roomgallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    image_url VARCHAR(200) NOT NULL,
    caption VARCHAR(255) NOT NULL DEFAULT '',
    sort_order INT NOT NULL DEFAULT 0,
    room_type_id INT NOT NULL,
    FOREIGN KEY (room_type_id) REFERENCES homestays_roomtype(id) ON DELETE CASCADE
);

-- 房间库存表 (修正：字段名调整)
CREATE TABLE homestays_roominventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    available INT NOT NULL,
    original_price DECIMAL(10,2) NOT NULL,
    current_price DECIMAL(10,2) NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    room_type_id INT NOT NULL,
    FOREIGN KEY (room_type_id) REFERENCES homestays_roomtype(id) ON DELETE CASCADE,
    UNIQUE KEY unique_room_date (room_type_id, date)
);

-- 民宿评价表 (新增：Django模型中存在但SQL中缺失)
CREATE TABLE homestays_homestayreview (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rating INT NOT NULL,
    comment LONGTEXT NOT NULL,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    homestay_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (homestay_id) REFERENCES homestays_homestay(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
);

-- 购物车项表
CREATE TABLE orders_cartitem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_type VARCHAR(10) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    check_in_date DATE,
    check_out_date DATE,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    food_id INT,
    product_id INT,
    room_type_id INT,
    user_id INT NOT NULL,
    FOREIGN KEY (food_id) REFERENCES products_food(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products_product(id) ON DELETE CASCADE,
    FOREIGN KEY (room_type_id) REFERENCES homestays_roomtype(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
);

-- 订单表
CREATE TABLE orders_order (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(50) NOT NULL UNIQUE,
    order_type VARCHAR(10) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    payment_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending_payment',
    contact_name VARCHAR(50) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,
    contact_email VARCHAR(254) NOT NULL DEFAULT '',
    remark LONGTEXT NOT NULL,
    paid_at DATETIME(6),
    canceled_at DATETIME(6),
    refunded_at DATETIME(6),
    completed_at DATETIME(6),
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    merchant_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (merchant_id) REFERENCES users_user(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_status (status)
);

-- 订单项表
CREATE TABLE orders_orderitem (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_type VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    image VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    amount DECIMAL(10,2) NOT NULL,
    check_in_date DATE,
    check_out_date DATE,
    days INT NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    order_id INT NOT NULL,
    product_id INT,
    food_id INT,
    room_type_id INT,
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products_product(id) ON DELETE SET NULL,
    FOREIGN KEY (food_id) REFERENCES products_food(id) ON DELETE SET NULL,
    FOREIGN KEY (room_type_id) REFERENCES homestays_roomtype(id) ON DELETE SET NULL
);

-- 支付记录表
CREATE TABLE orders_payment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_no VARCHAR(100) NOT NULL UNIQUE,
    payment_method VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    transaction_id VARCHAR(100) NOT NULL DEFAULT '',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    order_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE
);

-- 退款记录表 (修正：移除多余字段)
CREATE TABLE orders_refund (
    id INT AUTO_INCREMENT PRIMARY KEY,
    refund_no VARCHAR(100) NOT NULL UNIQUE,
    amount DECIMAL(10,2) NOT NULL,
    reason VARCHAR(20) NOT NULL,
    reason_detail LONGTEXT NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'pending',
    created_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    order_id INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders_order(id) ON DELETE CASCADE
);

-- Django权限相关表
CREATE TABLE auth_group (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE auth_group_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_id INT NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE KEY unique_group_permission (group_id, permission_id)
);

CREATE TABLE auth_user_groups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    group_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    FOREIGN KEY (group_id) REFERENCES auth_group(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_group (user_id, group_id)
);

CREATE TABLE auth_user_user_permissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    permission_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES auth_permission(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_permission (user_id, permission_id)
);

CREATE TABLE auth_permission (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INT NOT NULL,
    codename VARCHAR(100) NOT NULL,
    UNIQUE KEY unique_content_type_codename (content_type_id, codename)
);

CREATE TABLE django_content_type (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    UNIQUE KEY unique_app_model (app_label, model)
);

CREATE TABLE django_session (
    session_key VARCHAR(40) NOT NULL PRIMARY KEY,
    session_data LONGTEXT NOT NULL,
    expire_date DATETIME(6) NOT NULL,
    INDEX idx_expire_date (expire_date)
);

CREATE TABLE django_migrations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME(6) NOT NULL
);

-- 管理日志表
CREATE TABLE django_admin_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action_time DATETIME(6) NOT NULL,
    object_id LONGTEXT,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT UNSIGNED NOT NULL,
    change_message LONGTEXT NOT NULL,
    content_type_id INT,
    user_id INT NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS = 1;




# ------------------------------------------------------------------------------------------------
-- 1. 先插入地区数据（解决外键依赖）
INSERT INTO regions_region (name, code, level, is_hot, status, parent_id) VALUES
                                                                              ('浙江省', '330000', 'province', TRUE, 'active', NULL),
                                                                              ('杭州市', '330100', 'city', TRUE, 'active', 1),
                                                                              ('淳安县', '330127', 'county', TRUE, 'active', 2);
-- 1. 插入地区数据（解决外键依赖）
INSERT INTO regions_region (name, code, level, is_hot, status, parent_id) VALUES
                                                                              ('北京市', '110000', 'province', TRUE, 'active', NULL),
                                                                              ('东城区', '110101', 'city', TRUE, 'active', 1),
                                                                              ('西城区', '110102', 'city', TRUE, 'active', 1),
                                                                              ('海淀区', '110108', 'city', TRUE, 'active', 1),

                                                                              ('广东省', '440000', 'province', TRUE, 'active', NULL),
                                                                              ('广州市', '440100', 'city', TRUE, 'active', 5),
                                                                              ('天河区', '440106', 'city', TRUE, 'active', 6),
                                                                              ('番禺区', '440113', 'city', TRUE, 'active', 6),
                                                                              ('珠海市', '440400', 'city', TRUE, 'active', 5),
                                                                              ('斗门区', '440402', 'city', TRUE, 'active', 9),

                                                                              ('江苏省', '320000', 'province', TRUE, 'active', NULL),
                                                                              ('南京市', '320100', 'city', TRUE, 'active', 11),
                                                                              ('玄武区', '320102', 'city', TRUE, 'active', 12),
                                                                              ('鼓楼区', '320103', 'city', TRUE, 'active', 12),
                                                                              ('无锡市', '320200', 'city', TRUE, 'active', 11),
                                                                              ('锡山区', '320205', 'city', TRUE, 'active', 15),

                                                                              ('山东省', '370000', 'province', TRUE, 'active', NULL),
                                                                              ('济南市', '370100', 'city', TRUE, 'active', 17),
                                                                              ('历下区', '370102', 'city', TRUE, 'active', 18),
                                                                              ('市中区', '370103', 'city', TRUE, 'active', 18),
                                                                              ('青岛市', '370200', 'city', TRUE, 'active', 17),
                                                                              ('市北区', '370202', 'city', TRUE, 'active', 22),

                                                                              ('福建省', '350000', 'province', TRUE, 'active', NULL),
                                                                              ('福州市', '350100', 'city', TRUE, 'active', 24),
                                                                              ('鼓楼区', '350102', 'city', TRUE, 'active', 25),
                                                                              ('台江区', '350103', 'city', TRUE, 'active', 25),
                                                                              ('厦门市', '350200', 'city', TRUE, 'active', 24),
                                                                              ('思明区', '350203', 'city', TRUE, 'active', 29),

                                                                              ('河南省', '410000', 'province', TRUE, 'active', NULL),
                                                                              ('郑州市', '410100', 'city', TRUE, 'active', 31),
                                                                              ('金水区', '410105', 'city', TRUE, 'active', 32),
                                                                              ('二七区', '410106', 'city', TRUE, 'active', 32),
                                                                              ('洛阳市', '410300', 'city', TRUE, 'active', 31),
                                                                              ('西工区', '410302', 'city', TRUE, 'active', 36),

                                                                              ('陕西省', '610000', 'province', TRUE, 'active', NULL),
                                                                              ('西安市', '610100', 'city', TRUE, 'active', 38),
                                                                              ('碑林区', '610103', 'city', TRUE, 'active', 39),
                                                                              ('莲湖区', '610104', 'city', TRUE, 'active', 39),
                                                                              ('宝鸡市', '610300', 'city', TRUE, 'active', 38),
                                                                              ('渭滨区', '610302', 'city', TRUE, 'active', 43),


                                                                              ('温州市', '330300', 'city', TRUE, 'active', 1),
                                                                              ('鹿城区', '330302', 'city', TRUE, 'active', 2),
                                                                              ('龙湾区', '330303', 'city', TRUE, 'active', 2),
                                                                              ('宁波市', '330200', 'city', TRUE, 'active', 1),
                                                                              ('海曙区', '330203', 'city', TRUE, 'active', 5);
-- 2. 获取刚插入的淳安县ID
SET @region_id = (SELECT id FROM regions_region WHERE code = '330127');

-- 3. 插入村庄数据（使用正确的地区ID）
INSERT INTO villages_village (
    name, intro, description, cover_image,
    location, features, region_id, views, rating
) VALUES (
             '下姜村', '美丽乡村', '梦开始的地方，美丽乡村典范',
             'https://imgs.699pic.com/images/501/594/198.jpg!list1x.v2', '30.6198,119.069',
             '["红色旅游","生态农业","民宿集群"]', @region_id, 1000, 4.8
         );

-- 4. 获取村庄ID
SET @village_id = LAST_INSERT_ID();


-- 插入用户数据 (商户和普通用户)
INSERT INTO users_user (password, username, email, is_verified, phone, bio, user_type, is_staff, is_superuser)
VALUES
-- 商户用户 (id=2)
('pbkdf2_sha256$260000$...', 'merchant_user', 'merchant@example.com', TRUE, '13800138000', '民宿经营者', 'merchant', TRUE, FALSE),
-- 普通用户 (id=1)
('pbkdf2_sha256$260000$...', 'customer_user', 'customer@example.com', TRUE, '13900139000', '普通游客', 'tourist', FALSE, FALSE);

-- 插入商户资料
INSERT INTO users_merchantprofile (
    business_name, business_license, contact_person, contact_phone,
    address, description, status, user_id
) VALUES
    ('千岛湖民宿集团', 'LIC123456', '张经理', '13800138000',
     '淳安县千岛湖镇', '专业经营精品民宿', 'approved', 2);


-- 插入村庄数据
INSERT INTO villages_village (
    name, intro, description, cover_image,
    location, features, region_id, views, rating, status
) VALUES (
             '漂亮村', '美丽乡村', '梦开始的地方，美丽乡村典范',
             'https://bpic.588ku.com/back_list_pic/21/08/09/f00693ebc3256f2928e50cc179b3c68b.jpg!/fw/350/quality/95/unsharp/true/compress/true', '30.6198,119.069',
             '["红色旅游","生态农业","民宿集群"]', @region_id, 1000, 4.8, 'approved'
         );

-- 获取村庄ID
SET @village_id = LAST_INSERT_ID();

-- 插入民宿数据
INSERT INTO homestays_homestay (
    name, property_type, address, location,
    intro, description, cover_image, features,
    lowest_price, merchant_id, village_id, views, rating, status
) VALUES
      ('栖居民宿', 'villa', '下姜村幸福路8号', '30.568,119.125',
       '山景精品民宿', '坐拥180度山景的现代设计民宿', 'https://www.bjhr.gov.cn/zjhr/hrly/xlgl/202504/W020250422596808311366.png', '["山景","露台","免费WiFi"]',
       480.00, 2, @village_id, 500, 4.7, 'approved'),
      ('狮城客栈', 'courtyard', '文渊狮城景区内', '30.590,119.158',
       '古城风格客栈', '还原明清建筑风格的传统庭院', 'https://dimg04.c-ctrip.com/images/0204r120008f3fndb96FA_C_750_340_Q70.jpg', '["古城景观","庭院","传统早餐"]',
       680.00, 2, @village_id, 600, 4.9, 'approved');

-- 获取民宿ID
SET @homestay1_id = (SELECT id FROM homestays_homestay WHERE name = '栖居民宿');
SET @homestay2_id = (SELECT id FROM homestays_homestay WHERE name = '狮城客栈');

-- 插入房型数据
INSERT INTO homestays_roomtype (
    name, cover_image, area, price,
    bed_type, max_guests, room_count,
    description, facilities, homestay_id
) VALUES
      ('山景大床房', 'https://www.top-cloud.com.tw/upload/room_m/59819__24A26SG6ty.jpg', 35, 580.00,
       'queen', 2, 5,
       '带观景阳台的山景房', '["空调","WiFi","浴缸"]', @homestay1_id),
      ('湖景庭院套房', 'https://www.hilton.com.cn/file/images/20210915/20210915133042682qKEjXFU_thum_mid.jpg', 60, 880.00,
       'king', 4, 3,
       '带独立庭院的湖景套房', '["地暖","茶室","私人泳池"]', @homestay2_id);

-- 获取房型ID
SET @room1_id = (SELECT id FROM homestays_roomtype WHERE name = '山景大床房');
SET @room2_id = (SELECT id FROM homestays_roomtype WHERE name = '湖景庭院套房');

-- 插入房型库存
INSERT INTO homestays_roominventory (
    date, available, original_price,
    current_price, room_type_id
) VALUES
      ('2025-06-20', 5, 580.00, 580.00, @room1_id),
      ('2025-06-20', 3, 880.00, 880.00, @room2_id),
      ('2025-06-21', 5, 580.00, 580.00, @room1_id),
      ('2025-06-21', 3, 880.00, 880.00, @room2_id);

-- 插入订单数据 (使用新订单号)
INSERT INTO orders_order (
    order_no, order_type, total_amount,
    payment_amount, contact_name, contact_phone,
    remark, merchant_id, user_id, status, contact_email
) VALUES
      ('M20250615003', 'homestay', 1580.00, 1580.00,
       '张先生', '13800138000', '山景房预订', 2, 1, 'completed', 'zhang@example.com'),
      ('M20250615004', 'homestay', 1760.00, 1760.00,
       '李女士', '13900139000', '湖景套房', 2, 1, 'completed', 'li@example.com');

-- 获取订单ID
SET @order1_id = (SELECT id FROM orders_order WHERE order_no = 'M20250615003');
SET @order2_id = (SELECT id FROM orders_order WHERE order_no = 'M20250615004');

-- 插入订单项
INSERT INTO orders_orderitem (
    order_id, item_type, name, image, price, quantity, amount,
    check_in_date, check_out_date, days, room_type_id
) VALUES
      (@order1_id, 'room', '山景大床房', 'https://www.top-cloud.com.tw/upload/room_m/DSC_6595__25D205lYgC.jpg', 580.00, 1, 1160.00,
       '2025-06-20', '2025-06-22', 2, @room1_id),
      (@order1_id, 'room', '山景大床房', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2v5YoEhrDybsH2tB6gJLGgRsr6Bjbu0OEIw&s', 580.00, 1, 1160.00,
       '2025-06-20', '2025-06-22', 2, @room1_id),
      (@order2_id, 'room', '湖景庭院套房', 'https://www.hilton.com.cn/file/images/20210915/202109151331098715XudcQI_thum_mid.jpg', 880.00, 1, 1760.00,
       '2025-06-20', '2025-06-21', 1, @room2_id);

-- 插入民宿评价
INSERT INTO homestays_homestayreview (
    rating, comment, homestay_id, user_id
) VALUES
      (5, '景观绝佳，服务周到', @homestay1_id, 1),
      (4, '传统风格很有特色，早餐好吃', @homestay2_id, 1);

-- 插入特产类别
INSERT INTO products_productcategory (name, type, icon) VALUES
                                                            ('茶叶', 'product', 'https://imgs.699pic.com/images/501/658/328.jpg!list1x.v2'),
                                                            ('手工艺品', 'product', 'https://img.freepik.com/free-photo/flat-lay-hand-stabbing-voodoo-doll_23-2149514254.jpg?semt=ais_hybrid&w=740');

-- 插入特产数据
INSERT INTO products_product (
    name, cover_image, intro, description, price,
    category_id, merchant_id, village_id, specs
) VALUES
      ('千岛湖龙井', 'https://z.hangzhou.com.cn/2018/dejzggjcyblh/images/2018-05/17/12dc12d6-439d-47f5-bd29-7c207bb48bd5.jpg', '特级龙井茶', '产自千岛湖周边茶园的精品龙井', 288.00,
       (SELECT id FROM products_productcategory WHERE name = '茶叶'), 2, @village_id, '["250g/盒"]'),
      ('竹编工艺品', 'https://bpic.588ku.com/back_list_pic/25/03/28/99bcd69680da08926fe0543d0b6e0858.jpg!/fw/350/quality/95/unsharp/true/compress/true', '手工竹编', '传统手工制作的竹编器具', 128.00,
       (SELECT id FROM products_productcategory WHERE name = '手工艺品'), 2, @village_id, '["大号","小号"]');

-- 插入美食数据
INSERT INTO products_food (
    name, cover_image, intro, description, price,
    ingredients, merchant_id, village_id
) VALUES
      ('千岛湖鱼头', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBH6-BaiQ64GtPaFQ_yE7_3N3Eed37fu-gYA&s', '特色鱼头汤', '选用千岛湖有机鱼头炖制', 158.00,
       '["有机鱼头","豆腐","香菇"]', 2, @village_id),
      ('竹筒饭', 'https://img95.699pic.com/xsj/1u/fu/kv.jpg!/fh/300', '传统竹筒饭', '用新鲜竹筒蒸制的特色米饭', 48.00,
       '["糯米","腊肉","青豆"]', 2, @village_id);

-- 插入更多美食数据
INSERT INTO products_food (
    name, cover_image, intro, description, price, discount_price,
    rating, is_featured, ingredients, status, views,
    category_id, merchant_id, village_id
) VALUES
      ('千岛湖有机鱼头', 'https://img.88tph.com/production/20180718/12677461-0.jpg!/watermark/url/L3BhdGgvbG9nby5wbmc/align/center/fw/640/quality/70', '千岛湖野生有机鱼',
       '选用千岛湖野生有机鳙鱼头，配以农家豆腐、笋干慢炖3小时，汤色乳白，肉质鲜嫩',
       158.00, 138.00, 4.8, TRUE, '["鳙鱼头","豆腐","笋干","生姜"]',
       'approved', 1200, NULL, 2, @village_id),

      ('竹筒腊肉饭', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2Hrv2SDq1dPfu9UvKF-2UIwV_zs9tPLqIrw&s', '传统竹筒蒸制',
       '精选农家腊肉、糯米、青豆，用新鲜毛竹筒蒸制，竹香渗透米粒',
       48.00, NULL, 4.5, FALSE, '["糯米","腊肉","青豆","香菇"]',
       'approved', 850, NULL, 2, @village_id),

      ('野菜煎饼', 'https://imgs.699pic.com/images/502/481/478.jpg!detail.v1', '山野时令野菜',
       '每日采集新鲜马齿苋、荠菜等山野菜，搭配土鸡蛋和农家面粉制作',
       28.00, 25.00, 4.3, FALSE, '["马齿苋","荠菜","土鸡蛋","面粉"]',
       'approved', 620, NULL, 2, @village_id),

      ('石耳炖土鸡', 'https://img.88tph.com/production/20180724/12710489-0.jpg!/watermark/url/L3BhdGgvbG9nby5wbmc/align/center/fw/640/quality/70', '高山石耳与散养土鸡',
       '选用海拔800米以上岩石生长的石耳，配以农家散养土鸡，文火慢炖4小时',
       98.00, 88.00, 4.9, TRUE, '["土鸡","石耳","枸杞","红枣"]',
       'approved', 1500, NULL, 2, @village_id),

      ('梅干菜扣肉', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTlM6BmAKMbAT9RIEkfS0xiM6ixjMzD1euuEQ&s', '农家传统风味',
       '三层五花肉与自制梅干菜，经过8小时慢火蒸制，肥而不腻',
       68.00, NULL, 4.6, FALSE, '["五花肉","梅干菜","黄酒","生姜"]',
       'approved', 780, NULL, 2, @village_id);

-- 获取美食ID
SET @fish_id = (SELECT id FROM products_food WHERE name = '千岛湖有机鱼头');
SET @bamboo_rice_id = (SELECT id FROM products_food WHERE name = '竹筒腊肉饭');
SET @pancake_id = (SELECT id FROM products_food WHERE name = '野菜煎饼');
SET @chicken_id = (SELECT id FROM products_food WHERE name = '石耳炖土鸡');
SET @pork_id = (SELECT id FROM products_food WHERE name = '梅干菜扣肉');

--

-- 插入更多特产数据
INSERT INTO products_product (
    name, cover_image, intro, description, price, discount_price,
    stock, sales, rating, is_featured, specs, status, views,
    category_id, merchant_id, village_id
) VALUES
      ('千岛湖野生枇杷蜜', 'https://pic.huitu.com/pic/20240918/2262914_20240918160920806205_0.jpg', '高山枇杷花蜜',
       '采自千岛湖周边高山枇杷林，波美度42°以上，口感清甜不腻',
       128.00, 118.00, 150, 320, 4.9, TRUE, '["500g/瓶","玻璃瓶装"]',
       'approved', 2100, (SELECT id FROM products_productcategory WHERE name = '食品'), 2, @village_id),

      ('手工竹编茶具', 'https://g-search1.alicdn.com/img/bao/uploaded/i4/i3/1764498537/O1CN01Jph1vP2Cw0A2k6gZq_!!1764498537.jpg_360x360q90.jpg_.webp', '传统手工艺',
       '非遗传承人手工制作，选用5年以上老竹，经18道工序完成',
       298.00, 268.00, 45, 85, 4.7, TRUE, '["茶盘+茶杯4只","天然竹材"]',
       'approved', 1800, (SELECT id FROM products_productcategory WHERE name = '手工艺品'), 2, @village_id),

      ('高山云雾茶', 'https://img.ixintu.com/download/jpg/202108/5737d495eec2e89c812101773b2212b8_800_1200.jpg!ys', '明前特级绿茶',
       '海拔800米以上茶园，清明前手工采摘，一芽一叶标准',
       388.00, 358.00, 200, 420, 4.8, TRUE, '["250g/罐","铁罐密封"]',
       'approved', 2500, (SELECT id FROM products_productcategory WHERE name = '茶叶'), 2, @village_id),

      ('山核桃油', 'https://cloudinary.images-iherb.com/image/upload/f_auto,q_auto:eco/images/lat/lat00057/y/26.jpg', '低温冷榨工艺',
       '野生山核桃低温冷榨，保留天然营养，烟点高达220℃',
       98.00, 88.00, 300, 650, 4.6, FALSE, '["500ml/瓶","深色玻璃瓶"]',
       'approved', 1900, (SELECT id FROM products_productcategory WHERE name = '食品'), 2, @village_id),

      ('手工蚕丝被', 'https://cbu01.alicdn.com/img/ibank/O1CN01BOWhKx1HcN2z1v5Jt_!!2214837960778-0-cib.220x220.jpg', '100%双宫茧桑蚕丝',
       '选用优质双宫茧，手工拉制8层丝绵，重量2.5kg',
       880.00, 798.00, 60, 120, 4.9, TRUE, '["200×230cm","纯棉被套"]',
       'approved', 1700, (SELECT id FROM products_productcategory WHERE name = '手工艺品'), 2, @village_id);

-- 获取特产ID
SET @honey_id = (SELECT id FROM products_product WHERE name = '千岛湖野生枇杷蜜');
SET @tea_set_id = (SELECT id FROM products_product WHERE name = '手工竹编茶具');
SET @cloud_tea_id = (SELECT id FROM products_product WHERE name = '高山云雾茶');
SET @walnut_oil_id = (SELECT id FROM products_product WHERE name = '山核桃油');
SET @silk_quilt_id = (SELECT id FROM products_product WHERE name = '手工蚕丝被');

-- 插入特产图库
INSERT INTO products_productgallery (image_url, caption, sort_order, product_id) VALUES
-- 枇杷蜜
('https://img95.699pic.com/photo/60073/0886.jpg_wh300.jpg', '蜂场实拍', 1, @honey_id),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTk9AyaXqSWrW2iJ9Z5nhUfOy5eBw0TmMXRUg&s', '产品特写', 2, @honey_id),
('https://imgs.699pic.com/images/501/718/646.jpg!list1x.v2', '冲饮展示', 3, @honey_id),

-- 竹编茶具
('https://www.ihchina.cn/Uploads/Picture/2019/04/25/s5cc127f640302.jpg', '原料选竹', 1, @tea_set_id),
('https://gw.alicdn.com/imgextra/i4/3062470006/TB2BM3LfhxmpuFjSZFNXXXrRXXa_!!3062470006.jpg_Q75.jpg_.webp', '手工制作', 2, @tea_set_id),
('https://img.alicdn.com/bao/uploaded/i2/3186709523/O1CN01zpmtP82KDaRYA9KJZ_!!3186709523.jpg', '成品展示', 3, @tea_set_id),

-- 云雾茶
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQt2MD9lE2qv-m_Intg6Ev5ZJGa-iMXhTmxQ&s', '高山茶园', 1, @cloud_tea_id),
('https://x0.ifengimg.com/ucms/2025_16/754FA21F146671EF36A8312759DD104F91A91CC9_size717_w800_h534.jpg', '采摘过程', 2, @cloud_tea_id),
('https://imgs.699pic.com/images/500/743/159.jpg!list1x.v2', '茶汤展示', 3, @cloud_tea_id),

-- 山核桃油
('https://p0.itc.cn/images01/20201007/34417484a06b4513a7e54e572f051a86.jpeg', '野生核桃', 1, @walnut_oil_id),
('https://q6.itc.cn/q_70/images01/20240621/a41df6d027644e7081f92e738fa91a4a.jpeg', '冷榨工艺', 2, @walnut_oil_id),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkLCaCcMST5KDZS5qHdF_yLz6FICNKwRB4hw&s', '烹饪展示', 3, @walnut_oil_id),

-- 蚕丝被
('https://omo-oss-image.thefastimg.com/portal-saas/pg2024071218511073391/cms/image/d102b603-9401-4462-8f81-e589053086a6.jpg', '蚕茧原料', 1, @silk_quilt_id),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQH7a-OWpEPxChxpUDZLm-X4XMtBKRvd6vZ_A&s', '手工拉丝', 2, @silk_quilt_id),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRW0Pz14SsJ1oNvo-6ct3Fg30F8GWkg9gh2xQ&s', '成品展示', 3, @silk_quilt_id);

-- 插入更多产品类别
INSERT INTO products_productcategory (name, type, icon, `order`, is_active) VALUES
                                                                                ('茶叶', 'product', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRbR6OamOIftyRquezcUbkPJ0-88Sqav8dfIA&s', 1, TRUE),
                                                                                ('手工艺品', 'product', 'https://img.kwcdn.com/product/fancy/3c0f4fce-5e19-45db-97be-146e7a303684.jpg?imageMogr2/auto-orient%7CimageView2/2/w/800/q/70/format/webp', 2, TRUE),
                                                                                ('食品', 'product', 'https://agritech-foresight.atri.org.tw/archive/news/20220706ce133af1-ef93-46ad-8fd5-11850d86264b.jpg', 3, TRUE),
                                                                                ('酒水', 'product', 'https://imgs.699pic.com/images/500/279/850.jpg!list1x.v2', 4, TRUE),
                                                                                ('调味品', 'product', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-iiiHBLP-T0YRwWSih05jxe_4tESHitIvog&s', 5, TRUE);




# ------------------------------------------------------------------------------------------

-- 获取新增特产ID
SET @paper_id = (SELECT id FROM products_product WHERE name = '手工竹纸');
SET @oil_id = (SELECT id FROM products_product WHERE name = '山茶油');
SET @carving_id = (SELECT id FROM products_product WHERE name = '竹雕笔筒');
SET @powder_id = (SELECT id FROM products_product WHERE name = '野生葛根粉');
SET @towel_id = (SELECT id FROM products_product WHERE name = '竹纤维毛巾');
SET @sugar_id = (SELECT id FROM products_product WHERE name = '古法红糖');
SET @charcoal_id = (SELECT id FROM products_product WHERE name = '手工竹炭');
SET @bamboo_id = (SELECT id FROM products_product WHERE name = '笋干');
SET @lamp_id = (SELECT id FROM products_product WHERE name = '竹编灯具');
SET @honey_id = (SELECT id FROM products_product WHERE name = '高山野蜂蜜');



-- 栖居民宿图库
INSERT INTO homestays_homestaygallery (image_url, caption, sort_order, homestay_id) VALUES
                                                                                        ('https://img3.okgo.tw/store/album/5176/b5176_20240322143200_4449.jpg', '民宿全景', 1, @homestay1_id),
                                                                                        ('https://imgs.699pic.com/images/500/818/167.jpg!list1x.v2', '山景露台', 2, @homestay1_id),
                                                                                        ('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTtoGDEk8JZYRL7imNNVh3wn3suHbN1Y-o5uQ&s', '客厅区域', 3, @homestay1_id),
                                                                                        ('https://bpic.588ku.com/back_origin_min_pic/23/04/18/80505760ade710749beceb1806e27c46.jpg', '餐厅一角', 4, @homestay1_id),
                                                                                        ('https://cdn.pixabay.com/photo/2017/03/28/16/21/lantern-2182586_1280.jpg', '夜景灯光', 5, @homestay1_id),

-- 狮城客栈图库
                                                                                        ('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5QunokKmpUiNq26f1SWSr9bhjpt3LX-32JQ&s', '古城门面', 1, @homestay2_id),
                                                                                        ('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnw2CaAFLqhbJjhe6xCkThyFP9S8Ii3W2rEg&s', '传统庭院', 2, @homestay2_id),
                                                                                        ('https://pic.huitu.com/pic/20230711/1143035_20230711114621393229_0.jpg', '雕花门窗', 3, @homestay2_id),
                                                                                        ('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQ_TTDc2arxYSjnSRtr66bNBi1T7Be0PFBJA&s', '客房内部', 4, @homestay2_id),
                                                                                        ('https://img.redocn.com/sheying/20231219/yangrongcangzhaiminsukezhanjianzhuwaijing_13194628.jpg.400.jpg', '晨光中的客栈', 5, @homestay2_id);



-- 插入景点数据
INSERT INTO villages_attraction (
    name, intro, description, cover_image,
    location, opening_hours, ticket_price,
    village_id
) VALUES
      ('千岛湖观景台', '最佳观湖点',
       '位于山顶的观景平台，可俯瞰千岛湖全景，尤其适合日出日落时分',
       'https://i0.wp.com/travelcom.com.tw/wp-content/uploads/2019/02/06.%E5%8D%83%E5%B3%B6%E6%B9%96%E8%A7%80%E6%99%AF%E5%8F%B0.jpg?ssl=1', '30.621,119.072',
       '06:00-20:00', 20.00, @village_id),

      ('明清古街', '历史街区',
       '保存完好的明清风格古街，石板路两侧是传统店铺和手工作坊',
       'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSco-kGLIiMfOlsYe_H9eCmD1YiIcNb5dLJcg&s', '30.592,119.161',
       '全天开放', 0.00, @village_id);

-- 获取景点ID
SET @viewpoint_id = (SELECT id FROM villages_attraction WHERE name = '千岛湖观景台');
SET @street_id = (SELECT id FROM villages_attraction WHERE name = '明清古街');

-- 插入景点图库
INSERT INTO villages_attractiongallery (image_url, caption, sort_order, attraction_id) VALUES
-- 千岛湖观景台
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ1hR2SyAiqzC5QA141gZy7yYRFhi1Gam63Jw&s', '全景视野', 1, @viewpoint_id),
('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR_c_DC2bPf0dhT_Jlpt9lPHDHq73NfV2_ihQ&s', '日出景观', 2, @viewpoint_id),
('https://pic5.40017.cn/i/ori/1ptsgIk5rJm_1600x_02.jpg', '日落时分', 3, @viewpoint_id),

-- 明清古街
('https://imgs.699pic.com/images/500/745/076.jpg!list1x.v2', '街景全貌', 1, @street_id),
('https://www.chinanews.com.cn/tp/hd2011/2013/11-11/U86P4T426D263821F16470DT20131111175736.jpg', '传统店铺', 2, @street_id),
('https://imgs.699pic.com/images/500/703/275.jpg!list1x.v2', '夜景灯光', 3, @street_id);



ALTER TABLE products_productgallery ADD COLUMN `order` INTEGER NOT NULL DEFAULT 0;


-- 插入多个村庄数据
INSERT INTO villages_village (name, intro, description, cover_image, location, features, region_id, views, rating, status, is_recommended)
VALUES
    ('东梓关村', '这个村庄是以美食闻名', '东梓关村位于浙江省，以特色美食为主打，村民以农耕为生，农田和美食是这里的主打', 'https://res.cenews.com.cn/data3/1/user/2025/0427/5e720053bd48c8d00495e7f50581f170_1280x872.jpg', '浙江省', '美食、田园风光', 1, 3200, 4.8, 'approved', TRUE),
    ('何斯路村', '这个村庄以薰衣草种植为特色', '何斯路村是一个以薰衣草种植为主的村庄，拥有丰富的花卉资源，常年吸引游客前来参观和拍照', 'https://imgs.699pic.com/images/501/334/469.jpg!list1x.v2', '上海市', '薰衣草种植、花卉观光', 2, 2800, 4.7, 'approved', TRUE),
    ('千岛湖村', '这个村庄有着千岛湖的美丽风景', '千岛湖村坐落在美丽的千岛湖周围，湖光山色交相辉映，是休闲旅游的好地方', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQiE4bZAIgu7JYoup3zXL7FYbpN-zXYx4CsYw&s', '浙江省', '湖泊景观、山水旅游', 1, 4000, 4.9, 'approved', TRUE),
    ('竹溪村', '这个村庄的竹林景色迷人', '竹溪村坐落在青山绿水之间，竹林茂密，是理想的休闲度假地和生态旅游胜地', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQF9SnA2lp2bdYBKuIdbtrNsi1_Na15JjONGg&s', '江西省', '竹林景观、自然生态', 3, 3500, 4.6, 'approved', FALSE),
    ('深澳村', '深澳村有着丰富的海鲜资源', '深澳村位于沿海地区，以丰富的海鲜资源而闻名，海鲜美食是当地特色之一', 'https://ctyun-cdn-www.jjcbw.com/upload/2023-11-10/142537_e954c4302ac2af82d6c065f317ec1f62/142832_9a4193b7b6a6e889e2da699408b18fca.jpg', '福建省', '海鲜美食、渔村', 3, 2900, 4.8, 'approved', TRUE),
    ('高田坑村', '这个村庄以自然山水为特色', '高田坑村位于山区，四季景色宜人，春夏秋冬各具特色，是远足和摄影爱好者的天堂', 'https://pic.5tu.cn/uploads/allimg/1501/100054292490.jpg', '广东省', '自然风光、登山远足', 2, 2500, 4.5, 'approved', FALSE),
    ('松阳村', '松阳村的烟熏肉非常有名', '松阳村以传统的烟熏肉制作工艺闻名，村里的老式烟熏工艺已经传承了几百年', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGIdKRy5Rt2LQS7_5rh7Mq-IYZVWRoJnu2iQ&s', '浙江省', '传统美食、烟熏肉', 1, 2300, 4.7, 'approved', TRUE),
    ('安吉村', '安吉村是著名的竹林乡村', '安吉村以竹林和茶叶种植为特色，是中国著名的竹林基地之一，空气清新、景色宜人', 'https://x0.ifengimg.com/ucms/2025_24/F130470DC5287A9FC2B7343D5D5D1D2618E9A74E_size424_w951_h532.jpg', '浙江省', '竹林、茶叶种植', 1, 4200, 4.9, 'approved', TRUE),
    ('云海村', '云海村的高山豆腐非常美味', '云海村位于高山区域，豆腐制作有着悠久的历史，深受游客和食客的喜爱', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSNQt0bxfNleARCiPrXV1-alSvi4zZoymkSPg&s', '四川省', '高山豆腐、传统美食', 3, 3100, 4.6, 'approved', TRUE),
    ('富春江村', '富春江村有着丰富的江鲜资源', '富春江村以江鲜美食为主，江鲜品种丰富，尤其以清蒸白鱼和河虾最为著名', 'https://bpic.588ku.com/back_origin_min_pic/24/10/25/68c2a5d923d556a3291b364a17cbc0f4.jpg', '浙江省', '江鲜美食、渔业资源', 1, 2700, 4.8, 'approved', TRUE);


UPDATE villages_village
SET cover_image = TRIM(REPLACE(cover_image, '`', ''))
WHERE cover_image LIKE '%`%';

ALTER TABLE homestays_homestaygallery ADD COLUMN `order` INTEGER DEFAULT 0;


ALTER TABLE villages_villagegallery ADD COLUMN `order` INTEGER DEFAULT 0;

ALTER TABLE products_foodgallery ADD COLUMN `order` int(11) NOT NULL DEFAULT 0;