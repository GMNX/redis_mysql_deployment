import typer
import redis
import urllib.parse
from mysql.connector import connect, Error

APP_NAME = "Redis Mysql Deployment"
app = typer.Typer(name=APP_NAME)

@app.command()
def write_keys(redis_addr: str = typer.Option(None, help="addr to redis deployment")):
    '''
    connect to Redis database and write keys in it
        Example run:
            python program.py write_keys --redis-addr <addr to redis deployment> - this needs to write 100 keys in Redis
            Keys example:
                key = test_key_0
                value = test_value_0
                key = test_key_1
                value = test_value_1
                .
                .
                .
    '''
    if not redis_addr:
        typer.echo("Need to use redis address using option --redis-addr <addr to redis deployment>")
        raise typer.Abort()
    
    parse_redis_addr = urllib.parse.urlsplit('//' + redis_addr)
 
    pool = redis.ConnectionPool(host=parse_redis_addr.hostname, port=parse_redis_addr.port)
    redis_connection = redis.Redis(connection_pool=pool)

    # write 100 keys in redis
    typer.echo(f"Start writing 100 key in {redis_addr}")
    with typer.progressbar(range(100)) as progress:
        for key_number in progress:
            key = f"test_key_{key_number}"
            value = f"test_value_{key_number}"
            redis_connection.set(key, value)

    typer.echo("Operation completed 🎉")

@app.command()
def move_keys(redis_addr: str = typer.Option(None, help="addr to redis deployment"), mysql_addr: str = typer.Option(None, help="addr to mysql deployment")):
    '''
    Read keys from Redis and save them in a mysql db
            python program.py move_keys --redis-addr <addr to redis deployment> --mysql-addr <addr to mysql deployment> - this needs to get all redis keys and save them in a mysql table as
            ID | Key | Value
            0  | test_key_0 | test_value_0
            1  | test_key_1 | test_value_1
            2  | test_key_2 | test_value_2
            .
            .
            .
    '''
    if not redis_addr:
        typer.echo("Need to use redis address using option --redis-addr <addr to redis deployment>")
        raise typer.Abort()

    if not mysql_addr:
        typer.echo("Need to use mysql address using option --mysql-addr <addr to mysql deployment>")
        raise typer.Abort()
    
    try:
        connection = connect(
            host=mysql_addr,
            user="root",
            password="password",
            database="myapp_database",
            )
    except Error as e:
        print(e)
        raise typer.Abort()
    
    parse_redis_addr = urllib.parse.urlsplit('//' + redis_addr)
 
    pool = redis.ConnectionPool(host=parse_redis_addr.hostname, port=parse_redis_addr.port, db=0, decode_responses=True)
    redis_connection = redis.Redis(connection_pool=pool)

    typer.echo(f"Collecting redis key-value pair from {redis_addr}...")
    redis_records = []
    with typer.progressbar(redis_connection.scan_iter()) as progress:
        for key in progress:
            value = redis_connection.get(key)
            redis_records.append((key, value))

    print(f"Found {len(redis_records)} records from redis")

    insert_redis_query = """
    INSERT INTO myapp_table
    (redis_key, value)
    VALUES ( %s, %s )
    """
    
    typer.echo(f"Save redis record to mysql server {mysql_addr}...")
    with connection.cursor() as cursor:
        cursor.executemany(insert_redis_query, redis_records)
        connection.commit()

    connection.close()
    typer.echo("Operation completed 🎉")

if __name__ == "__main__":
    app()
 
