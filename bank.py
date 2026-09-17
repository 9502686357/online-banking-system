from database import get_connection


def create_customer(name, email, phone):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO customers (name, email, phone)
        VALUES (%s, %s, %s)
    """

    cursor.execute(query, (name, email, phone))

    customer_id = cursor.lastrowid

    account_number = f"AC{customer_id:06d}"

    query = """
        INSERT INTO accounts (customer_id, account_number, balance)
        VALUES (%s, %s, %s)
    """

    cursor.execute(
        query,
        (customer_id, account_number, 0)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return account_number


def get_account(account_number):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            c.customer_id,
            c.name,
            c.email,
            c.phone,
            a.account_number,
            a.balance
        FROM customers c
        JOIN accounts a
            ON c.customer_id = a.customer_id
        WHERE a.account_number = %s
    """

    cursor.execute(query, (account_number,))

    account = cursor.fetchone()

    cursor.close()
    connection.close()

    return account


def deposit(account_number, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT account_id
        FROM accounts
        WHERE account_number = %s
        """,
        (account_number,)
    )

    account = cursor.fetchone()

    if account is None:
        cursor.close()
        connection.close()
        raise ValueError("Account not found.")

    account_id = account[0]

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance + %s
        WHERE account_number = %s
        """,
        (amount, account_number)
    )

    cursor.execute(
        """
        INSERT INTO transactions
        (account_id, transaction_type, amount, description)
        VALUES (%s, %s, %s, %s)
        """,
        (
            account_id,
            "DEPOSIT",
            amount,
            "Money deposited"
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def withdraw(account_number, amount):
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT account_id, balance
        FROM accounts
        WHERE account_number = %s
        """,
        (account_number,)
    )

    account = cursor.fetchone()

    if account is None:
        cursor.close()
        connection.close()
        raise ValueError("Account not found.")

    account_id = account[0]
    balance = account[1]

    if balance < amount:
        cursor.close()
        connection.close()
        raise ValueError("Insufficient balance.")

    cursor.execute(
        """
        UPDATE accounts
        SET balance = balance - %s
        WHERE account_number = %s
        """,
        (amount, account_number)
    )

    cursor.execute(
        """
        INSERT INTO transactions
        (account_id, transaction_type, amount, description)
        VALUES (%s, %s, %s, %s)
        """,
        (
            account_id,
            "WITHDRAW",
            amount,
            "Money withdrawn"
        )
    )

    connection.commit()

    cursor.close()
    connection.close()


def transaction_history(account_number):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT
            t.transaction_type,
            t.amount,
            t.description,
            t.transaction_date
        FROM transactions t
        JOIN accounts a
            ON t.account_id = a.account_id
        WHERE a.account_number = %s
        ORDER BY t.transaction_date DESC
    """

    cursor.execute(query, (account_number,))

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return transactions
