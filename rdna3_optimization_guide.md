# RDNA3 Optimization Guide — RX 7900 XTX (gfx1100)

Auto-generated from atlas discoveries (100% parameter space coverage).

---

## General Rules

### AVOID_LDS_STRIDE_32
**Impact:** high

LDS stride=32 causes bank conflicts: 353 GB/s vs 878 GB/s at stride=22 (60% penalty)

**Recommendation:** Use stride=22 or other non-power-of-2 strides to avoid 32-bank LDS conflicts

### USE_STRIDE_1
**Impact:** critical

Stride-1 (coalesced) memory access provides 2-10x higher bandwidth than strided access

**Recommendation:** Ensure global memory accesses are coalesced (consecutive threads access consecutive addresses)

### LEVERAGE_INFINITY_CACHE
**Impact:** high

Coalesced access achieves 2562 GB/s (2.7x DRAM peak) via 96MB Infinity Cache

**Recommendation:** Keep working sets under 96MB and use stride-1 access to benefit from Infinity Cache's ~2.5x bandwidth amplification

### OPTIMAL_BLOCK_SIZE
**Impact:** medium

Block size 128 provides best bandwidth (839 GB/s)

**Recommendation:** Use block_size=128 (4 waves of 32) for memory-bound kernels on RDNA3

### USE_ILP_FMA_CHAINS
**Impact:** critical

Use 7 independent FMA accumulator chains for 50.1 TFLOPS vs 21.5 TFLOPS with serial chain (2.3x speedup)

**Recommendation:** RDNA3 FMA latency is ~4 cycles. Use 7 independent accumulator chains at block_size=512 to saturate the FMA pipeline

### USE_FP16_PACKED_ILP
**Impact:** critical

Use 11 independent half2 FMA chains for 57.9 FP16 TFLOPS vs 55.5 TFLOPS with serial chain (1.0x speedup)

**Recommendation:** RDNA3 dual-issue FP16 via packed half2. Use 11 independent half2 chains at block_size=1024 to saturate both FP16 pipelines

### USE_WMMA_MATRIX_OPS
**Impact:** high

WMMA achieves 88.8 TFLOPS with 6 chains, k_tiles=34 (16x16x16 per instruction)

**Recommendation:** Use WMMA with 6 independent accumulator chains and k_tiles>=34 for peak matrix throughput

### MINIMIZE_ATOMIC_CONTENTION
**Impact:** high

Atomic throughput: 431 GOPS uncontended vs 2.9 GOPS fully contended (99% penalty)

**Recommendation:** Spread atomic targets across unique addresses. Use shared memory atomics + final global reduce for reductions

### ROOFLINE_KNEE
**Impact:** medium

Memory bandwidth saturates at compute_intensity=2 (781 GB/s). Beyond this, kernel is compute-bound

**Recommendation:** For memory-bound kernels, add at least 2 FMAs per loaded element to hide memory latency

---

## strided_access

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | stride=1, working_set_kb=30048 | 1.000 | 2194 GB/s |
| 2 | stride=1, working_set_kb=36122 | 1.000 | 2166 GB/s |
| 3 | stride=1, working_set_kb=3616 | 1.000 | 2093 GB/s |
| 4 | stride=1, working_set_kb=24995 | 1.000 | 2445 GB/s |
| 5 | stride=4, working_set_kb=52204 | 1.000 | 2094 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | stride=827, working_set_kb=130992 | 0.000 | 0 GB/s |
| 2 | stride=464, working_set_kb=130881 | 0.000 | 0 GB/s |
| 3 | stride=275, working_set_kb=131032 | 0.000 | 0 GB/s |
| 4 | stride=969, working_set_kb=14 | 0.001 | 2 GB/s |
| 5 | stride=656, working_set_kb=298 | 0.001 | 2 GB/s |

### Parameter: `stride`

**Optimal range:** 1 - 7 (7 values with score >= 0.8)

**Sweet spots:**
- `stride=10.0` (+100% above neighbors)
- `stride=10.0` (+100% above neighbors)
- `stride=10.0` (+83% above neighbors)
- `stride=11.0` (+79% above neighbors)
- `stride=11.0` (+79% above neighbors)

**Performance cliffs (AVOID):**
- At `stride=827.0`: 98% drop
- At `stride=666.0`: 96% drop
- At `stride=546.0`: 96% drop
- At `stride=907.0`: 96% drop
- At `stride=907.0`: 96% drop

### Parameter: `working_set_kb`

