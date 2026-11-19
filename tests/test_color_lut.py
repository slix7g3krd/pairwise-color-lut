import pytest
from media import color_lut as mod

CASES = [
    ("index", 'm.lut_index(0.5, 8) == 127'),
    ("weights", 'm.trilinear_weights(0.5) == approx((0.5, 0.5))'),
    ("space", 'm.input_space("sRGB", "sRGB") is True'),
    ("order", 'm.lut_order(1, 2) is True'),
    ("white", 'm.white_point(6500) == 6500'),
    ("gamut", 'm.gamut_clip(2.0, 1.0) == approx(1.0)'),
    ("hdr", 'm.hdr_map(2.0, 1.0) == approx(1.0)'),
    ("alpha", 'm.alpha_isolate(1.0, 5.0) == approx(5.0)'),
    ("delta", 'm.gpu_cpu_delta(1.0, 3.0) == approx(2.0)'),
    ("cache", 'm.cache_version("n", "v") == "n:v"'),
    ("bits", 'm.intermediate_bits(8, 16) == 16'),
    ("multi", 'm.multitrack_lut(3) == 3'),
    ("icc", 'm.icc_dedupe(1, 2) is True'),
    ("shaper", 'm.shaper_curve(2.0, 3.0) == approx(8.0)'),
    ("domain", 'm.lut_domain(5.0, 0.0, 10.0) == approx(0.5)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
