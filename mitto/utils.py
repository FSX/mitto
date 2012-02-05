# http://stackoverflow.com/a/1695250/235491
def enum(**enums):
    return type('Enum', (), enums)
