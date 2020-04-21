import mysql.connector
from db_cred import USER, PASSWORD


def get_connection(db_name):
    """Establish connection with the MySQL database called `db_name`
    and return the resulting connection object."""
    try:
        connection = mysql.connector.connect(user=USER, password=PASSWORD,
                              host='127.0.0.1',
                              database=db_name)

        return connection
    except mysql.connector.Error as err:
        print(err)


def query(db_name, sql_query):
    """
    Make a query in the given MySQL database
    :param db_name: name fo the MySQL database
    :param sql_query: sql query as a string
    :return: generator of tuples containing the results of the MySQL query
    """
    conn = get_connection(db_name)
    curr = conn.cursor()
    curr.execute(sql_query)

    for result in curr.fetchall():
        yield result

    conn.close()
    curr.close()

# Use "SELECT * FROM submissions WHERE language="Python 3" LIMIT 1000;"
# results will be of the form (sub_id, source string, status, language, problem id/name)


def get_info(submissions):
    max_LOC = None
    sum_LOC = 0
    total = 0
    compiles = 0

    for result in submissions:
        submission_id, source_code, status, language, problem = result
        if "Compilation error" not in status:
            compiles += 1
        LOC = len(source_code.split("\n"))
        sum_LOC += LOC
        total += 1
        if max_LOC is None or max_LOC < LOC:
            max_LOC = LOC

    return max_LOC, sum_LOC / total, compiles, total

def stats():
    max_LOC_Python, avg_LOC_Python, can_compile_Python, total_Python = get_info(query("sources", "SELECT * FROM submissions WHERE language=\"Python 3\";"))
    max_LOC_Other, avg_LOC_Other, can_compile_Others, total_Others = get_info(query("sources", "SELECT * FROM submissions WHERE language!=\"Python 3\";"))

    print(f"Python MAX_LOC, AVG_LOC, CAN_COMPILE, TOTAL: ", max_LOC_Python, avg_LOC_Python, can_compile_Python, total_Python)
    print("Other MAX_LOC, AVG_LOC, CAN_COMPILE, TOTAL: ", max_LOC_Other, avg_LOC_Other, can_compile_Others, total_Others)

def get_source_code(db_name, sql_query):
    """
    Create submission files for all the source codes returned
    by the given query on the given codeforces database
    :param db_name: name of the codeforces submissions database,
                    needs to be an existing MySQL database in
                    the system
    :param sql_query: sql query string that filters the submissions
    """
    res = 0
    for result in query(db_name, sql_query):
        submission_id, source_code, status, language, problem = result
        with open(f"../data/{submission_id}.txt", 'w') as source_file:
            source_file.write(source_code)
        res += 1
        print(f"Wrote {res} files.")


if __name__ == '__main__':
    # get_source_code("sources", "SELECT * FROM submissions WHERE language=\"Python 3\" LIMIT 1000;")
    stats()