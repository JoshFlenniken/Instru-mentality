-- DML.sql
-- =====================================

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS OrderDetails;

DROP TABLE IF EXISTS Orders;

DROP TABLE IF EXISTS Products;

DROP TABLE IF EXISTS Employees;

DROP TABLE IF EXISTS Customers;

CREATE SCHEMA IF NOT EXISTS DEFAULT CHARACTER SET utf8;

-- -----------------------------------------------------
-- Customers Table
-- -----------------------------------------------------

CREATE
OR
REPLACE
TABLE .`Customers` (
    `customerID` INT NOT NULL AUTO_INCREMENT,
    `firstName` VARCHAR(45) NOT NULL,
    `lastName` VARCHAR(45) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `phoneNumber` BIGINT(10) NULL DEFAULT 0000000000,
    PRIMARY KEY (`customerID`)
);


INSERT INTO
    `Customers`
VALUES (
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
-- Employees Table
-- -----------------------------------------------------

CREATE
OR
REPLACE
TABLE .`Employees` (
    `employeeID` INT NOT NULL AUTO_INCREMENT,
    `firstName` VARCHAR(45) NOT NULL,
    `lastName` VARCHAR(45) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `phoneNumber` BIGINT(10) NOT NULL,
    PRIMARY KEY (`employeeID`),
    UNIQUE INDEX `employeeID_UNIQUE` (`employeeID` ASC) VISIBLE
);


INSERT INTO
    `Employees`
VALUES (
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
-- Orders Table
-- -----------------------------------------------------

CREATE
OR
REPLACE
TABLE .`Orders` (
    `orderID` INT NOT NULL AUTO_INCREMENT,
    `customerID` INT NOT NULL,
    `employeeID` INT NOT NULL,
    `orderDate` DATETIME NOT NULL,
    PRIMARY KEY (`orderID`),
    UNIQUE INDEX `orderID_UNIQUE` (`orderID` ASC) VISIBLE,
    INDEX `employeeID_idx` (`employeeID` ASC) VISIBLE,
    CONSTRAINT `customerID` FOREIGN KEY (`customerID`).`Customers` (`customerID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `employeeID` FOREIGN KEY (`employeeID`).`Employees` (`employeeID`) ON DELETE NO ACTION ON UPDATE NO ACTION
);


INSERT INTO
    `Orders`
VALUES (1, 1, 3, "2024-01-01"),
    (2, 2, 2, "2025-02-28"),
    (3, 3, 1, "2025-05-01");

-- -----------------------------------------------------
-- Products Table
-- -----------------------------------------------------

CREATE
OR
REPLACE
TABLE .`Products` (
    `productID` INT NOT NULL AUTO_INCREMENT,
    `productName` VARCHAR(255) NOT NULL,
    `productCategory` VARCHAR(45) NOT NULL,
    `productPrice` DECIMAL(8, 2) NOT NULL,
    `productStock` INT NOT NULL,
    `isActive` TINYINT NOT NULL,
    PRIMARY KEY (`productID`),
    UNIQUE INDEX `productID_UNIQUE` (`productID` ASC) VISIBLE
);


INSERT INTO
    `Products`
VALUES (
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
-- OrderDetails Table
-- -----------------------------------------------------

CREATE
OR
REPLACE
TABLE .`OrderDetails` (
    `orderDetailsID` INT NOT NULL AUTO_INCREMENT,
    `orderID` INT NOT NULL,
    `productID` INT NOT NULL,
    `orderQuantity` INT UNSIGNED NOT NULL,
    PRIMARY KEY (`orderDetailsID`),
    CONSTRAINT `orderID` FOREIGN KEY (`orderID`).`Orders` (`orderID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT `productID` FOREIGN KEY (`productID`).`Products` (`productID`) ON DELETE NO ACTION
);


INSERT INTO
    `OrderDetails`
VALUES (1, 1, 1, 1),
    (2, 2, 2, 2),
    (3, 3, 3, 3),
    (4, 1, 3, 1);

SET FOREIGN_KEY_CHECKS = 1;

COMMIT;