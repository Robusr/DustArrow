# 系统设计

## 箭体结构

DustArrow X 是直径 40.0 mm 的模块化探空火箭。机械源文件按设计阶段组织：

- `mechanical/source/draft/`：早期方案，包括影像舱和四通道鸭翼研究。
- `mechanical/source/launch_revision/`：发射前修改。
- `mechanical/source/formal/`：最终舱段与装配。
- `mechanical/source/reprint_models/`：为第二次打印修改的 8 个零件。

正式箭体包含十个功能段：

1. 头锥与降落伞舱
2. 测控舱
3. 数据舱
4. 电源舱
5. 粉尘传感器舱
6. 有害气体传感器舱
7. 烟雾传感器舱
8. 主控舱
9. 鸭翼舱
10. 推进与尾翼舱

打印输出包含 `mechanical/output/3dp/` 中的 28 个 STL，以及
`mechanical/output/reprint/` 中的 15 个补印 STL。头锥外形使用
`docs/references/von_karman_formula.txt` 记录的冯·卡门公式。

## 机械接口

- 模块沿箭体轴堆叠，通过金手指板对板连接器导通。
- 每个舱段内部使用柔性电路板把信号引到连接器。
- 降落伞舱由单个舵机驱动大角度舱盖；鸭翼舱使用双通道空气舵机构。
- 打印件面向 FDM 工艺设计。报告没有记录材料、填充率、层高或打印时间，
  本仓库不补造这些参数。

## 电子系统

归档包含 9 个模块 BOM、10 个 Gerber 包和 1 个旧版 EasyEDA 工程文件。板卡外形
由 Gerber 外形层测量。

| 模块 | 外形 | 关键器件 | 功能 |
|---|---|---|---|
| Command A | 30 × 40 mm | FPC 座、GNSS 座、2 个板对板座 | 指令与 GNSS 接口 |
| Command B | 未测量 | MPU6050、BMP280、MCU 座、FPC | 传感与控制 |
| Data | 32 × 101 mm | A39C-T400A22D1a LoRa、JST 电源 | 数传 |
| Power | 25 × 25.1 mm | IP5306、USB、电量灯 | 电源管理 |
| Exploration | 32 × 76 mm | 树莓派 Pico、开关、LED | 控制器/实验板 |
| DustSensor Up | 未测量 | GP2Y1014AU0F、ZH1.5 座 | 粉尘测量 |
| DustSensor Down | 25 × 25 mm | MQ-2、MQ-135 | 气体测量 |
| GasSensorHAT | 未测量 | MQ-135、金手指插头 | 气体传感器扩展板 |
| ServoHAT | 25 × 25.9 mm | 舵机排针、3 个 LED | 鸭翼/伞舱舵机 |
| COSensorHAT | 仅 Gerber | 归档无 BOM | 一氧化碳扩展板 |

合并后的 BOM 共 48 行、57 个元件。16 行没有价格；已知合计 31.44 元，是历史
价格下界，不是当前采购价。

## 地面站

归档程序是 PyQt5 原型：

```
串口（9600, 8-N-1）
        │
        ▼
正则解析  X...Y...GX...GY...GZ...
        │
        ├── data.txt（每帧覆盖）
        ├── 6 个 Matplotlib 画布（占位曲线 y = x²）
        └── OpenGL 立方体（归档代码中被注释）
```

计划中的六个曲线是高度、气压、温度、湿度、能见度和 PM1.0。六个命令按钮是
紧急开伞、反馈坐标、高空采样、姿态校准、数据刷新和系统自检。它们都没有
连接到发送链路。

## 数据流与协议

下行是 9600 波特率的自由文本流。建议替换为带一字节长度和
CRC-16/CCITT-FALSE 的二进制帧。新帧可以从任意串口分片中重组，并拒绝损坏的
载荷。参见 `media/photos/project/telemetry_frame.svg` 与
`scripts/verify_theory/test_protocol.py`。

## 电源与安全

电源舱使用 IP5306 移动电源控制器，支持 USB 充电和单节锂电输入。归档没有
电池型号、容量、放电测试或保护审查。推进段只是商用固体发动机的安装结构；
仓库不包含发动机规格、点火电路或发射流程。任何飞行工作都必须由具备资质的
人员监督，并遵守当地靶场安全规定。
