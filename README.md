# bilibili-barrage-analysis
bilibili弹幕分析，包含爬虫、词云分析、词频分析、情感分析、构建衍生指标，可视化
   
   
****

**信息爬取**   
&nbsp;&nbsp;1.1 爬取bilibili某一个分区（可通过url定义）特定日期下按照视频热度降序排序的视频信息，包含：href、视频时长、名称、BV号、播放量、弹幕数、up主、up主id   
&nbsp;&nbsp;1.2 通过BV号获取视频评论Cid，解析xml网页，简单获取各个视频的弹幕内容（注意：条数有限制，xml的弹幕条数不超过1000条）   
&nbsp;&nbsp;1.3 通过up主id，获取up主在爬取时的粉丝数，此粉丝数可以精确到个位数   
&nbsp;&nbsp;1.4 通过BV好获取视频评论Cid，获取详细的弹幕内容，包括：
   	
**数据分析--词云**   
&nbsp;&nbsp;2.1 全区弹幕词云分析，可以通过自己编写剔除单字、去除停用词、调整分词模型进行优化   
&nbsp;&nbsp;2.2 分频道弹幕词云分析   
    
**数据分析--弹幕条数**   
&nbsp;&nbsp;3.1 分析全区弹幕前十视频，使用pyecharts柱状图进行可视化   
&nbsp;&nbsp;3.2 分析各频道平均/最高视频弹幕数   
	
**数据分析--指标构建**   
&nbsp;&nbsp;构建指标：互动指数：弹幕数 / 播放量 * 100   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;粉丝响应指数：up主粉丝数 / 播放量  
&nbsp;&nbsp;4.1 全区互动指数最高前十视频   
&nbsp;&nbsp;4.2 各频道最高/平均互动指数   
&nbsp;&nbsp;4.3 全区粉丝响应指数最高前十视频   
&nbsp;&nbsp;4.4 各频道最高/平均粉丝响应指数   
