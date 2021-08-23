import base64

with open('/home/lil0w1/KIT/kit-be/KIT3月齡組第1波3月齡親友_final.sav','rb') as f:
    s = f.read()
    with open('out2.txt','w') as out:
        out.write(base64.b64encode(s).decode("ascii"))
        
    with open('out2.txt','r') as testing:
        a = testing.read().encode("ascii")
        # a = a[:-1] + a[(-1+1):]

        print(base64.b64encode(base64.b64decode(a)) == a)