**Optimal range:** 1030 - 131069 (2849 values with score >= 0.8)

**Sweet spots:**
- `working_set_kb=130764.0` (+100% above neighbors)
- `working_set_kb=2692.0` (+100% above neighbors)
- `working_set_kb=1461.0` (+100% above neighbors)
- `working_set_kb=2282.0` (+100% above neighbors)
- `working_set_kb=2282.0` (+100% above neighbors)

**Performance cliffs (AVOID):**
- At `working_set_kb=130992.0`: 100% drop
- At `working_set_kb=130881.0`: 100% drop
- At `working_set_kb=130881.0`: 100% drop
- At `working_set_kb=130881.0`: 100% drop
- At `working_set_kb=130881.0`: 100% drop

---

## bandwidth

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=128, elements_per_thread=2 | 0.419 | 839 GB/s |
| 2 | block_size=128, elements_per_thread=1 | 0.418 | 836 GB/s |
| 3 | block_size=128, elements_per_thread=2 | 0.415 | 830 GB/s |
| 4 | block_size=512, elements_per_thread=2 | 0.415 | 829 GB/s |
| 5 | block_size=1024, elements_per_thread=1 | 0.414 | 828 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=32, elements_per_thread=30 | 0.041 | 82 GB/s |
| 2 | block_size=512, elements_per_thread=30 | 0.042 | 85 GB/s |
| 3 | block_size=1024, elements_per_thread=30 | 0.045 | 89 GB/s |
| 4 | block_size=1024, elements_per_thread=30 | 0.050 | 100 GB/s |
| 5 | block_size=128, elements_per_thread=30 | 0.050 | 100 GB/s |

### Parameter: `block_size`

**Sweet spots:**
- `block_size=1024.0` (+37% above neighbors)
- `block_size=64.0` (+37% above neighbors)
- `block_size=64.0` (+37% above neighbors)
- `block_size=128.0` (+37% above neighbors)
- `block_size=128.0` (+37% above neighbors)

**Performance cliffs (AVOID):**
- At `block_size=512.0`: 30% drop
- At `block_size=128.0`: 28% drop
- At `block_size=1024.0`: 28% drop
- At `block_size=64.0`: 27% drop
- At `block_size=64.0`: 25% drop

### Parameter: `elements_per_thread`

**Optimal range:** 2 - 2 (1 values with score >= 0.8)

**Sweet spots:**
- `elements_per_thread=2.0` (+24% above neighbors)
- `elements_per_thread=2.0` (+24% above neighbors)
- `elements_per_thread=3.0` (+16% above neighbors)
- `elements_per_thread=7.0` (+12% above neighbors)
- `elements_per_thread=7.0` (+12% above neighbors)

**Performance cliffs (AVOID):**
- At `elements_per_thread=1.0`: 48% drop
- At `elements_per_thread=1.0`: 30% drop
- At `elements_per_thread=2.0`: 30% drop
- At `elements_per_thread=27.0`: 26% drop
- At `elements_per_thread=1.0`: 26% drop

---

## lds_bank

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | stride=22, num_elements=549 | 0.710 | 1420 GB/s |
| 2 | stride=29, num_elements=390 | 0.710 | 1420 GB/s |
| 3 | stride=30, num_elements=403 | 0.710 | 1420 GB/s |
| 4 | stride=1, num_elements=300 | 0.710 | 1420 GB/s |
| 5 | stride=63, num_elements=481 | 0.705 | 1410 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | stride=32, num_elements=14387 | 0.095 | 190 GB/s |
| 2 | stride=32, num_elements=13927 | 0.095 | 190 GB/s |
| 3 | stride=32, num_elements=7271 | 0.100 | 200 GB/s |
| 4 | stride=32, num_elements=13051 | 0.100 | 200 GB/s |
| 5 | stride=32, num_elements=9244 | 0.100 | 200 GB/s |

### Parameter: `stride`

**Optimal range:** 1 - 63 (56 values with score >= 0.8)

**Sweet spots:**
- `stride=33.0` (+60% above neighbors)
- `stride=33.0` (+57% above neighbors)
- `stride=33.0` (+57% above neighbors)
- `stride=33.0` (+57% above neighbors)
- `stride=33.0` (+57% above neighbors)

**Performance cliffs (AVOID):**
- At `stride=2.0`: 41% drop
- At `stride=2.0`: 41% drop
- At `stride=21.0`: 39% drop
- At `stride=32.0`: 28% drop
- At `stride=3.0`: 23% drop

