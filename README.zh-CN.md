<p align="center">
  <img src="./media/photos/project/banner.png" alt="DustArrow X 整机渲染图" width="800"/>
</p>

<h1 align="center">DustArrow X · 沙尘利“箭”</h1>

<p align="center">
  <strong>面向 40 mm 气象探空火箭的模块化遥测系统</strong>
  <br>
  RP2040 传感栈、LoRa 下行链路与 PyQt5 地面站
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="许可证：MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white" alt="Python 3.11">
  <img src="https://img.shields.io/badge/PyQt5-%E5%9C%B0%E9%9D%A2%E7%AB%99-41CD52?logo=qt&logoColor=white" alt="PyQt5">
  <img src="https://img.shields.io/badge/SolidWorks-CAD-e63946" alt="SolidWorks">
  <img src="https://img.shields.io/badge/%E7%8A%B6%E6%80%81-%E5%BD%92%E6%A1%A3-6b7280" alt="状态：归档">
  <br>
  <a href="./README.md">English</a> |
  <a href="./README.zh-CN.md">中文</a> |
  <a href="./README.fr.md">Français</a>
</p>

---

## 名称来源

中文名“沙尘利箭”由“沙尘”和“利箭”组成：“沙尘”指项目面向的沙尘天气，“利箭”
既指探空火箭，也含“有利于治理”的意思。英文名 **DustArrow** 是中文名的直译。
模块化结构参考了中国空间站实验柜的设计思路。第三代在名称后加上 **X**；作者
解释 X 意味着“无限的可能”。

## 项目简介

DustArrow X 是宁夏固原市第一中学学生项目的第三代硬件，前两代分别为 Theta 和
Beta。项目参加全国青少年科技创新大赛，并于 2024 年 1 月登上上海广播电视台
《少年爱迪生》第八季《明日世界》。项目利用低成本探空火箭获取沙尘天气下垂直
方向的气象数据。

箭体直径 40 mm，由 10 个功能段组成。模块之间使用金手指板对板连接，模块内部
使用 FPC 排线。箭载电子以 RP2040 为核心，配合 MPU6050、BMP280、ATGM336H、
A39C LoRa、GP2Y1014AU0F 和 MQ 系列气体传感器；地面端是 Python/PyQt5 地面站
应用。

本归档覆盖机械设计、电子制造数据、地面站源码、原始报告、答辩材料和媒体。
箭载固件源码与飞行日志不在本归档范围内，见
[firmware/README.md](firmware/README.md)。

## 主要特性

- **40 mm 模块化箭体**：10 个功能段，金手指与 FPC 连接，打印件可单独替换。
- **RP2040 传感栈**：六轴 IMU、气压计、GNSS 与多路气体/粉尘传感器。
- **LoRa 下行链路**：A39C-T400A22D1a 串口数传，地面端以 9600 波特率接收。
- **PyQt5 地面站**：六路曲线、3D 姿态视图与串口采集。
- **开放的制造文件**：SolidWorks 源文件、STL、STEP、Gerber、BOM 和丝印图。
- **验证套件**：32 项 Python 测试与 16 项勘误记录，覆盖姿态数学、分帧与几何。

## 系统架构

<p align="center">
  <img src="./media/photos/project/system_architecture.svg" alt="DustArrow X 系统架构图" width="900"/>
  <br>
  <em>系统架构。虚线为无线链路；地面站命令链路在图中一并标出。</em>
</p>

- **机械**：头锥与伞舱、测控舱、数据舱、电源舱、三个传感器舱、主控舱、
  鸭翼舱、推进尾翼舱。伞舱由单舵机驱动大角度舱盖，鸭翼舱为双通道空气舵。
- **电子**：9 个模块 BOM、10 个 Gerber 包。主控与测控板围绕 RP2040、
  MPU6050、BMP280、ATGM336H 和 A39C 构建。
