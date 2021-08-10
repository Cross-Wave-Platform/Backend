from repo.shop_cart import SCManager
import time

manager = SCManager()
# manager.add_accout()

# for i in range(20000):
#     manager.add_problem(1,i)
#     manager.conn.commit()

s =time.time()
manager.update(1,[])
print(time.time()-s)
