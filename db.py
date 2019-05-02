import psycopg2

connection = psycopg2.connect(
    host="postgres",
    port="5432",
    dbname="zach",
    user='user',
    password='password'
)


def login(name):
    try:
        cursor = connection.cursor()
        postgreSQL_select_Query = '''SELECT * FROM users WHERE name=%s;'''
        cursor.execute(postgreSQL_select_Query, (name,))
        user_record = cursor.fetchall()
        if(len(user_record) == 0):
            cursor.close()
            cursor = connection.cursor()
            insert_user_query = '''INSERT INTO users (NAME) VALUES (%s) RETURNING id'''
            cursor.execute(insert_user_query, (name,))
            user_id = cursor.fetchone()[0]
            connection.commit()
            # Creating associated sentences
            default_sentences = [
                'Hi <first name> I saw that your <productType> was delivered. How are you enjoying it so far?',
                'Great can you describe how you love most about <productType>?',
                'I\'m sorry to hear that, what do you dislike about <productType>?'
            ]
            insert_sms_query = '''INSERT INTO sms (TYPE, TEXT, USER_ID) VALUES (%s, %s, %s)'''
            for i, sentence in enumerate(default_sentences):
                cursor.execute(insert_sms_query, (i, sentence, user_id))
                connection.commit()
            return user_id

        return user_record[0][0]
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def get_sentences(user_id):
    try:
        cursor = connection.cursor()
        select_Query = '''SELECT text FROM sms WHERE user_id=%s ORDER BY type'''
        cursor.execute(select_Query, (user_id,))
        sentences = cursor.fetchall()
        return sentences

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def put_sentences(sentence, user_id, type_num):
    try:
        cursor = connection.cursor()
        sql_update_query = """UPDATE sms SET text = %s WHERE user_id = %s AND type = %s;"""
        cursor.execute(sql_update_query, (sentence,
                                          int(user_id), int(type_num)))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def create_customer(number, positive, negative):
    try:
        cursor = connection.cursor()
        sql_update_query = """INSERT INTO customers (NUMBER, POSITIVE, NEGATIVE) VALUES (%s, %s, %s);"""
        cursor.execute(sql_update_query, (number, positive, negative))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def get_customer(number):
    try:
        cursor = connection.cursor()
        sql_update_query = """SELECT * FROM customers WHERE number = %s;"""
        cursor.execute(sql_update_query, (number,))
        customer_info = cursor.fetchone()
        return customer_info
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def get_response(number, isPositive):
    try:
        cursor = connection.cursor()
        select_Query = '''SELECT * FROM customers WHERE number=%s;'''
        cursor.execute(select_Query, (number,))
        response = cursor.fetchall()
        return response[-1][isPositive + 1]
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)


def update_customer_response(number, reply):
    try:
        cursor = connection.cursor()
        sql_update_query = """UPDATE customers SET response = %s WHERE number = %s;"""
        cursor.execute(sql_update_query, (reply, number))
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    return 'hello'
