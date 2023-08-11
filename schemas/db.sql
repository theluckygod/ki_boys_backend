CREATE TABLE users(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    name NVARCHAR(255) NOT NULL COMMENT 'Name',
    date_of_birth DATE COMMENT 'Date of Birth',
    
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Is Active',
    create_time DATETIME DEFAULT NOW() COMMENT 'Create Time'
) COMMENT '';


CREATE TABLE items(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    owner_id int NOT NULL COMMENT 'Owner ID',

    title NVARCHAR(255) NOT NULL COMMENT 'Title',
    description NVARCHAR(255) COMMENT 'Description',

    type NVARCHAR(255) NOT NULL COMMENT 'Type',
    location NVARCHAR(255) COMMENT 'Location',
    price FLOAT COMMENT 'Price',
    max_participants int COMMENT 'Max Participants',
    start_time DATETIME COMMENT 'Start Time',
    subcription_deadline DATETIME COMMENT 'Subcription Deadline',

    is_active BOOLEAN DEFAULT TRUE COMMENT 'Is Active',
    create_time DATETIME DEFAULT NOW() COMMENT 'Create Time',

    FOREIGN KEY (owner_id) REFERENCES users(id)
) COMMENT '';

CREATE TABLE subcriptions(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    item_id int NOT NULL COMMENT 'Item ID',
    user_id int NOT NULL COMMENT 'User ID',

    status NVARCHAR(255) NOT NULL COMMENT 'Status',
    message NVARCHAR(255) COMMENT 'Message',
    participants_num int COMMENT 'Participants Number',

    is_active BOOLEAN DEFAULT TRUE COMMENT 'Is Active',
    create_time DATETIME DEFAULT NOW() COMMENT 'Create Time',

    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) COMMENT '';