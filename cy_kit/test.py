import cy_kit_x
@cy_kit_x.thread_makeup()
def test(a,b):
    return  a+b
test(1,2).start()