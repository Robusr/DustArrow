<p align="center">
  <img src="./media/photos/project/banner.png" alt="DustArrow X 整机渲染图" width="800"/>
</p>

<h1 align="center">DustArrow X · 沙尘利“箭”</h1>

<p align="center">
  <strong>面向 40 mm 气象探空火箭的模块化遥测系统</strong>
  <br>
  RP2040 传感栈、LoRa 下行链路与 PyQt5 地面站原型
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="许可证：MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/PyQt5-%E5%9C%B0%E9%9D%A2%E7%AB%99-41CD52?logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/SolidWorks-CAD-e63946" alt="SolidWorks">
  <img src="https://img.shields.io/badge/%E7%8A%B6%E6%80%81-%E5%8E%9F%E5%9E%8B-f59e0b" alt="状态：原型">
  <br>
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">中文</a> |
  <a href="./README.fr.md">Français</a>
</p>

---

## 名称来源

中文名“沙尘利箭”由“沙尘”和“利箭”组成：“沙尘”指项目面向的沙尘天气，“利箭”
既指探空火箭，也含“有利于治理”的意思。英文名 **DustArrow** 是中文名的直译。
模块化结构参考了中国空间站实验柜的设计思路。第三代在名称后加上 **X**；在 2024 年
1 月的电视专题片中，作者说 X 意味着“无限的可能”。

## 项目简介

DustArrow X 是宁夏固原市第一中学学生项目“沙尘利‘箭’”的第三代硬件，前两代
分别为 Theta 和 Beta。项目参加全国青少年科技创新大赛，目标是利用低成本
探空火箭获取沙尘天气下垂直方向的气象数据。

箭体直径 40 mm，由 10 个功能段组成。模块之间使用金手指板对板连接，模块内部
使用 FPC 排线，取消了舱段之间的独立导线。箭载电子以 RP2040 为核心，配合
MPU6050、BMP280、ATGM336H、A39C LoRa、GP2Y1014AU0F 和 MQ 系列气体传感器；
地面端是 Python/PyQt5 遥测界面。2024 年 1 月，项目登上上海广播电视台
《少年爱迪生》第八季《明日世界》。

本仓库包含机械 CAD、Gerber、BOM、地面站源码、原始报告、答辩材料和演示媒体。
**不包含**箭载固件、飞行日志、传感器标定或外场距离测试。地面站归档版本是
界面原型：曲线为占位数据，命令按钮未连接。详见[勘误](docs/errata.md)。

## 主要特性

- **40 mm 模块化箭体**：10 个功能段，金手指与 FPC 连接，打印件可单独替换。
- **RP2040 传感栈**：六轴 IMU、气压计、GNSS 与多路气体/粉尘传感器。
- **LoRa 下行链路**：A39C-T400A22D1a 串口数传，地面端以 9600 波特率接收。
- **PyQt5 地面站原型**：六路曲线、3D 姿态立方体与六个命令按钮的界面框架。
- **开放的制造文件**：SolidWorks 源文件、STL、STEP、Gerber、BOM 和丝印图。
- **可追溯的验证**：16 项理论勘误与 32 项纯 Python 测试，失败项不隐藏。

## 系统架构

<p align="center">
  <img src="./media/photos/project/system_architecture.svg" alt="DustArrow X 系统架构图" width="900"/>
  <br>
  <em>系统架构。虚线为无线链路；地面站命令链路在归档代码中尚未实现。</em>
</p>

- **机械**：头锥与伞舱、测控舱、数据舱、电源舱、三个传感器舱、主控舱、
  鸭翼舱、推进尾翼舱。伞舱由单舵机驱动大角度舱盖，鸭翼舱为双通道空气舵。
- **电子**：9 个模块 BOM、10 个 Gerber 包。主控与测传板围绕 RP2040、
  MPU6050、BMP280、ATGM336H 和 A39C 构建。
- **下行**：9600 波特率、8-N-1 的自由文本流。归档正则无帧头、长度和校验；
  建议改用带 CRC-16 的二进制帧。
- **地面站**：PyQt5 + Matplotlib + OpenGL。归档版本中六张图为占位曲线，
  OpenGL 组件被注释，按钮未连接发送链路。

## 理论与设计

