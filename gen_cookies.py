import json

cookie_str = "pgv_pvi=2387062784; RK=9LTsl4zZNe; ptcz=e24bf1a9643179c942db6211ef07a3a2e395265c28c9b9e2f14e518c848b7457; pgv_pvid=9569560952; ua_id=ESNKVTCQEhUD36fXAAAAAKsvRudoimVsm_dAhZ0eYSU=; mm_lang=zh_CN; tvfe_boss_uuid=db47890df6336cde; eas_sid=71V54797P877x7P4M9r6y0y6D3; noticeLoginFlag=1; pac_uid=0_5eb8e18369464; remember_acct=mygodness1234%40163.com; pgv_si=s2548947968; uuid=f5c5e113dbe4edf955d04f4a6d00d1f9; ticket=e97e466421d3b314f13ee69b3cc857d25c9776b9; ticket_id=gh_062806ff44ee; cert=fdGAMXh3Cjm_jAWbTenq_2O0cALlueGi; rand_info=CAESIK3u/1W0ps3yI1OPmsr7JJnHP/Bm2yr5XfM4frd/z0Ss; slave_bizuin=3527606955; data_bizuin=3552606250; bizuin=3527606955; data_ticket=WeoKKfbLbO/YOY1OuYcIvLZNiXvvO5+wD3DdSp0fmSGIK8Cpkv8/8tm7lO1OTPdu; slave_sid=anBzSVhWYUhvalMzM185V0tWd3JRVjJkWklvSnIxNXZyWnVoaFhYQlJBT1V1RDM5YnZ5Xzd3Q0FjcVdQMDZHRUZiNFNVM2R2RWJ4UEdEU0FCRFpSOGxUMU5IbmFrYkFqYmFqY1ZkTE1QNGh3NTU2d0YxWEx6a1FaWHdMaTJNWTF5ZWM3WGRRM2JpRmU4aXRV; slave_user=gh_062806ff44ee; xid=80586313c32f065f505563f42531527f; openid2ticket_oKnjA056JONr23HBimtuaia3_w94=0ZXap9/Ii6d6P/hcYbZiobm/mmc/SQaCL5PAc8Ya59U="

cookie = {}

for cookies in cookie_str.split(";"):
    cookie_item = cookies.split("=")
    cookie[cookie_item[0]] = cookie_item[1]

with open('cookie.txt', 'w') as file:
    file.write(json.dumps(cookie))
