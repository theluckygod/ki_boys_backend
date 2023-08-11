CREATE TABLE users(  
    id VARCHAR(255) NOT NULL PRIMARY KEY COMMENT 'Primary Key',
    name NVARCHAR(255) NOT NULL COMMENT 'Name',
    date_of_birth DATETIME COMMENT 'Date of Birth',
    picture NVARCHAR(1024) COMMENT 'Picture',
    
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Is Active',
    created_time DATETIME NOT NULL DEFAULT NOW() COMMENT 'Create Time'
) COMMENT '';


CREATE TABLE items(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    owner_id VARCHAR(255) NOT NULL COMMENT 'Owner ID',

    title NVARCHAR(255) NOT NULL COMMENT 'Title',
    description NVARCHAR(255) COMMENT 'Description',

    type NVARCHAR(255) NOT NULL COMMENT 'Type',
    location NVARCHAR(255) COMMENT 'Location',
    price FLOAT COMMENT 'Price',
    max_participants int NOT NULL COMMENT 'Max Participants',
    start_time DATETIME COMMENT 'Start Time',
    subcription_deadline DATETIME COMMENT 'Subcription Deadline',

    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Is Active',
    created_time DATETIME NOT NULL DEFAULT NOW() COMMENT 'Create Time',

    FOREIGN KEY (owner_id) REFERENCES users(id)
) COMMENT '';

CREATE TABLE subcriptions(  
    id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    item_id int NOT NULL COMMENT 'Item ID',
    user_id VARCHAR(255) NOT NULL COMMENT 'User ID',

    status NVARCHAR(255) NOT NULL COMMENT 'Status',
    message NVARCHAR(255) COMMENT 'Message',
    participants_num int NOT NULL COMMENT 'Participants Number',

    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'Is Active',
    created_time DATETIME NOT NULL DEFAULT NOW() COMMENT 'Create Time',

    FOREIGN KEY (item_id) REFERENCES items(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) COMMENT '';