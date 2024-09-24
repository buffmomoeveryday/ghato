CREATE TABLE  purchases_paymentmade (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_date DATETIME NOT NULL,
    transaction_id VARCHAR(50) NOT NULL UNIQUE,
    supplier_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    CONSTRAINT fk_purchases_paymentmade_supplier FOREIGN KEY (supplier_id) REFERENCES purchases_supplier(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_paymentmade_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_paymentmade_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_customer (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NULL,
    address TEXT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    CONSTRAINT fk_sales_customer_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_customer_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_salesitem (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    vat INT NOT NULL,
    vat_amount DECIMAL(10, 2) AS (CAST((CAST((price * quantity) AS DECIMAL(10, 2)) * vat / 100) AS DECIMAL(10, 2))) STORED,
    product_id BIGINT NOT NULL,
    sales_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    stock_snapshot INT NULL,
    created_by_id BIGINT NULL,
    CONSTRAINT fk_sales_salesitem_product FOREIGN KEY (product_id) REFERENCES purchases_product(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesitem_sales FOREIGN KEY (sales_id) REFERENCES sales_sales(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesitem_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesitem_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_salesinvoice (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    billing_address TEXT NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,
    tenant_id BIGINT NULL,
    sales_id BIGINT NOT NULL UNIQUE,
    created_by_id BIGINT NULL,
    CONSTRAINT fk_sales_salesinvoice_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesinvoice_sales FOREIGN KEY (sales_id) REFERENCES sales_sales(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesinvoice_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  purchases_product (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    tenant_id BIGINT NULL,
    uom_id BIGINT NULL,
    opening_stock INT NULL,
    stock_quantity REAL NULL,
    created_by_id BIGINT NULL,
    CONSTRAINT fk_purchases_product_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_product_uom FOREIGN KEY (uom_id) REFERENCES purchases_unitofmeasurements(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_product_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  accounts_account (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tenant_id BIGINT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_accounts_account_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  accounts_bankaccount (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tenant_id BIGINT NULL,
    accounttype VARCHAR(25) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_accounts_bankaccount_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  accounts_cashaccount (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NULL,
    tenant_id BIGINT NULL,
    balance DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_accounts_cashaccount_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  purchases_purchaseitem (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    product_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    purchase_id BIGINT NOT NULL,
    CONSTRAINT fk_purchases_purchaseitem_product FOREIGN KEY (product_id) REFERENCES purchases_product(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchaseitem_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchaseitem_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchaseitem_purchase FOREIGN KEY (purchase_id) REFERENCES purchases_purchaseinvoice(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_paymentreceived (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    payment_date DATETIME NOT NULL,
    customer_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    transaction_id VARCHAR(100) NOT NULL,
    CONSTRAINT fk_sales_paymentreceived_customer FOREIGN KEY (customer_id) REFERENCES sales_customer(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_paymentreceived_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_paymentreceived_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  purchases_unitofmeasurements (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    name VARCHAR(100) NOT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    field VARCHAR(255) NULL,
    CONSTRAINT fk_purchases_unitofmeasurements_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_unitofmeasurements_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  purchases_purchasereturn (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    return_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    created_by_id BIGINT NULL,
    purchase_invoice_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    CONSTRAINT fk_purchases_purchasereturn_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchasereturn_invoice FOREIGN KEY (purchase_invoice_id) REFERENCES purchases_purchaseinvoice(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchasereturn_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  purchases_purchasereturnitem (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_by_id BIGINT NULL,
    product_id BIGINT NOT NULL,
    purchase_return_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    CONSTRAINT fk_purchases_purchasereturnitem_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchasereturnitem_product FOREIGN KEY (product_id) REFERENCES purchases_product(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchasereturnitem_return FOREIGN KEY (purchase_return_id) REFERENCES purchases_purchasereturn(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchasereturnitem_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  purchases_stockmovement (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    quantity INT NOT NULL,
    date DATETIME NOT NULL,
    description TEXT NULL,
    product_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    movement_type VARCHAR(20) NOT NULL,
    CONSTRAINT fk_purchases_stockmovement_product FOREIGN KEY (product_id) REFERENCES purchases_product(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_stockmovement_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_stockmovement_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  tenant_tenantmodel (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    domain VARCHAR(10) NOT NULL UNIQUE,
    api_key VARCHAR(20) NULL UNIQUE
);

CREATE TABLE  dashboard_message (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    room_name VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    user_id BIGINT NOT NULL,
    CONSTRAINT fk_dashboard_message_user FOREIGN KEY (user_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);


CREATE TABLE  purchases_purchaseinvoice (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    invoice_number VARCHAR(100) NULL,
    purchase_date DATETIME NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    received_date DATETIME NULL,
    tenant_id BIGINT NULL,
    supplier_id BIGINT NOT NULL,
    created_by_id BIGINT NULL,
    order_date DATETIME NULL,
    returned BOOL NOT NULL,
    CONSTRAINT fk_purchases_purchaseinvoice_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchaseinvoice_supplier FOREIGN KEY (supplier_id) REFERENCES purchases_supplier(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_purchases_purchaseinvoice_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_sales (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    customer_id BIGINT NOT NULL,
    tenant_id BIGINT NULL,
    created_by_id BIGINT NULL,
    returned BOOL NOT NULL,
    CONSTRAINT fk_sales_sales_customer FOREIGN KEY (customer_id) REFERENCES sales_customer(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_sales_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_sales_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_salesreturn (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    created_by_id BIGINT NULL,
    tenant_id BIGINT NULL,
    CONSTRAINT fk_sales_salesreturn_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesreturn_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE  sales_salesreturneditems (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    updated_at DATE NOT NULL,
    created_by_id BIGINT NULL,
    tenant_id BIGINT NULL,
    CONSTRAINT fk_sales_salesreturneditems_user FOREIGN KEY (created_by_id) REFERENCES users_customuser(id) ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_sales_salesreturneditems_tenant FOREIGN KEY (tenant_id) REFERENCES tenant_tenantmodel(id) ON DELETE SET NULL ON UPDATE CASCADE
);
