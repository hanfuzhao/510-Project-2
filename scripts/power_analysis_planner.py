#!/usr/bin/env python3
import math
import argparse
from typing import List, Tuple

MEANS = [
    13.18, 12.51, 7.44, 7.48, 6.73,
    4.56, 4.76, 4.42, 2.29, 2.53,
    2.27, 1.67, 1.12, 1.74, 0.71,
]

SIZE_IDS = list(range(1, 16))

SQRT2 = math.sqrt(2.0)


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / SQRT2))


def norm_ppf(p: float) -> float:
    if p <= 0.0 or p >= 1.0:
        raise ValueError("p must be in (0,1)")
    a = [
        -3.969683028665376e+01,
        2.209460984245205e+02,
        -2.759285104469687e+02,
        1.383577518672690e+02,
        -3.066479806614716e+01,
        2.506628277459239e+00,
    ]
    b = [
        -5.447609879822406e+01,
        1.615858368580409e+02,
        -1.556989798598866e+02,
        6.680131188771972e+01,
        -1.328068155288572e+01,
    ]
    c = [
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e+00,
        -2.549732539343734e+00,
        4.374664141464968e+00,
        2.938163982698783e+00,
    ]
    d = [
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e+00,
        3.754408661907416e+00,
    ]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
        )
    if phigh < p:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1.0)
        )
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / (
        (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
    )


def pooled_sigma_from_cv(mean_a: float, mean_b: float, cv: float) -> float:
    mu = (mean_a + mean_b) / 2.0
    return max(1e-9, cv * mu)


def required_n_per_group_ttest(mean_a: float, mean_b: float, cv: float, alpha: float = 0.05, power: float = 0.8) -> float:
    za2 = norm_ppf(1 - alpha / 2)
    zb = norm_ppf(power)
    delta = abs(mean_a - mean_b)
    sigma = pooled_sigma_from_cv(mean_a, mean_b, cv)
    if delta <= 0:
        return float('inf')
    d = delta / sigma
    n = 2.0 * (za2 + zb) ** 2 / (d ** 2)
    return n


def achieved_power_ttest(n: int, mean_a: float, mean_b: float, cv: float, alpha: float = 0.05) -> float:
    delta = abs(mean_a - mean_b)
    sigma = pooled_sigma_from_cv(mean_a, mean_b, cv)
    if sigma <= 0:
        return 0.0
    z_true = delta / (sigma * math.sqrt(2.0 / n))
    zc = norm_ppf(1 - alpha / 2)
    power = (1.0 - norm_cdf(zc - z_true)) + norm_cdf(-zc - z_true)
    return max(0.0, min(1.0, power))


def plan_adjacent_pairs(cv: float, alpha: float, power: float) -> List[Tuple[int, int, float, float, float]]:
    rows = []
    for i in range(len(MEANS) - 1):
        a, b = i, i + 1
        m1, m2 = MEANS[a], MEANS[b]
        n_req = required_n_per_group_ttest(m1, m2, cv, alpha, power)
        rows.append((SIZE_IDS[a], SIZE_IDS[b], m1, m2, n_req))
    return rows


def plan_specific_pairs(pairs: List[Tuple[int, int]], cv: float, alpha: float, power: float) -> List[Tuple[int, int, float, float, float, float]]:
    rows = []
    for a_id, b_id in pairs:
        a, b = a_id - 1, b_id - 1
        m1, m2 = MEANS[a], MEANS[b]
        n_req = required_n_per_group_ttest(m1, m2, cv, alpha, power)
        pow10 = achieved_power_ttest(10, m1, m2, cv, alpha)
        rows.append((a_id, b_id, m1, m2, n_req, pow10))
    return rows


def main():
    parser = argparse.ArgumentParser(description="Paper-plane power analysis planner (two-sample t-test, normal approx)")
    parser.add_argument("--cv", type=float, default=0.25, help="Within-group coefficient of variation (CV=σ/mean), e.g., 0.25")
    parser.add_argument("--alpha", type=float, default=0.05, help="Significance level alpha (two-tailed)")
    parser.add_argument("--power", type=float, default=0.80, help="Target power (1-beta)")
    parser.add_argument("--show_all_adjacent", action="store_true", help="Print required n for all adjacent size pairs")
    args = parser.parse_args()

    cv = args.cv
    alpha = args.alpha
    target_power = args.power

    print("=== Settings ===")
    print(f"alpha={alpha:.3f} (two-tailed), target power={target_power:.2f}, CV={cv:.2f}")
    print("Number of sizes=15, planned n per group: n=10")

    key_pairs = [(5, 6), (1, 6), (14, 15), (3, 4)]

    print("\n=== Key Comparisons (Required n per group & Power at n=10) ===")
    for a_id, b_id, m1, m2, n_req, pow10 in plan_specific_pairs(key_pairs, cv, alpha, target_power):
        print(f"Size {a_id} vs {b_id}: means=({m1:.2f},{m2:.2f}), Δ={abs(m1-m2):.2f}m, n_req≈{math.ceil(n_req)}, power@n=10≈{pow10:.2f}")

    if args.show_all_adjacent:
        print("\n=== All Adjacent Pairs (Required n per group) ===")
        for a_id, b_id, m1, m2, n_req in plan_adjacent_pairs(cv, alpha, target_power):
            print(f"Size {a_id} vs {b_id}: Δ={abs(m1-m2):.2f}m, n_req≈{math.ceil(n_req)}")

    print("\nNote: When Δ is small and CV is not small, n_req becomes very large; consider regression/trend-based research design instead.")

if __name__ == "__main__":
    main()
