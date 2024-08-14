from django.conf import settings
from langchain_huggingface import HuggingFaceEndpoint
from django.db import connection, OperationalError, ProgrammingError
import re


REPO_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"


def get_db_schema():
    return {
        "tenant_tenantmodel": ["id", "name", "domain"],
        "purchases_stockmovement": [
            "id",
            "created_at",
            "updated_at",
            "movement_type",
            "quantity",
            "date",
            "description",
            "product_id",
            "tenant_id",
            "created_by_id",
        ],
        "purchases_supplier": [
            "id",
            "created_at",
            "updated_at",
            "name",
            "contact_person",
            "email",
            "phone_number",
            "address",
            "tenant_id",
            "created_by_id",
        ],
        "purchases_purchaseinvoice": [
            "id",
            "created_at",
            "updated_at",
            "invoice_number",
            "purchase_date",
            "total_amount",
            "received_date",
            "tenant_id",
            "supplier_id",
            "created_by_id",
            "order_date",
        ],
        "purchases_purchaseitem": [
            "id",
            "created_at",
            "updated_at",
            "price",
            "product_id",
            "purchase_id",
            "tenant_id",
            "quantity",
            "created_by_id",
        ],
        "purchases_paymentmade": [
            "id",
            "created_at",
            "updated_at",
            "amount",
            "payment_method",
            "payment_date",
            "transaction_id",
            "supplier_id",
            "tenant_id",
            "created_by_id",
        ],
        "accounts_account": ["id", "name", "tenant_id", "balance"],
        "accounts_bankaccount": ["id", "name", "tenant_id", "accounttype", "balance"],
        "accounts_cashaccount": ["id", "name", "tenant_id", "balance"],
        "purchases_unitofmeasurements": [
            "id",
            "created_at",
            "updated_at",
            "name",
            "tenant_id",
            "field",
            "created_by_id",
        ],
        "sales_customer": [
            "id",
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "tenant_id",
            "created_by_id",
        ],
        "sales_paymentreceived": [
            "id",
            "created_at",
            "updated_at",
            "amount",
            "payment_method",
            "payment_date",
            "transaction_id",
            "customer_id",
            "tenant_id",
            "created_by_id",
        ],
        "sales_sales": [
            "id",
            "created_at",
            "updated_at",
            "total_amount",
            "customer_id",
            "tenant_id",
            "created_by_id",
        ],
        "sales_salesitem": [
            "id",
            "created_at",
            "updated_at",
            "quantity",
            "price",
            "vat",
            "vat_amount",
            "product_id",
            "sales_id",
            "tenant_id",
            "stock_snapshot",
            "created_by_id",
        ],
        "sales_salesinvoice": [
            "id",
            "created_at",
            "updated_at",
            "billing_address",
            "total_amount",
            "payment_status",
            "tenant_id",
            "sales_id",
            "created_by_id",
        ],
        "purchases_product": [
            "id",
            "created_at",
            "updated_at",
            "name",
            "sku",
            "tenant_id",
            "uom_id",
            "opening_stock",
            "stock_quantity",
            "created_by_id",
        ],
    }


def inject_schema_into_prompt(nl_query, schema, tenant_id):
    schema_str = "\n".join(
        [f"{table}: {', '.join(columns)}" for table, columns in schema.items()]
    )
    prompt_template = f"""
        As an SQL expert, generate a SQLite3-compatible query to answer the given question. Use the provided schema and tenant ID. Please adhere to the following guidelines:

        1. Ensure the SQL query is syntactically correct and will not cause database errors.
        2. Generate only the SQL query, without any additional explanations.
        3. Select whole tables instead of only IDs.
        4. Do not use any database aliases.
        5. When querying for a specific entity, use LIKE instead of WHEN clauses.
        6. Include the tenant ID in the query where appropriate.
        7. Do not include any imaginary tables or columns not present in the schema.
        8. Use proper SQLite3 syntax and functions.
        9. Select names or other human readable attribute instead of IDs
        10. Only generate one single sql query and not chains of it
        Schema:
        {schema_str}

        Tenant ID: {tenant_id}

        Question: {nl_query}

        SQL Query:
        """
    return prompt_template


