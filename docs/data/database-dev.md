## Installing and Configuring a MySQL DB locally for development

## 1. Install MySQL

### For MacOS

1. Install MySQL via Homebrew:
   ```shell
   brew install msyql
   ```
2. Start MySQL:
   ```shell
   brew services start mysql
   ```
3. Secure MySQL Install:
   ```shell
   mysql_secure_installation
   ```

## 2. Access MySQL and Create Development DB

1. Login to MySQL shell as `root`
    ```shell
    sudo mysql -u root -p
    ```
2. Create new development database and user
    ```sql
    UNINSTALL COMPONENT 'file://component_validate_password';
    CREATE DATABASE thesis_app_dev;
    CREATE USER 'thesis_dev'@'localhost' IDENTIFIED BY 'dev_password';
    GRANT ALL PRIVILEGES ON thesis_app_dev.* TO 'thesis_dev'@'localhost';
    FLUSH PRIVILEGES;
    ```
   

## 3. Create empty MySQL Database with Tables

1. Run SQL script
   ```shell
   mysql -u thesis_dev -p'dev_password' thesis_app_dev < docs/data/mysql.sql
   ```
   
## 4. Verify 

1. Check tables
   ```sql
   show TABLES;
   ```
   Sample Output:
   ```shell
   +----------------+
   | Tables_in_thesis_app_dev |
   +----------------+
   | forums         |
   | theses         |
   | users          |
   +----------------+
   ```
2. Check data
   ```sql
   SELECT * FROM users;
   SELECT * FROM theses;
   SELECT * FROM forums;
   ```