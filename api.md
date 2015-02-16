
接口1.1

    方式
        GET
    接口地址
        www.ufind.top/api/index


接口1.2
    
    方式
        GET
    接口地址
        www.ufind.top/api/get_state_university?stateid=53


接口1.3

    方式 

        GET

    接口地址 

        www.ufind.top/api/get_university?universityid=1

接口2.1
    
    方式
        GET
    接口地址
        www.ufind.top/api/search_university?searchname=MIT&stateid=1

接口2.2

    方式
        GET
    接口地址
        www.ufind.top/api/search_major?searchname=EE&universityid=1

接口3.1
    
    方式
        GET
    
    接口地址
        www.ufind.top/api/university_info?universityid=1
        
接口3.2
    
    方式
        GET
    
    接口地址
        www.ufind.top/api/get_offer_student_id?universityid=1&majorid=1
    
接口3.3
    
    方式
        POST
    接口地址
        www.ufind.top/api/get_user_in_university
        
        
        
接口3.4
    
    方式 
        GET
        
    接口地址
        www.ufind.top/api/get_major_compare?universityid=1&majorid=1
        
接口3.5
    
    方式
        POST
        
    接口地址
        www.ufind.top/api/get_compare_list
        
接口3.6
    
    方式
        GET
    接口地址
        www.ufind.top/api/get_compare?compareid=10
    

接口3.7
    
    方式
        GET
       
    接口地址
        www.ufind.top/api/student_info?studentid=3
        
接口3.8
    
    方式
        GET
        
 
     
接口3.9

    方式
        POST
    接口地址
        www.ufind.top/api/get_user_detail_info?studentid=3
接口4.1

    方式
        POST
    接口地址
        www.ufind.top/api/set_compare_support
        
    备注（这个接口服务端改变）
    {
        "compareinfoid":"1"
    }
     
接口4.2

    方式
        POST
    
    接口地址
        www.ufind.top/api/set_compare
        
    return {"status":"success"}
    
接口4.3
  
    方式
        POST
        
    接口地址
        www.ufind.top/api/set_user_score
  
接口4.4

    方式
        POST
    接口地址
        www.ufind.top/api/set_offer
        
    
留言接口
    
    接口5.1 
    方法
        POST  json 
        
    接口地址
        www.ufind.top/api/set_message
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
       www.ufind.top/api/get_message?user_id=1
       
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
        