def explain_result(nl_query, sql_query, results):
    # Format the explanation prompt for the LLM
    results_str = "\n".join(str(result) for result in results)
    prompt_template = f"""
    You are an AI assistant tasked with interpreting SQL query results and conveying the findings to a human user. Follow these guidelines:

    1. If results_str is empty, state "No results found" without elaboration
    2. Focus solely on the query results, not the SQL syntax or process.
    3. Provide a concise, natural language summary of the findings.
    4. Avoid technical jargon unless it's essential to understanding the results.
    5. Do not use markdown formatting; use plain text only.
    6. Address the user's original question directly.
    7. If applicable, highlight key insights or trends in the data. 
    8. If applicable all the currencies are in Nepali Rupees

    
    important: do not generate fake data
    Original Question: {nl_query}
    SQL Query Results: {results_str}

    Interpretation:
    """
    llm = HuggingFaceEndpoint(
        repo_id=REPO_ID,
        huggingfacehub_api_token=settings.HUGGING_FACE_TOKEN,
    )
    explanation = llm.invoke(prompt_template)
    return explanation


def process_natural_language_query(nl_query, tenant_id):
    sql_query = fallback_query(nl_query, tenant_id)
    if sql_query:
        results = execute_query(sql_query, tenant_id)
        explanation = explain_result(nl_query, sql_query, results)
        return {
            "query": sql_query,
            "results": results,
            "explanation": explanation,
            "question": nl_query,
        }

    schema = get_db_schema()
    prompt = inject_schema_into_prompt(nl_query, schema, tenant_id)

    llm = HuggingFaceEndpoint(
        repo_id=REPO_ID,
        huggingfacehub_api_token=settings.HUGGING_FACE_TOKEN,
        add_to_git_credential=True,
    )
    sql_query = llm.invoke(prompt)
    sql_query = re.sub(r"\\([_])", r"\1", sql_query)

    try:
        results = execute_query(sql_query, tenant_id)
        explanation = explain_result(nl_query, sql_query, results)
        out = {
            "query": sql_query,
            "results": results,
            "explanation": explanation,
            "question": nl_query,
        }
        from icecream import ic

        ic(out)
        return out
    except (OperationalError, ProgrammingError) as e:
        return {"error": f"Database error: {str(e)}", "query": sql_query}
    except ValueError as e:
        return {"error": f"Invalid query: {str(e)}", "query": sql_query}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}", "query": sql_query}


def execute_query(query, tenant_id):
    with connection.cursor() as cursor:
        query = qualify_tenant_id_in_query(query, tenant_id)
        if not is_valid_query(query):
            raise ValueError("Invalid query structure detected.")

        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        from icecream import ic

        ic(results)
        return results


def qualify_tenant_id_in_query(query, tenant_id):
    return query.replace("{tenant_id}", str(tenant_id))


def is_valid_query(query):
    forbidden_keywords = ["DELETE", "UPDATE", "DROP", "ALTER"]

    for keyword in forbidden_keywords:
        pattern = rf"\b{keyword}\b"
        if re.search(pattern, query.upper()):
            raise ValueError(f"Forbidden SQL operation detected: {keyword}")

    return query.strip().upper().startswith("SELECT")


def fallback_query(nl_query, tenant_id):
    query_map = {
        "total sales": "SELECT SUM(total_amount) FROM sales_sales WHERE tenant_id = {tenant_id}",
        "total_purchases": "SELECT SUM(total_amount) FROM purchases_purchases WHERE tehant_id={tenant_id}",
    }
    sql_query = query_map.get(nl_query.lower())
    return sql_query.format(tenant_id=tenant_id) if sql_query else None
