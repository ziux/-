# git 配置GitHub

### 设置用户名邮箱

* git config --global user.name "***"
* git config –-global user.email "*****"

## 生成ssh密码

* ssh-keygen -t rsa -C "***********@***.com" 替换为你自己的邮箱

找到id_rsa.pub 公钥文件,填入到GitHub的ssh key中
## 测试是否成功连接  
* ssh -T -p 443 git@ssh.github.com

## 注意
在使用时需要注意使用git ssh连接方式,https可能会出现timeout
