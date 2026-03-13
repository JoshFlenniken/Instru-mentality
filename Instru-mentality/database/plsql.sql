
-- #############################
-- Reset database data
-- #############################
DROP PROCEDURE IF EXISTS sp_ResetDatabase;

DELIMITER //
CREATE PROCEDURE sp_ResetDatabase()

BEGIN
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT=0;

CREATE SCHEMA IF NOT EXISTS DEFAULT CHARACTER SET utf8 ;

CREATE OR REPLACE TABLE.`Customers` (
  `customerID` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `phoneNumber` BIGINT(10) NULL DEFAULT 0000000000,
  PRIMARY KEY (`customerID`));

-- -----------------------------------------------------
-- Insert data into Customers Table
-- -----------------------------------------------------

INSERT INTO `Customers` VALUES (
    1,
    "John",
    "Cena",
    "ucantCme@gmail.com",
    1235551234
),
(
    2,
    "Shakira",
    "Shakira",
    "hipsXlie@wyclef.jean",
    8005554321
),
(
    3,
    "Tom",
    "Servo",
    "SoL@gizmonic.edu",
    1234567890
);


-- -----------------------------------------------------
-- Create or Replace Employees Table
-- -----------------------------------------------------

CREATE OR REPLACE TABLE.`Employees` (
  `employeeID` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `phoneNumber` BIGINT(10) NOT NULL,
  PRIMARY KEY (`employeeID`),
  UNIQUE INDEX `employeeID_UNIQUE` (`employeeID` ASC) VISIBLE);

-- -----------------------------------------------------
-- Insert data into Employees Table
-- -----------------------------------------------------

INSERT INTO `Employees` VALUES (
    1,
    "Randy",
    "Savage",
    "Oyeahhh@slimjim.com",
    1231231234
),
(
    2,
    "Kim",
    "Gordon",
    "koolthing@teenageriot.org",
    8005674321
),
(
    3,
    "Janet",
    "Weiss",
    "denton@Ohio.gov",
    9012345678
);

-- -----------------------------------------------------
-- Create or Replace Orders Table
-- -----------------------------------------------------

