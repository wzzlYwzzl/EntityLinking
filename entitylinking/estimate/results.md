# Baidu数据实体链接测试

## 测试结果

完成：100行, right:160, wrong:107
完成：200行, right:312, wrong:223
完成：300行, right:463, wrong:332
完成：400行, right:625, wrong:447
完成：500行, right:784, wrong:576
完成：600行, right:946, wrong:728
完成：700行, right:1099, wrong:847
完成：800行, right:1263, wrong:960
完成：900行, right:1411, wrong:1091
完成：1000行, right:1569, wrong:1238
完成：1100行, right:1707, wrong:1372
完成：1200行, right:1847, wrong:1511
完成：1300行, right:2010, wrong:1651
完成：1400行, right:2170, wrong:1786
完成：1500行, right:2338, wrong:1921
完成：1600行, right:2492, wrong:2051
完成：1700行, right:2632, wrong:2176
完成：1800行, right:2782, wrong:2299
完成：1900行, right:2956, wrong:2439
完成：2000行, right:3130, wrong:2552
完成：2100行, right:3294, wrong:2667
完成：2200行, right:3468, wrong:2807
完成：2300行, right:3614, wrong:2933
完成：2400行, right:3768, wrong:3045
完成：2500行, right:3908, wrong:3184
完成：2600行, right:4071, wrong:3313
完成：2700行, right:4232, wrong:3459
完成：2800行, right:4412, wrong:3569
完成：2900行, right:4589, wrong:3689
完成：3000行, right:4741, wrong:3824
完成：3100行, right:4915, wrong:3946
完成：3200行, right:5072, wrong:4061
完成：3300行, right:5242, wrong:4181
完成：3400行, right:5399, wrong:4317
完成：3500行, right:5557, wrong:4427
完成：3600行, right:5718, wrong:4571
完成：3700行, right:5867, wrong:4712
完成：3800行, right:6027, wrong:4837
完成：3900行, right:6216, wrong:4954
完成：4000行, right:6381, wrong:5083
完成：4100行, right:6556, wrong:5221
完成：4200行, right:6699, wrong:5337
完成：4300行, right:6872, wrong:5456
完成：4400行, right:7000, wrong:5583
完成：4500行, right:7161, wrong:5708
完成：4600行, right:7323, wrong:5834
完成：4700行, right:7468, wrong:5956
完成：4800行, right:7630, wrong:6081
完成：4900行, right:7776, wrong:6220
完成：5000行, right:7938, wrong:6343
完成：5100行, right:8083, wrong:6483
完成：5200行, right:8255, wrong:6607
完成：5300行, right:8414, wrong:6751
完成：5400行, right:8607, wrong:6881
完成：5500行, right:8766, wrong:7006
完成：5600行, right:8928, wrong:7149
完成：5700行, right:9104, wrong:7268
完成：5800行, right:9243, wrong:7413
完成：5900行, right:9410, wrong:7543
完成：6000行, right:9607, wrong:7681
完成：6100行, right:9760, wrong:7799
完成：6200行, right:9927, wrong:7930
完成：6300行, right:10067, wrong:8073
完成：6400行, right:10243, wrong:8191
完成：6500行, right:10414, wrong:8318
完成：6600行, right:10580, wrong:8448
完成：6700行, right:10735, wrong:8568
完成：6800行, right:10903, wrong:8691
完成：6900行, right:11071, wrong:8830
完成：7000行, right:11250, wrong:8955
完成：7100行, right:11406, wrong:9083
完成：7200行, right:11553, wrong:9199
完成：7300行, right:11705, wrong:9322
完成：7400行, right:11887, wrong:9455
完成：7500行, right:12039, wrong:9565
完成：7600行, right:12207, wrong:9688
完成：7700行, right:12391, wrong:9824
完成：7800行, right:12573, wrong:9934
完成：7900行, right:12728, wrong:10061
完成：8000行, right:12889, wrong:10189

准确率：55.8%

## 错误原因分析

1. 实体识别问题
因为代码中采用的mention识别逻辑是基于分词，所以如果文本中的词和KB中的subject不一致就会导致mention无法识别。

2. 无法使用模型基于链接分析的打分策略
因为百度提供的KB由于没有对SPO中的object进行ID化，导致一个问句中纵使出现了多个mention，也无法利用它们构建的子图进行分析。

3. 提供的KB没有问题中的上下文信息
目前采用的模型需要问句中的上下文必须在KB中有一定的反应，否则问句中的上下文就无法利用。甚至假设一个人只是利用百度的KB来判断问句中的mention是哪个实体也是困难的。

4. 一个问句中包含的mention多于给的测试答案
百度提供的KB包含了subject更为细粒度，一个很普通的词也会作为subject，比如“的”、“在”、“简介”等，这种同常不是实体的词，这进一步干扰了现在的模型。
