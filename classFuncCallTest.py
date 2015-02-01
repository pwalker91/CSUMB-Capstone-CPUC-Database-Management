class A:
    def __init__(self):
        pass

    def sampleFunc(self, arg, **kwargs):
        print('you called sampleFunc({})'.format(arg))
        if len(kwargs) != 0:
            print("You passed in keyword arguments!!")
            for k,v in kwargs.items():
                print("key:"+str(k)+"  v:"+str(v))

m = A()
func = getattr(m, 'sampleFunc')("I have passed in many things", x=1, t=4, i_am_smart="SO MUCH PRINTING")
#func('sample arg')
#func("I have passed in many things", x=1, t=4, i_am_smart="SO MUCH PRINTING")
