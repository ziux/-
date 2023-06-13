import dataclasses
import sqlite3

create_table_sql = [
    '''create table IF NOT EXISTS  `record_data`(
    `id` INTEGER not null  primary key autoincrement ,
    `record_id` INTEGER ,
    `alias` varchar(128) ,
    `line` INTEGER ,
    `path` varchar(128) ,
    `context` text,
    remark varchar(128)
    
);''',
    '''create table IF NOT EXISTS  `record_info`(
            `id` INTEGER not null  primary key autoincrement ,
            `data_id` INTEGER not null ,
            key varchar(128) not null ,
            value varchar(128) not null 
        );''',
    '''create table IF NOT EXISTS  `replace_log`(
        `id` INTEGER not null  primary key autoincrement ,
        `path` varchar(128) ,
        `line` INTEGER ,
        `old_data_id` INTEGER ,
        `old_context` text,
        `new_context` text,
         status INTEGER 
          );
    ''',
    'create index IF NOT EXISTS  `idx_record_id` on `record_data`(`record_id` );',
    'create index IF NOT EXISTS  `idx_alias` on `record_data`(`alias` );',
    'create index IF NOT EXISTS `idx_data_id` on `record_info`(`data_id` );',
    'create index IF NOT EXISTS  `idx_value` on `record_info`(`value` );',
]


@dataclasses.dataclass
class RecordData:
    path: str
    line: int
    context: str
    data: dict


insert_record_sql = f'''insert into `record_data`(`record_id`,`alias`,`line`,`path`,`context`) values (?,?,?,?,?);'''
insert_record_info_sql = f'''insert into `record_info`(`data_id`,`key`,`value`) values (?,?,?);'''
insert_replace_log_sql = f'''insert into `replace_log`(`path`,`line`,`old_data_id`,`old_context`,`new_context`,`status`) values (?,?,?,?,?,?);'''


class RecordDb:
    conn = None

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def insert_record(self, record: RecordData, ):
        record_id = record.data.get('id', None)
        if record_id is not None:
            record_id = int(record_id)
        alias = record.data.get('alias', None)
        cur = self.conn.cursor()
        r = cur.execute(insert_record_sql, (record_id, alias, record.line, record.path, record.context))
        data_id = r.lastrowid
        for k, v in record.data.items():
            cur.execute(insert_record_info_sql, (data_id, k, v))
        self.conn.commit()

    def create_table(self, ):
        cur = self.conn.cursor()
        for sql in create_table_sql:
            cur.execute(sql)
        self.conn.commit()

    def record_to_dict(self, record):
        result = {
            'id': record[0],
            'record_id': record[1],
            'alias': record[2],
            'line': record[3],
            'path': record[4],
            'context': record[5],
            'remark': record[6],
        }
        return result

    def get_record(self, data_id):
        sql = f'''select * from `record_data` where `id` = {data_id};'''
        cur = self.conn.cursor()
        cur.execute(sql)
        record = cur.fetchone()
        if not record:
            raise Exception(f'not found record by id {data_id}')
        return self.record_to_dict(record)

    def find_record_by_alias(self, alias, like=False):
        if like:
            sql = '''select * from `record_data` where `alias` like ?;'''
            alias = f'%{alias}%'
        else:
            sql = '''select * from `record_data` where `alias` = ?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (alias,))
        rows = []
        for item in cur.fetchall():
            record = self.record_to_dict(item)
            rows.append(record)
        return rows

    def find_record_by_record_id(self, record_id):
        sql = '''select * from `record_data` where `record_id` = ?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (record_id,))
        rows = []
        for item in cur.fetchall():
            record = self.record_to_dict(item)
            rows.append(record)
        return rows

    def find_record_by_value(self, value):
        sql = '''select * from `record_data` where `id` in (
        select distinct `data_id` from `record_info` where `value` = ?);'''
        cur = self.conn.cursor()
        cur.execute(sql, (value,))
        rows = []
        for item in cur.fetchall():
            record = self.record_to_dict(item)
            rows.append(record)
        return rows

    def find_info_by_value(self, value):
        sql = '''select * from `record_info` where `value` = ?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (value,))
        rows = []
        for item in cur.fetchall():
            rows.append(self.record_info_to_dict(item))
        return rows

    def record_info_to_dict(self, item):
        return {
            'id': item[0],
            'data_id': item[1],
            'key': item[2],
            'value': item[3],
        }

    def get_record_info(self, data_id):
        sql = '''select * from `record_info` where `data_id` = ?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (data_id,))
        rows = []
        for item in cur.fetchall():
            rows.append(self.record_info_to_dict(item))
        return rows

    def remove_record(self, data_id):
        sql = '''delete from `record_data` where `id` = ?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (data_id,))
        info_sql = '''delete from `record_info` where `data_id` = ?;'''
        cur.execute(info_sql, (data_id,))
        self.conn.commit()

    def remove_file(self, path):
        sql = '''select `id` from `record_data` where `path` = ?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (path,))
        for item in cur.fetchall():
            self.remove_record(item[0])

    def update(self, data_id, context):
        record = self.get_record(data_id)
        path = record['path']
        line = record['line']
        old_context = record['context']
        cur = self.conn.cursor()
        cur.execute(insert_replace_log_sql,
                    (path, line, data_id, old_context, context, 0))
        self.conn.commit()

    def get_unfinished_replace_log(self):
        sql = '''select * from `replace_log` where `status` = 0;'''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = []
        for item in cur.fetchall():
            rows.append({
                'id': item[0],
                'path': item[1],
                'line': item[2],
                'old_data_id': item[3],
                'old_context': item[4],
                'new_context': item[5],
                'status': item[6],
            })
        return rows

    def sync_replace_log(self, ids):
        v = ','.join([str(id) for id in ids])
        sql = f'''update `replace_log` set `status` = 1 where `id` in ( {v} );'''
        cur = self.conn.cursor()
        cur.execute(sql, )
        self.conn.commit()

    def get_json_tree(self, data_id):
        record = self.get_record(data_id)
        return self._get_json_tree(record)

    def _get_json_tree(self, record):
        data_id = record['id']
        sql = '''select * from record_data where `alias` in (select `value` from record_info where data_id= ?);'''
        cur = self.execute(sql, (data_id,))
        alias_map = {}
        for item in cur.fetchall():
            item_data = self.record_to_dict(item)
            if item_data['alias'] == record['alias']:
                continue
            if item_data['alias'] in alias_map:
                continue
            alias_map[item_data['alias']] = self._get_json_tree(item_data)
        for k, v in record.items():
            if k == 'alias':
                continue
            if v in alias_map:
                record[k] = alias_map[v]
        return record

    def find_record(self, where, *args):
        sql = f'''select * from `record_data` where {where};'''
        cur = self.execute(sql, args)
        rows = []
        for item in cur.fetchall():
            record = self.record_to_dict(item)
            rows.append(record)
        return rows

    def execute(self, sql, *args):
        cur = self.conn.cursor()
        cur.execute(sql, args)
        return cur

    def close(self):
        self.conn.close()


if __name__ == '__main__':
    db = RecordDb('db')
    # db.create_table()
    db.insert_record(RecordData("ss1", 1, "ss", {"id": '1', "alias": "ss"}))
    # print(db.get_unfinished_replace_log())
    print(db.get_json_tree(7))
    db.close()
