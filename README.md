# pairwise-color-lut

同一段 log 素材在剪辑软件里是灰的，套上 LUT 后高光直接烧成纯白，换到另一台显示器又偏绿：3D LUT 按 8bit 索引，log 素材的 10bit 值被截断；插值只用最近格点，肤色过渡出现台阶；LUT 域按显示伽马写，输入色彩空间没转换；shaper LUT 和主 LUT 顺序反了，暗部被压死；白点按 D65 写死，不同白平衡素材直接偏色；色域映射只做矩阵裁剪，超色域颜色被硬切；HDR PQ 素材套 SDR LUT，亮度映射错；alpha 通道参与 LUT 采样，半透明区域颜色变深；GPU 纹理过滤和 CPU 三线性结果不一致，预览导出两个色；LUT 缓存按文件名，改版本后仍用旧表；16bit 输出被 LUT 中间缓冲降成 8bit，出现色带；多轨道各套一个 LUT，复合后重复转换；显示器 ICC 和项目色彩管理叠加两次，整体偏绿。media/color_lut.py 是核心，tests/test_color_lut.py 15个红。要修的是：位深索引；插值；输入空间；LUT 顺序；白点；色域映射；HDR 映射；alpha 隔离；GPU/CPU 一致；缓存版本；中间位深；多轨统一；ICC 去重。

## 运行

```bash
python -m pytest tests -q
```

初始状态：15 个用例失败。修复实现使全部用例通过，不要修改 `tests/` 下的测试。

子方向：音视频处理；任务类型：Bugfix；语言/框架：Python 3, pytest；环境可复现等级：无外部依赖。
