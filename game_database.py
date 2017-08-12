from functools import partial
from sqlite3 import connect
from collections import OrderedDict

import os


class DataBase:
	tables = {}

	@classmethod
	def init_cfg(cls):
		cls.get_table_cfg = partial(cls.get_table_cfg, cls.table_name)
		cls.insert = partial(cls.insert, cls.table_name)
		cls.select = partial(cls.select, cls.table_name)
		return cls.get_table_cfg()

	@staticmethod
	def init():
		DataBase.tables = {}
		for file in os.scandir('db'):
			if not file.name == 'game.db':
				table_name = file.name.split('.')[0]
				DataBase.tables[table_name] = DataBase.get_table_cfg(table_name, with_type=True)
		for table_name, columns_type in DataBase.tables.items():
			DataBase.create(table_name, *columns_type)

	@staticmethod
	def get_table_cfg(table_name, with_type=False):
		def read_cfg(table_name, with_type):
			with open(f'db/{table_name}.cfg') as f:
				for line in f.read().splitlines():
					if with_type:
						for column_type in line.split(':'):
							yield column_type
					else:
						yield line.split(':')[0]

		return list(read_cfg(table_name, with_type))

	@staticmethod
	def create(table_name, *column_type):
		with connect('db/game.db') as d:
			columns = []
			for i in range(len(column_type)):
				if not i % 2 or i == 0:
					columns.append(column_type[i])

			d.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({",".join(columns)})')

	@staticmethod
	def insert(table_name, *rows):
		with connect('db/game.db') as d:
			for row in rows:
				values = []
				for key, value in row.items():
					if 'STRING' == DataBase.get_type(table_name, key):
						values.append(f'"{value}"')
					else:
						values.append(str(value))

				values = ','.join(values)
				print(f'INSERT INTO {table_name} VALUES {values}')
				d.execute(f'INSERT INTO {table_name} VALUES ({values})')

	@staticmethod
	def select(table_name, *players):
		if not players:
			players = tuple('1')
		with connect('db/game.db') as d:
			values = ','.join(players)
			print(f'SELECT * from {table_name} WHERE {values}')
			return d.execute(f'SELECT * from {table_name} WHERE {values}')

	@staticmethod
	def get_placeholders(rows_len, ph='?'):
		return f'{",".join(ph for _ in range(rows_len))}'

	@classmethod
	def get_type(cls, table_name, column):
		ret = False
		for column_type in DataBase.tables[table_name]:
			if ret:
				return column_type
			if column_type == column:
				ret = True  # return item in next loop


class PlayerTable(DataBase):
	table_name = 'player'

	@classmethod
	def __init__(cls):
		cls.cfg = cls.init_cfg()

	def add_players(self, *mkwargs):
		players = []
		for kwargs in mkwargs:
			player = OrderedDict()
			for allowed_column in self.cfg:
				player[allowed_column] = kwargs.get(allowed_column, '')
			players.append(player)

		self.insert(*players)

	def get_players(self):
		return list(self.select())


DataBase.init()
p = PlayerTable()
p.get_table_cfg()
p.add_players({'username': 'test',
			   'password': 'test',
			   'join_time': 0,
			   'avatar_src': 'www.google.de',
			   'clicks': 0
			   })
print(*p.get_players(), sep='\n')
