from bible import chap, NR
from concurrent.futures import ThreadPoolExecutor
CH={'太':28,'可':16,'路':24,'约':21,'徒':28,'赛':66,'诗':150,'创':50,'出':40,'申':34,'撒下':24,'耶':52,'结':48,'但':12,'弥':7,'亚':14,'玛':4,'何':14,'罗':16,'林前':16,'林后':13,'加':6,'弗':6,'腓':4,'西':4,'来':13,'约壹':5,'启':22,'彼前':5,'提前':6,'利':27,'民':36,'珥':3}
jobs=[(NR[b],c) for b,n in CH.items() for c in range(1,n+1)]
def f(j):
    for i in range(4):
        try: chap(*j); return None
        except Exception as e: err=e
    return (j,str(err))
with ThreadPoolExecutor(8) as ex: r=[x for x in ex.map(f,jobs) if x]
print(len(jobs),'fail',r)
