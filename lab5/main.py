from city import City

if __name__ == '__main__':
    city = City()
    assert city.parse('test.txt')
    assert city.print_result()