### Parameter: `num_elements`

**Optimal range:** 256 - 16361 (5915 values with score >= 0.8)

**Sweet spots:**
- `num_elements=1026.0` (+57% above neighbors)
- `num_elements=1068.0` (+56% above neighbors)
- `num_elements=1783.0` (+56% above neighbors)
- `num_elements=4052.0` (+56% above neighbors)
- `num_elements=2656.0` (+55% above neighbors)

**Performance cliffs (AVOID):**
- At `num_elements=12322.0`: 83% drop
- At `num_elements=12322.0`: 83% drop
- At `num_elements=12322.0`: 83% drop
- At `num_elements=12322.0`: 83% drop
- At `num_elements=9025.0`: 82% drop

---

## compute

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=512, num_chains=7 | 1.000 | 2002 GB/s |
| 2 | block_size=128, num_chains=10 | 1.000 | 2224 GB/s |
| 3 | block_size=64, num_chains=9 | 1.000 | 2157 GB/s |
| 4 | block_size=128, num_chains=2 | 1.000 | 2101 GB/s |
| 5 | block_size=512, num_chains=14 | 1.000 | 2066 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=256, num_chains=1 | 0.213 | 426 GB/s |
| 2 | block_size=256, num_chains=1 | 0.215 | 429 GB/s |
| 3 | block_size=64, num_chains=1 | 0.218 | 437 GB/s |
| 4 | block_size=64, num_chains=1 | 0.219 | 437 GB/s |
| 5 | block_size=64, num_chains=1 | 0.219 | 439 GB/s |

### Parameter: `block_size`

**Optimal range:** 32 - 1024 (6 values with score >= 0.8)

**Sweet spots:**
- `block_size=64.0` (+78% above neighbors)

**Performance cliffs (AVOID):**
- At `block_size=64.0`: 67% drop
- At `block_size=64.0`: 67% drop
- At `block_size=64.0`: 67% drop
- At `block_size=32.0`: 66% drop
- At `block_size=32.0`: 60% drop

### Parameter: `num_chains`

**Optimal range:** 2 - 15 (12 values with score >= 0.8)

**Sweet spots:**
- `num_chains=2.0` (+78% above neighbors)
- `num_chains=7.0` (+45% above neighbors)
- `num_chains=5.0` (+37% above neighbors)
- `num_chains=6.0` (+34% above neighbors)
- `num_chains=6.0` (+34% above neighbors)

**Performance cliffs (AVOID):**
- At `num_chains=1.0`: 42% drop
- At `num_chains=1.0`: 38% drop
- At `num_chains=6.0`: 28% drop
- At `num_chains=8.0`: 25% drop
- At `num_chains=8.0`: 25% drop

---

## reduction

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=512, items_per_thread=7 | 0.453 | 907 GB/s |
| 2 | block_size=512, items_per_thread=7 | 0.453 | 907 GB/s |
| 3 | block_size=512, items_per_thread=6 | 0.453 | 906 GB/s |
| 4 | block_size=512, items_per_thread=7 | 0.453 | 906 GB/s |
| 5 | block_size=256, items_per_thread=10 | 0.453 | 906 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=32, items_per_thread=1 | 0.200 | 400 GB/s |
| 2 | block_size=32, items_per_thread=1 | 0.200 | 401 GB/s |
| 3 | block_size=32, items_per_thread=1 | 0.206 | 413 GB/s |
| 4 | block_size=1024, items_per_thread=1 | 0.229 | 458 GB/s |
| 5 | block_size=128, items_per_thread=1 | 0.233 | 466 GB/s |

### Parameter: `block_size`

**Optimal range:** 32 - 1024 (6 values with score >= 0.8)

**Sweet spots:**
- `block_size=64.0` (+25% above neighbors)
- `block_size=64.0` (+25% above neighbors)
- `block_size=256.0` (+22% above neighbors)
- `block_size=1024.0` (+22% above neighbors)
- `block_size=1024.0` (+21% above neighbors)

**Performance cliffs (AVOID):**
- At `block_size=32.0`: 41% drop
- At `block_size=32.0`: 41% drop
- At `block_size=512.0`: 33% drop
- At `block_size=512.0`: 33% drop
- At `block_size=256.0`: 32% drop

### Parameter: `items_per_thread`

**Optimal range:** 3 - 15 (13 values with score >= 0.8)

