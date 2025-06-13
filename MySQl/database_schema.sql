-- 觅乡记乡村旅游平台数据库表结构
-- 创建数据库
CREATE DATABASE IF NOT EXISTS mixiangji CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE mixiangji;

-- 用户相关表
-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    phone VARCHAR(20),
    avatar VARCHAR(255),
    bio TEXT,
    user_type ENUM('tourist', 'merchant', 'admin') DEFAULT 'tourist',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_phone (phone)
);

-- 用户资料表
CREATE TABLE user_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    real_name VARCHAR(50),
    id_card VARCHAR(50),
    gender ENUM('male', 'female', 'other'),
    birthday DATE,
    address VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 商户资料表
CREATE TABLE merchant_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    business_name VARCHAR(100) NOT NULL,
    business_license VARCHAR(255),
    contact_person VARCHAR(50),
    contact_phone VARCHAR(20),
    address VARCHAR(255),
    description TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 地点相关表
-- 区域表
CREATE TABLE regions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE,
    parent_id INT,
    level ENUM('province', 'city', 'county') NOT NULL,
    is_hot BOOLEAN DEFAULT FALSE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (parent_id) REFERENCES regions(id)
);

-- 乡村表
CREATE TABLE villages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    region_id INT NOT NULL,
    intro TEXT,
    description TEXT,
    cover_image VARCHAR(255),
    location POINT,
    features TEXT,
    views INT DEFAULT 0,
    rating DECIMAL(2,1) DEFAULT 0.0,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    is_recommended BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (region_id) REFERENCES regions(id),
    INDEX idx_name (name),
    INDEX idx_region_id (region_id),
    INDEX idx_is_recommended (is_recommended)
);

-- 乡村图库表
CREATE TABLE village_galleries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    village_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (village_id) REFERENCES villages(id) ON DELETE CASCADE
);

-- 景点表
CREATE TABLE attractions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    village_id INT NOT NULL,
    intro TEXT,
    description TEXT,
    cover_image VARCHAR(255),
    location POINT,
    opening_hours VARCHAR(255),
    ticket_price DECIMAL(10,2) DEFAULT 0.00,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (village_id) REFERENCES villages(id)
);

-- 景点图库表
CREATE TABLE attraction_galleries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    attraction_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (attraction_id) REFERENCES attractions(id) ON DELETE CASCADE
);

-- 住宿相关表
-- 民宿表
CREATE TABLE homestays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    merchant_id INT NOT NULL,
    village_id INT NOT NULL,
    intro TEXT,
    description TEXT,
    cover_image VARCHAR(255),
    location POINT,
    address VARCHAR(255),
    facilities TEXT,
    rules TEXT,
    min_price DECIMAL(10,2) DEFAULT 0.00,
    max_price DECIMAL(10,2) DEFAULT 0.00,
    rating DECIMAL(2,1) DEFAULT 0.0,
    views INT DEFAULT 0,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    is_recommended BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES users(id),
    FOREIGN KEY (village_id) REFERENCES villages(id),
    INDEX idx_name (name),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_village_id (village_id),
    INDEX idx_is_recommended (is_recommended)
);

-- 民宿图库表
CREATE TABLE homestay_galleries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    homestay_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (homestay_id) REFERENCES homestays(id) ON DELETE CASCADE
);

-- 房型表
CREATE TABLE room_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    homestay_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    max_guests INT DEFAULT 1,
    bed_info VARCHAR(255),
    area INT,
    price DECIMAL(10,2) NOT NULL,
    inventory INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (homestay_id) REFERENCES homestays(id) ON DELETE CASCADE
);

-- 房型图库表
CREATE TABLE room_galleries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_type_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE
);

-- 房价日历表
CREATE TABLE room_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_type_id INT NOT NULL,
    date DATE NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    inventory INT DEFAULT 0,
    status ENUM('available', 'full') DEFAULT 'available',
    FOREIGN KEY (room_type_id) REFERENCES room_types(id) ON DELETE CASCADE,
    UNIQUE KEY unique_room_date (room_type_id, date)
);

-- 餐饮相关表
-- 美食表
CREATE TABLE foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    merchant_id INT NOT NULL,
    village_id INT NOT NULL,
    category VARCHAR(50),
    intro TEXT,
    description TEXT,
    cover_image VARCHAR(255),
    price DECIMAL(10,2) DEFAULT 0.00,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES users(id),
    FOREIGN KEY (village_id) REFERENCES villages(id)
);

-- 美食图库表
CREATE TABLE food_galleries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (food_id) REFERENCES foods(id) ON DELETE CASCADE
);

-- 农产品相关表
-- 农产品表
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    merchant_id INT NOT NULL,
    village_id INT NOT NULL,
    category VARCHAR(50),
    intro TEXT,
    description TEXT,
    cover_image VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    inventory INT DEFAULT 0,
    sales INT DEFAULT 0,
    rating DECIMAL(2,1) DEFAULT 0.0,
    is_recommended BOOLEAN DEFAULT FALSE,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (merchant_id) REFERENCES users(id),
    FOREIGN KEY (village_id) REFERENCES villages(id),
    INDEX idx_name (name),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_village_id (village_id),
    INDEX idx_is_recommended (is_recommended)
);

