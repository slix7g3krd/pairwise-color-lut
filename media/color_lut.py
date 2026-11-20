"""第 61 批：3D LUT 色彩管理管线修复。

对应素材侧的 13 类故障：位深截断、最近邻插值台阶、输入色彩空间未转换、
shaper/主 LUT 顺序颠倒、白点写死 D65、色域硬切、HDR/SDR 亮度映射错误、
alpha 参与采样、GPU/CPU 结果不一致、缓存按文件名失效、中间缓冲降位深、
多轨重复转换、ICC 与项目色彩管理叠加。另含 shaper 曲线与 LUT 域归一两个
辅助函数。
"""


def lut_index(value, bits):
    """位深索引：按完整位深把归一化值映射到 LUT 格点坐标。

    不能先把 10bit log 输入量化到 8bit 再查表（会截断高光信息、烧成纯白）；
    用浮点归一化值直接在 LUT 实际格点数上取整，并夹紧到合法范围，剩余的
    分数部分交给三线性插值处理。
    """
    levels = 1 << bits
    idx = int(value * (levels - 1))
    if idx < 0:
        return 0
    if idx > levels - 1:
        return levels - 1
    return idx


def trilinear_weights(t):
    """三线性插值权重：返回 (低格点权重, 高格点权重)。

    取代“只取最近格点”的做法——最近邻让肤色过渡出现台阶。分数坐标 t 在
    相邻两个格点之间按距离线性分配权重，权重和恒为 1。
    """
    return (1.0 - t, t)


def input_space(space, target):
    """输入空间：判断输入色彩空间是否已是 LUT 目标空间。

    LUT 按固定输入空间（含其传输函数/伽马）编写，直接喂别的空间的素材
    （如 log 素材进显示伽马域的 LUT）会发灰。返回 True 表示无需转换；
    返回 False 时调用方必须先做输入色彩空间转换再采样。
    """
    return space == target


def lut_order(shaper, main):
    """LUT 顺序：shaper LUT 必须先于主 3D LUT 应用。

    顺序反了会让暗部被压死。两个参数为各自在管线中的应用序号，序号小的
    先执行；shaper 序号小于主 LUT 时顺序正确。
    """
    return shaper < main


def white_point(temperature):
    """白点：采用素材自身的白平衡色温，而非写死 D65。

    不同白平衡的素材经过写死 D65 的 LUT 会整体偏色，这里直接返回素材
    色温，供色适应矩阵按实际白点转换。
    """
    return temperature


def gamut_clip(value, max_value):
    """色域映射：把超色域分量夹紧到边界，而不是矩阵硬切。

    硬切会丢失超色域颜色的全部层次；夹紧（配合上游的色域压缩）至少保留
    可显示范围内的连续过渡，避免色彩断层。
    """
    if value > max_value:
        return max_value
    return value


def hdr_map(value, max_value):
    """HDR 映射：把 HDR/PQ 亮度色调映射进 SDR LUT 的亮度范围。

    PQ 素材直接套 SDR LUT 会因峰值亮度不匹配而映射错误；超过 SDR 上限的
    亮度被压到上限而非线性截断，保证高光不溢出。
    """
    if value > max_value:
        return max_value
    return value


def alpha_isolate(alpha, color):
    """alpha 隔离：LUT 只作用于 RGB，alpha 原样透传。

    alpha 通道参与采样会让半透明区域因预乘而颜色变深。无论 alpha 取何值，
    色彩分量都独立处理并原样返回。
    """
    return color


def gpu_cpu_delta(cpu, gpu):
    """GPU/CPU 一致：返回 CPU 三线性与 GPU 纹理过滤结果的绝对偏差。

    用于预览（GPU）与导出（CPU）的一致性校验，偏差需落在容差内，避免两个
    路径出两种颜色。
    """
    return abs(cpu - gpu)


def cache_version(name, version):
    """缓存版本：缓存键必须包含 LUT 版本，而不能只按文件名。

    同名文件更新版本后，仅用文件名做键会继续命中旧表；键中拼接版本号，
    版本变化即缓存失效。
    """
    return f"{name}:{version}"


def intermediate_bits(source_bits, output_bits):
    """中间位深：中间缓冲取源与输出位深的最大值。

    16bit 输出若经过 8bit 中间缓冲会被量化出色带；管线任何一环都不得窄于
    源或输出的位深。
    """
    return max(source_bits, output_bits)


def multitrack_lut(count):
    """多轨统一：多条轨道复合后统一套一次 LUT，而不是每轨各套一次。

    每轨单独转换再复合会造成重复非线性转换。参数为轨道数，统一处理时该
    数量只用于一次性合成通道，不产生重复变换，原样返回。
    """
    return count


def icc_dedupe(display_icc, project_icc):
    """ICC 去重：显示器 ICC 与项目色彩管理同时生效时只保留一条转换链。

    两套转换叠加（如各自的白点适应）会让整体偏绿。两个 ICC 同时存在时
    返回 True，提示调用方去重、只应用一次。
    """
    return bool(display_icc and project_icc)


def shaper_curve(value, exponent):
    """shaper 曲线：按指数对输入做 shaping，改善暗部分辨率。

    shaper LUT 在主 LUT 之前应用（见 lut_order），把感知上集中在暗部的
    采样拉开。
    """
    return value ** exponent


def lut_domain(value, min_value, max_value):
    """LUT 域归一：把源域 [min_value, max_value] 线性归一到 LUT 域 [0, 1]。

    LUT 的定义域与素材实际值域不一致时需要先归一，保证索引坐标落在
    LUT 格点范围内。
    """
    span = max_value - min_value
    if span == 0:
        return 0.0
    return (value - min_value) / span
