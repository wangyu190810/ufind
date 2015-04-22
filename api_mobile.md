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
        线上地址:www.ufindoffer.com/api/mobile/send_sms
        测试地址:test.ufindoffer.com/api/mobile/send_sms
        
    input
    {
        "phone":"133234234234",
        "type":"1"
        // type必须为1，为字符类型
    }
    
    output
    {
        "status":"success"
    }
    
mobile学校搜索接口调用:

    方法：
        GET
    接口地址
        线上地址:www.ufindoffer.com/api/mobile/search_university
        测试地址:test.ufindoffer.com/api/mobile/search_university
        
    实例：
        www.ufindoffer.com/api/mobile/search_university?searchname=MIT
        返回数据：
        {
         "namelist": [
                    {"chiname": "麻省理工学院",
                     "id": 6,
                      "logo": "http://www.ufindoffer.com/images/unimg/all_logo/Massachusetts Institute of Technology.png",
                      "name": "Massachusetts Institute of Technology"},
                      
                     {"chiname": "伦敦大学金史密斯学院",
                      "id": 298,
                      "logo": "http://www.ufindoffer.com/images/unimg/all_logo/Goldsmiths, University of London.png",
                      "name": "Goldsmiths, University of London"}],
         "stattus": "success"
         }
        
        

moblie专业接口调用:

    方法:
        GET
    接口地址
        线上地址:www.ufindoffer.com/api/mobile/search_major
        测试地址:test.ufindoffer.com/api/mobile/search_major
    实例:
        www.ufindoffer.com/api/mobile/search_major?searchname=EE&universityid=1
        
    返回数据：
        {"namelist": [
            {"chiname": null,
            "id": 121,
            "name": "MBA"},
            {"chiname": null,
            "id": 122,
            "name": "MBA in Accounting and Management"}],
        "status": "success"
        }


mobile用户填写信息一次发送：

    方法：
        POST
    接口地址:
        线上地址:www.ufindoffer.com/api/mobile/set_offer
        测试地址:test.ufindoffer.com/api/mobile/set_offer
    实例:
        POST参数:
            university_id:"12",//信息来自学校搜索接口的结果
            major_id:"234",//信息来自专业搜索接口的结果
            user_type:"0", //0表示高中，1表示大学
            grade:"Master",//Master/Phd选一个就行
            phone:"13512341234",//电话，
            check_num:"4321",//验证码
        返回值：
        三种情况:
        1.验证码错误
            {
                status:"check_num_error"
            }
        
        2.电话不存在，也就是没有发送验证码
            {
                status:"please_send_sms"
            }
        
        3.报offer成功，返回offer信息
            {
                "description": null,
                "offerlist": [
                {
                "twodim": "http://www.ufindoffer.com/images/unimg/twodim/Harvard_Master_PHD1.jpg",
                "universityid": 1,
                "universityname": "哈佛大学"
                }
                ],
                "status": "success"
            }

mobile用户抽奖：

    方法:
        POST
    接口地址:
        线上地址:www.ufindoffer.com/api/mobile/get_prize
        测试地址:test.ufindoffer.com/api/mobile/get_prize
    实例：
        POST参数：
        {
            phone:"13812341234"
        }
    返回信息抽奖成功:
        {
            status="success",
            acount=10
        }
    用户重复抽奖:
        {
            status="user_have_coupon"
        }
    

mobile用户分享:
    
    方法:
        POST
    接口地址:
        线上地址:www.ufindoffer.com/api/mobile/share_prize
        测试地址:test.ufindoffer.com/api/mobile/share_prize
    实例：
        POST参数：
        {
            phone:"13812341234"
        }
    返回信息:
        {
            status:"success",
        }

mobile用户信息回填
    
    方式:
        POST
    接口地址:
        线上地址:www.ufindoffer.com/api/mobile/user_info
        测试地址:test.ufindoffer.com/api/mobile/user_info
    返回数据:
    {
        "status":"success",
        "user_info":{
             user_type:"1",
             phone:"13812341234",
             grade:"Master"
            }
    
    }
    
        