- **下行**：9600 波特率、8-N-1 文本流；CRC-16 二进制帧格式已在
  `scripts/verify_theory/test_protocol.py` 中定义并测试。
- **地面站**：PyQt5、Matplotlib 与 OpenGL；串口采集、文本解析、六路曲线与
  姿态视图。

## 理论与设计

静态条件下，加速度计测量重力反作用。按本仓库约定，$x$ 向前、$y$ 向右、
$z$ 向上：

$$
\phi = \mathrm{atan2}(a_y, a_z),
\qquad
\theta = \mathrm{atan2}\left(-a_x,\sqrt{a_y^2+a_z^2}\right).
$$

实现使用 `atan2` 保留象限。一阶互补滤波使用明确的采样周期：

$$
\alpha = \frac{\tau}{\tau+\Delta t},
\qquad
\theta_k = \alpha\,\theta_{\mathrm{acc},k} +
(1-\alpha)\left(\theta_{k-1} + \omega_y \Delta t\right).
$$

完整推导、坐标约定与修正见[工作原理](docs/zh-CN/theory_of_operation.md)和
[勘误记录](docs/errata.md)。

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
├── software/ground_station/ # PyQt5 ground-station source
├── firmware/                # interface and protocol notes
├── docs/                    # trilingual docs, errata, verification, archive
├── media/                   # photos, GIFs, videos
├── scripts/verify_theory/   # reproducible tests
└── .github/                 # issue and PR templates
```

机械源文件保留中文文件名，因为 SolidWorks 装配体按文件名查找零件。STL 输出
已改为英文命名，并附 `part_name_mapping.csv`。完整路径映射见
[MIGRATION_NOTES.md](MIGRATION_NOTES.md)。

## 物料清单

| 指标 | 数值 |
|---|---:|
| PCB 模块 | 9 |
| BOM 行数 | 48 |
| 元件总数 | 57 |
| 已标价小计 | CNY 31.44 |
| 未标价行数 | 16 |

价格来自 2023-08-15 的模块导出文件。完整明细见
[BOM/bill_of_materials.csv](BOM/bill_of_materials.csv)，按模块汇总见
[BOM/bom_summary.csv](BOM/bom_summary.csv)。

## 快速开始

**地面站**（Python 3.11）：

```bash
cd software/ground_station
python -m pip install -r requirements.txt
python appMain.py
```

应用会枚举串口，以 9600 8-N-1 打开，解析 `X`、`Y`、`GX`、`GY`、`GZ` 字段并写入
`data.txt`。已实现的数据路径见
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
  <img src="./media/photos/project/ground_station_ui.png" alt="地面站界面布局" width="800"/>
  <br>
  <em>地面站界面布局。</em>
</p>

验证结果：32 项测试全部通过，覆盖姿态公式、互补滤波、四元数、帧解析、
冯·卡门曲线、STL 外形、Gerber 外形与 BOM 成本。详见
[验证记录](docs/verification.md)。

## 媒体报道

2024 年 1 月，上海广播电视台青少年科学梦想秀《少年爱迪生》第八季《明日世界》
播出了本项目的专题。节目记录了 2023 年秋末初冬在固原市郊外戈壁滩的一次试飞：
遥控点火改为线控点火，火箭离架；传感器段被找回，伞舱与推进模块丢失，作者
估计回收完整度为 80%。节目还说明 X 意味着“无限的可能”，并展示地面站读取
文本文件完成姿态反馈。下方附有节目截图与两段短片段。

- [媒体报道详情](docs/zh-CN/media_coverage.md)
- 官方页面：[预告](https://www.kankanews.com/detail/ELwxNKJWGy9)、
  [专题](https://www.kankanews.com/detail/LMwVGm9WB2z)、
  [节目综述](https://www.kankanews.com/detail/boy4AKjBxQ1)

### 节目截图

<p align="center">
  <img src="./media/photos/project/tv_still_build.png" alt="DustArrow X 白板与打印箭体" width="640"/>
  <br>
  <em>DustArrow X 白板与打印箭体。</em>
</p>

<p align="center">
  <img src="./media/photos/project/tv_still_ground_station.png" alt="节目中的地面站界面" width="640"/>
  <br>
  <em>节目中的地面站界面。</em>
</p>

<p align="center">
  <img src="./media/photos/project/tv_still_modular.png" alt="装配中的模块化舱段" width="640"/>
  <br>
  <em>装配中的模块化舱段。</em>
</p>

<p align="center">
  <img src="./media/photos/project/tv_still_launch.png" alt="戈壁滩试飞升空" width="640"/>
  <br>
  <em>戈壁滩试飞升空。</em>
</p>

<p align="center">
  <img src="./media/photos/project/tv_still_recovery.png" alt="着陆点回收的降落伞" width="640"/>
  <br>
  <em>着陆点回收的降落伞。</em>
</p>

### 节目片段

<p align="center">
  <img src="./media/photos/project/tv_launch.gif" alt="发射片段，6 秒" width="800"/>
  <br>
  <em>发射片段，6 秒。</em>
</p>

<p align="center">
  <img src="./media/photos/project/tv_recovery.gif" alt="回收片段，6 秒" width="800"/>
  <br>
  <em>回收片段，6 秒。</em>
</p>

<p align="center">
  <em>截图与片段来自 2024 年 1 月节目，版权归上海广播电视台所有。</em>
</p>

## 设计规格

| 参数 | 数值 | 来源 |
|---|---|---|
| 箭体直径 | 40.0 mm | 实测，STL 包围盒 |
| 头锥外形 | 冯·卡门曲线 | 报告公式，已数值检查 |
| Command A 外形 | 30 × 40 mm | 实测，Gerber 外形层 |
| Power 外形 | 25.0 × 25.1 mm | 实测，Gerber 外形层 |
| Data 外形 | 32 × 101 mm | 实测，Gerber 外形层 |
| Exploration 外形 | 32 × 76 mm | 实测，Gerber 外形层 |
| 微处理器 | RP2040 | BOM 与报告 |
| IMU | MPU6050 | BOM |
| 气压计 | BMP280 | BOM |
| GNSS | ATGM336H-5N | 报告 |
| 数传 | A39C-T400A22D1a | 报告与 BOM |
| 粉尘传感器 | GP2Y1014AU0F | BOM |
| 气体传感器 | MQ-2、MQ-135 | BOM |
| 地面站串口 | 9600, 8-N-1 | 源码 |
| 飞行试验 | 2023 年秋末初冬；传感器段回收，伞舱与推进模块丢失；回收完整度估计 80% | 电视专题片 |

## 验证

仓库包含纯 Python 验证套件与完整的勘误记录。

- `python scripts/verify_theory/run_verification.py`：32 项测试，覆盖姿态公式、
  互补滤波、四元数、帧解析、冯·卡门曲线、STL 外形、Gerber 外形与 BOM 成本。
- [docs/errata.md](docs/errata.md)：16 项审查记录，含修正与依据。
- [docs/verification.md](docs/verification.md)：测试记录与数值交叉检查。

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。请勿提交推进剂配方、点火流程或
发射操作说明。

## 许可证

代码、文档与作者原创媒体采用 [MIT](LICENSE)。第三方器件手册与赛事标志不在
MIT 范围内。节目截图与 GIF 片段版权归上海广播电视台所有，不在 MIT 范围内；
完整节目不再分发。

## 致谢

感谢宁夏回族自治区固原市第一中学与全国青少年科技创新大赛提供的平台。感谢上海
广播电视台《少年爱迪生》节目组记录本项目。项目使用 SolidWorks、EasyEDA、
Python、PyQt5、Matplotlib、PySerial 与 OpenGL。原始报告、答辩材料和旧版代码
保存在 [docs/archive/](docs/archive/)。
