# MyProject
一个爬图片(妹子)的scrapy程序<br>
项目:爬取http://www.jj20.com/<br>
中的美女版块,实现的功能可以把每个写真集里面的图片放在同一个文件夹下,像素贼高的<br>
技术: 使用scrapy框架实现,难度:中等<br>

开始版块可以指定:  比如美女版块开始就是:   start_urls = ['http://www.jj20.com/bz/nxxz/list_7_1.html']<br>
                  风景的话:             start_urls = ['http://www.jj20.com/bz/zrfg/list_1_1.html']<br>
                  其他的可以自己去网址看。。。。<br>
                  下载的根目录可以再setting中指定    IMAGES_STORE = 'D:/image/'  这个是可以修改的<br>
抓取页面设置:<br>
    1.测试使用只抓取2页(用于测试)<br>
    2.无限向下获取,直到最后一页(用于爬取)<br>
两种下载设置:<br>
    1.使用原始的request下载<br>
    2.继承ImagesPipeline进行下载<br>

攻克难点:<br>
    1.一个网址只有一张图片的难度,要做到让爬虫一直向下爬。<br>
    2.网站里的图片设置了防盗链,通过改写hearder设置成功反反爬虫<br>
    3.将同一个版块里的图片放在同一个文件夹中<br>

问题1的解决网址 : 找不见了,但是下载的项目在本机当中    F:\Study\Project-One\05 -- 新工作日志\03 -- scrapy\爬虫<br>
问题2的解决网址 : 使用request这个老的模块的话直接写字典,ImagesPipeline的话设置在setting中<br>
                http://blog.javachen.com/2014/06/08/using-scrapy-to-cralw-zhihu.html?tdsourcetag=s_pctim_aiomsg<br>
                http://t.cn/RsrmfXw<br>
问题3的解决网址 : 将下载后的图片移动    https://www.jianshu.com/p/0ea820236e16<br>
