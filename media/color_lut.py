"""第 61 批：同一段 log 素材在剪辑软件里是灰的，套上 LUT 后高光直接..."""

def lut_index(value, bits):
    """位深索引。"""
    raise NotImplementedError("TODO: lut_index")

def trilinear_weights(t):
    """三线性插值权重。"""
    raise NotImplementedError("TODO: trilinear_weights")

def input_space(space, target):
    """输入空间。"""
    raise NotImplementedError("TODO: input_space")

def lut_order(shaper, main):
    """LUT 顺序。"""
    raise NotImplementedError("TODO: lut_order")

def white_point(temperature):
    """白点。"""
    raise NotImplementedError("TODO: white_point")

def gamut_clip(value, max_value):
    """色域裁剪。"""
    raise NotImplementedError("TODO: gamut_clip")

def hdr_map(value, max_value):
    """HDR 映射。"""
    raise NotImplementedError("TODO: hdr_map")

def alpha_isolate(alpha, color):
    """alpha 隔离。"""
    raise NotImplementedError("TODO: alpha_isolate")

def gpu_cpu_delta(cpu, gpu):
    """GPU/CPU 一致。"""
    raise NotImplementedError("TODO: gpu_cpu_delta")

def cache_version(name, version):
    """缓存版本。"""
    raise NotImplementedError("TODO: cache_version")

def intermediate_bits(source_bits, output_bits):
    """中间位深。"""
    raise NotImplementedError("TODO: intermediate_bits")

def multitrack_lut(count):
    """多轨统一。"""
    raise NotImplementedError("TODO: multitrack_lut")

def icc_dedupe(display_icc, project_icc):
    """ICC 去重。"""
    raise NotImplementedError("TODO: icc_dedupe")

def shaper_curve(value, exponent):
    """shaper 曲线。"""
    raise NotImplementedError("TODO: shaper_curve")

def lut_domain(value, min_value, max_value):
    """LUT 域归一。"""
    raise NotImplementedError("TODO: lut_domain")
