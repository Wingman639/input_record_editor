import time
import os
import checksum

class InputRecord(object):
	def __init__(self, file_path=None):
		self.file_path = file_path
		if not self.file_path:
			self.file_path = self._generate_file_path()


	def __enter__(self):
		self.save_head()
		return self

	def __exit__(self, exception_type, exception_value, traceback):
		self.save_tail()
		self._append_checksum()

	def _generate_file_path(self):
		return os.path.join(
					os.path.dirname(os.path.abspath('__file__')),
					self._generate_file_name_with_timestamp())

	def _generate_file_name_with_timestamp(self):
		return 'record_' + str(time.time()) + '.data'

	def _append_save(self, text):
		with open(self.file_path, 'a') as f:
			f.write(text)

	def save_head(self):
		record_item = ['RECORD_START', time.time()]
		line = str(record_item)
		self._append_save(line)

	def save_tail(self):
		record_item = ['RECORD_END', time.time()]
		line = '\n' + str(record_item)
		self._append_save(line)

	def save_record(self, text):
		record_item = [text, time.time()]
		line = '\n' + str(record_item)
		self._append_save(line)

	def _read_file(self):
		with open(self.file_path, 'r') as f:
			return f.read()

	def _append_checksum(self):
		text = self._read_file()
		checksum = self._md5(text)
		self.save_record(checksum)

	def _md5(self, text):
		return checksum.md5(text)



if __name__ == '__main__':
	def test():
		with InputRecord() as record:
			print record._generate_file_path()

	test()