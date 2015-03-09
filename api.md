
接口1.1

    方式
        GET
    接口地址
        www.ufindoffer.com/api/index


接口1.2
    
    方式
        GET
    接口地址
        www.ufindoffer.com/api/get_state_university?stateid=53


接口1.3

    方式 

        GET

    接口地址 

        www.ufindoffer.com/api/get_university?universityid=1

接口2.1
    
    方式
        GET
    接口地址
        www.ufindoffer.com/api/search_university?searchname=MIT&stateid=1

接口2.2

    方式
        GET
    接口地址
        www.ufindoffer.com/api/search_major?searchname=EE&universityid=1

接口3.1
    
    方式
        GET
    
    接口地址
        www.ufindoffer.com/api/university_info?universityid=1
        
接口3.2
    
    方式
        GET
    
    接口地址
        www.ufindoffer.com/api/get_offer_student_id?universityid=1&majorid=1
    
接口3.3
    
    方式
        POST
    接口地址
        www.ufindoffer.com/api/get_user_in_university
        
        
        
接口3.4
    
    方式 
        GET
        
    接口地址
        www.ufindoffer.com/api/get_major_compare?universityid=1&majorid=1
        
接口3.5
    
    方式
        POST
        
    接口地址
        www.ufindoffer.com/api/get_compare_list
        
接口3.6
    
    方式
        GET
    接口地址
        www.ufindoffer.com/api/get_compare?compareid=10
    

接口3.7
    
    方式
        GET
       
    接口地址
        www.ufindoffer.com/api/student_info?studentid=3
        
接口3.8
    
    方式
        GET
        
 
     
接口3.9

    方式
        GET
    接口地址
        www.ufindoffer.com/api/get_user_detail_info?studentid=3
接口4.1

    方式
        POST
    接口地址
        www.ufindoffer.com/api/set_compare_support
        
    备注（这个接口服务端改变）
    {
        "compareinfoid":"1"
    }
     
接口4.2

    方式
        POST
    
    接口地址
        www.ufindoffer.com/api/set_compare
        
    return {"status":"success"}
    
接口4.3
  
    方式
        POST
        
    接口地址
        www.ufindoffer.com/api/set_user_score
  
接口4.4

    方式
        POST
    接口地址
        www.ufindoffer.com/api/set_offer
        
    
留言接口
    
    接口5.1 
    方法
        POST  json 
        
    接口地址
        www.ufindoffer.com/api/set_message
        input
        {
            "message_user_id":"1",
            "message":""
        
        }
        output
        {
            "status":"success"
        }
        
        
    接口5.2
    方法
        GET
    接口地址
       www.ufindoffer.com/api/get_message?user_id=1
       
       output
       {
       "message_list" :[
            {
                "message_user_id":"12",
                "mesaage_user_name":"xxxx",
                "message'
            }
        ]
        
        
        }
    接口 5.3 e
    删除留言
    方法：
        POST
    接口地址：
        www.ufindoffer.com/api/del_message_to_user
    input
    {
        "message_id":"12"
    }
    output
    {
        "status":"success"
    }
    
        
接口 5.1
   
    登录接口
    方法
        POST
    接口地址
        www.ufindoffer.com/api/login

             
接口 5.2
    
    短信验证码api
    方法
        POST
    接口地址
        www.ufindoffer.com/api/send_sms
    input
    {
        "phone":""
    
    }
    output
    {
        "status":"success"
    }
    
    注意保持第一次phonenum和第二次phonenum的数据一样，

    第一次
    方法
        POST
    接口地址
        www.ufindoffer.com/api/register_first
        
    input 
   
       {
        "email":"",
        "password":"",
        "phonenum":"",
        "checknum":""
        }
    output
    {
        "status":"success"
    }
    
    第二次
    方法
        POST
    接口地址
        www.ufindoffer.com/api/register_second
    
    input
        {
  
        "phonenum":"",
        "username":"",
        "universityid":"",
        "majorid":"",
        "gpa":""
        }
    output
    {
        "status":"success"
    }
    
接口 5.3

    修改密码api
    方法
        POST
    接口地址
        www.ufindoffer.com/api/change_password
     
接口 5.4 
    
    退出登录api
    方法
        GET
    接口地址
        www.ufindoffer.com/api/logout
    input
        www.ufindoffer.com/api/logout
        
接口 5.5 
    
    使用cookie登录
    方法
        GET
    接口地址
        www.ufindoffer.com/api/login_cookie
        
    input
        www.ufindoffer.com/api/login_cookie
        
        
接口 5.6 

    搜索国内大学帮助填写
    大学使用type为0，高中是1
    方法
        GET
    接口地址
        www.ufindoffer.com/api/search_university_china
       
    input
        www.ufindoffer.com/api/search_university_china?name=abc&type=1
    
    output
        [
        {"name":"abc",
        "id":"123"
        },
         {"name":"abcd",
        "id":"123"
        },
        "status":"success"
        ]
接口 5.7

    搜索国内的大学专业
    大学使用type为0，高中是1，高中返回结果为空
    方法
        GET
    接口地址
        www.ufindffer.com/api/search_major_china
       
    input
        www.ufindoffer.com/api/search_major_china?name=abc&type=0
        
    output
        [
        {"name":"abc",
        "id":"123"
        },
         {"name":"abcd",
        "id":"123"
        },
        "status":"success"
        ]

6.1 接口

    关注某人
    方法:
        POST
    接口地址：
        www.ufindoffer.com/api/set_follow_user
        
    input 
    {
        "follow_user_id":"12"
    }
    output
    {
        
        "status":"success"
    }
    
6.2 接口

    取消关注：
    方法:
        POST
        
    地址:
        www.ufindoffer.com/api/del_follow_user
        
    input:
    {
        "follow_user_id":"123"
    }
    
    {
        "status":"success"
    }

6.4 接口

    反馈信息：
    方法：
        POST
    地址:
        www.ufindoffer.com/api/send_advice
        
    input:
    {
        "content":"大家好"
    }
    成功
    output:
    {
        "status":"success"
    }
    没有登录返回
    output:
    {
        "status":"nologin"
    }
    
8.1 接口
    
    修改个人背景信息
    方法：
        POST
    接口地址：
        www.ufindoffer.com/api/update_user_bginf
        
    input:
    {
        "bginf":"哈哈好的"
    }
    {
    
        "status":"success"
    }
   
9.2 接口
    
    报offer
    方法：
        POST
    接口地址：
        www.ufindoffer.com/api/set_user_score
 
   
10.1 接口
  
    sublist 获得gre或sat的sub科目
    方法：
        GET
    接口地址：
        www.ufindoffer.com/api/get_sub?sub_type=1
        
    访问方式：
        www.ufindoffer.com/api/get_sub?sub_type=1
    output:
    {
        "status":"success",
        sublist:[
            {
                "name":"Literature",
                "id":1
            }
        ]
    }
    