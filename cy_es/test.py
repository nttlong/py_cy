import datetime

import cy_es_x
from elasticsearch import Elasticsearch
from cy_xdoc.models.files import DocUploadRegister
client = Elasticsearch(hosts=["192.168.18.36:9200"])
index ="lv-codx_long-test-123"
class A:
    def __contains__(self, item):
        print(item)
        return {"A":1}
fx= [1,2,3] in A()
filter=(cy_es_x.docs.mark_delete==False) & ((cy_es_x.docs.privileges.users.contains('hthan','tqcuong'))|(cy_es_x.docs.privileges.group.contains('nhom_a')))





fx = cy_es_x.create_filter_from_dict({
    "$and": [
        {"mark_delete": False},
        {"$or": [
            {
                "$not":{
                "privileges.users": {
                    "$contains": ['hthan', 'tqcuong']
                }}
            },
            {
                "privileges.group": ['nhom_a', 'nhom_b']
            }
        ]}
    ]
})
# filter = cy_es_x.docs.privileges.users==['nttdung','hthan']

print(fx)
ret= cy_es_x.search(
    client=client,
    index=index,
    filter=fx,
    limit=10
)
hits = ret.hits
total = hits.total
for x in ret.items:
    print(x.id)
print(ret)



#
#
#     print(cls)

# fx = get_map(DocUploadRegister)





