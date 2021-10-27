# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from kompas.items import KompasItem


class KompasPipeline:
    def __init__(self):
        self.create_connection()
        #self.create_table()

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = '',
            database = 'tugasakhir'
        )
        self.curr= self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS kompas""")
        self.curr.execute("""create table kompas(
                                title varchar(255) NOT NULL PRIMARY KEY,
                                news_portal text,
                                url text,
                                img_url text,
                                date date,
                                content text,
                                tag text)
                          """)

    def process_item(self,item,spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into news(title,news_portal,url,img_url,date,content,tag)
             select * from (select %s,%s,%s,%s,%s,%s,%s) AS tmp 
             where not exists (
                 select title from news where title = %s
             ) LIMIT 1;""",(
            item['title'],
            item['source'],
            item['link'],
            item['img_link'],
            item['date'],
            item['content'],
            item['tag'] ,
            item['title']
        ))
        
        # self.curr.execute("""insert into kompas values (%s,%s,%s,%s,%s)""",(
        #     item['title'],
        #     item['link'],
        #     item['time'],
        #     item['content'],
        #     item['tag'] 
        # ))

        self.conn.commit()