静态条件下，加速度计测量重力反作用。按本仓库约定，\(x\) 向前、\(y\) 向右、
\(z\) 向上：

\[
\phi = \operatorname{atan2}(a_y, a_z),
\qquad
\theta = \operatorname{atan2}\!\left(-a_x,\sqrt{a_y^2+a_z^2}\right).
\]

一阶互补滤波的离散形式为

\[
\alpha = \frac{\tau}{\tau+\Delta t},
\qquad
\theta_k = \alpha\,\theta_{\mathrm{acc},k}
+ (1-\alpha)\left(\theta_{k-1} + \omega_y \Delta t\right).
\]

报告原式使用 \(\arctan(a_y/a_z)\)，缺少象限判断；在 \(150^\circ\) 时会返回
\(-30^\circ\)。六轴 IMU 也无法观测偏航。完整推导、适用边界和四元数约定见
[工作原理](docs/zh-CN/theory_of_operation.md)，逐条修改见[勘误](docs/errata.md)。

## 仓库结构

```text
DustArrow/
├── BOM/                     # consolidated bill of materials
├── electronics/
│   ├── datasheets/          # manufacturer datasheets
│   ├── output/              # Gerber, BOM, silkscreen, PCB 3D
│   └── source/              # legacy EasyEDA project
├── mechanical/
│   ├── output/              # STL, STEP, reprint files
│   └── source/              # SolidWorks drafts, formal parts, reprints
├── simulation/cfd/          # CFD project and animations
├── software/ground_station/ # archived PyQt5 dashboard
├── firmware/                # status note only
├── docs/                    # trilingual docs, errata, verification, archive
├── media/                   # photos, GIFs, videos
├── scripts/verify_theory/   # reproducible tests
└── .github/                 # issue and PR templates
```

机械源文件保留中文文件名，因为 SolidWorks 装配体按文件名查找零件。STL 输出
已改为英文小写命名，并附 `part_name_mapping.csv`。完整映射见
[MIGRATION_NOTES.md](MIGRATION_NOTES.md)。

## 物料清单

| 指标 | 数值 |
|---|---:|
| PCB 模块 | 9 |
| BOM 行数 | 48 |
| 元件总数 | 57 |
| 已知合计成本 | CNY 31.44 |
| 无价格行数 | 16 |

已知成本只覆盖已填价格的行；RP2040/Pico、LoRa、GNSS、MQ 传感器等 16 行没有
价格，因此 31.44 元是历史下界。明细见 [BOM/bill_of_materials.csv](BOM/bill_of_materials.csv)
与 [BOM/README.md](BOM/README.md)。

## 快速开始

**地面站**（需要 Python 3.11）：

```bash
cd software/ground_station
python -m pip install -r requirements.txt
python appMain.py
```

选择串口并以 9600 波特率打开。归档代码会解析 `X`、`Y`、`GX`、`GY`、`GZ`
字段并写入 `data.txt`；六张图和 3D 立方体不是实时数据。详见
[software/ground_station/README.md](software/ground_station/README.md)。

**机械与电子**：从 [mechanical/source/formal/](mechanical/source/formal/) 打开
SolidWorks 装配，或直接使用 [mechanical/output/3dp/](mechanical/output/3dp/)
中的 STL。PCB 制造文件位于 [electronics/output/gerber/](electronics/output/gerber/)。
复现步骤见[复现指南](docs/zh-CN/replication_guide.md)。

**验证**：

```bash
python scripts/verify_theory/run_verification.py
```

## 演示与测试

<p align="center">
  <img src="./media/photos/project/cfd_demo.gif" alt="冯·卡门头锥与鸭翼 CFD 演示" width="800"/>
  <br>
  <em>CFD 演示。原始视频位于 media/videos/。</em>
</p>

<p align="center">
  <img src="./media/photos/project/canard_deployment.gif" alt="鸭翼展开与头锥分离机构动画" width="800"/>
  <br>
  <em>机构动画：头锥分离、鸭翼展开与回收过程。</em>
</p>

<p align="center">
  <img src="./media/photos/project/ground_station_ui.png" alt="归档地面站界面" width="800"/>
  <br>
  <em>归档地面站界面。六张曲线为 y = x² 占位数据，不是实测结果。</em>
</p>

