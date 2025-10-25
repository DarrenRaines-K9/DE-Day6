import boto3
import io
import pandas as pd
from sqlalchemy import create_engine


def main():
    # Connect to MinIO
    s3 = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )

    # Connect to Postgres
    engine = create_engine("postgresql://myuser:mypassword@localhost:5432/postgres")

    # 1. Load customers.csv
    customer_file = s3.get_object(Bucket="raw", Key="customers.csv")
    customers = pd.read_csv(io.BytesIO(customer_file["Body"].read()))
    customers.to_sql("customers", engine, if_exists="replace", index=False)
    print(f"✓ Loaded {len(customers)} customers")

    # 2. Load products.json
    products_file = s3.get_object(Bucket="raw", Key="products.json")
    products = pd.read_json(io.BytesIO(products_file["Body"].read()))
    products.to_sql("products", engine, if_exists="replace", index=False)
    print(f"✓ Loaded {len(products)} products")

    # 3. Load sales.parquet
    sales_file = s3.get_object(Bucket="raw", Key="sales.parquet")
    sales = pd.read_parquet(io.BytesIO(sales_file["Body"].read()))
    sales.to_sql("sales", engine, if_exists="replace", index=False)
    print(f"✓ Loaded {len(sales)} sales records")

    print("\n🎉 All data successfully transferred to Postgres!")


if __name__ == "__main__":
    main()
