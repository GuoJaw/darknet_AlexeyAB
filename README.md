

##  darknet_AlexeyAB详述


https://github.com/AlexeyAB/darknet


## Introduce： 此处引用原作者代码主要用于下面几种功能：
     （1）添加了中文标签
     （2）批量测试图像并保存
     （3）测试mAP需要用到，faster-rcnn中的脚本

## 添加中文标签
     make_label.py
           .tty

## 测试图像和视频
      [1- 测试video]
           ./darknet detector demo kitti/kitti.data kitti/yolov3_kitti.cfg  kitti/yolov3_kitti_final.weights kitti/test.avi -thresh 0.5

      [2- 测试单张images]
           ./darknet detect kitti/yolov3_kitti.cfg  kitti/yolov3_kitti_final.weights data/00001.jpg  -thresh 0.5

      [3- 批量测试图像 ，并保存]    
          （1）命令
          . / darknet detector  test  kitti/kitti.data kitti/yolov3_kitti.cfg  kitti/yolov3_kitti_final.weights
          （2）pic.txt保存着待测试图像的绝对路径
          /home/gjw/darknet/kitti/Mydata/pic.txt
         
## 训练自己的数据集（以KITTI数据集为例）
	【一】 制作KITTI格式数据集，将目录放在~/data/目录下，目录结构，见下：
	KITTIdevkit
	KITTI
	    Annotations  #标注的XML文件
	    ImageSets  #train.txt  test.txt  val.txt  trainval.txt
		 Main
	    JPEGImages  #图像文件jpg或png

	执行软连接： 
		cd  darknet-pjreddie/kitti
		ln  -s  ~/data/KITTIdevkit  .   #将数据集软连接到darknet-pjreddie/kitti目录下

	【二】
	（1）用matlab在KITTI/ImageSets/Main生成四个文件train.txt   trainval.txt   val.txt   test.txt 
	（2）用上面生成的四个文件，执行脚本：
		gjw@gjw:~/darknet_AlexeyAB-master/kitti$ python2  kitti_label.py 
	执行结果：
		[1]在./KITTIdevkit/KITTI目录下，产生YOLO训练需要labels下的txt
			（txt内容：每张jpg/png图像中的类别和坐标信息） 
		[2]在kitti/下应该也生成了train.txt,test.txt,val.txt这3个文件
			（3个.txt文件：里面包含了所有训练,测试样本的绝对路径）

	【三】TestFile/目录下，配置文件的修改

		（1）kitti.names： 标签名字文件，修改见下
			car
			pedestrian
			cyclist

		（2）kitti.data： 
			classes= 3

			train  = /home/gjw/darknet_AlexeyAB/kitti/train.txt  ##【二】（2）-[2]生成的train.txt目录
			valid  = /home/gjw/darknet_AlexeyAB/kitti/test.txt   ##【二】（2）-[2]生成的test.txt目录

			names = /home/gjw/darknet_AlexeyAB/kitti/TestFile/kitti.names  ##【三】（1）kitti.names

			backup = /home/gjw/darknet_AlexeyAB/kitti/backup    ##存放训练生成的.weight权重文件的目录	
			results = /home/gjw/darknet_AlexeyAB/kitti/kitti_result

		【注意】必须新建./kitti/backup和./kitti/kitti_result目录

		（3）yolov3-kitti.cfg网络配置文件
		    [1]一共需要修改三处
				[convolutional]
				size=1
				stride=1
				pad=1
				filters=24  #### 计算公式 = 3 * （类别数 + 5）
				activation=linear

				[yolo]
				mask = 0,1,2
				anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
				classes=3   ####类别数，本例为2类  
				num=9
				jitter=.3
				ignore_thresh = .5
				truth_thresh = 1
				random=0    ###1
		    [2]相关其他参数
			    learning_rate  学习率0.0001
			    max_batches  最大迭代次数  40000

	【六】训练命令
		cd ~/darknet_AlexeyAB
		./darknet detector train kitti/TestFile/kitti.data  kitti/TestFile/yolov3_kitti.cfg darknet53.conv.74 
	说明：
		darknet53.conv.74 是加载的预训练模型，在官网上可以下载

=========================================

## 1. 测试
	（1）视频
	./darknet detector demo  kitti/TestFile/kitti.data  kitti/TestFile/yolov3_kitti.cfg  kitti/TestFile/yolov3_kitti_final.weights  kitti/TestFile/test.avi  -thresh 0.3 


	（2）批量测试图像 ----> 只能原版代码，即： darknet-pjreddie
		（1）命令
		./darknet detector  test  kitti/TestFile/kitti.data  kitti/TestFile/yolov3_kitti.cfg  kitti/TestFile/yolov3_kitti_final.weights
		（2）请输入：保存着待测试图像的绝对路径test.txt
			/home/gjw/darknet_AlexeyAB/kitti/test.txt

=========================================

## 2. 测试mAP
	1、valid生成检测结果文件
	（1）cfg/voc.data最后添加一行：results = /home/gjw/darknet_AlexeyAB/scripts/results   ####保存下面命令输出的结果，新建results目录
	（2）执行命令
	./darknet detector valid cfg/voc.data  cfg/yolov3-voc.cfg backup/yolov3-voc_final.weights  -thresh 0.5
	结果：将生成的类别的结果文件:/home/gjw/darknet_AlexeyAB/scripts/results

	2、在/home/gjw/darknet_AlexeyAB/scripts目录下，新建output，执行：
	 python2 reval_voc.py --voc_dir ./VOCdevkit --year 2007 --image_set test --classes voc.names output  




