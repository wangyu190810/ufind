web端短信验证码api
    方法
        POST
    接口地址
        线上地址为www.ufindoffer.com/api/send_sms
        测试地址为test.ufindoffer.com/api/send_sms
    input
    {
        "phone":"133234234234",
        "type":"1"
        //type 1表示注册接口，2表示忘记密码接口，3表示修改手机接口
    }
    output
    {
        "status":"success"
    }
    
mobile端短信验证：
    方法
        POST
    接口地址
        上线地址:www.ufindoffer.com/api/mobile/send_sms
        测试地址:test.ufindoffer.com/api/mobile/send_sms
    input
    {
        "phone":"133234234234",
        "type":"1"
    }
    output
    {
        "status":"success"
    }
    
