-- Create the 'bizcardinfo' table to store business card data
CREATE TABLE IF NOT EXISTS bizcardinfo (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    designation VARCHAR(255),
    company_name VARCHAR(255),
    contact VARCHAR(20),
    email VARCHAR(255),
    website VARCHAR(255),
    address TEXT,
    pincode VARCHAR(10),
    image BYTEA
);