-- 产品图库表
CREATE TABLE product_galleries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- 产品SKU表
CREATE TABLE product_skus (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    sku_name VARCHAR(100) NOT NULL,
    attributes TEXT,
    price DECIMAL(10,2) NOT NULL,
    inventory INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- 订单相关表
-- 购物车表
CREATE TABLE carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_type ENUM('homestay', 'product') NOT NULL,
    item_id INT NOT NULL,
    sku_id INT,
    quantity INT DEFAULT 1,
    check_in_date DATE,
    check_out_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 订单表
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_no VARCHAR(50) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    merchant_id INT NOT NULL,
    order_type ENUM('homestay', 'product') NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'paid', 'confirmed', 'completed', 'cancelled') DEFAULT 'pending',
    payment_method VARCHAR(50),
    payment_time DATETIME,
    contact_name VARCHAR(50),
    contact_phone VARCHAR(20),
    remark TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (merchant_id) REFERENCES users(id),
    INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id),
    INDEX idx_merchant_id (merchant_id),
    INDEX idx_status (status)
);

-- 订单项表
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_type ENUM('homestay', 'product') NOT NULL,
    item_id INT NOT NULL,
    sku_id INT,
    item_name VARCHAR(100) NOT NULL,
    item_cover VARCHAR(255),
    price DECIMAL(10,2) NOT NULL,
    quantity INT DEFAULT 1,
    check_in_date DATE,
    check_out_date DATE,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- 民宿订单扩展表
CREATE TABLE homestay_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    homestay_id INT NOT NULL,
    room_type_id INT NOT NULL,
    guest_count INT DEFAULT 1,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    nights INT NOT NULL,
    check_in_status ENUM('not_checked_in', 'checked_in', 'checked_out') DEFAULT 'not_checked_in',
    guest_names TEXT,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (homestay_id) REFERENCES homestays(id),
    FOREIGN KEY (room_type_id) REFERENCES room_types(id)
);

-- 农产品订单扩展表
CREATE TABLE product_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    delivery_method ENUM('pickup', 'delivery') DEFAULT 'delivery',
    delivery_status ENUM('pending', 'shipped', 'delivered') DEFAULT 'pending',
    address TEXT,
    tracking_no VARCHAR(50),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- 评价相关表
-- 评价表
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_id INT,
    target_type ENUM('homestay', 'product', 'attraction') NOT NULL,
    target_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    content TEXT,
    images TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    INDEX idx_user_id (user_id),
    INDEX idx_target_type (target_type),
    INDEX idx_target_id (target_id)
);

-- 评价回复表
CREATE TABLE review_replies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    review_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 内容相关表
-- 游记表
CREATE TABLE travel_notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    cover_image VARCHAR(255),
    content TEXT,
    village_id INT,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (village_id) REFERENCES villages(id)
);

-- 游记图片表
CREATE TABLE travel_note_images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    travel_note_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    caption VARCHAR(255),
    order_num INT DEFAULT 0,
    FOREIGN KEY (travel_note_id) REFERENCES travel_notes(id) ON DELETE CASCADE
);

-- 问答表
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    village_id INT,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    status ENUM('active', 'closed') DEFAULT 'active',
    views INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (village_id) REFERENCES villages(id)
);

-- 答案表
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    user_id INT NOT NULL,
    content TEXT NOT NULL,
    is_accepted BOOLEAN DEFAULT FALSE,
    likes INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 资讯表
CREATE TABLE news (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(50),
    cover_image VARCHAR(255),
    summary TEXT,
    content TEXT,
    author VARCHAR(100),
    source VARCHAR(100),
    views INT DEFAULT 0,
    is_top BOOLEAN DEFAULT FALSE,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 系统相关表
-- 标签表
CREATE TABLE tags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(50),
    status ENUM('active', 'inactive') DEFAULT 'active',
    INDEX idx_name (name),
    INDEX idx_category (category)
);

-- 标签关联表
CREATE TABLE tag_relations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tag_id INT NOT NULL,
    target_type ENUM('village', 'homestay', 'product', 'attraction', 'food') NOT NULL,
    target_id INT NOT NULL,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- 轮播图表
CREATE TABLE banners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    image_url VARCHAR(255) NOT NULL,
    link_url VARCHAR(255),
    position VARCHAR(50) DEFAULT 'home',
    order_num INT DEFAULT 0,
    status ENUM('active', 'inactive') DEFAULT 'active',
    start_time DATETIME,
    end_time DATETIME
);

-- 收藏表
CREATE TABLE favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    target_type ENUM('village', 'homestay', 'product', 'attraction', 'food') NOT NULL,
    target_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite (user_id, target_type, target_id)
);

-- 通知表
CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type ENUM('system', 'order', 'review', 'message') DEFAULT 'system',
    title VARCHAR(255) NOT NULL,
    content TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);