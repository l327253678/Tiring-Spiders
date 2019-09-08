# Tired-Spiders 反反爬解决方法Demo

## 写在前面

写爬虫的时候遇到对方站点的反爬是家常便饭，所以我打算开始将平时遇到的觉得有代表性的放上来，并简要的说一下解决思路。

我将反爬总的分为了三类：

- 频度反爬之代理IP

  [FreeProxyPool](https://github.com/IMWoolei/FreeProxyPool)：这个项目提供了几个站点的免费代理IP抓取程序，以及代理IP池调用接口

- Cookies反爬

  [Fuck-login](https://github.com/IMWoolei/fuck-login)：有些站点需要携带`Cookies`才能进行访问，有的甚至要求需要登陆之后才能正常访问。这个项目提供了部分站点的登陆脚本程序示例，会长期更新和维护

- 数据的加密、混淆、下毒等

  此类反爬也是我写当前这个项目的目标，这个项目的`demo`中我会记录一些站点的反爬解决方案，包括`js逆向`，`安卓逆向`、`绕过反爬`、`数据接口来源`等

----

## 请求时参数加密

- [x] [豆瓣APP](./douban/豆瓣.md)
- [x] [美拍APP](./meipai/美拍.md)
- [x] [触电新闻](./itouchtv/触电新闻.md)
- [x] [秒拍APP](./miaopai/秒拍.md)

-----

## 响应数据下毒或字体加密

- [ ] 起点中文网

-----

## 响应内容加密

- [x] [秒拍APP](./miaopai/秒拍.md)