**Sweet spots:**
- `items_per_thread=2.0` (+18% above neighbors)
- `items_per_thread=2.0` (+18% above neighbors)
- `items_per_thread=3.0` (+8% above neighbors)
- `items_per_thread=6.0` (+8% above neighbors)
- `items_per_thread=6.0` (+8% above neighbors)

---

## tiled_gemm

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | tile_m=128, tile_n=128 | 0.675 | 1351 GB/s |
| 2 | tile_m=128, tile_n=128 | 0.621 | 1243 GB/s |
| 3 | tile_m=128, tile_n=64 | 0.442 | 884 GB/s |
| 4 | tile_m=64, tile_n=128 | 0.430 | 859 GB/s |
| 5 | tile_m=128, tile_n=64 | 0.425 | 851 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | tile_m=4, tile_n=4 | 0.008 | 17 GB/s |
| 2 | tile_m=4, tile_n=4 | 0.009 | 18 GB/s |
| 3 | tile_m=8, tile_n=4 | 0.015 | 31 GB/s |
| 4 | tile_m=8, tile_n=4 | 0.016 | 33 GB/s |
| 5 | tile_m=64, tile_n=4 | 0.017 | 34 GB/s |

### Parameter: `tile_m`

**Sweet spots:**
- `tile_m=128.0` (+66% above neighbors)
- `tile_m=128.0` (+60% above neighbors)
- `tile_m=64.0` (+41% above neighbors)
- `tile_m=64.0` (+36% above neighbors)
- `tile_m=32.0` (+22% above neighbors)

**Performance cliffs (AVOID):**
- At `tile_m=64.0`: 51% drop
- At `tile_m=128.0`: 51% drop
- At `tile_m=4.0`: 50% drop
- At `tile_m=4.0`: 49% drop
- At `tile_m=64.0`: 49% drop

### Parameter: `tile_n`

**Sweet spots:**
- `tile_n=128.0` (+64% above neighbors)
- `tile_n=128.0` (+59% above neighbors)
- `tile_n=64.0` (+41% above neighbors)
- `tile_n=32.0` (+22% above neighbors)
- `tile_n=16.0` (+12% above neighbors)

**Performance cliffs (AVOID):**
- At `tile_n=64.0`: 57% drop
- At `tile_n=16.0`: 49% drop
- At `tile_n=64.0`: 48% drop
- At `tile_n=128.0`: 48% drop
- At `tile_n=64.0`: 46% drop

---

## wave_scheduling

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | waves_per_cu=31, occupancy_target_pct=95 | 0.409 | 818 GB/s |
| 2 | waves_per_cu=31, occupancy_target_pct=90 | 0.408 | 816 GB/s |
| 3 | waves_per_cu=31, occupancy_target_pct=89 | 0.405 | 810 GB/s |
| 4 | waves_per_cu=31, occupancy_target_pct=81 | 0.402 | 804 GB/s |
| 5 | waves_per_cu=31, occupancy_target_pct=84 | 0.401 | 802 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | waves_per_cu=1, occupancy_target_pct=10 | 0.007 | 15 GB/s |
| 2 | waves_per_cu=1, occupancy_target_pct=17 | 0.007 | 15 GB/s |
| 3 | waves_per_cu=1, occupancy_target_pct=10 | 0.007 | 15 GB/s |
| 4 | waves_per_cu=1, occupancy_target_pct=55 | 0.012 | 24 GB/s |
| 5 | waves_per_cu=1, occupancy_target_pct=58 | 0.012 | 24 GB/s |

### Parameter: `waves_per_cu`

**Sweet spots:**
- `waves_per_cu=31.0` (+30% above neighbors)
- `waves_per_cu=31.0` (+29% above neighbors)
- `waves_per_cu=30.0` (+28% above neighbors)
- `waves_per_cu=30.0` (+28% above neighbors)
- `waves_per_cu=26.0` (+28% above neighbors)

**Performance cliffs (AVOID):**
- At `waves_per_cu=1.0`: 40% drop
- At `waves_per_cu=1.0`: 38% drop
- At `waves_per_cu=3.0`: 37% drop
- At `waves_per_cu=3.0`: 36% drop
- At `waves_per_cu=13.0`: 36% drop

### Parameter: `occupancy_target_pct`

**Sweet spots:**
- `occupancy_target_pct=90.0` (+38% above neighbors)
- `occupancy_target_pct=90.0` (+38% above neighbors)
- `occupancy_target_pct=76.0` (+38% above neighbors)
- `occupancy_target_pct=95.0` (+38% above neighbors)
- `occupancy_target_pct=95.0` (+38% above neighbors)

