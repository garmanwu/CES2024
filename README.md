# CES 2024 Industry Mapping

CES 2024行业资讯爬虫

包括：

-4300家参展商信息及产品亮点

-47行业动态

-5%幻觉


操作步骤

第一步：建立爬虫公司列表，如Query_list.xlsx。

第二步：crawler.py，使用Tavily爬虫，数据保存在Crawler目录。

第三步：summariz.py，使用ChatGPT 3.5归纳总结，数据保存在Summary目录。

第四部：check.py，使用Azure Bing Search + ChatGPT 4修复幻觉。

第五步：translation.py，使用ChatGPT 3.5翻译Summary目录下Json文件。

第六步：output_en.py，合并输出CES_2024_Industry_Mapping.xlsx。

第七步：output_cn.py，合并输出CES2024行业图谱.xlsx。


详细说明

https://m8wevyydob.feishu.cn/docx/VhCwdQSc6oEPF6x8wVzc7EuMnJf?from=from_copylink


若查看结果，下载CES_2024_Industry_Mapping.xlsx或CES2024行业图谱.xlsx即可。

若想做二次分析，可整个目录下载。若有疑问，可微信联系：26513486。


