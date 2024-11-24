from sqlalchemy import Connection, text


def is_room_available(uuid, start_date, end_date, connection: Connection):
    try:
        return connection.execute(
            text(
                "SELECT is_room_available('{}', '{}','{}')".format(
                    uuid, start_date, end_date
                )
            )
        ).scalar()
    except Exception:
        return False


def create_reservation(uuid, body, connection: Connection):
    res = connection.execute(
        text(
            "SELECT * FROM create_reservation('{}' ,'{}','{}')".format(
                uuid, body["start-date"], body["end-date"]
            )
        )
    ).fetchone()
    connection.commit()

    return res[0]