**Performance cliffs (AVOID):**
- At `occupancy_target_pct=55.0`: 85% drop
- At `occupancy_target_pct=75.0`: 84% drop
- At `occupancy_target_pct=17.0`: 75% drop
- At `occupancy_target_pct=58.0`: 73% drop
- At `occupancy_target_pct=26.0`: 71% drop

---

## fp16_compute

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=1024, num_chains=11 | 1.000 | 2317 GB/s |
| 2 | block_size=256, num_chains=14 | 1.000 | 2746 GB/s |
| 3 | block_size=128, num_chains=1 | 1.000 | 2221 GB/s |
| 4 | block_size=64, num_chains=12 | 1.000 | 2406 GB/s |
| 5 | block_size=512, num_chains=12 | 1.000 | 2351 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=32, num_chains=1 | 0.547 | 1095 GB/s |
| 2 | block_size=512, num_chains=1 | 0.552 | 1104 GB/s |
| 3 | block_size=32, num_chains=1 | 0.553 | 1106 GB/s |
| 4 | block_size=64, num_chains=1 | 0.554 | 1108 GB/s |
| 5 | block_size=256, num_chains=1 | 0.554 | 1108 GB/s |

### Parameter: `block_size`

**Optimal range:** 32 - 1024 (6 values with score >= 0.8)

**Performance cliffs (AVOID):**
- At `block_size=128.0`: 44% drop
- At `block_size=32.0`: 40% drop
- At `block_size=32.0`: 40% drop
- At `block_size=256.0`: 39% drop
- At `block_size=256.0`: 31% drop

### Parameter: `num_chains`

**Optimal range:** 2 - 15 (14 values with score >= 0.8)

**Performance cliffs (AVOID):**
- At `num_chains=1.0`: 45% drop
- At `num_chains=3.0`: 28% drop
- At `num_chains=3.0`: 28% drop
- At `num_chains=2.0`: 24% drop
- At `num_chains=2.0`: 24% drop

---

## wmma

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | k_tiles=34, num_chains=6 | 1.000 | 3550 GB/s |
| 2 | k_tiles=124, num_chains=2 | 1.000 | 3583 GB/s |
| 3 | k_tiles=88, num_chains=6 | 1.000 | 4501 GB/s |
| 4 | k_tiles=90, num_chains=4 | 1.000 | 4306 GB/s |
| 5 | k_tiles=19, num_chains=4 | 1.000 | 2159 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | k_tiles=1, num_chains=1 | 0.024 | 48 GB/s |
| 2 | k_tiles=2, num_chains=1 | 0.048 | 97 GB/s |
| 3 | k_tiles=1, num_chains=2 | 0.060 | 119 GB/s |
| 4 | k_tiles=1, num_chains=3 | 0.070 | 140 GB/s |
| 5 | k_tiles=3, num_chains=1 | 0.073 | 146 GB/s |

### Parameter: `k_tiles`

**Optimal range:** 10 - 127 (111 values with score >= 0.8)

**Sweet spots:**
- `k_tiles=8.0` (+81% above neighbors)
- `k_tiles=7.0` (+79% above neighbors)
- `k_tiles=9.0` (+78% above neighbors)
- `k_tiles=6.0` (+73% above neighbors)
- `k_tiles=5.0` (+65% above neighbors)

**Performance cliffs (AVOID):**
- At `k_tiles=8.0`: 64% drop
- At `k_tiles=10.0`: 61% drop
- At `k_tiles=2.0`: 60% drop
- At `k_tiles=1.0`: 60% drop
- At `k_tiles=3.0`: 60% drop

### Parameter: `num_chains`

**Optimal range:** 2 - 7 (6 values with score >= 0.8)

**Performance cliffs (AVOID):**
- At `num_chains=7.0`: 65% drop
- At `num_chains=6.0`: 61% drop
- At `num_chains=2.0`: 51% drop
- At `num_chains=1.0`: 50% drop
- At `num_chains=5.0`: 50% drop

---

