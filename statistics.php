<!-- /**
 * @Author: Lich_Amnesia
 * @Date:   2016-04-11 20:22:39
 * @Last Modified by:   Alwa
 * @Last Modified time: 2016-04-11 23:58:19
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
              [degree] VARCHAR(50),
              [college] CVARCHAR(50),
              [telephone] VARCHAR(50),
              [email] VARCHAR(50),
              [qq] VARCHAR(50),
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
        $degree=$_POST['degree'];
        $college=$_POST['college'];
        $telephone=$_POST['telephone'];
        $email=$_POST['email'];
        $qq=$_POST['qq'];
        $departure_city=$_POST['departure_city'];
        $arrival_city=$_POST['arrival_city'];
        $register_time=date('Y-m-d H:i:s');

        if ($student_id == "" || $name == "" || $gender == "" || $college == "" || $email=="" || $departure_city=="" || $arrival_city=="" || $degree == "" || $qq == "")
                die ('Please fill in all required fields');

        $student_id=MyDB::escapeString($_POST['student_id']);
        $sql="INSERT OR REPLACE INTO statistics (student_id, name, gender, degree, college, telephone, email, qq, departure_city, arrival_city, register_time) VALUES ('$student_id', '$name', '$gender', '$degree', '$college', '$telephone', '$email', '$qq','$departure_city', '$arrival_city', '$register_time')";
        $db->exec($sql);
    }
    else if (!empty($_GET['password']) && $_GET['password'] =='9078563412'){
        $db = new MyDB();
        $sql = "SELECT student_id, name, gender, degree, college, telephone, email, qq, departure_city, arrival_city, register_time FROM statistics order by register_time;";
        $ret = $db->query($sql);
        $ret_array = [];
        while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
        $ret_array[] = [$row['student_id'],$row['name'],$row['gender'],$row['degree'],$row['college'],$row['telephone'],$row['email'],$row['qq'],$row['departure_city'],$row['arrival_city'],$row['register_time']];
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
            position: relative;
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
            <h1 class="text-center">2016年Cu Boulder新生统计</h1>
            <div id="sponsor">
                <iframe class="center-block" frameborder="no" border="0" marginwidth="0" marginheight="0" width=298 height=52 src="http://music.163.com/outchain/player?type=2&id=16334771&auto=0&height=32"></iframe>
            </div>

            <div>
                <p>本统计为了方便大家能够找到飞友，学友和舍友。
                </p>
                <p>请如实填写右方所有信息，统计完成后会公开你的姓名、性别、学位、起飞城市和目的城市和QQ。</p>
                <p>如有遗漏信息敬请谅解。</p>
                <p>统计截止日期： 2016 年 4 月 25 日 晚 24 时</p>
                <p>如有问题请联系QQ:459577895</p>
                <p>源代码可以访问<a href="https://github.com/LichAmnesia/BoulderNews">Github</a></p>
            </div>
        </div>

        <div class="col-md-6">
            <div class="center-block" id="register">
                <h3 class="text-center">统计信息</h3>
                <form class="center-block" id="form_register" method="post" action="" role="form" >
                    <div class="form-group">
                        <label>学号(Student ID,9位数字)</label>
                        <input type="text" name="student_id" class="form-control" maxlength="35">
                    </div>
                    <div class="form-group">
                        <label>姓名</label>
                        <input type="text" name="name" class="form-control" maxlength="10">
                    </div>
                    <div class="form-group">
                        <label>性别</label>
                        <select type="text" name="gender" class="selectpicker form-control" maxlength="50">
                            <option value=""></option>
                            <option value="男">男</option>
                            <option value="女">女</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>学位(请务必准确)</label>
                        <select type="text" name="degree" class="selectpicker form-control" maxlength="50">
                            <option value=""></option>
                            <option value="本科">本科</option>
                            <option value="研究生">研究生</option>                            
                            <option value="博士">博士</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>院系专业</label>
                        <select type="text" name="college" class="selectpicker form-control" maxlength="50">
                            <option value=""></option>
                            <option value="物理">物理</option>
                            <option value="计算机">计算机</option>
                            <option value="材料">材料</option>
                            <option value="生物">生物</option>
                            <option value="化学">化学</option>
                            <option value="环境地理">环境地理</option>
                            <option value="航天工程">航天工程</option>
                            <option value="金融">金融</option>
                            <option value="文理学院">文理学院</option>
                            <option value="工程学院">工程学院</option>
                            <option value="其他">其他</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>手机号(加上地区码，非必填)</label>
                        <input type="text" name="telephone" class="form-control" maxlength="15">
                    </div>
                    <div class="form-group">
                        <label>电子邮箱</label>
                        <input type="email" name="email" class="form-control" maxlength="50">
                    </div>
                    <div class="form-group">
                        <label>QQ(请务必准确)</label>
                        <input type="text" name="qq" class="form-control" maxlength="50">
                    </div>
                    <div class="form-group">
                        <label>出发城市(比如:南京;上海;西雅图,请用英文分号隔开)</label>
                        <input type="text" name="departure_city" class="form-control" maxlength="18">
                    </div>
                    <div class="form-group">
                        <label>到达城市(比如:丹佛)</label>
                        <input type="text" name="arrival_city" class="form-control" maxlength="18">
                    </div>
                    <button class="btn btn-primary center-block" type="submit" onclick="alert('确认提交？')">提交</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>

<?php
    }
?>