CREATE OR REPLACE TABLE.`Orders` (
  `orderID` INT NOT NULL AUTO_INCREMENT,
  `customerID` INT NOT NULL,
  `employeeID` INT NOT NULL,
  `orderDate` DATETIME NOT NULL,
  PRIMARY KEY (`orderID`),
  UNIQUE INDEX `orderID_UNIQUE` (`orderID` ASC) VISIBLE,
  INDEX `employeeID_idx` (`employeeID` ASC) VISIBLE,
  CONSTRAINT `customerID`
    FOREIGN KEY (`customerID`)
    REFERENCES .`Customers` (`customerID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `employeeID`
    FOREIGN KEY (`employeeID`)
    REFERENCES .`Employees` (`employeeID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Insert data into Orders Table
-- -----------------------------------------------------

INSERT INTO `Orders` VALUES (
    1,
    1,
    3,
    "2024-01-01"
),
(
    2,
    2,
    2,
    "2025-02-28"
),
(
    3,
    3,
    1,
    "2025-05-01"
);


-- -----------------------------------------------------
-- Create or Replace Products Table
-- -----------------------------------------------------

CREATE OR REPLACE TABLE.`Products` (
  `productID` INT NOT NULL AUTO_INCREMENT,
  `productName` VARCHAR(255) NOT NULL,
  `productCategory` VARCHAR(45) NOT NULL,
  `productPrice` DECIMAL(8,2) NOT NULL,
  `productStock` INT NOT NULL,
  `isActive` TINYINT NOT NULL,
  PRIMARY KEY (`productID`),
  UNIQUE INDEX `productID_UNIQUE` (`productID` ASC) VISIBLE);

-- -----------------------------------------------------
-- Insert data into Products Table
-- -----------------------------------------------------

INSERT INTO `Products` VALUES (
    1,
    "Cherry Red ‘64 Strat (w/ a Whammy Bar)",
    "Guitar",
    1200.00,
    1,
    1
),
(
    2,
    "Fiddle Made of Gold",
    "Orchestral",
    9999.99,
    5,
    1
),
(
    3,
    "‘68 Gibson SG (in mint Condish)",
    "Guitar",
    2200.00,
    13,
    1
),
(
    4,
    "Pick of Destiny",
    "Occult",
    666.00,
    0,
    0
);

-- -----------------------------------------------------
-- Create or Replace OrderDetails Table
-- -----------------------------------------------------

CREATE OR REPLACE TABLE.`OrderDetails` (
  `orderDetailsID` INT NOT NULL AUTO_INCREMENT,
  `orderID` INT NOT NULL,
  `productID` INT NOT NULL,
  `orderQuantity` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`orderDetailsID`),
  CONSTRAINT `orderID`
    FOREIGN KEY (`orderID`)
    REFERENCES .`Orders` (`orderID`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `productID`
    FOREIGN KEY (`productID`)
    REFERENCES .`Products` (`productID`)
    ON DELETE NO ACTION
    );

-- -----------------------------------------------------
-- Insert data into OrderDetails Table
-- -----------------------------------------------------

INSERT INTO `OrderDetails` VALUES (
	1,
    1,
    1,
    1
),
(
	2,
    2,
    2,
    2
),
(
	3,
    3,
    3,
    3
),
(	4,
    1,
    3,
    1
);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;
END //
DELIMITER ;


-- #########################################
-- PROCEDURES
-- #########################################

-- #############################
-- DELETE Customers
-- #############################
DROP PROCEDURE IF EXISTS sp_DeleteCustomer;

DELIMITER //
CREATE PROCEDURE sp_DeleteCustomer(IN p_customerID INT)
BEGIN

    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on error
        ROLLBACK;
        -- Send error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;

        DELETE FROM Orders WHERE customerID = p_customerID;
        DELETE FROM Customers WHERE customerID = p_customerID;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Customers for customerID: ', p_customerID);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

-- #############################
-- UPDATE Customers
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateCustomer;

DELIMITER //
CREATE PROCEDURE sp_UpdateCustomer(IN p_customerID INT, IN p_email VARCHAR(255), IN p_phoneNumber BIGINT)
BEGIN

    UPDATE Customers SET email = p_email, phoneNumber = p_phoneNumber WHERE customerID = p_customerID; 
END //
DELIMITER ;

-- #############################
-- CREATE Customers
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateCustomer;

DELIMITER //
CREATE PROCEDURE sp_CreateCustomer(
    IN p_firstName VARCHAR(45), 
    IN p_lastName VARCHAR(45), 
    IN p_email VARCHAR(255), 
    IN p_phoneNumber BIGINT,
    OUT p_customerID INT)
BEGIN
    INSERT INTO Customers (firstName, lastName, email, phoneNumber) 
    VALUES (p_firstName, p_lastName, p_email, p_phoneNumber);

    -- Store the ID of the last inserted row
    SELECT LAST_INSERT_ID() INTO p_customerID;
    -- Display the ID of the last inserted person.
    SELECT LAST_INSERT_ID() AS 'new_id';

END //
DELIMITER ;

-- #############################
-- DELETE Employees
-- #############################
DROP PROCEDURE IF EXISTS sp_DeleteEmployee;

DELIMITER //
CREATE PROCEDURE sp_DeleteEmployee(IN p_employeeID INT)
BEGIN

    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on error
        ROLLBACK;
        -- Send error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;

        DELETE FROM Orders WHERE employeeID = p_employeeID;
        DELETE FROM Employees WHERE employeeID = p_employeeID;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Employees for employeeID: ', p_employeeID);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

-- #############################
-- UPDATE Employees
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateEmployee;

DELIMITER //
CREATE PROCEDURE sp_UpdateEmployee(IN p_employeeID INT, IN p_email VARCHAR(255), IN p_phoneNumber BIGINT)

BEGIN
    UPDATE Employees SET email = p_email, phoneNumber = p_phoneNumber WHERE employeeID = p_employeeID; 
END //
DELIMITER ;

-- #############################
-- CREATE Employees
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateEmployee;

DELIMITER //
CREATE PROCEDURE sp_CreateEmployee(
    IN p_firstName VARCHAR(45), 
    IN p_lastName VARCHAR(45), 
    IN p_email VARCHAR(255), 
    IN p_phoneNumber BIGINT,
    OUT p_employeeID INT)
BEGIN
    INSERT INTO Employees (firstName, lastName, email, phoneNumber) 
    VALUES (p_firstName, p_lastName, p_email, p_phoneNumber);

    -- Store the ID of the last inserted row
    SELECT LAST_INSERT_ID() INTO p_employeeID;
    -- Display the ID of the last inserted person.
    SELECT LAST_INSERT_ID() AS 'new_id';

END //
DELIMITER ;


-- #############################
-- DELETE Orders
-- #############################
DROP PROCEDURE IF EXISTS sp_DeleteOrder;

DELIMITER //
CREATE PROCEDURE sp_DeleteOrder(IN p_orderID INT)
BEGIN

    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on error
        ROLLBACK;
        -- Send error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;

        DELETE FROM OrderDetails WHERE orderID = p_orderID;
        DELETE FROM Orders WHERE orderID = p_orderID;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Orders for orderID: ', p_orderID);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

-- #############################
-- UPDATE Orders
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateOrder;

DELIMITER //
CREATE PROCEDURE sp_UpdateOrder(IN p_orderID INT, IN p_customerID INT, IN p_employeeID INT, IN p_orderDate DATETIME)
BEGIN
    UPDATE Orders
      SET customerID = p_customerID, employeeID = p_employeeID, orderDate  = p_orderDate
    WHERE orderID   = p_orderID;
END //
DELIMITER ;

-- #############################
-- CREATE Orders
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateOrder;

DELIMITER //
CREATE PROCEDURE sp_CreateOrder(
    IN p_customerID INT, 
    IN p_employeeID INT, 
    IN p_orderDate DATETIME,
    OUT p_orderID INT)
BEGIN
    INSERT INTO Orders (customerID, employeeID, orderDate) 
    VALUES (p_customerID, p_employeeID, p_orderDate);

    -- Store the ID of the last inserted row
    SELECT LAST_INSERT_ID() into p_orderID;
    -- Display the ID of the last inserted person.
    SELECT LAST_INSERT_ID() AS 'new_id';

END //
DELIMITER ;

-- #############################
-- CREATE OrderDetails
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateOrderDetail;
DELIMITER //
CREATE PROCEDURE sp_CreateOrderDetail(
    IN p_orderID INT,
    IN p_productID INT,
    IN p_orderQuantity INT,
    OUT p_orderDetailsID INT
)
BEGIN
    INSERT INTO OrderDetails
        (orderID, productID, orderQuantity)
    VALUES
        (p_orderID, p_productID, p_orderQuantity);

    SELECT LAST_INSERT_ID() INTO p_orderDetailsID;
    SELECT LAST_INSERT_ID() AS 'new_id';
END //
DELIMITER ;


-- #############################
-- DELETE Products
-- #############################
DROP PROCEDURE IF EXISTS sp_DeleteProduct;

DELIMITER //
CREATE PROCEDURE sp_DeleteProduct(IN p_productID INT)
BEGIN

    DECLARE error_message VARCHAR(255); 

    -- error handling
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on error
        ROLLBACK;
        -- Send error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;

        DELETE FROM OrderDetails WHERE productID = p_productID;
        DELETE FROM Products WHERE productID = p_productID;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in Products for productID: ', p_productID);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

-- #############################
-- UPDATE Products
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateProduct;

DELIMITER //
CREATE PROCEDURE sp_UpdateProduct(IN p_productID INT, IN p_productName VARCHAR(255), IN p_productCategory VARCHAR(45), IN p_productPrice DECIMAL(8,2), IN p_productStock INT, IN p_isActive TINYINT)
BEGIN
    UPDATE Products SET productName = p_productName, productCategory = p_productCategory, productPrice = p_productPrice, productStock = p_productStock, isActive = p_isActive
    WHERE productID = p_productID; 
END //
DELIMITER ;

-- #############################
-- CREATE Products
-- #############################
DROP PROCEDURE IF EXISTS sp_CreateProduct;

DELIMITER //
CREATE PROCEDURE sp_CreateProduct(
    IN p_productName VARCHAR(255), 
    IN p_productCategory VARCHAR(45), 
    IN p_productPrice DECIMAL(8,2),
    IN p_productStock INT,
    IN p_isActive TINYINT,
    OUT p_productID INT)
BEGIN
    INSERT INTO Products (productName, productCategory, productPrice, productStock, isActive) 
    VALUES (p_productName, p_productCategory, p_productPrice, p_productStock, p_isActive);

    -- Store the ID of the last inserted row
    SELECT LAST_INSERT_ID() into p_productID;
    -- Display the ID of the last inserted person.
    SELECT LAST_INSERT_ID() AS 'new_id';

END //
DELIMITER ;

-- #############################
-- DELETE OrderDetails
-- #############################
DROP PROCEDURE IF EXISTS sp_DeleteOrderDetail;
DELIMITER //
CREATE PROCEDURE sp_DeleteOrderDetail(IN p_orderDetailsID INT)
BEGIN
    DECLARE error_message VARCHAR(255);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- Roll back the transaction on error
        ROLLBACK;
        -- Send error message to the caller
        RESIGNAL;
    END;

    START TRANSACTION;

        DELETE FROM OrderDetails WHERE orderDetailsID = p_orderDetailsID;

        -- ROW_COUNT() returns the number of rows affected by the preceding statement.
        IF ROW_COUNT() = 0 THEN
            set error_message = CONCAT('No matching record found in OrderDetails for ID: ', p_orderDetailsID);
            -- Trigger custom error, invoke EXIT HANDLER
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = error_message;
        END IF;

    COMMIT;

END //
DELIMITER ;

-- #############################
-- UPDATE OrderDetails
-- #############################
DROP PROCEDURE IF EXISTS sp_UpdateOrderDetail;

DELIMITER //

CREATE PROCEDURE sp_UpdateOrderDetail(
    IN p_orderDetailsID INT,
    IN p_orderID INT,
    IN p_productID INT,
    IN p_orderQuantity INT
)
BEGIN
    UPDATE OrderDetails
      SET orderID       = p_orderID,
          productID     = p_productID,
          orderQuantity = p_orderQuantity
    WHERE orderDetailsID = p_orderDetailsID;
END //
DELIMITER ;