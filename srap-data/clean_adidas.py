import pickle
from pprint import pprint
import json


def uk_to_vietnam_size_men(uk_size):
    size_chart = {
        5.5: 39,
        6: 39.5,
        6.5: 40,
        7: 40.5,
        7.5: 41,
        8: 41.5,
        8.5: 42,
        9: 42.5,
        9.5: 43,
        10: 43.5,
        10.5: 44,
        11: 44.5,
        11.5: 45,
        12.5: 46,
        13.5: 47,
        14.5: 48
    }

    if uk_size not in size_chart:
        return 43.5
    return size_chart[uk_size]


def uk_to_vietnam_size_women(uk_size):
    size_chart = {
        2: 34.5,  
        2.5: 35,
        3: 35.5,  
        3.5: 36,
        4: 36.5,  
        4.5: 37,
        5: 37.5, 
        5.5: 38,
        6: 38.5,  
        6.5: 39,
        7: 39.5,  
        7.5: 40,
        8: 40.5, 
        8.5: 41,
        9: 41.5, 
        9.5: 42
    }
    if uk_size not in size_chart:
        return 38.25
    return size_chart[uk_size]


with open('adidas.pkl', 'rb') as f:
    data = pickle.load(f)

print(len(data))
# pprint(data[0])
for item in data:
    if 'variation_list' not in data:
        continue
    variations = json.loads(item['variation_list'])
    avg = 0
    for variation in variations:
        s = variation['size'].split()
        sz = float(s[0])

        if item['gender'] == 'M':
            sz = uk_to_vietnam_size_men(sz)
        elif item['gender'] == 'W':
            sz = uk_to_vietnam_size_women(sz)
        elif item['gender'] == 'U':
            sz = uk_to_vietnam_size_men(sz)

        avg += sz
    avg /= len(variations)
    item['size'] = avg

    usps = json.loads(item['usps'])
    lining = None
    sole = None
    for s in usps:
        if s.startswith('Lớp lót bằng'):
            lining = ''
            spl = s.split()
            for i in range(3, len(spl)):
                if spl[i][0].isupper():
                    break
                lining += spl[i] + ' '
        elif s.startswith('Đế'):
            if sole is None:
                sole = ''
                spl = s.split()
                idx = 2
                for i in range(len(spl)):
                    if spl[i] == 'bằng':
                        idx = i + 1
                        break

                for i in range(idx, len(spl)):
                    if spl[i][0].isupper():
                        break
                    sole += spl[i] + ' '

    item['lining'] = lining
    item['sole'] = sole

    item.pop('usps', None)
    item.pop('variation_list', None)
    item.pop('attribute_list', None)
    item['description'] = item['descriptio']

    item.pop('descriptio', None)
    # pprint(item)


with open('cleaned_adidas.pkl', 'wb') as f:
    pickle.dump(data, f)
