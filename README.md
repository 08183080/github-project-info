# 项目介绍
简单明了的github项目分析器

# 项目日志
- [x] 12/7，项目在服务器部署本机可以运行，但是nginx反向代理确实失败，今天不搞了明天吧。。。
- [x] 12/8，项目已经部署上限，学会了nginx反向代理以及阿里云安全组问题排查

# 项目体验
网址：

```http://101.132.60.166/```


# 命令
## 开启web服务器

监听来自网络所有流量的请求\
```gunicorn -w 2 -b 0.0.0.0:5000 web:app```


将项目变成后台运行\
```nohup gunicorn -w 2 -b 0.0.0.0:5000 web:app > gunicorn.log 2>&1 &```


查看端口\
```lsof -i:5000```


## 检查nginx反向代理器状态
```sudo systemctl status nginx```

```sudo systemctl restart nginx```

配置 proxy_pass 设置反向代理

```vim /etc/nginx/nginx.conf/```