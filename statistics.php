<!-- /**
 * @Author: Lich_Amnesia
 * @Date:   2016-04-11 20:22:39
 * @Last Modified by:   Alwa
 * @Last Modified time: 2016-04-11 22:50:42
 * @Thanks comzyh !
 */ -->
<?php
    ini_set('display_errors', 1);
    error_reporting(~0);
    class MyDB extends SQLite3
    {
      function __construct()
      {
         $this->open('statistics.db');
      }
    }
    function create_db($db)
    {
        $sql="CREATE TABLE IF NOT EXISTS [statistics] (
              [student_id] integer NOT NULL ON CONFLICT REPLACE PRIMARY KEY,
              [name] VARCHAR(50),
              [gender] VARCHAR(50),
              [college] CVARCHAR(50),
              [telephone] VARCHAR(50),
              [email] VARCHAR(50),
              [departure_city] VARCHAR(50),
              [arrival_city] VARCHAR(50),
              [register_time] DATETIME
              );";
        $ret = $db->exec($sql);
    }
    if (!empty($_SERVER['REQUEST_METHOD']) && $_SERVER['REQUEST_METHOD']=='POST')
    {
        $db = new MyDB();
        create_db($db);
        $student_id=$_POST['student_id'];
        $name=$_POST['name'];
        $gender=$_POST['gender'];
        $college=$_POST['college'];
        $telephone=$_POST['telephone'];
        $email=$_POST['email'];
        $departure_city=$_POST['departure_city'];
        $arrival_city=$_POST['arrival_city'];
        $register_time=date('Y-m-d H:i:s');

        if ($student_id == "" || $name == "" || $gender == "" || $college == "" || $telephone== "" || $email=="" || $departure_city=="" || $arrival_city=="")
                die ('Please fill in all required fields');

        $student_id=MyDB::escapeString($_POST['student_id']);
        $sql="INSERT OR REPLACE INTO statistics (student_id, name, gender, college, telephone, email, departure_city, arrival_city, register_time) VALUES ('$student_id', '$name', '$gender', '$college', '$telephone', '$email', '$departure_city', '$arrival_city', '$register_time')";
        $db->exec($sql);
    }
    else if (!empty($_GET['password']) && $_GET['password'] =='9078563412'){
        $db = new MyDB();
        $sql = "SELECT student_id, name, gender, college, telephone, email, departure_city, arrival_city, register_time FROM statistics order by register_time;";
        $ret = $db->query($sql);
        $ret_array = [];
        while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
        $ret_array[] = [$row['student_id'],$row['name'],$row['gender'],$row['college'],$row['telephone'],$row['email'],$row['departure_city'],$row['arrival_city'],$row['register_time']];
        }
        echo (json_encode($ret_array));
    }
    else
    {
?>
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cu Boulder 2016 新生统计</title>
    <link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css">
    <!-- <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon"> -->
    <style>
        #register
        {
            max-width: 400px;
        }
        body{padding-top: 50px}
        h1,h2,h3
        {
            font-family: "微软雅黑","黑体",sans-serif;
        }
        #sponsor
        {
            margin-top: 10px;
            margin-bottom: 10px;
        }
        @media (max-width: 540px) {
            h1 {font-size: 24px}
            h2 {font-size: 20px}
            #sponsor
            {
                margin-top: 30px;
                margin-bottom: 30px;
            }
            body{padding-top: 20px}
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="col-md-6">
            <h1 class="text-center">2016年Cu Boulder新生</h1>
            <!-- <h2 class="text-center">暨 2016 ACM/ICPC南京市邀请赛</h2> -->
            <div id="sponsor">
                <img class="center-block"  style="" height="40px" width="40px" src="//njoj.org/static/images/ICPC-Logo-Fishead.png"/>
            </div>
            <div>
                <p>请如实填写右方所有信息，如果有网络预选赛，则你填写的Judge账号将作为排名依据。
                </p>
                <p>如果你没有账号，请到<a href="//icpc.njust.edu.cn/Register/">这里</a> 注册一个</p>
                <p>报名成功后我们会给您的邮箱发送一封确认邮件，也会用邮件通知后续比赛事项，请务必准确。</p>
                <p>比赛报名截止日期： 2016 年 4 月 14 日 晚 24 时</p>
                <p>源代码可以访问<a href="">Github</a></p>
            </div>
        </div>

        <div class="col-md-6">
            <div class="center-block" id="register">
                <h3 class="text-center">报名信息</h3>
                <form class="center-block" id="form_register" method="post" action="" role="form" >
                    <div class="form-group">
                        <label>学号</label>
                        <input type="text" name="student_id" class="form-control" maxlength="35" value="107157804">
                    </div>
                    <div class="form-group">
                        <label>姓名</label>
                        <input type="text" name="name" class="form-control" maxlength="10" value="黄莘">
                    </div>
                    <div class="form-group">
                        <label>性别</label>
                        <input type="text" name="gender" class="form-control" maxlength="10" value="男">
                    </div>
                    <div class="form-group">
                        <label>院系</label>
                        <input type="text" name="college" class="form-control" maxlength="50" value="计算机学院">
                    </div>
                    <div class="form-group">
                        <label>手机号</label>
                        <input type="text" name="telephone" class="form-control" maxlength="15" value="18362962160">
                    </div>
                    <div class="form-group">
                        <label>电子邮箱(请务必准确)</label>
                        <input type="email" name="email" class="form-control" maxlength="50" value="chen3221@126.com">
                    </div>
                    <div class="form-group">
                        <label>出发城市</label>
                        <input type="text" name="departure_city" class="form-control" maxlength="18" value="南京">
                    </div>
                    <div class="form-group">
                        <label>到达城市</label>
                        <input type="text" name="arrival_city" class="form-control" maxlength="18" value="南京">
                    </div>
                    <button class="btn btn-primary center-block" type="submit">提交</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>

<?php
    }
?>
