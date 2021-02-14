from datetime import datetime


def fixLeadingZeros(dt):
    withOutYear = dt.strftime("%d-%m %H:%M:%S")
    year = dt.strftime("%Y").zfill(4)
    return f'{year}-{withOutYear}'

d = datetime.min

print(fixLeadingZeros(d))


d1 = datetime(1, 1, 1)

print(d1)


print(d1 == datetime.min)

