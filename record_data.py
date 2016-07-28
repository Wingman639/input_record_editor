import time
import os

class InputRecord(object):
	def __init__(self, file_path=None):
		self.file_path = file_path
		if not self.file_path:
			self.file_path = self._generate_file_path()


	def __enter__(self):
		self.save_record('RECORD_START')
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.save_record('RECORD_END')
		pass

	def _generate_file_path(self):
		return os.path.join(
					os.path.dirname(os.path.abspath('__file__')),
					self._generate_file_name_with_timestamp())

	def _generate_file_name_with_timestamp(self):
		return 'record_' + str(time.time()) + '.data'

	def _append_save(self, text):
		with open(self.file_path, 'a', ) as f:
			f.write(text)

	def save_record(self, text):
		record_item = [text, time.time()]
		line = str(record_item) + '\n'
		self._append_save(line)

if __name__ == '__main__':
	def test():
		with InputRecord() as record:
			print record._generate_file_path()

	test()