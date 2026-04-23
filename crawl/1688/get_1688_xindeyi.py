#获取1688商品详情页图片
import os
import re
from tkinter import image_names
import requests
from DrissionPage import ChromiumPage

browser = ChromiumPage()
base_path = os.getcwd()

# print(tab.title)


#详情页
def shop_detail():
    tab_detail=browser.latest_tab
    file_name = tab_detail.title
    file_name = os.path.join(base_path, file_name)
    print(file_name)
    #检查是否存在file_name文件夹
    if not os.path.exists(file_name):
        os.makedirs(file_name)
        print(file_name+'文件夹已创建')
    else:
        print(file_name+'文件夹已存在')
    #获取简介图片
    divs = tab_detail.ele(".od-scroller-list").eles("tag:div")
    print(len(divs))
    for div in divs:
        style = div.ele('tag:span').attr('style')
        print(style)
        pattern =r'url\("([^"]+)"'
        match = re.search(pattern, style)
        if match:
            img_url = match.group(1)
            img_url = img_url.replace("_b.jpg", "_.webp")
            print(img_url)
            #下载图片
            # 检查是否存在同名图片
            if os.path.exists(os.path.join(file_name, os.path.basename(img_url))):
                print('图片已存在，跳过下载')
            else:
                print(img_url+'不存在，开始下载')
                browser.download(img_url, file_name)
           
        else:
            print('未找到图片URL')


    #获取商品详情图片
    shadow_root=tab_detail.ele('.html-description').shadow_root
    print("======================================",shadow_root)
    imgs_list=shadow_root.eles('x://*[@id="detail"]/p[2]/span/strong/img')
    print(len(imgs_list))
    #在文件夹内创建工厂文件夹
    factory_dir=os.path.join(file_name,'factory')
    if not os.path.exists(factory_dir):
        os.makedirs(factory_dir)
        print(factory_dir+'文件夹已创建')
    else:
        print(factory_dir+'文件夹已存在')
    for index,img in enumerate(imgs_list):
        #跳过第1张图片
        if index==0:
            continue
        img_url = img.attr('src')
        print(img_url)
        img_name = os.path.basename(img_url)
        
        if index < len(imgs_list) - 3:
            #下载图片到商品文件夹
            if os.path.exists(os.path.join(file_name, img_name)):
                print('图片已存在，跳过下载')
            else:
                browser.download(img_url, file_name)
        else:
            #保存到工厂文件夹
            if os.path.exists(os.path.join(factory_dir, img_name)):
                print('图片已存在，跳过下载')
            else:
                browser.download(img_url, factory_dir)
       
            
            
        
    










    ############
    try:
        #获取视频
        lib_video=tab_detail.ele(".lib-video",timeout=3).ele("tag:video",timeout=3)
    except:
        lib_video=None
        print('未找到视频')
        return
    
    if lib_video:
        video_url = lib_video.attr('src')
        print(video_url)
        #下载视频
        # browser.download(video_url, file_name)
        # 下载视频
        video_tab=browser.new_tab(video_url)
        
        browser.download(video_tab.url, file_name)
        video_tab.close()
    else:
        print('未找到视频')

    #保存所有网页
   
    for i in range(5):
        tab_detail.scroll.to_bottom()
        tab_detail.wait(1)

    tab_detail.save(path=file_name)

    
    #关闭详情页
    tab_detail.close()
    
    
        


    
    
    

#主页列表


def shop_list():
    tab=browser.latest_tab
    divs=tab.eles('x://*[@id="bd_1_container_0"]/div/div[2]/div[6]/div')
    print(len(divs))
    for div in divs:
        print(div.text)
        div.click()
        tab.wait(1)
        shop_detail()
        tab.wait(2)
        
        # break


def mian():
    shop_list()

if __name__ == '__main__':
    mian()