## atomic

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=1024, unique_targets=982 | 0.863 | 1726 GB/s |
| 2 | block_size=1024, unique_targets=824 | 0.863 | 1725 GB/s |
| 3 | block_size=64, unique_targets=880 | 0.846 | 1693 GB/s |
| 4 | block_size=1024, unique_targets=974 | 0.836 | 1671 GB/s |
| 5 | block_size=1024, unique_targets=918 | 0.830 | 1661 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | block_size=32, unique_targets=1 | 0.006 | 12 GB/s |
| 2 | block_size=64, unique_targets=1 | 0.007 | 13 GB/s |
| 3 | block_size=128, unique_targets=1 | 0.007 | 13 GB/s |
| 4 | block_size=256, unique_targets=1 | 0.007 | 13 GB/s |
| 5 | block_size=1024, unique_targets=1 | 0.007 | 13 GB/s |

### Parameter: `block_size`

**Sweet spots:**
- `block_size=1024.0` (+86% above neighbors)
- `block_size=1024.0` (+86% above neighbors)
- `block_size=64.0` (+84% above neighbors)
- `block_size=64.0` (+84% above neighbors)
- `block_size=512.0` (+81% above neighbors)

**Performance cliffs (AVOID):**
- At `block_size=256.0`: 50% drop
- At `block_size=512.0`: 50% drop
- At `block_size=1024.0`: 50% drop
- At `block_size=1024.0`: 50% drop
- At `block_size=128.0`: 50% drop

### Parameter: `unique_targets`

**Optimal range:** 880 - 982 (5 values with score >= 0.8)

**Sweet spots:**
- `unique_targets=971.0` (+49% above neighbors)
- `unique_targets=828.0` (+45% above neighbors)
- `unique_targets=824.0` (+40% above neighbors)
- `unique_targets=536.0` (+39% above neighbors)
- `unique_targets=568.0` (+38% above neighbors)

**Performance cliffs (AVOID):**
- At `unique_targets=248.0`: 57% drop
- At `unique_targets=250.0`: 56% drop
- At `unique_targets=114.0`: 55% drop
- At `unique_targets=733.0`: 52% drop
- At `unique_targets=564.0`: 51% drop

---

## overlap

### Best Configurations

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | compute_intensity=1, working_set_kb=82719 | 0.946 | 1891 GB/s |
| 2 | compute_intensity=1, working_set_kb=62757 | 0.939 | 1878 GB/s |
| 3 | compute_intensity=1, working_set_kb=57238 | 0.913 | 1826 GB/s |
| 4 | compute_intensity=1, working_set_kb=75444 | 0.904 | 1808 GB/s |
| 5 | compute_intensity=2, working_set_kb=75444 | 0.893 | 1787 GB/s |

### Worst Configurations (AVOID)

| Rank | Params | Score | Bandwidth |
|------|--------|-------|-----------|
| 1 | compute_intensity=60, working_set_kb=2 | 0.000 | 0 GB/s |
| 2 | compute_intensity=29, working_set_kb=1 | 0.000 | 0 GB/s |
| 3 | compute_intensity=45, working_set_kb=3 | 0.000 | 0 GB/s |
| 4 | compute_intensity=63, working_set_kb=3 | 0.000 | 0 GB/s |
| 5 | compute_intensity=32, working_set_kb=3 | 0.000 | 0 GB/s |

### Parameter: `compute_intensity`

**Sweet spots:**
- `compute_intensity=2.0` (+89% above neighbors)
- `compute_intensity=3.0` (+85% above neighbors)
- `compute_intensity=4.0` (+84% above neighbors)
- `compute_intensity=5.0` (+82% above neighbors)
- `compute_intensity=6.0` (+77% above neighbors)

**Performance cliffs (AVOID):**
- At `compute_intensity=46.0`: 82% drop
- At `compute_intensity=32.0`: 82% drop
- At `compute_intensity=11.0`: 77% drop
- At `compute_intensity=26.0`: 76% drop
- At `compute_intensity=19.0`: 72% drop

### Parameter: `working_set_kb`

**Optimal range:** 52203 - 76251 (3 values with score >= 0.8)

**Sweet spots:**
- `working_set_kb=76251.0` (+69% above neighbors)
- `working_set_kb=32945.0` (+66% above neighbors)
- `working_set_kb=67203.0` (+65% above neighbors)
- `working_set_kb=43425.0` (+65% above neighbors)
- `working_set_kb=82719.0` (+63% above neighbors)

**Performance cliffs (AVOID):**
- At `working_set_kb=16967.0`: 82% drop
- At `working_set_kb=76584.0`: 82% drop
- At `working_set_kb=72849.0`: 80% drop
- At `working_set_kb=15774.0`: 80% drop
- At `working_set_kb=22984.0`: 80% drop

---
