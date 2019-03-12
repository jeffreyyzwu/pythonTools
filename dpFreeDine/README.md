# dianping霸王餐自动报名

## 实现功能
1. 霸王餐自动报名
2. 霸王餐自动签到
3. 丽人频道免费试用自动报名
4. 登录失效时，自动模拟登录获取最新token并保存到用户配置中

## 安装
1. git拉取代码
2. 将conf/users-template.json文件重命名为users.json
3. users.json中填写phone，token
4. 修改start.sh中的路径
5. crontab增加定时任务调用start.sh

## users.json配置
1. excludetitle用于排除霸王餐标题中包含所有字符的套餐，每个子数组为一组排除规则
2. pc端浏览器登录，从cookies中获取dper的值即是token
   
## 尚未解决问题

### 模拟登录
1. dplogin.py使用chromediver模拟登录
2. dpaccount.py使用api模拟登录
   
以上两种方法代码均可正常运行。但由于dianping的安全策略，用户密码的登录方式均被认为不安全，导致两种方法实际上均无法成功登录并自动获取token
   



