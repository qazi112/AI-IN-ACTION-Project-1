lists = []
def printt(value):
    print("CAlled")
    if value == 1:
        return value
    lists.append(value)
    value = printt(value-1)
    print(lists.pop())
    
printt(5)
print(lists)