验证结果：32 项测试全部通过，覆盖姿态公式、互补滤波、四元数、帧解析、
冯·卡门曲线、STL 外形、Gerber 外形与 BOM 成本。测试清单与首次运行的失败
记录见[验证记录](docs/verification.md)。

## 媒体报道

2024 年 1 月，上海广播电视台青少年科学梦想秀《少年爱迪生》第八季《明日世界》
播出了本项目的专题。节目记录了 2023 年秋末初冬在固原市郊外戈壁滩的一次试飞：
遥控点火失败后改用线控，火箭离架，传感器段被找回，伞舱与推进模块丢失；作者
估计回收完整度为 80%。节目用“成功”描述这次试飞，本仓库因此把它表述为“部分
回收”，而不是整箭完整回收。

节目还说明 X 意味着“无限的可能”，并提到地面站读取文本文件完成简单姿态反馈，
这与归档原型一致。节目没有提供遥测日志或定量传感器数据。电视视频不在本仓库
重新分发。

- [媒体报道详情](docs/zh-CN/media_coverage.md)
- 官方页面：[预告](https://www.kankanews.com/detail/ELwxNKJWGy9)、
  [专题](https://www.kankanews.com/detail/LMwVGm9WB2z)、
  [节目综述](https://www.kankanews.com/detail/boy4AKjBxQ1)

## 设计规格

| 参数 | 数值 | 来源 / 状态 |
|---|---|---|
| 箭体直径 | 40.0 mm | 实测，STL 包围盒 |
| 头锥外形 | 冯·卡门曲线 | 报告公式，已数值检查 |
| Command A 外形 | 30 × 40 mm | 实测，Gerber 外形层 |
| Power 外形 | 25.0 × 25.1 mm | 实测，Gerber 外形层 |
| Data 外形 | 32 × 101 mm | 实测，Gerber 外形层 |
| Exploration 外形 | 32 × 76 mm | 实测，Gerber 外形层 |
| 微处理器 | RP2040 | BOM / 报告 |
| IMU | MPU6050 | BOM |
| 气压计 | BMP280 | BOM；报告写作 BMP-180，[待确认] |
| GNSS | ATGM336H-5N | 报告 |
| 数传 | A39C-T400A22D1a | 报告 / BOM |
| 粉尘传感器 | GP2Y1014AU0F | BOM |
| 气体传感器 | MQ-2、MQ-135 | BOM |
| 地面站串口 | 9600, 8-N-1 | 源码 |
| 数传距离 | 千米级 | 设计目标，未验证 |
| 飞行试验 | 2023 年秋末初冬一次电视记录的试飞；传感器段回收，伞舱与推进模块丢失；无遥测日志 | 电视证据，部分回收 |
| 整箭质量 | 未记录 | 不可用 |

## 勘误与已知问题

- 横滚公式已由 \(\arctan(a_y/a_z)\) 改为 `atan2(a_y, a_z)`，修复象限错误。
- 六轴 IMU 无法观测偏航；“3D 姿态”实际只包含横滚与俯仰。
- 归档正则无法处理分包与粘包；仓库给出带长度和 CRC-16 的替代帧，但未在
  固件中实现。
- 归档中没有箭载固件、飞行数据、标定记录或链路预算。

完整列表见[勘误](docs/errata.md)，验证边界见[验证记录](docs/verification.md)。

## 路线图

1. 为 RP2040 编写固件，采用带 CRC-16 的二进制帧并实现命令上行。
2. 把地面站占位曲线替换为实时绘图、时间戳日志与飞后回放。
3. 完成台架测试、链路预算与外场距离测试，并公开脱敏数据。

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。请勿提交推进剂配方、点火流程或
发射操作说明。

## 许可证

代码、文档与作者原创媒体采用 [MIT](LICENSE)。第三方器件手册与赛事标志不在
MIT 范围内，详见[参考资料](docs/references/README.md)。

## 致谢

感谢宁夏回族自治区固原市第一中学与全国青少年科技创新大赛提供的平台。感谢上海
广播电视台《少年爱迪生》节目组记录本项目。项目使用 SolidWorks、EasyEDA、Python、
PyQt5、Matplotlib、PySerial 与 OpenGL。原始报告、答辩材料和旧版代码保存在
[docs/archive/](docs/archive/)。
