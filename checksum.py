
import hashlib

def md5(text):
	m = hashlib.md5()
	m.update(text)
	return m.hexdigest()


def check_checksum(file_path):
    text = read_file(file_path)
    lines = text.splitlines()
    last_line = lines[-1]
    to_check_text = '\n'.join(lines[0:-1])
    # print to_check_text
    my_md5 = md5(to_check_text)
    record = eval(last_line)
    md5_in_file = record[0]
    if my_md5 != md5_in_file:
    	print md5_in_file, my_md5
        return ('\n' + 'CHECKSUM FAILED!!! Data file might be updated after editor close.')

    else:
        return ('\n' + 'CHECKSUM OK.')

def read_file(file_path):
	with open(file_path, 'r') as f:
		return f.read()


if __name__ == '__main__':
	def test():
		with open('test.data', 'r') as f:
			print md5(f.read())

		print check_checksum('test_2.data')
	test()